from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer, Vertical, Horizontal, Container
from textual.widgets import Footer, Header, Static, Button, Input, ListItem, ListView, Label, Log
from textual.screen import Screen
from textual import on
from rich.console import Console

console = Console()

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
    def print_text_input(self, event: Button.Pressed):
        text_input = self.query_one("#generate_text_input", Input)
        user_text = text_input.value
        return user_text
        #self.log_message(f"user_text: {user_text}")

    def log_message(self, message: str) -> None:
        """Append a message to the internal log widget."""
        log_widget = self.query_one("#log_widget", Static)
        current_text = str(log_widget.render())  # get current text
        log_widget.update(f"{current_text}\n{message}")  # append new line
        


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