from code_agent.creat_react_code_agent.code_agent_react import CodeAgentReact

code_agent = CodeAgentReact(model="moonshotai/kimi-k2-instruct", model_provider="nvidia")

agent = code_agent.create_agent()