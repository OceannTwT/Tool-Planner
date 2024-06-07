import json
import argparse
import time
import os

from toolbench.inference.Downstream_tasks.rapidapi import rapidapi_wrapper



class Planner:
    def __init__(self, input_file="", output_file=""):
        self.input_file = input_file
        self.output_file = output_file