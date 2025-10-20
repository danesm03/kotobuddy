import os

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual import on, events
from textual.containers import  Horizontal, Vertical, Container, HorizontalScroll, Center, CenterMiddle
from textual.widgets import Static, Label, Header, Footer, ListView, ListItem, Button, Input, ContentSwitcher
from textual.message import Message


from utils.word_parser import InputText
from utils.data_types import Flashcard, get_due_cards, Difficulty, to_word_node, SavedText, Node, get_saved_texts
from utils.db import engine, texts_engine

from sqlmodel import Session
from datetime import date, timedelta





    


class WordClicked(Message): 
        def __init__(self, node):
            super().__init__()
            self.node = node

class AddToFlashcards(Button):
    def __init__(self, node):
        super().__init__(label="Add To Flashcards", classes="add-to-flash-btn", variant="primary")
        self.node = node

    def on_click(self, event: events.Click) -> None:
        flashcard = Flashcard(word=self.node.root_word, difficulty=Difficulty.HARD, review_date=date.today() + timedelta(days=Difficulty.HARD.value))
        with Session(engine) as session:
            if flashcard == None:
                print("Flashcard is none")
            else:
                session.add(flashcard)
                session.commit()
        
    
class Word(Button):
    def __init__(self, word_node):
        self.node = word_node
        super().__init__(self.node.word, classes="word")
        

    def on_click(self, event: events.Click) -> None:
        self.post_message(message=WordClicked(self.node))


class ReadViewScreen(Screen):

    BINDINGS = [
        ("t", "save_text", "Save Text")
    ]

    def __init__(self, handler):
        super().__init__()
        self.input_handler = handler

    def compose(self):
        yield Header()
        yield Footer()
        yield Vertical(
            HorizontalScroll(
            id="readtext-ctnr"
        ),
            Horizontal(id="info-panel"),
            id="readview_master"
        )
        yield Vertical(id="title-save-ctnr")


    def on_word_clicked(self, message: WordClicked) -> None:
        panel = self.query_one("#info-panel")
        panel.remove_children()

        panel.mount(
        Label(content=f"Definition:{message.node.definition}          "),
        Label(content= f"Reading:{message.node.reading}          "),
        AddToFlashcards(message.node)
        )
    
    def assemble_text(self):
        print(f"Nodes on mount: {self.nodes}")  # Debugging
        for node in self.nodes:
            self.query_one("#readtext-ctnr").mount(Word(node))
        
    
    def on_mount(self):
        self.input_handler.to_word_nodes()
        self.nodes = self.input_handler.nodes
        self.assemble_text()

    def action_save_text(self):
        container = self.query_one("#title-save-ctnr")
        container.mount(Input(id="title-entry", placeholder="Text Title"))
        container.mount(Button("Save Text", id="save-text-btn", variant="primary"))

    def nodes_to_sqlmodel(self,saved_text):
        nodes = self.input_handler.nodes
        if not nodes:
            raise ValueError("text is empty, no word nodes available")
        nodelist = []
        print(f"len_nodes:{len(nodes)} nodes:{nodes}")
        for node in nodes:
            if node.definition != None:
                nodelist.append(Node(word=node.word, root_word=node.root_word, unknown=node.unknown, definition=node.definition, reading=node.reading, saved_text=saved_text))
        print(f"len_nodelist:{len(nodelist)}")
        return nodelist


    @on(Button.Pressed, "#save-text-btn")
    def write_text_save(self):
        title = self.query_one("#title-entry", Input).value
        text_to_save = SavedText(title=title, text=self.input_handler.text)
        nodes=self.nodes_to_sqlmodel(text_to_save)
        text_to_save.nodes = nodes
        with Session(texts_engine) as session:
            if text_to_save == None:
                print("text to save is None")
            else: 
                session.add(text_to_save)
                session.commit()
        """
        container = self.query_one("#title-save-ctnr")
        title_entry = self.query_one("#title-entry", Input)
        save_button = self.query_one("#save-text-btn", Button)
        container.remove(title_entry)
        container.remove(save_button)
"""



    
        


class SavedTextsScreen(Screen):
    def __init__(self):
        super().__init__(id="saved-texts-screen")
        self.texts = []
    
    

    def compose(self):
        yield Header()
        yield Footer()
        with Center():
            yield ListView(
                    id="saved-texts-list"
                )
        yield CenterMiddle(
            Button("Delete Text", id="delete-text-btn", variant="primary"   )
        )

    
    def assemble_list_view(self):
        text_list = self.query_one("#saved-texts-list", ListView)
        text_list.clear()  # newer Textual; if not available, use remove_children()
        for text in self.texts:
            item = ListItem(Label(text.title))
            item.data = {"id": text.id}
            text_list.mount(item)

    def on_mount(self):
        with Session(texts_engine) as session:
            self.texts = get_saved_texts(session)
        self.assemble_list_view()

    @on(ListView.Selected, "#saved-texts-list")
    def push_text_to_readview(self, event: ListView.Selected):
        text_list = self.query_one("#saved-texts-list", ListView)
        selected_item = text_list.highlighted_child
        if selected_item and getattr(selected_item, "data", None):
            tid = selected_item.data["id"]
            selected_text = next((t for t in self.texts if t.id == tid), None)
            if selected_text:
                input_handler = InputText()
                input_handler.update(selected_text.text)
                self.app.push_screen(ReadViewScreen(input_handler))

    @on(Button.Pressed, "#delete-text-btn")
    def delete_saved_text(self):
        text_list = self.query_one("#saved-texts-list", ListView)
        selected_item = text_list.highlighted_child
        if selected_item and getattr(selected_item, "data", None):
            tid = selected_item.data["id"]
            selected_text = next((t for t in self.texts if t.id == tid), None)
            if selected_text:
                with Session(texts_engine) as session:
                    session.delete(selected_text)
                    session.commit()
                    self.texts = get_saved_texts(session)
            self.assemble_list_view()
            

    
class SavedCardsScreen(Screen):
    
    def __init__(self):
        super().__init__(id="saved-cards-screen")
        self.counter = 0 
        self.due_cards = []



    def compose(self):
        yield Header()
        yield Footer()
        
        with CenterMiddle(id="card_sides"):
                yield Button("Card Front", id="card-front")
                yield Button("Card Back", id="card-back")
        with CenterMiddle(id="switcher-cntr"):
            with ContentSwitcher(id="card_switcher", initial="card-front"):
                yield Static(id="card-front")
                yield Static(id="card-back")
            
                             
        yield Horizontal(
            Button("Easy", id="easy", variant="success"),
            Button("Medium", id="medium", variant="warning"),
            Button("Hard", id="hard", variant="error"),
            Button("Delete Card", id="delete-card", variant="primary"),
            id="difficulties"
        )
        


    def save_cards(self,difficulty):
        if not self.due_cards:
            print("no cards to save")
            return
        card = self.get_curr_card()
        if not card:
            return
        with Session(engine) as session:
            card.difficulty = difficulty
            card.review_date = date.today() + timedelta(days=card.difficulty.value)
            print(f"Card {card.word} updated to review_date: {card.review_date}")
            session.add(card)
            session.commit()
            self.due_cards = get_due_cards(session)
        if self.due_cards:
            self.counter = (self.counter + 1) % len(self.due_cards)
        else:
            self.counter = 0
        print(f"Cards left for review: {len(self.due_cards)} counter:{self.counter} ")
        self.assemble_card()


    def get_curr_card(self):
        if not self.due_cards:
            return None
        if self.counter >= len(self.due_cards):
            self.counter = 0
        return self.due_cards[self.counter]
        

    def assemble_card(self):
        cs = self.query_one(ContentSwitcher)
        front = cs.query_one("#card-front", Static)
        back = cs.query_one("#card-back", Static)
        if not self.due_cards:
            self.counter = 0
            front.update("No cards for review")
            back.update("")
            return
        card = to_word_node(self.get_curr_card().word)
        front.update(card.root_word)
        back.update(f"Definition:{card.definition}, Reading:{card.reading}")


    def on_mount(self):
        with Session(engine) as session:
            self.due_cards = get_due_cards(session)
        if not self.due_cards:
            print("no cards available for review on mount")
        self.counter = 0
        self.assemble_card()
        


    @on(Button.Pressed, "#card-front")
    def switch_front(self):
        self.query_one(ContentSwitcher).current = "card-front"

    @on(Button.Pressed, "#card-back")
    def switch_back(self):
        self.query_one(ContentSwitcher).current = "card-back"

    @on(Button.Pressed, "#easy")
    def save_as_easy(self):
        self.save_cards(Difficulty.EASY)
    @on(Button.Pressed, "#medium")
    def save_as_med(self):
        self.save_cards(Difficulty.MEDIUM)

    @on(Button.Pressed, "#hard")
    def save_as_hard(self):
        self.save_cards(Difficulty.HARD)

    @on(Button.Pressed, "#delete-card")
    def delete_card(self):
        card = self.get_curr_card()
        if not card:
            print("no card to delete")
            return
        with Session(engine) as session:
            session.delete(card)
            session.commit()
            self.due_cards = get_due_cards(session)
            self.assemble_card()

    





class GenerateScreen(Screen):
    def __init__(self):
        super().__init__(id="generate-screen")
        self.input_text = ""
        self.input_handler = InputText()
    
    BINDINGS = [
        ("ctrl+d", "toggle_dark_mode", "Toggle Dark Mode"),#("return", "app.push_screen(GenerateScreen)", "Start")
    ]    

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Input(
            placeholder="Enter Japanese here ...",
            type="text",
            max_length=25000,
            id="generate_text_input"
        )
        
        yield Horizontal(
            Button("Saved Cards", id="saved-cards-btn", variant="primary"),
            Button("Generate", id="generate-text-btn", variant="primary"),
            Button("Saved Texts", id="saved-texts-btn", variant="primary"),
            id="gentextscrn-cntnr",
        )




    def push_txt_to_readview(self):
        #self.input_handler.to_word_nodes()
        self.app.push_screen(ReadViewScreen(self.input_handler))
        
        


    
    @on(Button.Pressed, "#generate-text-btn")

    def update_input_text(self):
        self.input_text = self.query_one("#generate_text_input", Input).value
        self.input_handler.update(self.input_text)
        self.push_txt_to_readview()
        #self.log_message(self.input_handler.to_word_nodes())

















        


class StartScreen(Screen):
    def __init__(self):
        super().__init__(id="start-screen")
    BINDINGS = [
        
        ("d", "toggle_dark_mode", "Toggle Dark Mode")]


    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Vertical(
            Center(
            Label(r"""
    /$$   /$$  /$$$$$$  /$$$$$$$$  /$$$$$$  /$$$$$$$  /$$   /$$ /$$$$$$$  /$$$$$$$  /$$     /$$
    | $$  /$$/ /$$__  $$|__  $$__/ /$$__  $$| $$__  $$| $$  | $$| $$__  $$| $$__  $$|  $$   /$$/
    | $$ /$$/ | $$  \ $$   | $$   | $$  \ $$| $$  \ $$| $$  | $$| $$  \ $$| $$  \ $$ \  $$ /$$/ 
    | $$$$$/  | $$  | $$   | $$   | $$  | $$| $$$$$$$ | $$  | $$| $$  | $$| $$  | $$  \  $$$$/  
    | $$  $$  | $$  | $$   | $$   | $$  | $$| $$__  $$| $$  | $$| $$  | $$| $$  | $$   \  $$/   
    | $$\  $$ | $$  | $$   | $$   | $$  | $$| $$  \ $$| $$  | $$| $$  | $$| $$  | $$    | $$    
    | $$ \  $$|  $$$$$$/   | $$   |  $$$$$$/| $$$$$$$/|  $$$$$$/| $$$$$$$/| $$$$$$$/    | $$    
    |__/  \__/ \______/    |__/    \______/ |_______/  \______/ |_______/ |_______/     |__/   
    """, id="title")),
        Static("[bold]コトバディ[/bold]", id="kotobuddy_subtitle"),
        Horizontal(
            Button("Start", id="start-btn", variant="primary" ),
            id="start-btn-container",
        ),
        id="start-screen"
    )



        
        

    
        

class KotobuddyApp(App):
    BINDINGS = [
        ("d", "toggle_dark_mode", "Toggle Dark Mode"),
        ("s", "to_start_screen", "Start Screen"),
        ("b","back", "Back"),
    ]

    CSS_PATH = "kotobuddy.tcss"


    def compose(self):

        """What widgets is this app composed of?"""
        yield Header()
        yield Footer()

    def action_toggle_dark_mode(self):
        if self.theme == "textual-light":
            self.theme = "textual-dark"
        else:
            self.theme = "textual-light"
    
   
    
    def action_to_start_screen(self):
        stack = getattr(self, "screen_stack", [])
        for idx, scr in enumerate(stack):
            if getattr(scr, "id", None) == "start-screen":
                
                while len(self.screen_stack) - 1 > idx:
                    self.pop_screen()
                return
        self.push_screen(StartScreen())
            
 
    
    def on_mount(self):

        self.push_screen(StartScreen())

    @on(Button.Pressed, "#start-btn")
    def start_kotobuddy(self):
        stack = getattr(self, "screen_stack", [])
        for idx, scr in enumerate(stack):
            if getattr(scr, "id", None) == "generate-screen":
                
                while len(self.screen_stack) - 1 > idx:
                    self.pop_screen()
                return
            
        self.push_screen(GenerateScreen())




    @on(Button.Pressed, "#saved-cards-btn")
        
    def enter_savedcards(self):
        
        stack = getattr(self, "screen_stack", [])
        for idx, scr in enumerate(stack):
            if getattr(scr, "id", None) == "saved-cards-screen":
                
                while len(self.screen_stack) - 1 > idx:
                    self.pop_screen()
                return
        
        self.push_screen(SavedCardsScreen())

    @on(Button.Pressed, "#saved-texts-btn")
    def enter_savedtexts(self):
        stack = getattr(self, "screen_stack", [])
        for idx, scr in enumerate(stack):
            if getattr(scr, "id", None) == "saved-texts-screen":
                
                while len(self.screen_stack) - 1 > idx:
                    self.pop_screen()
                return
            
        self.push_screen(SavedTextsScreen())


