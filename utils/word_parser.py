import MeCab
from jamdict import Jamdict
from fugashi import Tagger
import unidic
from ui.interface import GenerateScreen

class InputText:
    def __init__(self,text):
        self.text = GenerateScreen.print_text_input()

class SentenceNode:
    def __init__(self, text):
        self.text = text

class WordNode:
    def __init__(self, word, root_word, definition):
        self.word = word
        self.root_word = root_word
        self.definition = definition

    
