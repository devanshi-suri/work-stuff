from smolagents import CodeAgent, InferenceClientModel

# Initialize a model (using Hugging Face Inference API)
model = InferenceClientModel()  # Uses a default model

# Create an agent with no tools
agent = CodeAgent(tools=[], model=model)

# Run the agent with a task
result = agent.run(
    "What is the code to create a binary search tree?")
print(result)

from smolagents import DuckDuckGoSearchTool


agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=model,
)

# Now the agent can search the web!
result = agent.run("What is the current weather in Paris?")
print(result)
