import asyncio
from autogen_core.models import UserMessage
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import TextMentionTermination

model = OllamaChatCompletionClient(model="llama3.2")

async def teamconfig(topic):
    # result = await model.create([UserMessage(content="What day is it today?", source="user")])
    # print(result.content)

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
    return team

async def debate(team):
    # stream the conversation
    async for message in team.run_stream(task="Start the debate."):
        if isinstance(message, TaskResult):
            message = f"Stop Reason:", message.stop_reason
            yield message
        else:
            message = f"{message.source}: {message.content}"
            yield message
        
async def main():
    # topic = topic
    team = await teamconfig()
    async for message in debate(team):
        print('-'*20)
        print(message)

if __name__ == "__main__":
    #   topic = "Best pasta shape"
      asyncio.run(main())
