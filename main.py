from ui.interface import KotobuddyApp
from sqlmodel import SQLModel
from utils.word_parser import *
from utils.db import engine


SQLModel.metadata.create_all(engine)



if __name__ == "__main__":   
    KotobuddyApp().run()