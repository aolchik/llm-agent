
# Obervability & Feedback

## Decision

Helicone + Truelens

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

## crewai testing feature

(+) scores each task separatedly
(-) do not explain reasons behind scores
(-) do not trace evaluator interactions

## Evals
https://cookbook.openai.com/examples/evaluation/getting_started_with_openai_evals
https://wandb.ai/wandb_fc/openai-evals/reports/OpenAI-Evals-Demo-Using-W-B-Prompts-to-Run-Evaluations--Vmlldzo0MTI4ODA3

(+) flexibility
(-) requires an ideal answer (task spec wouldn't be enough?)
(-) requires a lot of manual work
(-) learning curve
(-) uncertainty of how to apply to multi-step agents
(-) uncertainty of how to apply with no ideal answers

### Helicone
 
(+) Accurate cost tracking
(+) Timeline view
(+) Free tier

### Langtrace

(-) No timeline view
(+) Better metrics than AgenOps

## Truelens
https://www.trulens.org/

(+) easy to use
(+) run on current executions
(+) support for multiple metrics
(+) can run on logged interactions
(+) feedback cost measured separatedly

# LLM Abstractions

## LiteLLM

(+) Custom LLM facade implementation may solve AgentOps tracking issues (see https://docs.agentops.ai/v1/integrations/litellm)
(-) Do not track LLM calls through langchain_community.chat_models.ChatLiteLLM
(-) Documentation is not good.
(-) Do not seem to support Google Gemini authentication throught credentials.

# Vector Databases

## Pinecode

(+) Free tear
(+) Easy to use
(+) Good documentation
(-) Does not support pagination