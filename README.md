 TalkToTube — Chat with Any YouTube Video!

TalkToTube is an AI-powered YouTube transcript assistant where users can paste any YouTube video link and get answers instantly — without watching the full video!
It uses RAG (Retrieval Augmented Generation) to fetch accurate responses based on real video content.
Secure authentication and modern FastAPI backend included!

✨ Features

 Ask Questions From Any YouTube Video
Just paste a link — no need to watch the whole video.

> RAG Powered AI Responses
The app intelligently extracts video transcript → chunks → stores embeddings in ChromaDB → retrieves relevant context for accurate answers.

> User Authentication
Secure login & signup using PostgreSQL for user storage.

⚡ FastAPI Backend
Lightweight, scalable, production-ready API.

> Simple & Clean Frontend
UI built using HTML, CSS, JavaScript — easy to use and fast.

 Tech Stack : 
Layer	Technology
Backend	FastAPI
Database	PostgreSQL
Vector Store	ChromaDB
AI Model	(Groq / OpenAI / any used by you)
Transcript Fetching	YouTube Transcripts API
Frontend	HTML, CSS, JavaScript
Authentication	JWT Tokens
Deployment	(GitHub + Vercel or Railway, etc.)
⚙️ How It Works (Architecture)
User Inputs YouTube Link
         ⬇
Extract Transcript → Chunking → Embedding
         ⬇
Store embeddings in ChromaDB
         ⬇
User asks a question
         ⬇
Relevant transcript chunks fetched (RAG)
         ⬇
AI generates accurate answer based on video content

 >Running Locally
1️⃣ Clone the repo
git clone https://github.com/your-username/TalkToTube.git
cd TalkToTube

2️⃣ Create and update .env
DB_URL=postgres-url
YOUTUBE_API_KEY=your-key
GROQ_API_KEY=your-key
JWT_SECRET=your-secret

3️⃣ Install backend dependencies
pip install -r requirements.txt

4️⃣ Start FastAPI server
uvicorn app.main:app --reload

5️⃣ Open the frontend

Simply open index.html in your browser

> Authentication

Users must log in / sign up

Valid users can store query history in PostgreSQL

JWT tokens for secure API access

📸 Screenshots (Add when hosted)
Upload YouTube Link	Ask Questions
(Add screenshot here)	(Add screenshot here)
📌 Future Enhancements

🎧 Support for audio-only content

🌍 Multi-language transcript support

💬 Chat history per video

🚀 Improved UI with modern framework (React / Next.js)

📱 Mobile responsive interface

⭐ If You Like This Project

Don’t forget to Star ⭐ the repository!
It motivates me to build more awesome AI apps 😊

📬 Contact

Feel free to connect for collaboration or feedback:

Developer: Shivam Soni

LinkedIn: www.linkedin.com/in/shivam-soni11

