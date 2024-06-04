import json
import argparse
import openai
from tenacity import retry, wait_random_exponential, stop_after_attempt
import os

@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(key, messages, functions=None, function_call=None, model="gpt-3.5-turbo",stop=None, **args):
    
    json_data = {
        "model": model,
        "messages": messages,
        "max_tokens": 1024,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        **args
    }
    # print(json_data)
    if stop is not None:
        json_data.update({"stop": stop})
    if functions is not None:
        json_data.update({"functions": functions})
    if function_call is not None:
        json_data.update({"function_call": function_call})
    
    try:
        if model == "gpt-3.5-turbo":
            openai.api_key = key
        else:
            raise NotImplementedError
        openai_response = openai.ChatCompletion.create(
            **json_data,
        )
        json_data = json.loads(str(openai_response))
        return json_data 

    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"OpenAI calling Exception: {e}")
        return e

class GPTFactory:
    def __init__(self, model="gpt-3.5-turbo", openai_key=""):
        self.model = model
        self.conversation_history = []
        self.openai_key = openai_key

    def add_conv(self, conv):
        self.conversation_history.append(conv)

    def set_default_conv(self):
        self.conversation_history = [
            {"role":"system","content":""}
        ]

    def change_conv(self,conv):
        self.conversation_history = conv

    def predict(self, **gpt_args):
        print(gpt_args)
        json_data = chat_completion_request(self.openai_key, self.conversation_history, **gpt_args)
        self.conversation_history.append({"role": "assistant", "content": json_data["choices"][0]["message"]["content"]})
        print(json_data["choices"][0]["message"]["content"])