from kivy.config import Config
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '600')

from os.path import dirname, join

from kivy.garden.iconfonts import register

from app import MainApp

register(
    "FeatherIcons",
    join(dirname(__file__), "assets/fonts/feather/feather.ttf"),
    join(dirname(__file__), "assets/fonts/feather/feather.fontd"),
    )

MainApp().run()
