from lib2to3.fixes.fix_input import context

import nest_asyncio
from streamlit import markdown

nest_asyncio.apply()

import aiohttp
import asyncio

from IPython.display import display, Markdown

import os
import streamlit as st

def generate_response(prompt, context):
    class LLM:
        url: str = 'http://10.100.30.243:1224/generate'

        async def get_response(self, json_data) -> str:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.url, json=json_data) as response:
                    if response.status != 200:
                        raise Exception(f"Error: {response.status}")
                    return await response.json()

    answer = asyncio.run(LLM().get_response(
                {
                    "system_prompt": "You are a helpful assistant, you speak all languages",
                    #"n": "3",
                    #"apply_chat_template": True,
                    "prompt":  message["content"] +  prompt, #"Привет! Расскажи о себе",
                    "stop": None,
                    "max_tokens": max_tokens,
                    "choice": None,
                    "schema": None,
                    "regex": None,
                    "temperature": temperature
                }
            ))
    #context += f"user: {prompt}" + " " + f"assistant: {answer}" + ". "
    print(context)
    return answer

st.set_page_config(page_title = "Llama 3.1 chatbot 🤖")
with st.sidebar:
    st.title("Llama 3.1 chatbot 🤖")
    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    max_tokens = st.sidebar.slider('max_tokens', min_value=64, max_value=10000, value=10000, step=8)

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    context = ''
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt, context)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
