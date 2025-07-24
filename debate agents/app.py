import streamlit as st
from debate_agents import debate, teamconfig
import asyncio

st.title("Watch 2 agents debate on a topic of your choice!")
st.write("What should the agents debate on?")
topic = st.text_input("Enter the topic of debate.")

clicked = st.button("Start Debate", type="primary")

chat = st.container()


if clicked:
    chat.empty()
    async def main():
        team = await teamconfig(topic)
        with chat:
           async for message in debate(team):
                if message.startswith('Annie'):
                    with st.chat_message(name="Annie", avatar="😃"):
                        st.write(message)
                elif message.startswith('Satoru'):
                    with st.chat_message(name="Satoru", avatar="⚪️"):
                       st.write(message)
                elif message.startswith('Suguru'):
                    with st.chat_message(name="Suguru", avatar="⚫️"):
                       st.write(message)
    asyncio.run(main())