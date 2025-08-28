# yt.py
import re
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, Language
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_community.vectorstores import FAISS
from langchain_cohere import CohereEmbeddings, ChatCohere
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langdetect import detect
import streamlit as st


from urllib.parse import urlparse, parse_qs

def extract_video_id(url: str) -> str | None:
    """Extract the YouTube video ID from a URL, supporting various formats."""
    parsed = urlparse(url)

    # Try extracting 'v' parameter from the query
    query_params = parse_qs(parsed.query)
    if 'v' in query_params:
        return query_params['v'][0]

    # If no 'v' in query, use the last segment of the path
    path_segments = parsed.path.rstrip('/').split('/')
    if path_segments:
        return path_segments[-1]

    return None



def build_chain(video_url: str):
    # Fetch transcript
    video_id=extract_video_id(video_url)

    ytt_api = YouTubeTranscriptApi()
    fetched_transcript = ytt_api.fetch(video_id)

    # Save transcript
    with open("text.txt", "w", encoding="utf-8") as f:
        for snippet in fetched_transcript:
            f.write(snippet.text + "\n")
    


    # Load into Documents
    loader = TextLoader("text.txt", encoding="utf-8")
    docs = loader.load()



    # Split transcript
    splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.MARKDOWN,
        chunk_size=300,
        chunk_overlap=0,
    )
    chunks = splitter.split_documents(docs)

   
    full_text = " ".join(chunk.page_content for chunk in chunks)
    lang = detect(full_text)  # 'en' for English, 'hi' for Hindi etc.

    if lang == "hi":
        embeddings = "embed-multilingual-v3.0"
    else:
        embeddings = "embed-english-v3.0"

    # Cohere embeddings
    embeddings = CohereEmbeddings(
        model="embed-english-v3.0",
        cohere_api_key=st.secrets["COHERE_API_KEY"]
    )

    # Vector DB
    vector_store = FAISS.from_documents(chunks, embeddings)
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

    # LLM
    llm = ChatCohere(
        model="command-r-plus",
        cohere_api_key=st.secrets["COHERE_API_KEY"]

    )

    # Prompt
    prompt = PromptTemplate(
        template="""
          You are a helpful assistant.
          Answer ONLY from the provided transcript context.
          If the context is insufficient, just say you don't know.

          {context}
          Question: {question}
        """,
        input_variables=['context', 'question']
    )

    # Formatter
    def format_docs(retrieved_docs):
        return "\n\n".join(doc.page_content for doc in retrieved_docs)

    # Build runnable chain
    parallel_chain = RunnableParallel({
        'context': retriever | RunnableLambda(format_docs),
        'question': RunnablePassthrough()
    })

    parser = StrOutputParser()
    main_chain = parallel_chain | prompt | llm | parser

    return main_chain
