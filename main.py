import time
import json
import logging
from config import args
from utils import print_exp
from src.toolkits.loader import ToolkitParser
from model.GPTFactory.GPTFactory import GPTFactory


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
    factory.predict(**gpt_args)
    messages["content"] = "So how do i find it?"
    factory.add_conv(messages)
    factory.predict(**gpt_args)


if __name__ == '__main__':
    test_gptfactory()

    pass