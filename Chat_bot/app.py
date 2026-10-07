from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
import streamlit as st
import openai

load_dotenv()
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
os.environ['LANGCHAIN_TRACING_V2']="true"
os.environ["LANGCHAIN_PROJECT"]="Chat_bot"

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are an helpful assistant.please provide the most accurate answer related to the user query"),
        ("user",'Question:{question}')
    ]
)

def generate_response(llm,temprature,max_tokens,question,api_key):
    openai.api_key=api_key
    llm=ChatOpenAI(model=llm)
    parser=StrOutputParser()
    chain=prompt|llm|parser
    
    response=chain.invoke({'question':question})
    return response

st.title("Q&A chatbot with openai")
st.sidebar.title("Settings")
api_key=st.sidebar.text_input("Enter the openai api key",type="password")
llm=st.sidebar.selectbox("select an OpenAi model",["gpt-4o","gpt-4-turbo","gpt-4"])
temprature=st.sidebar.slider("temprature",min_value=0.0,max_value=1.0,value=.7)
max_tokens=st.sidebar.slider("max_tokens",min_value=50,max_value=250,value=100)

st.write("Ask your Query")
user_input=st.text_input("You:")

if user_input:
    response=generate_response(llm,temprature,max_tokens,user_input,api_key)
    st.write(response)
else:
    st.write("pls provide the query")    