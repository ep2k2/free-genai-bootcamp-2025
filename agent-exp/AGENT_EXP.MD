#

Given a song title find, parse and return a json structured list of japanese vocabulary in dictionary-from, along with a JLPT Nx level 

# Target Technical spec
- Python: write simple pythonic code
- LLM: use Gemini 2.0 Flash
- use uv as package manager
- use uv for virtual environments


# Technical uncertainty
- how strong the 'reasoning' of the target LLM model needs to be in order to make effective function-calling tool use
- how easy to extend
-- octotools with a new custom tool 'card' is in practice (in this case a non-LLM tool)
-- as Japanese tokeniser (including morphological analysis) web API using yomi https://ookii-tsuki.github.io/yomi/
--- a possible alternative might be local code using e.g. https://github.com/mocobeta/janome;
- whether an additional tool to check and enforce a JSON schema is necessary to consistently return valid and consistent JSON (scenario is creation of a dictionary form vocabulary list from the song)

# Approach
- clone https://github.com/octotools/octotools
- create a new virtual environment using uv 
-- hcurl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="/custom/path" sh
- test install using 
-- cd octotools/tools/python_code_generator
-- python tool.py
- connect to Gemini API
-- include GEMINI_API_KEY in .env file
-- check .gitignore
-- test connectivity
- create a new tool card
-- implement new tool following the structure of existing tools as stored in the octotools/tools directory
-- enable tool by configuring subset of tools for tasks by setting the enabled_tools argument in tasks/solve.py
- potentially repeat for info gathering (trying to avoid automated scraping) and/or JSON schema enforcement of output if and as needed
-- consider BS4
-- consider JsonSchema

# Plan tracking
