import json
import argparse
import os
from sklearn.cluster import KMeans
from src.toolkits.preprocessing import ToolAPI
from model.Simcse.sim import ToolEmb

class ToolkitList:
    def __init__(self, ToolEmb=None, toolkit_num=1):
        self.tool_emb = ToolEmb
        self.tool_kits = []
        self.tool_kit_num = toolkit_num
        self.kmeans = None

    def generate_toolkit(self):
        emb_list = []
        for idx, emb in enumerate(self.tool_emb.tool_emb):
            emb_arr = emb.numpy()
            emb_list.append(emb_arr)
        self.kmeans = KMeans(n_clusters=self.tool_kit_num, random_state=0).fit(emb_list)
        for i in range(self.tool_kit_num):
            self.tool_kits.append(ToolkitParser("", "", i))
        for idx in range(len(self.tool_emb.tool_emb)):
            tool_json = self.tool_emb.tool_rebuild_json
            self.tool_kits[self.kmeans.labels_[idx]].tool_lists.append(ToolAPI(tool_json["id"],
                                                                               tool_json["desc"],
                                                                               tool_json["name"],
                                                                               tool_json["p_name"],
                                                                               tool_json["api_doc"],
                                                                               tool_json["functionality"]
                                                                               ))


    
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
