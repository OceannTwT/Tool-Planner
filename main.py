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

def test_planner():
    parser = PlannerParser(20, args.input_query_file, args.output_answer_file)
    print(parser.query_list[0].generate_plan())
    parser.query_list[0].generate_steps()
    # parser.generate_query_list()

def test_loader():
    name = "123"
    desc = "happy every day"
    dic = {"desc": desc, "name": name}

    toolkit = ToolkitParser()
    toolkit.loads_toolkit(dic, 0)
    # print(toolkit.get_description())
    toolkit.toolkit_exp()

    # tokenizer = AutoTokenizer.from_pretrained("/root/autodl-tmp/sup-simcse-roberta-base")
    # model = AutoModel.from_pretrained("/root/autodl-tmp/sup-simcse-roberta-base")
    # toolsim = ToolEmb(tokenizer, model)
    # toolsim.compute_tool_emb(args.tool_output_file)
    toolsim = ToolEmb()
    toolsim.rebuild_json(args.toolkit_output_file)
    toolkit_list = ToolkitList(toolsim, 20)
    toolkit_list.generate_toolkit()
    print("Labels:\n", toolkit_list.labels)
    for idx, tool in enumerate(toolkit_list.tool_kits[13].tool_lists):
        print(tool.get_api_tot_name(), tool.tool_id)
    # print(toolkit_list.tool_kits[1].generate_description())
    # toolkit_list.tool_kits[1].toolkit_exp()
    # toolkit_list.dumps()
    # toolkit_list.tool_kits[0].tool_list

def test_gptfactory():
    factory = GPTFactory("gpt-3.5-turbo", "sk-bm-YImlouVDbMgMQ87eOWzBT3BlbkFJPImmmDgc4MaSwuKLbGGk")
    gpt_args = {"temperature": 0.7, 
                "top_p": 1,
                "frequency_penalty": 0,
                "presence_penalty": 0}
    messages = {"role":"user","content":"Hello, what is the weather today?"}
    factory.set_default_conv()
    factory.add_conv(messages)
    res = factory.predict(**gpt_args)
    messages["content"] = "So how do i find it?"
    factory.add_conv(messages)
    res = factory.predict(**gpt_args)

def test_preprocessing():
    dic = find_json_files(args.tool_env)
    dir = list_directories(args.tool_api_dir)
    toolp = ToolProcessor(args.tool_env)
    # toolp.tools_list[-1].exp()
    # print(toolp.tools_list[-1].fetch_func())
    # print(len(toolp.tools_list))
    # for idx, tool in tqdm(enumerate(toolp.tools_list)):
    #     toolp.tools_list[idx].fetch_func()
    toolp.dumps()

def test_toolsim():
    tokenizer = AutoTokenizer.from_pretrained("/root/autodl-tmp/sup-simcse-roberta-base")
    model = AutoModel.from_pretrained("/root/autodl-tmp/sup-simcse-roberta-base")
    toolsim = ToolEmb(tokenizer, model)
    toolsim.compute_tool_emb(args.tool_output_file)
    print(toolsim.tool_emb[0].numpy())
    # cosine_sim_0_1 = 1 - cosine(toolsim.tool_emb[0], toolsim.tool_emb[1])
    # cosine_sim_0_2 = 1 - cosine(toolsim.tool_emb[0], toolsim.tool_emb[2])

    # print("Cosine similarity between \"%s\" and \"%s\" is: %.3f" % (toolsim.tool_func[0], toolsim.tool_func[1], cosine_sim_0_1))
    # print("Cosine similarity between \"%s\" and \"%s\" is: %.3f" % (toolsim.tool_func[0], toolsim.tool_func[2], cosine_sim_0_2))



if __name__ == '__main__':
    test_planner()
    
    pass