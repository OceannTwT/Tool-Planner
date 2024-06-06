
FORMAT_TOOL_FUNCTIONARITY_FUNCTION = """

You will be provided with a tool, its description, name, and API documentation.
Based on this information, briefly tell me the functionality of this tool without outputting unnecessary information,
only describing the API functionality.

"""

FORMAT_TOOL_FUNCTIONARITY_USER_FUNCTION = """
Tool Name: {tool_name}.
Tool Description: {pack_name},{tool_description}.
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