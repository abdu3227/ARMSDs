from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import mainthread


Builder.load_file("views/tasks/tasks.kv")
class Tasks(BoxLayout):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)