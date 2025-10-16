from sqlmodel import Field, SQLModel, Session, select
from datetime import date, timedelta
from enum import Enum
from typing import Optional
from utils.word_parser import InputText, WordNode




class Difficulty(Enum):
    EASY = 3
    MEDIUM = 2
    HARD = 1


class Flashcard(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    word: str
    review_date: date
    difficulty: Difficulty
    
    @classmethod
    def set_review_date(cls, word, difficulty, **kwargs):
        review_date = date.today() + timedelta(days=difficulty.value)
        return cls(word=word, difficulty=difficulty, review_date=review_date, **kwargs)
    
    def to_word_node(cls, word, difficulty, **kwargs):
        text = InputText(text=word)
        node = text.to_word_nodes()
        return node[0]


def get_due_cards(session: Session):
    today = date.today()
    statement = select(Flashcard).where(Flashcard.review_date <= today)
    results = session.exec(statement)
    return list(results)
