import MeCab
from jamdict import Jamdict
import fugashi
import ipadic
from rich.console import Console



class WordNode:

    def __init__(self, word, root_word, unknown):

        self.word = word
        self.root_word = root_word
        self.unknown = unknown
        self.definition = self.get_definition()


    
    def get_definition(self):
            """Fetches the jamdict definition, returns the first entry. Senses is the raw english response of the first entry, gloss is the polished definition"""
            result = Jamdict().lookup(self.root_word)
            if result.entries and result.entries[0].senses:
                 return ", ".join(g.text for g in result.entries[0].senses[0].gloss)
            else: 
                 return None
            
    def __repr__(self):
         return f"WordNode({self.word},{self.root_word},{self.definition})"


    
class InputText:
    def __init__(self):
        self.text = ""
        self.nodes = []
    
    def update(self, new_text: str):
        self.text = new_text

    def to_word_nodes(self):
        """REMOVE results list and returning in final functionality, just there for testing purposes to print to the LOG"""

        
        tagger = fugashi.GenericTagger(ipadic.MECAB_ARGS)
        text = self.text
        for word in tagger(text):
            lemma = word.feature[6]
            node = WordNode(word.surface, lemma, word.is_unk)
            self.nodes.append(node)
        return self.nodes
            #results.append(f"Token: {node.word}\tLemma: {node.root_word} Definition: {node.definition}")

    


        