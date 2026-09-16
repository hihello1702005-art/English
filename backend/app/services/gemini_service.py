import json
from app.core.config import settings
from app.schemas.contracts import AIAnalysis, SpeechSignals
class GeminiService:
    """Language interpretation only; objective speech metrics remain provider-owned."""
    async def speaking_feedback(self, *, reference_text:str, teacher_transcript:str, speech:SpeechSignals, difficulty:str) -> AIAnalysis:
        if not settings.gemini_api_key: raise RuntimeError("Gemini is not configured.")
        from google import genai
        client=genai.Client(api_key=settings.gemini_api_key)
        prompt={"task":"Return JSON only matching the requested fields. Explain language, not pronunciation metrics.","reference_transcript":reference_text,"teacher_transcript":teacher_transcript,"speech_signals":speech.model_dump(),"lesson_difficulty":difficulty,"target_variety":"British English","schema":AIAnalysis.model_json_schema()}
        response=client.models.generate_content(model=settings.gemini_model,contents=json.dumps(prompt))
        return AIAnalysis.model_validate_json(response.text)
