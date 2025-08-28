# YouTube Chatbot 🎥💬

[Live Demo](https://youtubechatbotv1.streamlit.app/)

## Overview
This app allows you to **ask questions about any YouTube video** by simply providing its URL.  
It extracts the video transcript, processes it with **LangChain + Cohere embeddings**, and then lets you chat with the video content.

---

## Features
- 🔗 Enter a YouTube video URL
- 📜 Automatically fetches the transcript
- ✂️ Splits transcript into chunks for better context understanding
- 🌍 Detects transcript language (English / Hindi)
- 🧠 Uses **Cohere embeddings + FAISS vector store** for semantic search
- 🤖 Answers your questions using **Cohere LLM (command-r-plus)**
- ❓ If transcript lacks information, the bot will say it doesn't know

---

## Tech Stack
- Streamlit – Web UI  
- LangChain – Framework for chaining LLMs  
- Cohere – Embeddings + LLM  
- FAISS – Vector similarity search  
- YouTube Transcript API – Fetching transcripts  
- Python – Programming language  

---

## How It Works
1. **Extract Video ID** from YouTube URL  
   - Supports `https://www.youtube.com/watch?v=...` and `https://youtu.be/...` formats.
2. **Fetch Transcript** using `YouTubeTranscriptApi`
3. **Save Transcript** locally (`text.txt`)
4. **Split Transcript** into manageable chunks
5. **Detect Language** (English/Hindi) to choose embeddings
6. **Embed Chunks** with Cohere
7. **Store in FAISS** for efficient semantic search
8. **Query with LLM** (Cohere command-r-plus) using retrieved context

---

## Setup & Installation

### 1. Clone Repo
```bash
git clone https://github.com/yourusername/youtube-chatbot.git
cd youtube-chatbot
