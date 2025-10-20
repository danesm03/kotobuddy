from sqlmodel import Field, SQLModel, Session, select, Relationship
from enum import Enum
from typing import Optional, List
from utils.word_parser import InputText
from datetime import date



#Handling for Flashcards
class Difficulty(Enum):
    EASY = 2
    MEDIUM = 1
    HARD = 0


class Flashcard(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    word: str
    review_date: date
    difficulty: Difficulty
    

def get_due_cards(session: Session):
    today = date.today()
    statement = select(Flashcard).where(Flashcard.review_date <= today)
    ##THIS IS WRONG JUST FOR TESTING vv
    #statement = select(Flashcard).where(Flashcard.review_date > today)
    results = session.exec(statement)
    return list(results)


def to_word_node(word):
        text = InputText()
        text.update(word)
        node = text.to_word_nodes()
        if not node:
            raise ValueError("no nodes produced for word: " + str(word))
        return node[0]


#Handling for SavedTexts
class Node(SQLModel, table=True):
     id: Optional[int] = Field(default=None, primary_key=True)
     word: str
     root_word: str
     unknown: bool
     definition: str
     reading: str
     saved_text_id: Optional[int] = Field(default=None, foreign_key="savedtext.id")
     saved_text: Optional["SavedText"] = Relationship(back_populates="nodes")

     

class SavedText(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    text: str
    nodes: List["Node"] = Relationship(back_populates="saved_text")

def get_saved_texts(session: Session):
     return list(
          session.exec(select(SavedText))
          )

 


