import json
import argparse
import time
import os

from config import args
from model.Simcse.sim import ToolEmb
from src.toolkits.loader import ToolkitParser, ToolkitList
from model.GPTFactory.GPTFactory import GPTFactory
# from toolbench.inference.Downstream_tasks.rapidapi import rapidapi_wrapper
from src.task_conf.prompt_template import PROMPT_OF_PLAN_MAKING, PROMPT_OF_PLAN_MAKING_USER, PROMPT_OF_PLAN_EXPLORATION, PROMPT_OF_THE_INTOOLKIT_ERROR_OCCURS, PROMPT_OF_THE_CROSSTOOLKIT_ERROR_OCCURS, PROMPT_OF_THE_OUTPUTS



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
        self.steps = []
        for toolkit in self.toolkit_list.tool_kits:
            self.toolkits_prompt = self.toolkits_prompt + toolkit.toolkit_exp()
        # print(self.toolkits_prompt)
        # print(self.toolkit_list.tool_kits[0].toolkit_exp())
    

    def generate_plan(self):
        if self.devise_plan is "":
            gpt_fact = GPTFactory()
            gpt_fact.set_key(args.openai_key)
            system = PROMPT_OF_PLAN_MAKING
            user = PROMPT_OF_PLAN_MAKING_USER
            system = system.replace("{toolkit_list}", self.toolkits_prompt)
            user = user.replace("{user_query}", self.input_query)
            gpt_fact.set_sys_conv(system)
            gpt_fact.add_user_conv(user)
            self.devise_plan = gpt_fact.predict()
        return self.devise_plan
    
    def generate_steps(self):
        try:
            plan_json = json.loads(self.devise_plan)
            for idx, thought_str in enumerate(plan_json):
                key = list(thought_str.keys())[0]
                method = thought_str[key]
                toolkit_id = key.split(" ")[-1]
                self.steps.append({toolkit_id, method})
        except Exception as e:
            print(f"Generate Steps Error: {e}")
            return None
        return self.steps
