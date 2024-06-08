export TOOLBENCH_KEY="l6Of3p9J0K51ZnSgs4QUePouF7GAixYIyNRVctawzECBjXDhqv"
export OPENAI_KEY="sk-bm-YImlouVDbMgMQ87eOWzBT3BlbkFJPImmmDgc4MaSwuKLbGGk"
export PYTHONPATH=./

python main.py \
    --toolkit_dir src/toolkits \
    --tool_api_dir datas/toolenv/tools/ \
    --backbone_model gpt_3.5 \
    --openai_key $OPENAI_KEY \
    --method DFS_woFilter_w2 \
    --tool_env datas/toolenv/tools/ \
    --tool_output_file tool_lib/tool_library.json \
    --toolkit_output_file tool_lib/toolkit_library.json \
    --input_query_file data_example/instruction/G3_query.json \
    --output_answer_file data_example/instruction/tool_result.json \
    --toolbench_key $TOOLBENCH_KEY