"""
Main FastAPI application for AI Chat Assistant
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import logging
from datetime import datetime

from chat_service import ChatService
from database import SessionLocal, engine, Base, ChatHistory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="AI Chat Assistant API",
    description="An intelligent chat assistant powered by OpenAI GPT",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chat service
chat_service = ChatService()


# Request/Response Models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"


class ChatResponse(BaseModel):
    response: str
    session_id: str


class ClearSessionRequest(BaseModel):
    session_id: str


class HistoryResponse(BaseModel):
    id: int
    user_message: str
    assistant_response: str
    timestamp: datetime
    session_id: str


# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AI Chat Assistant API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/api/chat",
            "clear": "/api/clear",
            "history": "/api/history/{session_id}",
            "health": "/api/health"
        }
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db=Depends(get_db)):
    """
    Process user message and generate AI response
    
    Args:
        request: ChatRequest with message and session_id
        
    Returns:
        ChatResponse with AI-generated response
    """
    try:
        logger.info(f"Received message from session {request.session_id}: {request.message[:50]}...")
        
        # Generate response using chat service
        response = await chat_service.generate_response(
            message=request.message,
            session_id=request.session_id
        )
        
        # Store in database
        chat_entry = ChatHistory(
            user_message=request.message,
            assistant_response=response,
            session_id=request.session_id,
            timestamp=datetime.utcnow()
        )
        db.add(chat_entry)
        db.commit()
        
        logger.info(f"Response generated successfully for session {request.session_id}")
        
        return ChatResponse(
            response=response,
            session_id=request.session_id
        )
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate response: {str(e)}"
        )


@app.post("/api/clear")
async def clear_session(request: ClearSessionRequest):
    """
    Clear conversation context for a specific session
    
    Args:
        request: ClearSessionRequest with session_id
    """
    try:
        chat_service.clear_context(request.session_id)
        logger.info(f"Cleared context for session {request.session_id}")
        return {"message": f"Session {request.session_id} cleared successfully"}
    except Exception as e:
        logger.error(f"Error clearing session: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear session: {str(e)}"
        )


@app.get("/api/history/{session_id}", response_model=List[HistoryResponse])
async def get_history(session_id: str, limit: int = 50, db=Depends(get_db)):
    """
    Retrieve chat history for a specific session
    
    Args:
        session_id: Session identifier
        limit: Maximum number of messages to return
        
    Returns:
        List of chat history entries
    """
    try:
        history = db.query(ChatHistory).filter(
            ChatHistory.session_id == session_id
        ).order_by(
            ChatHistory.timestamp.desc()
        ).limit(limit).all()
        
        # Reverse to get chronological order
        history.reverse()
        
        return history
    except Exception as e:
        logger.error(f"Error retrieving history: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve history: {str(e)}"
        )


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

