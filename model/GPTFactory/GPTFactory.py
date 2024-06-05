import json
import argparse
import openai
import time
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
        self.TRY_TIME=6
        self.time = time.time()

    def add_conv(self, conv):
        self.conversation_history.append(conv)

    def set_key(self, openai_key):
        self.openai_key = openai_key

    def set_sys_conv(self, sys_prompt):
        self.conversation_history = [
            {"role":"system","content":sys_prompt}
        ]
    
    def add_user_conv(self, user_prompt):
        message = {"role":"user","content":user_prompt}
        self.conversation_history.append(message)

    def set_default_conv(self):
        self.conversation_history = [
            {"role":"system","content":""}
        ]

    def change_conv(self,conv):
        self.conversation_history = conv

    def clear_conv(self):
        self.conversation_history = []

    def predict(self, **gpt_args):
        # print(gpt_args)
        self.time = time.time()
        for _ in range(self.TRY_TIME):
            if _ != 0:
                time.sleep(15)
            json_data = chat_completion_request(self.openai_key, self.conversation_history, **gpt_args)
            try:
                self.conversation_history.append({"role": "assistant", "content": json_data["choices"][0]["message"]["content"]})
                return json_data["choices"][0]["message"]["content"]
            except BaseException as e:
                print(f"Parsing Exception: {repr(e)}. Try again.")
                if json_data is not None:
                    print(f"OpenAI return: {json_data}")

            