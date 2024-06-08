import json
import argparse
import os
from sklearn.cluster import KMeans
from config import args
from src.toolkits.preprocessing import ToolAPI
from src.task_conf.prompt_template import FORMAT_TOOLKIT_FUNCTIONARITY_FUNCTION, FORMAT_TOOLKIT_FUNCTIONARITY_USER_FUNCTION
from model.GPTFactory.GPTFactory import GPTFactory
from model.Simcse.sim import ToolEmb

class ToolkitList:
    def __init__(self, ToolEmb=None, toolkit_num=1):
        self.tool_emb = ToolEmb
        self.tool_kits = []
        self.tool_kit_num = toolkit_num
        self.kmeans = None
        self.labels = []

    def generate_toolkit(self):
        need_kmeans = False
        has_toolkit_func = True
        for idx in range(len(self.tool_emb.tool_func)):
            tool_json = self.tool_emb.tool_rebuild_json[idx]
            if int(tool_json["toolkit"]) is -1:
                need_kmeans = True
            if tool_json["toolkit_fun"] is "":
                has_toolkit_func = False
        # print(need_kmeans, has_toolkit_func)

        if need_kmeans:
            emb_list = []
            for idx, emb in enumerate(self.tool_emb.tool_emb):
                emb_arr = emb.numpy()
                emb_list.append(emb_arr)
            self.kmeans = KMeans(n_clusters=self.tool_kit_num, random_state=0).fit(emb_list)
        
        for i in range(self.tool_kit_num):
            self.tool_kits.append(ToolkitParser("", "", i))
        for idx in range(len(self.tool_emb.tool_func)):
            tool_json = self.tool_emb.tool_rebuild_json[idx]
            toolkit_id = self.kmeans.labels_[idx] if need_kmeans else tool_json["toolkit"]
            self.labels.append(toolkit_id)
            toolkit_func = "" if need_kmeans else tool_json["toolkit_fun"]
            self.tool_kits[toolkit_id].add_tool(ToolAPI(tool_json["id"],
                                                        tool_json["api_dest"],
                                                        tool_json["api_doc"],
                                                        tool_json["functionality"],
                                                        int(toolkit_id),
                                                        toolkit_func
                                                        ))
            if has_toolkit_func and not need_kmeans:
                self.tool_kits[toolkit_id].toolkit_description = toolkit_func
        # for idx in range(self.tool_kit_num):
        #     self.tool_kits[idx].generate_description()
        # for idx in range(len(self.tool_emb.tool_func)):
        #     tool_json = self.tool_emb.tool_rebuild_json[idx]
        #     toolkit_id = self.kmeans.labels_[idx] if need_kmeans else tool_json["toolkit"]
        #     tool = ToolAPI(tool_json["id"],tool_json["desc"],tool_json["name"],
        #                    tool_json["p_name"],tool_json["api_doc"],tool_json["functionality"],
        #                    toolkit_id, self.tool_kits[toolkit_id].get_description())
    
    def dumps(self):
        for idx in range(self.tool_kit_num):
            self.tool_kits[idx].generate_description()
            self.tool_kits[idx].dumps()

    
class ToolkitParser:
    def __init__(self, toolkit_description="", toolkit_name="", toolkit_id=0):
        self.toolkit_id = toolkit_id
        self.toolkit_description = toolkit_description
        self.toolkit_name = toolkit_name
        self.tool_lists = [] 

    def get_description(self):
        return self.toolkit_description
    
    def generate_description(self):
        if self.toolkit_description is "":
            gpt_fact = GPTFactory()
            gpt_fact.set_key(args.openai_key)
            system = FORMAT_TOOLKIT_FUNCTIONARITY_FUNCTION
            user = FORMAT_TOOLKIT_FUNCTIONARITY_USER_FUNCTION
            gpt_fact.set_sys_conv(system)
            tool_list_str = "{"
            for tool in self.tool_lists:
                tool_list_str = tool_list_str + f"[API{tool.tool_id} {tool.api_dest['type_name']}.{tool.api_dest['package_name']}.{tool.api_dest['name']}, Functionality: {tool.func}], "
            tool_list_str = tool_list_str + "}"
            # print(tool_list_str)
            user = user.replace("{tool_list}", tool_list_str)
            gpt_fact.add_user_conv(user)
            self.toolkit_description = gpt_fact.predict()
            for idx, tool in enumerate(self.tool_lists):
                self.tool_lists[idx].toolkit_fun = self.toolkit_description
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

    def toolkit_exp(self):
        exp = f"[Toolkit {self.toolkit_id}, Desc[{self.toolkit_description}]]\n"
        return exp
    
    def dumps(self):
        for idx in range(len(self.tool_lists)):
            tool = self.tool_lists[idx]
            with open(args.toolkit_output_file, "a") as f:
                f.write(tool.dumps() + '\n')
