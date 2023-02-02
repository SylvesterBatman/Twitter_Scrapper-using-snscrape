import streamlit as st


import pandas as pd
import json


def main():
    st.title("Twitter Scrapper using streamlit")
    menu = ["Dataset","About"]
    choice = st.sidebar.selectbox("Menu",menu)




    if choice == "Dataset":
        st.subheader("Dataset")


        data_file = st.file_uploader("Upload dataset",type=["csv"])
        if st.button("process"):
            if data_file is not None:
                st.write(type(data_file))
                file_details = {"filename":data_file.name,"filetype":data_file.type,"filesize":data_file.size}
                st.write(file_details)
                df = pd.read_csv(data_file)
                st.dataframe(df)

    

    else:
        st.subheader("About")




if __name__=='__main__':
    main()