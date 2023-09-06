from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.properties import ColorProperty, ListProperty, ObjectProperty
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.metrics import dp, sp

Builder.load_string("""
<FlatField>:
    padding: [dp(6), (self.height - self.line_height)/2]
""")
class FlatField(TextInput):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.background_normal = ""
        self.background_active = ""
        self.background_disabled = ""
        self.background_color = [0,0,0,0]
        self.write_tab = False

class TextField(FlatField):
    bcolor = ColorProperty([0,0,0,1])
    main_color = ColorProperty([1,1,1,1])
    radius = ListProperty([1])
    def __init__(self, **kw):
        super().__init__(**kw)

        with self.canvas.before:
            self.border_color = Color(rgba=self.bcolor)
            self.border_draw = RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)
            self.back_color = Color(rgba=self.main_color)
            self.back_draw = RoundedRectangle(
                pos=[self.pos[0]+1.5, self.pos[1]+1.5], 
                size=[self.size[0]-3, self.size[1]-3], 
                radius=self.radius
                )

        self.bind(size=self.update)
        self.bind(pos=self.update)

    def on_main_color(self, inst, value):
        self.back_color.rgba = value

    def on_bcolor(self, inst, value):
        self.border_color.rgba = value

    def update(self, *args):
        self.border_draw.pos = self.pos
        self.border_draw.size = self.size

        self.back_draw.pos=[self.pos[0]+1.5, self.pos[1]+1.5] 
        self.back_draw.size=[self.size[0]-3, self.size[1]-3]

    def on_radius(self, *args): 
        self.back_draw.radius=self.radius
        self.border_draw.radius=self.radius

class OutlineTextField(FlatField):
    bcolor = ColorProperty([0,0,0,1])
    main_color = ColorProperty([1,1,1,1])
    radius = ListProperty([1])
    def __init__(self, **kw):
        super().__init__(**kw)

        with self.canvas.before:
            self.border_color = Color(rgba=self.bcolor)
            self.border_draw = Line(
                width=dp(1.5),
                rounded_rectangle=[self.pos[0], self.pos[1], self.size[0], self.size[1], self.radius[0]]
            )
            # self.border_draw = RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)
            # self.back_color = Color(rgba=self.main_color)
            # self.back_draw = RoundedRectangle(
            #     pos=[self.pos[0]+1.5, self.pos[1]+1.5], 
            #     size=[self.size[0]-3, self.size[1]-3], 
            #     radius=self.radius
            #     )

        self.bind(size=self.update)
        self.bind(pos=self.update)

    def on_main_color(self, inst, value):
        self.back_color.rgba = value

    def on_bcolor(self, inst, value):
        self.border_color.rgba = value

    def update(self, *args):
        self.border_draw.rounded_rectangle=[self.pos[0], self.pos[1], self.size[0], self.size[1], self.radius[0]]

    def on_radius(self, *args): 
        self.border_draw.rounded_rectangle=[self.pos[0], self.pos[1], self.size[0], self.size[1], self.radius[0]]


class SearchBar(FlatField):
    choices = ListProperty(['Awel 01', 'Dawd 02', 'Jamel 03'])
    suggestion_widget = ObjectProperty(allownone=True)
    def __init__(self, **kw):
        super().__init__(**kw)
        self.multiline = False
        self.dropdown = None
    def on_text(self, inst, text):
        try:
            #Close all dropdown already open
            if self.dropdown:
                self.dropdown.dismiss()
                self.dropdown = None
            # Show the current suggestions
            self.show_suggestions(text)

        except:
            pass

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if self.dropdown:
            self.dropdown.dismiss()
            self.dropdown = None

        # if keycode[0] == ord("\r"):
        #     self.text = self.values[0]

        else:
            super().keyboard_on_key_down(window, keycode, text, modifiers)

    def open_dropdown(self, *args):
        if self.dropdown:
            self.dropdown.open(self)
    def show_suggestions(self, suggestions:str):
        try:
            self.dropdown = DropDown()
            self.dropdown.auto_width = False
            self.dropdown.size_hint_x = None
            self.dropdown.width = Window.width* .4
            x: int = 0
            for i in self.choices:
                b = Button()

                if self.suggestion_widget:
                    b = self.suggestion_widget()
                b.text = i
                b.size_hint_y = None
                b.height = dp(54)

                self.dropdown.add_widget(b)
                x += 1
            if x > 0:
                self.dropdown.open(self)


        except:
            pass