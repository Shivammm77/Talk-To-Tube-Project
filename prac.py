from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
# 1. RAG Setup (simplified)
# ... (load, split, embed documents and store in Chroma) ...
import os
load_dotenv()
api = os.getenv("youtube_api")
vectorstore = Chroma(...)
retriever = vectorstore.as_retriever()

# 2. LLM Setup
llm = ChatGroq(model="llama-3.1-8b-instant", api_key=api, temperature=0.3)

# 3. Define Prompt with History
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful AI assistant. Answer questions based on the provided context and conversation history."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

# 4. Create RAG Chain
rag_chain = (
    {"context": retriever, "question": lambda x: x["question"]}
    | prompt
    | llm
)

# 5. Integrate Memory with RunnableWithMessageHistory
store = {}  # In-memory store for session histories (for demonstration)

def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)

# Invoke the chain with a session ID
answer = conversational_rag_chain.invoke({"question": "What is LangChain?"}, config={"configurable": {"session_id": "user123"}})
print(answer)