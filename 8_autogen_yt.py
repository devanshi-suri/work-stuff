import asyncio
from autogen_core.models import UserMessage
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import TextMentionTermination


model = OllamaChatCompletionClient(model="llama3.2")

async def main():
    # result = await model.create([UserMessage(content="What day is it today?", source="user")])
    # print(result.content)
    topic = "Who is the best singer in English pop music in the last 10 years?"

    host = AssistantAgent(
         name = "Annie",
         model_client=model,
         system_message=f"You are Annie, a host agent for a debate. The topic of the debate is {topic}. You will moderate the debate between Satoru and Suguru. At the beginning, introduce the round number and at the beginning of round 3, announce that this will be the last round. After the last round, thank the audience and yell terminate.",
    )
    suppoter = AssistantAgent(
         name = "Satoru",
         system_message = f"You are Satoru, a agent that debats other agents. You will be debating on the topic {topic} against another agent. Keep your respinses limited to 50 words.",
         model_client=model,
    )
    critic = AssistantAgent(
         name = "Suguru",
         system_message = f"You are Suguru, a critic agent in a debate. You will be debating on the topic {topic} against Satoru. Keep your respinses limited to 50 words.",
         model_client=model,
    )

    text_termination_condition = TextMentionTermination("TERMINATE","terminate")
    team = RoundRobinGroupChat(participants=[host, suppoter, critic], max_turns=14, termination_condition=text_termination_condition)

    #  run the team and print after completion

    '''res = await team.run(task="Start the debate.")
    for message in res.messages:
        print('-'*20)
        print(f"{message.source}: {message.content}")'''

    # stream the conversation
    async for message in team.run_stream(task="Start the debate."):
        print('-'*20)
        if isinstance(message, TaskResult):
            print("Stop Reason:", message.stop_reason)
        else:
            print(f"{message.source}: {message.content}")
        

if __name__ == "__main__":
      asyncio.run(main())