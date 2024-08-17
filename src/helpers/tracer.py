import os
from dotenv import load_dotenv

load_dotenv()

AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")
LANGTRACE_API_KEY = os.getenv("LANGTRACE_API_KEY")
if AGENTOPS_API_KEY:
    import agentops

if LANGTRACE_API_KEY:
    from langtrace_python_sdk import langtrace

class Tracer:

    def init(self, default_tags=[]):
        if AGENTOPS_API_KEY:
            agentops.init(AGENTOPS_API_KEY, default_tags=default_tags)
        
        if LANGTRACE_API_KEY:
            langtrace.init(api_key=LANGTRACE_API_KEY)

    def end(self):
        if AGENTOPS_API_KEY:
            agentops.end_session("Success")
        
