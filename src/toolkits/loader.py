import json
import argparse
import os

class ToolkitParser:
    def __init__(self, toolkit_description="", toolkit_name="", toolkit_id=0):
        self.toolkit_id = toolkit_id
        self.toolkit_description = toolkit_description
        self.toolkit_name = toolkit_name
        self.tool_lists = [] 

    def get_description(self):
        return self.toolkit_description
    
    def get_id(self):
        return self.toolkit_id
    
    def get_name(self):
        return self.toolkit_name

    def loads_toolkit(self, toolkit_dict, id):
        self.toolkit_description = toolkit_dict["desc"]
        self.toolkit_name = toolkit_dict["name"]
        self.toolkit_id = id

    def add_tool(self, tool_args):
        self.tool_lists.append(tool_args)

    def tool_exp(self):
        print(f"|| Toolkit {self.toolkit_id}, Name:[{self.toolkit_name}], Desc[{self.toolkit_description}] ||")
        return
