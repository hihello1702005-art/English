"""Provider boundary. No scores are produced until a real speech provider is configured."""
from typing import Protocol
from app.schemas.contracts import SpeechSignals
class SpeechAnalysisService(Protocol):
    async def analyse(self, *, audio_url:str, reference_text:str, locale:str="en-GB") -> SpeechSignals: ...
class UnconfiguredSpeechAnalysisService:
    async def analyse(self, *, audio_url:str, reference_text:str, locale:str="en-GB") -> SpeechSignals:
        raise RuntimeError("Speech analysis is not configured. Connect a provider before requesting pronunciation measurements.")
