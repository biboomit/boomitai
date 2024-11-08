def delete_files(file_ids):
    for file_id in file_ids:
        openai.File.delete(file_id)

# Optionally, add a cleanup at the end of the script
def cleanup():
    if st.session_state.files_to_delete:
        delete_files(st.session_state.files_to_delete)
        st.session_state.files_to_delete = []