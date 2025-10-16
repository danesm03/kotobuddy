import os

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual import on, events
from textual.containers import  Horizontal, Vertical, Container, HorizontalScroll
from textual.widgets import Static, Label, Header, Footer, ListView, ListItem, Button, Input, ContentSwitcher
from textual.message import Message


from utils.word_parser import InputText
from utils.data_types import Flashcard, get_due_cards, Difficulty
from utils.db import engine

from sqlmodel import Session, SQLModel






    


class WordClicked(Message): 
        def __init__(self, node):
            super().__init__()
            self.node = node

class AddToFlashcards(Button):
    def __init__(self, node):
        super().__init__(label="Add To Flashcards", classes="add-to-flash-btn", variant="primary")
        self.node = node

    def on_click(self, event: events.Click) -> None:
        flashcard = Flashcard.set_review_date(word=self.node.root_word, difficulty=Difficulty.EASY)
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

    def on_word_clicked(self, message: WordClicked) -> None:
        panel = self.query_one("#info-panel")
        panel.remove_children()

        panel.mount(
        Label(content=f"Definition:{message.node.definition}          "),
        AddToFlashcards(message.node)
        )
    
    def assemble_text(self):
        for node in self.nodes:
            self.query_one("#readtext-ctnr").mount(Word(node))
        
    
    def on_mount(self):
        self.input_handler.to_word_nodes()
        self.nodes = self.input_handler.nodes
        self.assemble_text()

    def action_save_text(self):
        my_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(my_dir)
        data_dir = os.path.join(project_root, "data")
        with open(os.path.join(data_dir, "text_data.py"), "a") as f:
            f.write(f'TextData(id="{self.input_handler.text[:5]}", text="{self.input_handler.text}")\n')
        


class SavedTextsScreen(Screen):
    def compose(self):
        yield Header()
        yield Footer()
        #placeholder list - need to add item adder logic
        yield ListView(
            id="saved-texts-list"
        )
    
    def assemble_list_view(self):
        pass
        #for text in texts_list:
            #self.query_one("#saved-texts-list").mount(ListItem(text.id))

class SavedCardsScreen(Screen):
    
    def __init__(self):
        super().__init__()
        
        self.session = Session(engine)
        self.cards = get_due_cards(self.session)
    def compose(self):
        yield Header()
        yield Footer()
        with Horizontal(id="card_sides"):
            yield Button("Card Front", id="card-front")
            yield Button("Card Back", id="card-back")
        with ContentSwitcher(initial="card-front"):
            yield Static(id="card-front")
            yield Static(id="card-back")
                             
        yield Horizontal(
            Button("Easy", id="easy", variant="success"),
            Button("Medium", id="medium", variant="warning"),
            Button("Hard", id="hard", variant="error")
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.query_one(ContentSwitcher).current = event.button.id  
    
        
    def assemble_card(self):
        curr_card = self.cards[0].to_word_node()
        front = self.query_one("card-front")
        back = self.query_one("card-back")
        front.update(curr_card.root_word)
        back.update(curr_card.definition)


        


    




    def on_mount(self):
        self.assemble_card()


class GenerateScreen(Screen):
    def __init__(self):
        super().__init__()
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
        yield Static("Logs:\n", id="log_widget")
        yield Horizontal(
            Button("Saved Cards", id="saved-cards-btn", variant="primary"),
            Button("Generate", id="generate-text-btn", variant="primary"),
            Button("Saved Texts", id="saved-texts-btn", variant="primary"),
            id="gentextscrn-cntnr",
        )




    def push_txt_to_readview(self):
        self.input_handler.to_word_nodes()
        self.app.push_screen(ReadViewScreen(self.input_handler))
        
        


    #TEST LOGGING TO VERIFY THAT INPUT TEXT CAN BE PORTED ELSEWHERE
    @on(Button.Pressed, "#generate-text-btn")

    def update_input_text(self):
        self.input_text = self.query_one("#generate_text_input", Input).value
        self.input_handler.update(self.input_text)
        self.push_txt_to_readview()
        #self.log_message(self.input_handler.to_word_nodes())


    """def log_message(self, message: str) -> None:
        log_widget = self.query_one("#log_widget", Static)
        current_text = str(log_widget.render())  # get current text
        log_widget.update(f"{current_text}\n{message}")  # append new line"""














        


class StartScreen(Screen):
    BINDINGS = [
        ("d", "toggle_dark_mode", "Toggle Dark Mode")]


    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Vertical(
            Static(r"""
    /$$   /$$  /$$$$$$  /$$$$$$$$  /$$$$$$  /$$$$$$$  /$$   /$$ /$$$$$$$  /$$$$$$$  /$$     /$$
    | $$  /$$/ /$$__  $$|__  $$__/ /$$__  $$| $$__  $$| $$  | $$| $$__  $$| $$__  $$|  $$   /$$/
    | $$ /$$/ | $$  \ $$   | $$   | $$  \ $$| $$  \ $$| $$  | $$| $$  \ $$| $$  \ $$ \  $$ /$$/ 
    | $$$$$/  | $$  | $$   | $$   | $$  | $$| $$$$$$$ | $$  | $$| $$  | $$| $$  | $$  \  $$$$/  
    | $$  $$  | $$  | $$   | $$   | $$  | $$| $$__  $$| $$  | $$| $$  | $$| $$  | $$   \  $$/   
    | $$\  $$ | $$  | $$   | $$   | $$  | $$| $$  \ $$| $$  | $$| $$  | $$| $$  | $$    | $$    
    | $$ \  $$|  $$$$$$/   | $$   |  $$$$$$/| $$$$$$$/|  $$$$$$/| $$$$$$$/| $$$$$$$/    | $$    
    |__/  \__/ \______/    |__/    \______/ |_______/  \______/ |_______/ |_______/     |__/   
    """, id="title"),
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
        ("b","back", "Back"),
        ("s", "to_start_screen", "Start Screen")
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
    
    def action_back(self):
        return super().action_back()
    
    def action_to_start_screen(self):
        self.push_screen(StartScreen())
            
 
    
    def on_mount(self):
        self.push_screen(StartScreen())

    @on(Button.Pressed, "#start-btn")
    def start_kotobuddy(self):
        self.push_screen(GenerateScreen())

    @on(Button.Pressed, "#saved-cards-btn")
    def enter_savedcards(self):
        self.push_screen(SavedCardsScreen())

    @on(Button.Pressed, "#saved-texts-btn")
    def enter_savedtexts(self):
        self.push_screen(SavedTextsScreen())


