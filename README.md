# AI CRM System using FastAPI & LangGraph

##  Project Overview
This project is an AI-powered CRM system designed for healthcare professionals to manage interactions using AI agents.

---

##  Tech Stack
- Frontend: React
- Backend: FastAPI
- AI: LangGraph
- Language: Python, JavaScript

---

##  Features
- Log interaction with HCPs
- Suggest next steps using AI
- Fetch patient information
- Send notifications
- Generate summaries
- AI Agent with 5 tools

---

##  Architecture

React → FastAPI → LangGraph → Tools → Response

---

##  Project Structure
backend/
frontend/
---

##  How to Run

### Backend

cd backend
uvicorn main:app --reload


### Frontend

cd frontend
npm install
npm start


---

##  API Endpoint

POST /agent

Example request:

{
"input": "suggest next step"
}
