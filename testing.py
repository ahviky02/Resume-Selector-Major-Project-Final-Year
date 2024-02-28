import streamlit as st

# Title of the app
st.title('Multiple File Uploader')

# Allow users to upload multiple files
uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True)

# If files are uploaded
if uploaded_files:
    st.write("### Uploaded files:")
    for uploaded_file in uploaded_files:
        st.write(uploaded_file.name)
