from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import mainthread


Builder.load_file("views/insights/insights.kv")
class Insights(BoxLayout):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)

    def homePage(self):
        App.get_running_app().root.ids.scrn_mngr.current = "scrn_admin"