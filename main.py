import time
import json
import logging
from tqdm import tqdm 
from config import args
from utils import print_exp
from src.toolkits.loader import ToolkitParser
from model.GPTFactory.GPTFactory import GPTFactory
from src.toolkits.preprocessing import find_json_files, list_directories, ToolProcessor


def test_loader():
    name = "123"
    desc = "happy every day"
    dic = {"desc": desc, "name": name}

    toolkit = ToolkitParser()
    toolkit.loads_toolkit(dic, 0)
    # print(toolkit.get_description())
    toolkit.tool_exp()

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
    toolp.tools_list[-1].exp()
    print(toolp.tools_list[-1].fetch_func())
    print(len(toolp.tools_list))
    # for idx, tool in tqdm(enumerate(toolp.tools_list)):
    #     toolp.tools_list[idx].fetch_func()
    toolp.dumps()


if __name__ == '__main__':
    test_preprocessing()

    pass