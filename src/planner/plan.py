import json
import argparse
import time
import os
import requests
from config import args
from model.Simcse.sim import ToolEmb
from src.toolkits.loader import ToolkitParser, ToolkitList
from model.GPTFactory.GPTFactory import GPTFactory
from termcolor import colored
from utils import change_name, standardize
# from toolbench.inference.Downstream_tasks.rapidapi import rapidapi_wrapper
from src.task_conf.prompt_template import PROMPT_OF_PLAN_MAKING, PROMPT_OF_PLAN_MAKING_USER, PROMPT_OF_CALLING_ONE_TOOL_SYSTEM, PROMPT_OF_CALLING_ONE_TOOL_USER, PROMPT_OF_PLAN_EXPLORATION, PROMPT_OF_THE_INTOOLKIT_ERROR_OCCURS, PROMPT_OF_THE_CROSSTOOLKIT_ERROR_OCCURS, PROMPT_OF_THE_OUTPUTS

def fetch_api_json(tool):
    api_dest = tool.api_dest
    api_doc = tool.api_doc
    output_json = {}
    output_json["category_name"] = api_dest["type_name"]
    output_json["api_name"] = api_dest["name"]
    output_json["api_description"] = api_dest["desc"]
    output_json["required_parameters"] = api_doc["required_parameters"]
    output_json["optional_parameters"] = api_doc["optional_parameters"]
    output_json["tool_name"] = api_dest["package_name"]
    return output_json

def api_json_to_openai_json(api_json,standard_tool_name):
        
    description_max_length=256
    templete =     {
        "name": "",
        "description": "",
        "parameters": {
            "type": "object",
            "properties": {
            },
            "required": [],
            "optional": [],
        }
    }
        
    map_type = {
        "NUMBER": "integer",
        "STRING": "string",
        "BOOLEAN": "boolean"
    }

    pure_api_name = change_name(standardize(api_json["api_name"]))
    templete["name"] = pure_api_name+ f"_for_{standard_tool_name}"
    templete["name"] = templete["name"][-64:]

    templete["description"] = f"This is the subfunction for tool \"{standard_tool_name}\", you can use this tool."
        
    if api_json["api_description"].strip() != "":
        tuncated_description = api_json['api_description'].strip().replace(api_json['api_name'],templete['name'])[:description_max_length]
        templete["description"] = templete["description"] + f"The description of this function is: \"{tuncated_description}\""
    if "required_parameters" in api_json.keys() and len(api_json["required_parameters"]) > 0:
        for para in api_json["required_parameters"]:
            name = standardize(para["name"])
            name = change_name(name)
            if para["type"] in map_type:
                param_type = map_type[para["type"]]
            else:
                param_type = "string"
            prompt = {
                "type":param_type,
                "description":para["description"][:description_max_length],
            }

            default_value = para['default']
            if len(str(default_value)) != 0:    
                prompt = {
                    "type":param_type,
                    "description":para["description"][:description_max_length],
                    "example_value": default_value
                }
            else:
                prompt = {
                    "type":param_type,
                    "description":para["description"][:description_max_length]
                }

            templete["parameters"]["properties"][name] = prompt
            templete["parameters"]["required"].append(name)
        for para in api_json["optional_parameters"]:
            name = standardize(para["name"])
            name = change_name(name)
            if para["type"] in map_type:
                param_type = map_type[para["type"]]
            else:
                param_type = "string"

            default_value = para['default']
            if len(str(default_value)) != 0:    
                prompt = {
                    "type":param_type,
                    "description":para["description"][:description_max_length],
                    "example_value": default_value
                }
            else:
                prompt = {
                    "type":param_type,
                    "description":para["description"][:description_max_length]
                }

            templete["parameters"]["properties"][name] = prompt
            templete["parameters"]["optional"].append(name)

    return templete, api_json["category_name"],  pure_api_name

def call_toolbench(service_url, payload, headers, timeout=15):
    try:
        response = requests.post(service_url, json=payload, headers=headers, timeout=timeout)
    except Exception as e:
        print(f"Request Rapid API Error: {e}")
        return json.dumps({"error": f"API not working error...", "response": ""}), 6
    if response.status_code != 200:
        return json.dumps({"error": f"request invalid, data error. status_code={response.status_code}", "response": ""}), 12
    try:
        response = response.json()
    except:
        print(response)
        return json.dumps({"error": f"request invalid, data error", "response": ""}), 12
    if response["error"] == "API not working error...":
        status_code = 6
    elif response["error"] == "Unauthorized error...":
        status_code = 7
    elif response["error"] == "Unsubscribed error...":
        status_code = 8
    elif response["error"] == "Too many requests error...":
        status_code = 9
    elif response["error"] == "Rate limit per minute error...":
        print("Reach api calling limit per minute, sleeping...")
        time.sleep(10)
        status_code = 10
    elif response["error"] == "Message error...":
        status_code = 11
    else:
        status_code = 0
    return json.dumps(response), status_code

class PlannerParser:
    def __init__(self, toolkit_num = 1, input_file="", output_file="", toolkit_dir=args.toolkit_output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.query_list = []
        self.toolkit_num = toolkit_num
        self.toolkit_list = None
        self.toolkit_dir = toolkit_dir
        try:
            self.load_toolkit()
        except Exception as e:
            print(f"Load Toolkit Error: {e}")
        try:
            self.generate_query_list()
        except Exception as e:
            print(f"Generate Query List Error: {e}")

    def load_toolkit(self):
        toolsim = ToolEmb()
        toolsim.rebuild_json(self.toolkit_dir)
        self.toolkit_list = ToolkitList(toolsim, self.toolkit_num)
        self.toolkit_list.generate_toolkit()
        

    def generate_query_list(self):
        query_doc = json.load(open(self.input_file, "r"))
        for idx, query in enumerate(query_doc):
            planner = PlannerProcessor(query["query"], self.toolkit_list)
            self.query_list.append(planner)


class PlannerProcessor:
    def __init__(self, input_query="", toolkit_list=None):
        self.input_query = input_query
        self.toolkit_list = toolkit_list
        self.toolkits_prompt = ""
        self.devise_plan = ""
        self.service_url = "http://8.218.239.54:8080/rapidapi"
        self.steps = []
        self.have_plan = 0
        for toolkit in self.toolkit_list.tool_kits:
            self.toolkits_prompt = self.toolkits_prompt + toolkit.toolkit_exp()
        # print(self.toolkits_prompt)
        # print(self.toolkit_list.tool_kits[0].toolkit_exp())
    

    def generate_plan(self):
        if self.devise_plan is "":
            gpt_fact = GPTFactory()
            gpt_fact.set_key(args.openai_key)
            system = PROMPT_OF_PLAN_MAKING
            if self.have_plan:
                system = PROMPT_OF_THE_CROSSTOOLKIT_ERROR_OCCURS + PROMPT_OF_PLAN_MAKING
            user = PROMPT_OF_PLAN_MAKING_USER
            system = system.replace("{toolkit_list}", self.toolkits_prompt)
            user = user.replace("{user_query}", self.input_query)
            gpt_fact.set_sys_conv(system)
            gpt_fact.add_user_conv(user)
            self.devise_plan = gpt_fact.predict()
            self.have_plan = 1
        return self.devise_plan
    
    def generate_steps(self):
        try:
            plan_json = json.loads(self.devise_plan)
            for idx, thought_str in enumerate(plan_json):
                key = list(thought_str.keys())[0]
                method = thought_str[key]
                toolkit_id = key.split(" ")[-1]
                self.steps.append([toolkit_id, method])
        except Exception as e:
            print(f"Generate Steps Error: {e}")
            return None
        return self.steps
    
    def process(self):
        idx = 0
        response = []
        while idx < len(self.steps):
            step = self.steps[idx]
            json_response, status_code = self.process_steps(step)
            response.append(json_response)
            if status_code == 1:
                print(colored("Toolkit Invalid, Replanning to new steps",color="red"))
                privious_steps = self.steps
                privious_response = response
                response = []
                self.generate_plan()
                self.generate_steps()
                st = 0
                while st <= idx:
                    if privious_steps[0] != step[0]:
                        break
                    response.append(privious_response[st])
                    st = st + 1
                idx = st - 1
            idx = idx + 1
        gpt_fact = GPTFactory()
        gpt_fact.set_key(args.openai_key)
        system = PROMPT_OF_THE_OUTPUTS
        user = PROMPT_OF_CALLING_ONE_TOOL_USER
        user = system.replace("{task_description}", self.input_query)
        json_path = json.dumps({"plan": self.steps, "plan_strategy": response})
        user = user.replace("{thought_text}", json_path)
        gpt_fact.set_sys_conv(system)
        gpt_fact.add_user_conv(user)
        answer = gpt_fact.predict()
        print(answer)
        return answer

    def process_steps(self, step):
        step_id, step_plan = step[0], step[1]
        # print(step[0], step[1])
        toolkit = self.toolkit_list.tool_kits[int(step_id)].tool_lists
        for tool in toolkit:
            tool_api_json = fetch_api_json(tool)
            package_name = standardize(tool.api_dest["package_name"])
            openai_function_json, cate_name, pure_api_name = api_json_to_openai_json(tool_api_json, package_name)
            open_functions = [openai_function_json]
            gpt_fact = GPTFactory()
            gpt_fact.set_key(args.openai_key)
            system = PROMPT_OF_PLAN_EXPLORATION + PROMPT_OF_CALLING_ONE_TOOL_SYSTEM
            user = PROMPT_OF_CALLING_ONE_TOOL_USER
            system = system.replace("{task_description}", self.input_query)
            user = user.replace("{thought_text}", step_plan)
            gpt_fact.set_sys_conv(system)
            gpt_fact.add_user_conv(user)
            # print(gpt_fact.conversation_history)
            new_prediction = gpt_fact.predict_fun(functions = open_functions)
            action_input = new_prediction["arguments"]
            payload = {
                        "category": tool.api_dest["type_name"],
                        "tool_name": tool.api_dest["package_name"],
                        "api_name": pure_api_name,
                        "tool_input": action_input,
                        "strip": args.observ_compress_method,
                        "toolbench_key": args.toolbench_key
            }
            print(colored(f"query to {payload['category']}-->{payload['tool_name']}-->{payload['api_name']}",color="yellow"))
            headers = {"toolbench_key": args.toolbench_key}
            json_response, status_code = call_toolbench(self.service_url, payload, headers)
            if status_code == 0:
                return json_response, status_code
        return json.dumps({"error": f"Toolkit False Error", "response": ""}), 1


    # def fix_step(self):
    #     pass
