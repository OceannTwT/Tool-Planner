import time
import json
import logging
from tqdm import tqdm 
from config import args
from utils import print_exp
from scipy.spatial.distance import cosine
from src.toolkits.loader import ToolkitParser, ToolkitList
from model.GPTFactory.GPTFactory import GPTFactory
from model.Simcse.sim import ToolEmb
from src.planner.plan import PlannerParser
from src.toolkits.preprocessing import find_json_files, list_directories, ToolProcessor
from transformers import AutoModel, AutoTokenizer

def generate_result():
    dic = find_json_files(args.tool_env)
    dir = list_directories(args.tool_api_dir)
    toolp = ToolProcessor(args.tool_env)
    toolp.dumps()

    tokenizer = AutoTokenizer.from_pretrained("/root/autodl-tmp/sup-simcse-roberta-base")
    model = AutoModel.from_pretrained("/root/autodl-tmp/sup-simcse-roberta-base")
    toolsim = ToolEmb(tokenizer, model)
    toolsim.compute_tool_emb(args.tool_output_file)
    # toolsim = ToolEmb()
    toolsim.rebuild_json(args.toolkit_output_file)
    toolkit_list = ToolkitList(toolsim, args.toolkit_num)
    toolkit_list.generate_toolkit()
    toolkit_list.dumps()

    parser = PlannerParser(args.toolkit_num, args.input_query_file, args.output_answer_file)
    parser.query_list[0].generate_plan()
    parser.query_list[0].generate_steps()
    parser.query_list[0].process()

if __name__ == '__main__':
    generate_result()
    
    pass