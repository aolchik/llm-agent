import os
import uuid
from pydantic import BaseModel
from enum import Enum
from typing import Literal, Optional
from langtrace_python_sdk import langtrace
from helpers.logger import logger

AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")
LANGTRACE_API_KEY = os.getenv("LANGTRACE_API_KEY")

# AgentOps is not being imported anymore as it cannot be completely disabled
if not AGENTOPS_API_KEY:
    agentops = None


class TracerAnnotation(BaseModel):
    session: Optional[str] = None
    app: str = ''

    def tags(self):
        return [self.app] if self.app else []

    def generate_session(self):
        self.session = str(uuid.uuid4())


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

    def init(self, default_tags=[], session_id=None) -> TracerAnnotation:
        logger.debug(f"Tracer initialized with provider: {self.provider}")

        annotation = TracerAnnotation(app=self.annotation.app)

        if not session_id:
            annotation.generate_session()
        else:
            annotation.session = session_id

        if len(default_tags) > 0:
            tags = default_tags
        else:
            tags = self.annotation.tags()

        if self.provider == 'agentops':
            agentops.init(AGENTOPS_API_KEY, default_tags=[tags])

        if self.provider == 'langtrace':
            langtrace.init(api_key=LANGTRACE_API_KEY)

        self.annotation = annotation
        return annotation

    def end(self):
        logger.debug(f"Tracer ended with provider: {self.provider}")

        if self.provider == 'agentops':
            agentops.end_session("Success")

    def get_proxy_config(self, use_cache=True,
                         annotation_context: TracerAnnotation | None = None
                         ) -> LLMProxyConfig | None:
        logger.debug(f"Tracer get_proxy_config with provider: {self.provider}")

        if self.provider == 'helicone':
            headers = {
                "Helicone-Auth": f"Bearer {os.getenv('HELICONE_API_KEY')}",
                "Helicone-Cache-Enabled": f"{use_cache}",
            }

            if annotation_context:
                annotation = annotation_context
            else:
                # Warning: not thread safe
                annotation = self.annotation

            if annotation:
                if annotation.session:
                    headers["Helicone-Session-Id"] = \
                        annotation.session
                if annotation.app:
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
            TracerFactory.tracer_instance.annotation = TracerAnnotation(
                app='llm_agent')
        return TracerFactory.tracer_instance

# USAGE
# from helpers.tracer import TracerFactory
# tracer = TracerFactory.get_tracer()
