import streamlit as st
from helpers import *


def main():
    st.write(
        """
        # American Bank Savings HRIS with AI

        Powered with LLM GPT 💥

        ```python

        streamlit = "easy"  GPT = "cool"  both = "💥"
        ```
        """)
    st.subheader("Customer Fulfillment Feature added to Teller HRIS")

    # Upload Bills
    pdf_files = st.file_uploader("Upload Form",
                                 type=["pdf"],
                                 accept_multiple_files=True)
    extract_button = st.button("Transfer")

    if extract_button:
        with st.spinner("Processing"):
            data_frame = create_docs(pdf_files)
            st.write(data_frame.head())
            data_frame["TOTAL"] = data_frame["TOTAL"].astype(float)
            st.write("Average deposit amount: ", data_frame['TOTAL'].mean())

            # convert to csv
            convert_to_csv = data_frame.to_csv(index=False).encode("utf-8")


            st.download_button(
                "Download",
                convert_to_csv,
                "CSV_Deposit_Receipt.csv",
                "text/csv",
                key="download-csv"
            )
        st.success("Processed")



#Invoking main function
if __name__ == '__main__':
    main()