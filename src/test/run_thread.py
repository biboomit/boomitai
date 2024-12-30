from threads_messages import ThreadMessageRetriever


retriever = ThreadMessageRetriever()

messages = retriever.get_thread_messages(
    thread_id='thread_v48StiBZGNinBnMP6JNmuO57')

for message in messages['message_ids']:
    print(f"Message ID: {message['id']}")
    
# print(retriever.get_message_content(
#     thread_id='thread_v48StiBZGNinBnMP6JNmuO57',
#     message_id='msg_1c6uusQfBW4BfpCho1pqufMi'
# ))
