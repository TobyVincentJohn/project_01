from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.outbound_call_service import OutboundCallService
from app.models.calling_lists import CallingList
from pydantic import BaseModel
from typing import Optional
import logging
from ....services.elevenlabs_call_service import ElevenLabsCallService

router = APIRouter()
logger = logging.getLogger(__name__)
call_service = ElevenLabsCallService()

class CallStatusUpdate(BaseModel):
    CallSid: str
    CallStatus: str
    CallDuration: Optional[int] = None

class OutboundCallRequest(BaseModel):
    phone_number: str
    first_message: str
    custom_prompt: Optional[str] = None

@router.post("/process-list/{calling_list_id}")
async def process_calling_list(
    calling_list_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Start processing a calling list."""
    # Verify calling list exists
    calling_list = db.query(CallingList).filter(CallingList.id == calling_list_id).first()
    if not calling_list:
        raise HTTPException(status_code=404, detail="Calling list not found")
    
    # Initialize service
    call_service = OutboundCallService(db)
    
    # Add to background tasks
    background_tasks.add_task(call_service.process_calling_list, calling_list_id)
    
    return {"message": f"Started processing calling list {calling_list_id}"}

@router.post("/status")
async def call_status_webhook(
    status_update: CallStatusUpdate,
    db: Session = Depends(get_db)
):
    """Handle Twilio status callback webhook."""
    try:
        call_service = OutboundCallService(db)
        call_service.handle_call_status_update(
            status_update.CallSid,
            status_update.CallStatus,
            status_update.CallDuration
        )
        return {"message": "Status updated successfully"}
    except Exception as e:
        logger.error(f"Error handling status update: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing status update")

@router.post("/connect")
async def connect_call():
    """Handle Twilio connect webhook when call is answered."""
    # This is where we'll integrate with ElevenLabs for the AI conversation
    # For now, return a simple TwiML response
    return {
        "twiml": """
        <?xml version="1.0" encoding="UTF-8"?>
        <Response>
            <Say>Hello! This is an automated call. Goodbye!</Say>
            <Hangup/>
        </Response>
        """
    }

@router.post("/outbound-call")
async def initiate_outbound_call(request: OutboundCallRequest):
    """
    Initiates an outbound call using ElevenLabs Conversational AI
    
    Args:
        request: OutboundCallRequest containing:
            - phone_number: The number to call
            - first_message: The first message the agent should say
            - custom_prompt: Optional custom system prompt for the agent
    """
    try:
        call_sid = await call_service.initiate_outbound_call(
            to_number=request.phone_number,
            first_message=request.first_message,
            custom_prompt=request.custom_prompt
        )
        return {"status": "success", "call_sid": call_sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 