# Tech stack
Django HTML Templates usinf Jinja2 and FastAPI's built-in support

Refer to backend-lang-portal/BACKEND_SPEC.md for the back-end APIs to be used

# Dashboard structure

This is to define the minimal prototye UI for a learner dashboard

Keep all on one page as a SPA, use modern clean UI design to make the suggestions below work

## Title: My dashboard

Set of boxed sections horizontally arranged showing

-Title: Study sessions

-- subsection:Last
--- Name of study session e.g. Typing tutor
--- Timestamp of session
--- number of correct and incorrect answers from that session with a tick and a cross respectively

--subsection: Recent sessions
--- list of last 5 study sessions, showing title and date/time
--- each study session can be clicked on to view full details

-Title: My word groups
-- subsection:Last studied
--- list of word groups with a count of how many words are in each group
--- each word group can be clicked on to view the group details

- A space below where full information can be seen if an item above is selected