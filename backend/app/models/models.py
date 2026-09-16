from datetime import datetime
from enum import Enum
from sqlalchemy import Boolean, DateTime, Enum as SAEnum, ForeignKey, Index, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.database.session import Base
class Role(str,Enum): ADMIN="admin"; TEACHER="teacher"
class Timestamped(Base):
    __abstract__=True
    created_at: Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
    updated_at: Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
class User(Timestamped):
    __tablename__="users"; id:Mapped[int]=mapped_column(primary_key=True); email:Mapped[str]=mapped_column(String(255),unique=True,index=True); full_name:Mapped[str]=mapped_column(String(150)); password_hash:Mapped[str]=mapped_column(String(255)); role:Mapped[Role]=mapped_column(SAEnum(Role),default=Role.TEACHER,index=True); is_active:Mapped[bool]=mapped_column(Boolean,default=True)
class Lesson(Timestamped):
    __tablename__="lessons"; id:Mapped[int]=mapped_column(primary_key=True); title:Mapped[str]=mapped_column(String(255),index=True); description:Mapped[str]=mapped_column(Text); lesson_type:Mapped[str]=mapped_column(String(20)); difficulty:Mapped[str]=mapped_column(String(20),index=True); duration_seconds:Mapped[int]=mapped_column(Integer); tags:Mapped[list]=mapped_column(JSON,default=list); published:Mapped[bool]=mapped_column(Boolean,default=False,index=True); created_by_id:Mapped[int]=mapped_column(ForeignKey("users.id"))
class LessonMedia(Timestamped):
    __tablename__="lesson_media"; id:Mapped[int]=mapped_column(primary_key=True); lesson_id:Mapped[int]=mapped_column(ForeignKey("lessons.id",ondelete="CASCADE"),index=True); url:Mapped[str]=mapped_column(String(2048)); media_type:Mapped[str]=mapped_column(String(30)); file_size:Mapped[int|None]=mapped_column(Integer); duration_seconds:Mapped[int|None]=mapped_column(Integer); metadata_json:Mapped[dict]=mapped_column(JSON,default=dict)
class LessonTranscript(Timestamped):
    __tablename__="lesson_transcripts"; id:Mapped[int]=mapped_column(primary_key=True); lesson_id:Mapped[int]=mapped_column(ForeignKey("lessons.id",ondelete="CASCADE"),unique=True); content:Mapped[str]=mapped_column(Text); locale:Mapped[str]=mapped_column(String(20),default="en-GB")
class LessonNote(Timestamped):
    __tablename__="lesson_notes"; id:Mapped[int]=mapped_column(primary_key=True); lesson_id:Mapped[int]=mapped_column(ForeignKey("lessons.id",ondelete="CASCADE"),index=True); content:Mapped[str]=mapped_column(Text); position:Mapped[int]=mapped_column(Integer,default=0)
class Vocabulary(Timestamped):
    __tablename__="vocabulary"; id:Mapped[int]=mapped_column(primary_key=True); lesson_id:Mapped[int]=mapped_column(ForeignKey("lessons.id",ondelete="CASCADE"),index=True); word:Mapped[str]=mapped_column(String(120)); meaning:Mapped[str]=mapped_column(Text); example_sentence:Mapped[str]=mapped_column(Text); phonetic:Mapped[str|None]=mapped_column(String(200)); reference_audio_url:Mapped[str|None]=mapped_column(String(2048)); locale:Mapped[str]=mapped_column(String(20),default="en-GB")
class ComprehensionQuestion(Timestamped):
    __tablename__="comprehension_questions"; id:Mapped[int]=mapped_column(primary_key=True); lesson_id:Mapped[int]=mapped_column(ForeignKey("lessons.id",ondelete="CASCADE"),index=True); prompt:Mapped[str]=mapped_column(Text); question_type:Mapped[str]=mapped_column(String(20)); options:Mapped[list]=mapped_column(JSON,default=list); correct_answer:Mapped[str|None]=mapped_column(Text)
class ComprehensionAnswer(Timestamped):
    __tablename__="comprehension_answers"; id:Mapped[int]=mapped_column(primary_key=True); question_id:Mapped[int]=mapped_column(ForeignKey("comprehension_questions.id")); user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),index=True); answer:Mapped[str]=mapped_column(Text); is_correct:Mapped[bool|None]=mapped_column(Boolean)
class SpeakingAttempt(Timestamped):
    __tablename__="speaking_attempts"; id:Mapped[int]=mapped_column(primary_key=True); user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),index=True); lesson_id:Mapped[int|None]=mapped_column(ForeignKey("lessons.id"),index=True); audio_url:Mapped[str]=mapped_column(String(2048)); reference_text:Mapped[str]=mapped_column(Text); transcript:Mapped[str|None]=mapped_column(Text); provider:Mapped[str|None]=mapped_column(String(100)); analysis_status:Mapped[str]=mapped_column(String(30),default="pending",index=True)
class SpeechScore(Timestamped):
    __tablename__="speech_scores"; id:Mapped[int]=mapped_column(primary_key=True); attempt_id:Mapped[int]=mapped_column(ForeignKey("speaking_attempts.id",ondelete="CASCADE"),unique=True); pronunciation:Mapped[float|None]=mapped_column(); fluency:Mapped[float|None]=mapped_column(); accuracy:Mapped[float|None]=mapped_column(); intonation:Mapped[float|None]=mapped_column(); raw_provider_data:Mapped[dict]=mapped_column(JSON,default=dict)
class SpeechFeedback(Timestamped):
    __tablename__="speech_feedback"; id:Mapped[int]=mapped_column(primary_key=True); attempt_id:Mapped[int]=mapped_column(ForeignKey("speaking_attempts.id",ondelete="CASCADE"),unique=True); grammar_score:Mapped[float|None]=mapped_column(); vocabulary_score:Mapped[float|None]=mapped_column(); feedback:Mapped[dict]=mapped_column(JSON,default=dict); model:Mapped[str|None]=mapped_column(String(100))
class PracticeWord(Timestamped):
    __tablename__="practice_words"; id:Mapped[int]=mapped_column(primary_key=True); user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),index=True); vocabulary_id:Mapped[int|None]=mapped_column(ForeignKey("vocabulary.id")); word:Mapped[str]=mapped_column(String(120)); status:Mapped[str]=mapped_column(String(30),default="active")
class UserProgress(Timestamped):
    __tablename__="user_progress"; user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),primary_key=True); lessons_completed:Mapped[int]=mapped_column(Integer,default=0); speaking_seconds:Mapped[int]=mapped_column(Integer,default=0); current_streak:Mapped[int]=mapped_column(Integer,default=0)
class UserLessonProgress(Timestamped):
    __tablename__="user_lesson_progress"; __table_args__=(UniqueConstraint("user_id","lesson_id"),); id:Mapped[int]=mapped_column(primary_key=True); user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),index=True); lesson_id:Mapped[int]=mapped_column(ForeignKey("lessons.id"),index=True); progress_percent:Mapped[int]=mapped_column(Integer,default=0); completed:Mapped[bool]=mapped_column(Boolean,default=False)
class Notification(Timestamped):
    __tablename__="notifications"; id:Mapped[int]=mapped_column(primary_key=True); user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),index=True); title:Mapped[str]=mapped_column(String(255)); body:Mapped[str]=mapped_column(Text); read:Mapped[bool]=mapped_column(Boolean,default=False)
