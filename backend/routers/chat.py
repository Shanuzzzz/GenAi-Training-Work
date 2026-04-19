from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import uuid
import os
from openai import OpenAI
from dotenv import load_dotenv

import schemas, models
from database import get_db
from dependencies import get_current_user

load_dotenv()

router = APIRouter()

# Initialize OpenAI Client automatically picking up OPENAI_API_KEY from .env
client = OpenAI()

@router.post("/query", response_model=schemas.ChatResponse)
def chat_query(
    query: schemas.ChatQuery, 
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session_id = query.session_id or str(uuid.uuid4())
    
    # Save user message
    user_msg = models.ChatHistory(
        user_id=current_user.id,
        session_id=session_id,
        role="user",
        content=query.message
    )
    db.add(user_msg)
    
    # Dynamic AI Integration Setup
    # Creating a system context based on Gov schemes
    system_prompt = """
    You are a GovScheme AI Assistant explicitly built to help Indian citizens understand 
    government benefits. Provide clear, concise, and helpful answers. Mention schemes 
    like PM Awas Yojana, PM-KISAN, and Ayushman Bharat when relevant. Use simple language 
    and format your output clearly.
    """
    
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query.message}
            ],
            max_tokens=300,
            temperature=0.7
        )
        agent_response = completion.choices[0].message.content
    except Exception as e:
        print(f"OpenAI Error: {e}")
        agent_response = "I am currently experiencing high network traffic communicating with the AI Core. Please try again in a moment."
    
    # Save Assistant message
    ai_msg = models.ChatHistory(
        user_id=current_user.id,
        session_id=session_id,
        role="assistant",
        content=agent_response
    )
    db.add(ai_msg)
    db.commit()
    
    return schemas.ChatResponse(
        response=agent_response,
        session_id=session_id,
        suggested_actions=["Check Eligibility Criteria", "How to apply?"]
    )

@router.get("/history/{session_id}")
def get_chat_history(
    session_id: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    history = db.query(models.ChatHistory).filter(
        models.ChatHistory.user_id == current_user.id,
        models.ChatHistory.session_id == session_id
    ).order_by(models.ChatHistory.timestamp).all()
    return history
