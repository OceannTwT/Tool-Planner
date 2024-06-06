import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--backbone_model', type=str, default="toolllama", required=False, help='chatgpt_function or davinci or toolllama')
    parser.add_argument('--openai_key', type=str, default="", required=False, help='openai key for chatgpt_function or davinci model')
    parser.add_argument('--model_path', type=str, default="your_model_path/", required=False, help='')
    parser.add_argument('--tool_api_dir', type=str, default="your_tools_path/", required=False, help='')
    parser.add_argument('--toolkit_dir', type=str, default="your_toolkits_path/", required=False, help='')
    parser.add_argument('--tool_env', type=str, default="your_toolenv_path/", required=False, help='')
    parser.add_argument('--method', type=str, default="CoT@1", required=False, help='method for answer generation: CoT@n,Reflexion@n,BFS,DFS,UCT_vote')
    parser.add_argument('--tool_output_file', type=str, default="tool_lib/tool_library.json", required=False, help='Tool lib for description')
    parser.add_argument('--toolkit_output_file', type=str, default="tool_lib/toolkit_library.json", required=False, help='Toolkit lib for description')
    parser.add_argument('--input_query_file', type=str, default="", required=False, help='input path')
    parser.add_argument('--output_answer_file', type=str, default="",required=False, help='output path')
    parser.add_argument('--toolbench_key', type=str, default="",required=False, help='your toolbench key to request rapidapi service')
    parser.add_argument('--rapidapi_key', type=str, default="",required=False, help='your rapidapi key to request rapidapi service')
    parser.add_argument('--use_rapidapi_key', action="store_true", help="To use customized rapidapi service or not.")
    parser.add_argument('--api_customization', action="store_true", help="To use customized api or not.")

    parsed_args = parser.parse_args()
    return parsed_args


args = parse_arguments()
