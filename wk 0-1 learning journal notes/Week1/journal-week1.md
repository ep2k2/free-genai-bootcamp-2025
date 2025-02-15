** Week 1 **

see .pNG for screenshots through week

# summary of tools used
- IDE: Windsurf, looked at some front-end AI options but stuck with creating in Windsurf flow
- Backend: python, FastAPI, uvicorn
- Dashboard: Django/Jinja2, HTML/CSS/Javascript
- Typing Tutor: HTML/CSS/Javascript

# Investigation into AI code tools
- many editors/assistants/IDEs - some claiming to be agentic, others no-code or UI orientated _etc._

# Backend
- imported AI-created schema from the image in exampro repo using Claude 3.5
- added an extra table to cover the parts of speech e.g. each word is a verb, adverb, noun, pronoun etc.
- created specific python load programs for the seed data in case needed to reload
- also used DB Browser to view the data, and add some info to the tables manually
- implemented back-end endpoints - adding to as thought useful
- used Windsurf - largely on free 'Cascade Base' model moving up to Claude 3.5 as needed
- Used python and FastAPI to create the back-end
- used uvicorn to serve the FastAPI app

# Frontend
- created typing tutor game using HTML/CSS/Javascript   
- integrated with back-end endpoints to record word reviews (correct/incorrect)
- used Django/Jinja2 templates to create a minimal dashboard UI (AI created something fancier but pared back to parts implemented by me) 
- populated the dashboard with info from back-end endpoints
- used uvicorn to also serve the typing tutor/practice game 

# Running locally
- installed Ollama locally
--  and pulled llama3.2 model
-- successfully ran on local machine using CLI with cuda
-- successfully ran using API also

- installed in Docker and ran
-- did not complete getting Nvidia driver/toolkit configured


# some other notes
- want to explore more the relationship between the Model Context Protocol (MCP) and RAG
https://www.anthropic.com/news/model-context-protocol
https://modelcontextprotocol.io/introduction