from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, Horizontal, Vertical
from textual.widgets import Static, Collapsible, Label, Header, Footer, ListView, ListItem, Button, Input
from textual.screen import Screen
from textual import on
from rich.console import Console
from utils.word_parser import InputText


console = Console()

class ReadViewScreen(Screen):
#NEED TO FIGURE OUT HOW TO GENERATE THE TEXT TO BE ALL WORD OBJECTS
    def __init__(self):
        super().__init__()
    def compose(self):
        yield Header()
        yield Footer()


class Word(HorizontalGroup):
    def __init__(self, word_node):
        super().__init__()
        self.node = word_node
    def compose(self):
        with Collapsible(collapsed =True):
            yield Label(self.node.word)
    

class SavedTextsScreen(Screen):
    BINDINGS = [
        ("ctrl+d", "toggle_dark_mode", "Toggle Dark Mode"),#("return", "app.push_screen(GenerateScreen)", "Start")
    ] 

    def compose(self):
        yield Header()
        yield Footer()
        #placeholder list - need to add item adder logic
        yield ListView(
            ListItem(Label("One")),
            ListItem(Label("Two")),
            ListItem(Label("Three")),
        )

class SavedCardsScreen(Screen):
    BINDINGS = [
        ("ctrl+d", "toggle_dark_mode", "Toggle Dark Mode"),#("return", "app.push_screen(GenerateScreen)", "Start")
    ] 

    def compose(self):
        yield Header()
        yield Footer()
        #placeholder list - need to add item adder logic
        yield ListView(
            ListItem(Label("One")),
            ListItem(Label("Two")),
            ListItem(Label("Three")),
        )


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
    #TEST LOGGING TO VERIFY THAT INPUT TEXT CAN BE PORTED ELSEWHERE
    @on(Button.Pressed, "#generate-text-btn")

    def update_input_text(self):
        self.input_text = self.query_one("#generate_text_input", Input).value
        self.input_handler.update(self.input_text)
        self.log_message(self.input_handler.to_word_nodes())


    def log_message(self, message: str) -> None:
        """Append a message to the internal log widget."""
        log_widget = self.query_one("#log_widget", Static)
        current_text = str(log_widget.render())  # get current text
        log_widget.update(f"{current_text}\n{message}")  # append new line

    #DYNAMIC WORD NODE GENERATION
    """
    def generate_node_buttons(self):
        for node in self.input_handler.nodes:
            yield Word(node)
    """






        


class StartScreen(Screen):
    BINDINGS = [
        ("d", "toggle_dark_mode", "Toggle Dark Mode"),#("return", "app.push_screen(GenerateScreen)", "Start")
    ]


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

    """
    @on(Button.Pressed, "#generate-text-btn")
    def push_read_view_screen(self):
        self.push_screen(ReadViewScreen())
    """