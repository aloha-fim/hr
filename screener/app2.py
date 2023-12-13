import streamlit as st
import os
from dotenv import load_dotenv
from utils import *
import uuid

#Creating session variables
if 'unique_id' not in st.session_state:
    st.session_state['unique_id'] =''

def main():
    load_dotenv()

    st.set_page_config(page_title="American Bank Savings")

    st.write(
        """
        # Example American Bank Savings HRIS with AI

        Powered with LLM GPT 💥

        ```python
        # AI powered
        streamlit = "easy"
        GPT = "cool"
        both = "💥"
        ```
        """)
    st.title("HRIS AI")
    st.subheader("Upload Thousands of Resumes Now")

    job_description = st.text_area("Input 'HR JOB DESCRIPTION'",key="1")

    #document_count = st.text_input("No.of 'RESUMES' to return",key="2")

    document_count = st.slider(
        "Number of Top Results", min_value=1, max_value=3, key="2"
    )
    # Upload the Resumes (pdf files)
    pdf = st.file_uploader("Upload Resumes, Employee Survey, Exit Interviews, etc.", type=["pdf"],accept_multiple_files=True)

    submit=st.button("AI Computation Now")

    if submit:
        with st.spinner('Processing...'):

            #Creating a unique ID, so that we can use to query and get only the user uploaded documents from PINECONE vector store
            st.session_state['unique_id']=uuid.uuid4().hex

            #Create a documents list out of all the user uploaded pdf files
            final_docs_list=create_docs(pdf,st.session_state['unique_id'])

            #Displaying the count of resumes that have been uploaded
            st.write("*Resumes uploaded* :"+str(len(final_docs_list)))

            #Create embeddings instance
            embeddings=create_embeddings_load_data()

            #Push data to PINECONE
            push_to_pinecone(os.getenv("PINECONE_API"),os.getenv("PINECONE_TYPE"),os.getenv("PINECONE_NAME"),embeddings,final_docs_list)

            #Fecth relavant documents from PINECONE
            relavant_docs=similar_docs(job_description,document_count,os.getenv("PINECONE_API"),os.getenv("PINECONE_TYPE"),os.getenv("PINECONE_NAME"),embeddings,st.session_state['unique_id'])

            #t.write(relavant_docs)

            #Introducing a line separator
            st.write(":seedling:" * 30)

            #For each item in relavant docs - we are displaying some info of it on the UI
            for item in range(len(relavant_docs)):

                st.subheader("🔑 "+str(item+1))

                #Displaying Filepath
                st.write("**File** : "+relavant_docs[item][0].metadata['name'])

                #Introducing Expander feature
                with st.expander('Show results'):
                    st.info("**Causal Ranking** : "+str(relavant_docs[item][1]))
                    #st.write("***"+relavant_docs[item][0].page_content)

                    #Gets the summary of the current item using 'get_summary' function that we have created which uses LLM & Langchain chain
                    summary = get_summary(relavant_docs[item][0])
                    st.write("**Summary** : "+summary)

        st.success("Better than sifting through 5,000 files one at a time")


#Invoking main function
if __name__ == '__main__':
    main()
