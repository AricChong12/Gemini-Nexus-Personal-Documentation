from google.adk.agents.llm_agent import Agent  #import  lib

# root_agent = Agent(
#     model='gemini-2.5-flash',
#     name='root_agent',
#     description='A helpful assistant for user questions.',
#     instruction='Answer user questions to the best of your knowledge',
# )

root_agent = Agent(
    model='gemini-2.5-flash',  #define ai model
    name='math_tutor_agent',   #name of the ai agent
    description='Helps students learn algebra by guiding them through problemsolving steps.',
    #description of what the ai agent does
    instruction='You are a patient math tutor. Help students with algebra problems.'
    #instruction to guide the ai agent created how to work
)
