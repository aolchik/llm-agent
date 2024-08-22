import os

#from langchain_openai.llms.base import OpenAI
from google.oauth2 import service_account

from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from langchain_google_genai import ChatGoogleGenerativeAI


def get_model_name(llm):
  if isinstance(llm, ChatGoogleGenerativeAI):
    return llm.model.split('/')[-1]
  elif isinstance(llm, Ollama):
    return llm.model
  elif isinstance(llm, ChatOpenAI):
    return llm.model_name
  else:
    raise ValueError(f"Unknown LLM model: {llm}")

def get_llm(model_name):
  if model_name == 'gemini-1.5-flash':
    service_account_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
    credentials = service_account.Credentials.from_service_account_file(service_account_file)
    return ChatGoogleGenerativeAI(model='gemini-1.5-flash',
                                  verbose=True,
                                  temperature=0,
                                  credentials=credentials)
  elif model_name == 'openhermes':
    return Ollama(model='openhermes')
  elif model_name == 'gpt-4o':
    return ChatOpenAI(model='gpt-4o',
                  verbose=True,
                  temperature=0)
  else:
    return None