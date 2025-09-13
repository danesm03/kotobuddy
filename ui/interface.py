from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer, Vertical, Horizontal, Container
from textual.widgets import Footer, Header, Static, Button
from textual.screen import Screen

class GenerateScreen(Screen):
    pass

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
    Static("[bold]コトバーディ[/bold]", id="kotobuddy_subtitle"),
    Horizontal(
        Button("Start", id="start-btn", variant="default"),
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

    

    