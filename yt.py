from youtube_transcript_api import YouTubeTranscriptApi , TranscriptsDisabled , NoTranscriptFound
from langchain_core.prompts import MessagesPlaceholder
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings 
from langchain_community.vectorstores import FAISS
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel , RunnablePassthrough , RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
import os
load_dotenv()

import os
load_dotenv()
api = os.getenv("Youtube_llm")
def indexing( vd_id: str):
 try : 
        yt_api = YouTubeTranscriptApi()
        fetch_context = yt_api.fetch(vd_id , languages=[ "en" , "hi" ])
        transcript_text = " ".join(t.text for t in fetch_context)
        if not transcript_text :
            print("the error is transcript text is empty")
            return None
        spillter = RecursiveCharacterTextSplitter(chunk_size = 200 , chunk_overlap = 20)
        chunks = spillter.split_text(transcript_text)
        hf = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vector_store = FAISS.from_texts(chunks , embedding=hf)
        retriever = vector_store.as_retriever(search_type = "mmr" , search_kwargs = {"k" : 2})
        return retriever    
        
 except TranscriptsDisabled :
        print("No caption available")
        return None
 except NoTranscriptFound:
        print("No transcript found for this video.")
        return None
 
def format_doc(result):
     context = "\n\n".join(doc.page_content for doc in result)
     return context



def ask_question(video_id: str, question: str):
    retriever = indexing(video_id)
    llm = ChatGroq(model="llama-3.1-8b-instant", api_key=api, temperature=0.3)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a YouTube transcript helper. If answer not in context, say: I don't know."),
        
        ("human", "Context:\n{context}\n\nQuestion: {question}")
    ])
    
    parallel_chain = RunnableParallel({
        "context": retriever| RunnableLambda(format_doc),
        "question": RunnablePassthrough()
    }) 
    
    
    response = parallel_chain|prompt | llm | StrOutputParser()
    answer = response.invoke(question)
       
    
    return  answer