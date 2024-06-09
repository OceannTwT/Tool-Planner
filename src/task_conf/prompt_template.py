
FORMAT_TOOL_FUNCTIONARITY_FUNCTION = """

You will be provided with a tool, its description, name, and API documentation.
Based on this information, briefly tell me the functionality of this tool without outputting unnecessary information,
only describing the API functionality.

"""

FORMAT_TOOL_FUNCTIONARITY_USER_FUNCTION = """
Tool Name: {tool_name}.
Tool Description: {pack_description},{tool_description}.
API documentation:: {api_doc}.
Please remember, tell me the functionality of this tool without outputting unnecessary information,
ONLY describing the API functionality in short description.
"""

FORMAT_TOOLKIT_FUNCTIONARITY_FUNCTION = """
You will be provided a toolkit with a list tool, including tool functionality and name.
Based on this information, briefly tell me the functionality of this toolkit without outputting unnecessary information,
only describing the toolkit functionality.
"""

FORMAT_TOOLKIT_FUNCTIONARITY_USER_FUNCTION = """
Tool List: {tool_list}.
Please remember, tell me the functionality of this tool without outputting unnecessary information,
ONLY describing the API functionality in short description.
"""

PROMPT_OF_PLAN_MAKING = """
You will be provided with the toolkits, the clustered names of toolkits, and the descriptions of
the function of the toolkits.Your task is to interact with API toolkits to construct user queries
and use the functionalities of the toolkits to answer the queries. 
The toolkits list: {toolkit_list}

You need to identify the most suitable toolkits based on the user’s requirements, and then outline your solution plan based
on the toolkits you’ve selected.Remember, your goal is not to directly answer the query but
to identify the toolkits and provide a solution plan. 

Please Give the plan in this format, replace the {tool_x.id} to the real toolkit id, and {solution} to your plan thought:
[{"Toolkit {tool_1.id}": "{solution}"}, {"Toolkit {tool_2.id}": "{solution}"}, {"..."}, {"Toolkit {tool_final.id}": "{solution}"}]
Divise a plan to resolve the problem:
"""

PROMPT_OF_PLAN_MAKING_USER = """
Only give the plan in the format and DO NOT generate unnecessary information.
Here is the user’s question: {user_query}.
"""

PROMPT_OF_CALLING_ONE_TOOL_SYSTEM = """

You are Tool-GPT, and you can solve specific problems using given tools (functions).
You will receive a problem description and the specific method of function calls to execute the solution from the toolkit. 
By invoking this API, you can obtain the results of the thought process regarding this part of the problem. 
Task description: {task_description}.

"""

PROMPT_OF_CALLING_ONE_TOOL_USER = """
Thought: {thought_text}.
Provide the accurate API input and message as you can!
"""

PROMPT_OF_PLAN_EXPLORATION = """
Let’s begin executing this step of the plan. You will be provided with documentation for all
the APIs contained within this step’s toolkit, along with the parameters required to call the
APIs. Please randomly select one API from this toolkit to satisfy the user’s requirements,
or select the specified API if the user has indicated one. Consult the usage documentation
for this API, then make the API call and provide the response. Afterward, briefly analyze
the current status and determine the next step. If the API call is successful, proceed to the
next step as planned. If it fails, invoke another API from the toolkit. If all APIs in the toolkit
have been tried and failed, revert to the previous node and revise this step. Keep the analysis
concise, ideally no more than three sentences.
"""

PROMPT_OF_THE_INTOOLKIT_ERROR_OCCURS = """
This is not your first attempt at this task. The previously called APIs have all failed, and you
are now in the intermediate state of an In-Toolkit plan exploration. Before you decide on
new actions, I will first show you the actions you have taken previously for this state. Then,
you must develop an action that is different from all these previous actions. Here are some
previous candidate actions: [previous API]. Now, please analyze the current state and then
call another API within the same toolkit where the previously failed APIs are located.
"""

PROMPT_OF_THE_CROSSTOOLKIT_ERROR_OCCURS = """
This is not your first attempt at this task. All the APIs planned within the previous toolkits
have failed, and you are now in the intermediate state of a Cross-Toolkit plan exploration.
Before you decide on new actions, I will first show you the actions you have taken previously
for this state. Then, you must develop an action that is different from all these previous
actions. Here are some previous candidate actions: [previous API, previous toolkit]. Now,
please revert to the previous node, revise the plan for this step, and use a different toolkit.
"""

PROMPT_OF_THE_OUTPUTS = """
If you believe you have obtained the result capable of answering the task, please invoke this
function to provide the final answer. Remember: the only part displayed to the user is the
final answer, so it should contain sufficient information.
Task_Description:{task_description}
"""

PROMPT_OF_THE_OUTPUTS_USER = """
Resolving Procedure:{response_thought_list}
Please provide the final answer.
"""