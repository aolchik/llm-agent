
# End Platform Comparison


## Test Automation
so that
  previous fetures are supported at agent change
  understand the support of each platform to tests

feat: feedback report for each task

## Cost Control

spike: CrewAi - Long Term memory - how to reuse information already gathered

spike: helicone: using cache and adding data

bug: trulens: cost tracking now working

## Observability

feat: helicone: use session paths and names to better track agents and tasks

refactor: tracer: support parallel execution

refactor: llm wrapper: reuse instance models through factory pattern

## Investigation, Debugging and Experimentation

feat: support for questioning the result

bug: logger not working
  works on canvas
  does not work during agent execution

## Quality metrics

spike: how to compare quality of different outputs

## Integrations

spike: composio.dev

spike: crewai: human interaction agent

spike: langraph for event collection
  https://github.com/crewAIInc/crewAI-examples/blob/main/CrewAI-LangGraph/README.md

## Agent Architecture & Models
so that
  compare cost, latency and quality of different agent architectures
  see https://artificialanalysis.ai/


spike: LLM Powered Autonoous Agents
  https://lilianweng.github.io/posts/2023-06-23-agent/

spike: [Optimizing LLM Apps - 2024-01-08](https://klu.ai/blog/optimizing-llm-app-features)

spike: crewai: hierarchical process
  bug: didn't write the final report 1/2
  bug: didn't explain attributes 2/2
  bug: scores where done from 1 to 10 1/2
  bug: too expensive (USD3.69)
  bug: Support for Higher-end LLM Models
    Why Bedrock is 5 if it does not support OpenAI
  
spike: other llms

feat: support Azure OpenAI

spike: crewai: manager

spike: crewai: planner

spike: crew training

feat: improvement agent

## Report Improvement

bug: research report is not being generated

bug: research report in the wrong folder

bug: better support for agents is considering LangGraph Cloud
  Separate LangGraph and LangChain

feat: validate all tasks meet requirements

feat: overall score per platform

feat: fact checker
  crewAI - Langchain it is easier to use?
    where are the evidences?
  LangGraph cloud is not yet available
  claimed features should be validated
  references are considering main sites only

feat: code evaluation agent

feat: support for scientific papers research

feat: translate report

feat: remaining attributes

feat: remaning platforms

feat: scores are too close
  review criterias and re-evaluate scores
  improve criteria task

## Refactor

refactor: renomear src/tool_valuator_agent para src/agent

## Support for any research

## Scalability

spike: parallelization & async execution