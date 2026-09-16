from pydantic import BaseModel, Field
class RegisterRequest(BaseModel): email:str; full_name:str=Field(min_length=2,max_length=150); password:str=Field(min_length=12,max_length=128)
class LoginRequest(BaseModel): email:str; password:str
class TokenResponse(BaseModel): access_token:str; token_type:str="bearer"
class LessonCreate(BaseModel): title:str; description:str; lesson_type:str; difficulty:str; duration_seconds:int=Field(gt=0); tags:list[str]=[]; published:bool=False
class SpeechSignals(BaseModel): transcript:str|None=None; pronunciation:float|None=None; fluency:float|None=None; accuracy:float|None=None; intonation:float|None=None; provider_data:dict={}
class AIAnalysis(BaseModel): grammar_score:float|None=None; vocabulary_score:float|None=None; feedback:str; strengths:list[str]=[]; areas_to_improve:list[str]=[]; practice_words:list[str]=[]; recommendations:list[str]=[]
