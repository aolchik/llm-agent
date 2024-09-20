import os
import uuid
from pydantic import BaseModel
from enum import Enum
from typing import Literal
from langtrace_python_sdk import langtrace
from helpers.logger import logger

AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")
LANGTRACE_API_KEY = os.getenv("LANGTRACE_API_KEY")

if not AGENTOPS_API_KEY:
    agentops = None


class TracerAnnotation(BaseModel):
    session: str = str(uuid.uuid4())
    app: str | None

    def tags(self):
        return [self.app] if self.app else []


class TraceProvider(Enum):
    provider: str


class LLMProxyConfig(BaseModel):
    url: str
    headers: dict


class Tracer(BaseModel):
    provider: Literal['agentops',
                      'helicone',
                      'langtrace',
                      'disabled'] = 'disabled'
    annotation: TracerAnnotation | None = None

    def init(self, default_tags=[]):
        logger.debug(f"Tracer initialized with provider: {self.provider}")

        if len(default_tags) > 0:
            tags = default_tags
        else:
            tags = self.annotation.tags()

        if self.provider == 'agentops':
            agentops.init(AGENTOPS_API_KEY, default_tags=[tags])

        if self.provider == 'langtrace':
            langtrace.init(api_key=LANGTRACE_API_KEY)

    def end(self):
        logger.debug(f"Tracer ended with provider: {self.provider}")

        if self.provider == 'agentops':
            agentops.end_session("Success")

    def get_proxy_config(self, use_cache=True) -> LLMProxyConfig | None:
        logger.debug(f"Tracer get_proxy_config with provider: {self.provider}")

        if self.provider == 'helicone':
            headers = {
                "Helicone-Auth": f"Bearer {os.getenv('HELICONE_API_KEY')}",
                "Helicone-Cache-Enabled": f"{use_cache}",
            }
            if self.annotation:
                if self.annotation.session:
                    headers["Helicone-Session-Id"] = \
                        self.annotation.session
                if self.annotation.app:
                    headers["Helicone-Property-App"] = self.annotation.app
            return LLMProxyConfig(
                url="https://oai.helicone.ai/v1",
                headers=headers)
        return None

    def get_tracer_annotation(self):
        return self.annotation


class TracerFactory:
    tracer_instance = None

    @staticmethod
    def get_tracer():
        if TracerFactory.tracer_instance is None:
            TracerFactory.tracer_instance = Tracer()
        return TracerFactory.tracer_instance

# USAGE
# from helpers.tracer import TracerFactory
# tracer = TracerFactory.get_tracer()
