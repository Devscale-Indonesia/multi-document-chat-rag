from huey.contrib.djhuey import task
from core.ai.prompt_manager import PromptManager
from core.methods import send_chat_message
from chats.models import Conversation
from core.ai.chroma import chroma, openai_ef

@task()
def process_chat(message, document_id):
    Conversation.objects.create(message=message, role="user")

    collection = chroma.get_collection(name=document_id, embedding_function=openai_ef)

    content = collection.query(
        query_texts=[message],
        n_results=3,
    )

    chats = Conversation.objects.all()
    messages = [{ "role": "system", "content": f"You are a helpful assistant. Answer the user's question based on the context provided. Content: {content}, Important: The response should be plain text, no format or table. use double break line for new paragraph"}]

    for chat in chats:
        messages.append({ "role": chat.role, "content": chat.message})


    p = PromptManager()
    p.set_messages(messages)
    res = p.generate()

    print(p.get_messages())

    Conversation.objects.create(message=res, role="assistant")
    send_chat_message(res)
