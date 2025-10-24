from jamdict import Jamdict
import fugashi
import ipadic


class WordNode:

    def __init__(self, word, root_word, unknown, definition, reading):

        self.word = word
        self.root_word = root_word
        self.unknown = unknown
        self.definition = definition
        self.reading = reading

            
    def __repr__(self):
         return f"WordNode({self.word},{self.root_word},{self.definition})"


    
class InputText:
    def __init__(self):
        self.text = ""
        self.nodes = []
        self.jd = Jamdict()
    
    def update(self, new_text: str):
        self.text = new_text



    def get_definition_and_reading(self, word, pos):
            
            """Fetches the jamdict definition, returns the first entry. Senses is the raw english response of the first entry, gloss is the polished definition"""
            result = None
            if pos.startswith("助詞"):
                result = self.jd.lookup(word, pos=["particle"])
                print(f"particle result:{result}")
            else:              
                result = self.jd.lookup(word)
            
            if result.entries and result.entries[0].senses:  
                definition = " , ".join(g.text for g in result.entries[0].senses[0].gloss)
                reading = result.entries[0].kana_forms[0].text
                return definition, reading
            else: 
                definition =  None
                reading = "N/A"
                return definition, reading
            
    def to_word_nodes(self):
        
        """REMOVE results list and returning in final functionality, just there for testing purposes to print to the LOG"""

        print(f"self.text= {self.text}")
        print(f"self.nodes before:{self.nodes}")
        tagger = fugashi.GenericTagger(ipadic.MECAB_ARGS)
        text = self.text
        for word in tagger(text):
            pos = word.feature[0]
            lemma = word.feature[6]
            #conj_type = word.feature[5]
            definition, reading = self.get_definition_and_reading(lemma, pos)
            
            node = WordNode(word.surface, lemma, word.is_unk, definition, reading)
            self.nodes.append(node)
        print(f"self.nodes after:{self.nodes}")
        return self.nodes
            #results.append(f"Token: {node.word}\tLemma: {node.root_word} Definition: {node.definition}")

    


            