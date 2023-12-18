from langchain.llms import OpenAI
from pypdf import PdfReader
import pandas as pd
import re
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType

import openai
import os
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

# chat = ChatOpenAI(temperature=.7, model="gpt-3.5-turbo")

# Extract Info rom PDF file
def get_pdf_text(pdf_doc):
    text=""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Extract data from text
def extracted_data(pages_data):
    template = """Extract all the following values : Account Number, Name, Date,
         SUBTOTAL, TOTAL, From and Terms from: {pages}

        Expected output: remove any dollar symbols {{'Account Number': '12345678','Name': 'Jane Doe','Date': '05/04/2023','TOTAL': '399.95', 'SUBTOTAL': '399.95', 'From': 'DEPOSIT TICKET', 'Terms': 'sign here if cash received'}}
        """
    prompt_template = PromptTemplate(input_variables=["pages"], template=template)
    llm = OpenAI(temperature=.7)
    full_response=llm(prompt_template.format(pages=pages_data))

    return full_response

# create documents from the uploaded pdfs
def create_docs(user_pdf_list):
    df = pd.DataFrame({'Account Number': pd.Series(dtype='int'),
                   'Name': pd.Series(dtype='str'),
                   'Date': pd.Series(dtype='str'),
	              'SUBTOTAL': pd.Series(dtype='int'),
                   'TOTAL': pd.Series(dtype='int'),
	                'From': pd.Series(dtype='str'),
                   'Terms': pd.Series(dtype='str')

                    })

    for filename in user_pdf_list:

        print(filename)
        raw_data=get_pdf_text(filename)
        #print(raw_data)
        #print("extracted raw data")

        llm_extracted_data=extracted_data(raw_data)
        #print("llm extracted data")
        #Adding items to our list - Adding data & its metadata

        pattern = r'{(.+)}' # capture one or more of any character, except newline
        match = re.search(pattern, llm_extracted_data, re.DOTALL)

        if match:
            extracted_text = match.group(1)
            # Converting the extracted text to a dictionary
            data_dict = eval('{' + extracted_text + '}')
            print(data_dict)
        else:
            print("No match found.")


        # df=df.append([data_dict], ignore_index=True) #this won't work!!
        df = pd.concat([df, pd.DataFrame([data_dict])], ignore_index=True)

        # df = pd.concat(df, pd.DataFrame([eval('{' +item+'}')]), ignore_index=True )

        print("complete")
        #df=df.append(save_to_dataframe(llm_extracted_data), ignore_index=True)

    df.head()
    return df