import MeCab
from jamdict import Jamdict
import fugashi
import ipadic
from rich.console import Console



class WordNode:
    def __init__(self, word, root_word, unknown):
        self.word = word
        self.root_word = root_word
        self.known = unknown

    
class InputText:
    def __init__(self):
        self.text = ""
    
    def update(self, new_text: str):
        self.text = new_text

    def to_word_nodes(self):
        """REMOVE results list and returning in final functionality, just there for testing purposes"""
        results = []
        tagger = fugashi.GenericTagger(ipadic.MECAB_ARGS)
        text = self.text
        for word in tagger(text):
            lemma = word.feature[6]
            node = WordNode(word.surface, lemma, word.is_unk)
            results.append(f"Token: {node.word}\tLemma: {node.root_word}")
        return results