import os
from google.oauth2 import service_account
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from langchain_google_genai import ChatGoogleGenerativeAI
from helpers.tracer import TracerFactory
from pydantic import BaseModel

tracer = TracerFactory.get_tracer()


def get_model_name(llm):
    if isinstance(llm, ChatGoogleGenerativeAI):
        return llm.model.split('/')[-1]
    elif isinstance(llm, Ollama):
        return llm.model
    elif isinstance(llm, ChatOpenAI):
        return llm.model_name
    else:
        raise ValueError(f"Unknown LLM model: {llm}")


class ModelParams(BaseModel):
    use_cache: bool = True


def get_llm(model_provider, model_name, config: ModelParams = ModelParams()):
    """
    Get the LLM model based on the model provider and model name.
    model_provider: str
        google, openai, ollama
    model_name: str
        gemini-1.5-flash, openhermes, gpt-4o, gpt-3.5-turbo
    """
    if model_provider == 'google':
        google_valid_models = ['gemini-1.5-flash']

        if model_name not in google_valid_models:
            raise Exception(f"Invalid Google model: {model_name}")

        service_account_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
        credentials = service_account.Credentials.\
            from_service_account_file(service_account_file)
        return ChatGoogleGenerativeAI(model=model_name,
                                      verbose=True,
                                      temperature=0,
                                      credentials=credentials)

    elif model_provider == 'ollama':
        ollama_valid_models = ['openhermes']

        if model_name not in ollama_valid_models:
            raise Exception(f"Invalid Ollama model: {model_name}")

        return Ollama(model=model_name)

    elif model_provider == 'openai':
        openai_valid_models = ['gpt-4o', 'gpt-3.5-turbo-1106']

        if model_name not in openai_valid_models:
            raise Exception(f"Invalid OpenAI model: {model_name}")

        params = {
            "model": model_name,
            "temperature": 0,
            "verbose": True,
            "stream_usage": True,  # required for Helicone cost tracking
        }

        if tracer:
            proxy_config = tracer.get_proxy_config(config.use_cache)
            if proxy_config:
                if proxy_config.url:
                    params["base_url"] = proxy_config.url
                if proxy_config.headers:
                    params["default_headers"] = proxy_config.headers

        return ChatOpenAI(**params)
    else:
        raise Exception(f"Unknown model provider: {model_provider}")
