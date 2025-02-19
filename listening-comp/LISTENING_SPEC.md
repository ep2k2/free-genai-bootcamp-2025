# ff


## Overview - the Plan

- Setup Lightning AI to host
-- Langchain (https://github.com/PaulLockettOrg/LangServe-lightning)
-- but install Claude 3.5 on Langchain itself?!
-- use Model Context Protocol (MCP) so that  Claude can download transcripts from YouTube ---- using MCP (https://github.com/michaellatman/mcp-get)
---- via Youtube MCP Server (https://github.com/adhikasp/mcp-youtube))
--- create NLPTx style and level listening comprehension exercises from transcript
--- future direction could be to
---- generate audio files for practice sessions from transcript
---- generate picture files to support review sessions
---- create single question review segment
---- create 30 min multiple question exam practice session

- Langsmith
-- Langsmith for observability
-- LangGraph Studio for monitoring/management UI

- Local lang-portal
-- call API on Langchain with Youtube URL,  target lanuage "jp" 
-- [receive review session info and review info during or post session]




# Other notes

## Also looked at
- https://github.com/javedali99/audio-to-text-transcription
- Youtube download API


- Trae
- Streamlit community cloud
- Langsmith, Langchain, LangGraph/Studio
- Glama