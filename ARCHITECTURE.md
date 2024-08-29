
# Obervability

## Decision

Helicone

## Options

### AgentOps 

(+) Timeline view
(+) Free tier
(+) Easily integrated
(-) Some LLM calls are not tracked
(-) Inaccurate cost tracking
    Tried to interface LLM calls through LiteLLM, but it is not that simple to authenticate Google.
    example:
        openai: 0.07
        helicone: 0.078
        agentops:
            log: 0.058
            web: <0.01

### Helicone
 
(+) Accurate cost tracking
(+) Timeline view
(+) Free tier

### Langtrace

(-) No timeline view
(+) Better metrics than AgenOps

# LLM Abstractions

## LiteLLM

(+) Custom LLM facade implementation may solve AgentOps tracking issues (see https://docs.agentops.ai/v1/integrations/litellm)
(-) Do not track LLM calls through langchain_community.chat_models.ChatLiteLLM
(-) Documentation is not good.
(-) Do not seem to support Google Gemini authentication throught credentials.