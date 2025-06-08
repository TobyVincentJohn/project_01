from pydantic_settings import BaseSettings
from pydantic import Field

class ElevenLabsSettings(BaseSettings):
    ELEVENLABS_API_KEY: str = Field(..., env="ELEVENLABS_API_KEY")
    ELEVENLABS_AGENT_ID: str = Field(..., env="ELEVENLABS_AGENT_ID")
    TWILIO_ACCOUNT_SID: str = Field(..., env="TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN: str = Field(..., env="TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER: str = Field(..., env="TWILIO_PHONE_NUMBER")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

elevenlabs_settings = ElevenLabsSettings() 