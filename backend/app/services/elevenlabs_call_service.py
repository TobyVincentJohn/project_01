from typing import Optional
import requests
from twilio.rest import Client
from ..core.elevenlabs_config import elevenlabs_settings

class ElevenLabsCallService:
    def __init__(self):
        self.twilio_client = Client(
            elevenlabs_settings.TWILIO_ACCOUNT_SID,
            elevenlabs_settings.TWILIO_AUTH_TOKEN
        )
        self.agent_id = elevenlabs_settings.ELEVENLABS_AGENT_ID
        self.api_key = elevenlabs_settings.ELEVENLABS_API_KEY
        
    async def initiate_outbound_call(
        self,
        to_number: str,
        first_message: str,
        custom_prompt: Optional[str] = None
    ):
        """
        Initiates an outbound call using ElevenLabs Conversational AI
        
        Args:
            to_number: The phone number to call
            first_message: The first message the agent should say
            custom_prompt: Optional custom system prompt for the agent
        """
        # Configure the agent for Twilio compatibility
        self._configure_agent_audio()
        
        # Create the call using Twilio
        call = self.twilio_client.calls.create(
            to=to_number,
            from_=elevenlabs_settings.TWILIO_PHONE_NUMBER,
            url=f"https://api.elevenlabs.io/v1/agents/{self.agent_id}/call/start",
            method="POST",
            status_callback=f"https://api.elevenlabs.io/v1/agents/{self.agent_id}/call/status",
            status_callback_method="POST",
            headers={
                "xi-api-key": self.api_key,
                "Content-Type": "application/json"
            },
            parameters={
                "first_message": first_message,
                "system_prompt": custom_prompt
            } if custom_prompt else {
                "first_message": first_message
            }
        )
        
        return call.sid
        
    def _configure_agent_audio(self):
        """Configures the agent to use the correct audio format for Twilio"""
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        # Configure TTS output format
        requests.patch(
            f"https://api.elevenlabs.io/v1/agents/{self.agent_id}/settings",
            headers=headers,
            json={
                "voice": {
                    "format": "mulaw",
                    "sample_rate": 8000
                }
            }
        )
        
        # Configure input format
        requests.patch(
            f"https://api.elevenlabs.io/v1/agents/{self.agent_id}/settings",
            headers=headers,
            json={
                "advanced": {
                    "input_format": "mulaw_8000"
                }
            }
        ) 