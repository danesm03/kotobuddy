from ui.interface import KotobuddyApp
from sqlmodel import SQLModel
from utils.word_parser import *
from utils.db import engine, texts_engine
from utils.data_types import Flashcard, SavedText, Node


SQLModel.metadata.create_all(bind=engine, tables=[Flashcard.__table__])

# Create tables for SavedText and Node in texts_engine
SQLModel.metadata.create_all(bind=texts_engine, tables=[SavedText.__table__, Node.__table__])



if __name__ == "__main__":   
    KotobuddyApp().run()