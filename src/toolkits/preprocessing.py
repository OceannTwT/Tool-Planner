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

class ToolAPI:
    def __init__(self, tool_id, desc, name, p_name, api_doc):
        self.p_name = p_name
        self.desc = desc 
        self.name = name
        self.api_doc = api_doc
        self.tool_id = tool_id
        self.func = ""

    def get_api_doc(self):
        return self.api_doc
    
    def get_desc(self):
        return self.desc
    
    def fetch_func(self):
        if self.func is not "":
            return self.func
       
        gpt_fact = GPTFactory()
        gpt_fact.set_key(args.openai_key)
        system = FORMAT_TOOL_FUNCTIONARITY_FUNCTION
        user = FORMAT_TOOL_FUNCTIONARITY_USER_FUNCTION
        gpt_fact.set_sys_conv(system)
        user = user.replace("{tool_name}",self.name)
        user = user.replace("{pack_name}",self.p_name)
        user = user.replace("{tool_description}", self.desc)
        user = user.replace("{api_doc}", str(self.api_doc))
        # print(user)
        gpt_fact.add_user_conv(user)
        self.func = gpt_fact.predict()
        return self.func
    
    def dumps(self):
        data = {"functionality": self.func, 
                     "id": self.tool_id,
                     "name": self.name
                     }
        json_data = json.dumps(data)
        return json_data
    
    def exp(self):
        print(f"API {self.tool_id}: Name [{self.name}], Desc[{self.desc}]")
        

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
            package_name = tool_package["tool_description"]
            for tool in tool_package["api_list"]:
                tool_desc = tool.get("description", "")
                tool_name = tool.get("name", "")
                pack = ToolAPI(id_iter, tool_desc, tool_name, package_name, tool)
                tools.append(pack)
                id_iter = id_iter + 1
        return tools
        
    def dumps(self, start_id=0):
        for idx in tqdm(range(start_id, len(self.tools_list))):
            tool = self.tools_list[idx]
            tool.fetch_func()
            with open(args.tool_output_file, "a") as f:
                f.write(tool.dumps() + '\n')

