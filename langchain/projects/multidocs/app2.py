# for env
import os
from dotenv import find_dotenv, load_dotenv
# GPT LLM
import openai
# Langchain to feed in private data
# open gpt
from langchain.chat_models import ChatOpenAI
# open file
from langchain.document_loaders import PyPDFLoader
# chat with your data by wrap LLM
from langchain.chains.question_answering import load_qa_chain


