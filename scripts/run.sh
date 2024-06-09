export TOOLBENCH_KEY=""
export OPENAI_KEY=""
export PYTHONPATH=./

python main.py \
    --toolkit_dir src/toolkits \
    --tool_api_dir datas/toolenv/tools/ \
    --backbone_model gpt_3.5 \
    --toolkit_num 20 \
    --openai_key $OPENAI_KEY \
    --tool_env datas/toolenv/tools/ \
    --tool_output_file tool_lib/tool_library.json \
    --toolkit_output_file tool_lib/toolkit_library.json \
    --input_query_file data/instruction/G3_query.json \
    --output_answer_file data/instruction/tool_result.json \
    --simcse_file model_lib/sup-simcse-roberta-base \
    --toolbench_key $TOOLBENCH_KEY