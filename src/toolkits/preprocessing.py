import json
import argparse
import os
from tqdm import tqdm 
from config import args
from model.GPTFactory.GPTFactory import GPTFactory
from src.task_conf.prompt_template import FORMAT_TOOL_FUNCTIONARITY_FUNCTION, FORMAT_TOOL_FUNCTIONARITY_USER_FUNCTION

def find_json_files(target_directory):
    """
    Find json suffix
    """
    json_files = []
    for root, dirs, files in os.walk(target_directory):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    return json_files


def list_directories(path):
    try:
        items = os.listdir(path)
        directories = [item for item in items if os.path.isdir(os.path.join(path, item))]
        return directories
    except Exception as e:
        print(f"Error: {e}")
        return []
    
def convert_to_snake_case(s):
    s = s.lower()
    s = s.replace(' ', '_')
    return s

class ToolAPI:
    def __init__(self, tool_id, api_dest, api_doc, func="", toolkit=-1, toolkit_fun=""):
        self.api_dest = api_dest
        self.api_doc = api_doc
        self.tool_id = tool_id
        self.func = func
        self.toolkit = toolkit
        self.toolkit_fun = toolkit_fun

    def get_api_doc(self):
        return self.api_doc
    
    def get_api_tot_name(self):
        name_str = self.api_dest["type_name"] + "." + self.api_dest["package_name"] + "." + self.api_dest["name"]
        return name_str
    
    def get_desc(self):
        return self.api_dest["desc"]
    
    def fetch_func(self):
        if self.func is not "":
            return self.func
       
        gpt_fact = GPTFactory()
        gpt_fact.set_key(args.openai_key)
        system = FORMAT_TOOL_FUNCTIONARITY_FUNCTION
        user = FORMAT_TOOL_FUNCTIONARITY_USER_FUNCTION
        gpt_fact.set_sys_conv(system)
        user = user.replace("{tool_name}",self.api_dest["name"])
        user = user.replace("{pack_description}",self.api_dest["package_desc"])
        user = user.replace("{tool_description}", self.api_dest["desc"])
        user = user.replace("{api_doc}", str(self.api_doc))
        # print(user)
        gpt_fact.add_user_conv(user)
        self.func = gpt_fact.predict()
        return self.func
    
    def dumps(self):
        data = {"functionality": self.func, 
                     "id": self.tool_id,
                     "api_dest": self.api_dest,
                     "api_doc": self.api_doc,
                     "toolkit": self.toolkit,
                     "toolkit_fun": self.toolkit_fun
                     }
        print(data)
        json_data = json.dumps(data)
        return json_data
    
    def exp(self):
        print(f"API {self.tool_id}: Name [{self.api_dest['name']}], Desc[{self.api_dest['desc']}]")
        

class ToolProcessor:
    def __init__(self, tool_env=""):
        self.tool_env = tool_env
        self.tools_list = self.tool_reader(tool_env)


    def tool_reader(self, tool_env):
        dir_list = list()
        sub_dir = list_directories(tool_env)
        for sub_dir in tqdm(sub_dir):
            next_dir = tool_env + sub_dir
            file = find_json_files(next_dir)
            dir_list = dir_list + file
        tools = []
        id_iter = 0
        for idx, file_dir in enumerate(dir_list):
            tool_package = json.load(open(file_dir, "r"))
            dir_list = file_dir.split("/")
            type_name = dir_list[-2]
            package_desc = tool_package["tool_description"]
            package_name = tool_package["standardized_name"]
            for tool in tool_package["api_list"]:
                tool_desc = tool.get("description", "")
                tool_name = tool.get("name", "")
                tool_name = convert_to_snake_case(tool_name)
                api_dest = {"name": tool_name, "package_name": package_name,
                            "type_name": type_name, "desc": tool_desc, "package_desc": package_desc}
                pack = ToolAPI(id_iter, api_dest, tool)
                tools.append(pack)
                id_iter = id_iter + 1
        return tools
        
    def dumps(self, start_id=0):
        for idx in tqdm(range(start_id, len(self.tools_list))):
            tool = self.tools_list[idx]
            tool.fetch_func()
            with open(args.tool_output_file, "a") as f:
                f.write(tool.dumps() + '\n')

