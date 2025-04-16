from huey.contrib.djhuey import task

from core.ai.chroma import chroma, openai_ef
from core.ai.mistral import mistral
from core.ai.prompt_manager import PromptManager
from core.methods import send_notification
from documents.models import DOC_PROCESS_DONE, Document
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings


@task()
def process_document(document: Document):
    filename = document.file.name

    uploaded_pdf = mistral.files.upload(
        file={
            "file_name": filename,
            "content": open(f"media/{filename}", "rb"),
        },
        purpose="ocr",
    )
    signed_url = mistral.files.get_signed_url(file_id=uploaded_pdf.id)
    print(signed_url)

    send_notification("notification", "Document processing started")
    ocr_response = mistral.ocr.process(
        model="mistral-ocr-latest",
        document={"type": "document_url", "document_url": signed_url.url},
        include_image_base64=False,
    )

    content = ""

    for page in ocr_response.dict().get("pages", []):
        content += page["markdown"]


    send_notification("notification", "Summarizing the document")
    pm = PromptManager()
    pm.add_message(
        "system",
        " Summarize the following document. And get the bullets point of the content, Only the summarization part is required. DO NOT ADD ANY EXTRA TEXT.",
    )
    pm.add_message("user", f"document: {content}")

    res = pm.generate()

    document.raw_text = content
    document.summary_text = res
    document.status = DOC_PROCESS_DONE
    document.save()

    send_notification("notification", "Splitting the document into chunks")
    splitter = SemanticChunker(OpenAIEmbeddings())
    documents = splitter.create_documents([content])

    send_notification("notification", "Creating embeddings for the chunks")
    collection = chroma.create_collection(name=document.id, embedding_function=openai_ef)

    collection.add(
        documents=[doc.model_dump().get("page_content") for doc in documents],
        ids=[str(i) for i in range(len(documents))]
    )
    send_notification("done", document.id)


