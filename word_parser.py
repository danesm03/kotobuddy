import MeCab
from jamdict import Jamdict
from fugashi import Tagger
import unidic

class InputText:
    def __init__(self,text):
        self.text = text

class SentenceNode:
    def __init__(self, text):
        self.text = text

class WordNode:
    def __init__(self, word, root_word, definition):
        self.word = word
        self.root_word = root_word
        self.definition = definition

    
