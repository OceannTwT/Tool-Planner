import torch
import json
from scipy.spatial.distance import cosine
from transformers import AutoModel, AutoTokenizer

# Import our models. The package will take care of downloading the models automatically
class ToolEmb:
    def __init__(self, tokenizer=None, model=None):
        self.tokenizer = tokenizer
        self.model = model
        self.tool_func = []
        self.tool_rebuild_json = []
        self.tool_emb = None

    def rebuild_json(self, tool_lib_path):
        with open(tool_lib_path, "r") as f:
            for idx, line in enumerate(f):
                tool_json = json.loads(line)
                self.tool_func.append(tool_json["functionality"])
                self.tool_rebuild_json.append(tool_json)

    def compute_tool_emb(self, tool_lib_path):
        if len(self.tool_rebuild_json) is 0:
            with open(tool_lib_path, "r") as f:
                for idx, line in enumerate(f):
                    tool_json = json.loads(line)
                    self.tool_func.append(tool_json["functionality"])
                    self.tool_rebuild_json.append(tool_json)
        inputs = self.tokenizer(self.tool_func, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            self.tool_emb = self.model(**inputs, output_hidden_states=True, return_dict=True).pooler_output


