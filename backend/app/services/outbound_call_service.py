from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from elevenlabs import generate
from app.models.calling_lists import Contact, CallStatus
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class OutboundCallService:
    def __init__(self, db: Session):
        self.db = db
        self.twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
    def get_next_contact(self, calling_list_id: int) -> Optional[Contact]:
        """Get the next contact to call from the calling list."""
        return self.db.query(Contact).filter(
            Contact.calling_list_id == calling_list_id,
            Contact.is_called == False,
            (Contact.next_attempt_after.is_(None) | (Contact.next_attempt_after <= datetime.utcnow()))
        ).order_by(
            Contact.attempts.asc(),
            Contact.id.asc()
        ).first()

    async def process_calling_list(self, calling_list_id: int):
        """Process all contacts in a calling list."""
        while True:
            contact = self.get_next_contact(calling_list_id)
            if not contact:
                break
                
            try:
                await self.make_call(contact)
            except Exception as e:
                logger.error(f"Error processing contact {contact.id}: {str(e)}")
                self._update_contact_status(contact, CallStatus.FAILED, str(e))

    async def make_call(self, contact: Contact):
        """Make an outbound call to a contact."""
        try:
            # Initialize call with Twilio
            call = self.twilio_client.calls.create(
                url=f"{settings.BASE_URL}/api/v1/calls/connect",  # Webhook for when call is answered
                to=contact.phone_number,
                from_=settings.TWILIO_PHONE_NUMBER,
                status_callback=f"{settings.BASE_URL}/api/v1/calls/status",  # Webhook for call status updates
                status_callback_event=['initiated', 'ringing', 'answered', 'completed'],
                timeout=30  # Timeout after 30 seconds if no answer
            )
            
            # Update contact with attempt
            contact.attempts += 1
            contact.last_call_timestamp = datetime.utcnow()
            self.db.commit()
            
            return call.sid
            
        except TwilioRestException as e:
            logger.error(f"Twilio error for contact {contact.id}: {str(e)}")
            self._update_contact_status(contact, CallStatus.FAILED, str(e))
            raise

    def _update_contact_status(self, contact: Contact, status: CallStatus, notes: str = None):
        """Update contact status after a call attempt."""
        contact.last_call_status = status
        contact.last_call_timestamp = datetime.utcnow()
        
        if notes:
            contact.call_notes = notes
            
        if status in [CallStatus.NO_ANSWER, CallStatus.BUSY, CallStatus.FAILED]:
            # Schedule next attempt based on number of attempts
            delay_hours = min(2 ** contact.attempts, 48)  # Exponential backoff, max 48 hours
            contact.next_attempt_after = datetime.utcnow() + timedelta(hours=delay_hours)
        elif status == CallStatus.COMPLETED:
            contact.is_called = True
            
        self.db.commit()

    def handle_call_status_update(self, call_sid: str, status: str, duration: int = None):
        """Handle status callback from Twilio."""
        # Map Twilio status to our CallStatus
        status_mapping = {
            'completed': CallStatus.COMPLETED,
            'no-answer': CallStatus.NO_ANSWER,
            'busy': CallStatus.BUSY,
            'failed': CallStatus.FAILED,
        }
        
        if status in status_mapping:
            # Find contact by call SID (you'll need to store this mapping)
            # For now, this is a placeholder
            contact = self.db.query(Contact).filter(Contact.call_sid == call_sid).first()
            if contact:
                self._update_contact_status(contact, status_mapping[status])
                if duration:
                    contact.call_duration = duration
                    self.db.commit() 