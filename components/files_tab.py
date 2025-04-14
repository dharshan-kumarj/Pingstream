import streamlit as st

def files_tab(tab):
    with tab:
        st.subheader("Files")
        uploaded_file = st.file_uploader("Upload File", type=None)
        if uploaded_file:
            file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "Size": uploaded_file.size}
            st.json(file_details)
        return uploaded_file
