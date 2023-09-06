import hashlib
from datetime import datetime
from threading import Thread


from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import mainthread, Clock
from kivy.uix.modalview import ModalView
from widgets.popups import ConfirmDialog

Builder.load_file("views/houses/houses.kv")
class Houses(BoxLayout):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        Clock.schedule_once(self.render, .1)
        self.currentHouse = None

    def render(self, _):
        t1 = Thread(target=self.get_houses(), daemon=True)
        t1.start()
    def add_new(self):
        md = ModHouse()
        md.callback = self.add_house
        md.open()
    def add_house(self, mv):
        fname = mv.ids.fname
        lname = mv.ids.lname
        uname = mv.ids.uname
        pwd = mv.ids.pwd
        cpwd = mv.ids.cpwd

        if len(fname.text.strip()) < 3:
            # Inform user that first name is invalid
            return

        _pwd = pwd.text.strip()
        upass = hashlib.sha3_256(_pwd.encode()).hexdigest()
        dt = datetime.now()
        _date = datetime.strftime(dt, "%Y/%m/%d %H:%M")
        house = {
                "firstName": fname.text.strip(),
                "lastName": lname.text.strip(),
                "username": uname.text.strip(),
                "password": upass,
                "createdAt": _date,
                "signedIn": "2023/01/12 14:25:06"

            }
        self.set_houses([house])

    def update_house(self, house):
        mv = ModHouse()
        mv.first_name = house.first_name
        mv.last_name = house.last_name
        mv.username = house.username
        mv.callback = self.set_update

        mv.open()
    def set_update(self, mv):
        print("updating...")


    def get_houses(self):
        houses = [
            {
                "HouseNo": "2345678",
                "RentedName": "Abdu",
                "Size": "120 meter sqoure",
                "PurposeofRent": "for business",
                "createdAt": "2023/01/10 12:45:56",
                "Price": "$2000/month"
            },
            {
                "HouseNo": "22/678",
                "RentedName": "Dawd",
                "Size": "120 meter sqoure",
                "PurposeofRent": "for living",
                "createdAt": "2023/01/10 12:45:56",
                "Price": "$200/month"
            },
            {
                "HouseNo": "3/378",
                "RentedName": "Awel",
                "Size": "120 meter sqoure",
                "PurposeofRent": "for business",
                "createdAt": "2023/01/10 12:45:56",
                "Price": "$2000/month"
            },
        ]
        self.set_houses(houses)

    @mainthread
    def set_houses(self, houses:list):
        grid = self.ids.gl_users
        grid.clear_widgets()

        for u in houses:
            ut = HouseTile()
            ut.first_name = u['HouseNo']
            ut.last_name = u['RentedName']
            ut.username = u['Size']
            ut.password = u['PurposeofRent']
            ut.created = u['createdAt']
            ut.last_login = u['Price']
            ut.callback = self.delete_house
            ut.bind(on_release=self.update_house)

            grid.add_widget(ut)
    def delete_house(self, houses):
        self.currentHouse = houses
        dl = ConfirmDialog()
        dl.title = "Delete House"
        dl.subtitle = "Are you sure you want to delete this house"
        dl.textConfirm = "Yes, Delete"
        dl.textCancel = "Cancel"
        dl.confirmColor = App.get_running_app().color_tertiary
        dl.cancelColor = App.get_running_app().color_primary
        dl.confirmCallback = self.delete_from_view
        dl.open()
    def delete_from_view(self, ConfirmDialog):

        if self.currentHouse:
            self.currentHouse.parent.remove_widget(self.currentHouse)
class HouseTile(ButtonBehavior,BoxLayout):
    first_name = StringProperty("")
    last_name = StringProperty("")
    username = StringProperty("")
    password = StringProperty("")
    created = StringProperty("")
    last_login = StringProperty("")
    callback = ObjectProperty(allownone=True)
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        Clock.schedule_once(self.render, .1)

    def render(self, _):
        pass
    def delete_house(self):
        if self.callback:
            self.callback(self)

class ModHouse(ModalView):
    first_name = StringProperty("")
    last_name = StringProperty("")
    username = StringProperty("")
    created = StringProperty("")
    last_login = StringProperty("")
    callback = ObjectProperty(allownone=True)
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        Clock.schedule_once(self.render, .1)

    def render(self, _):
        pass
    def on_first_name(self, inst, fname):
        self.ids.fname.text = fname
        self.ids.title.text = "Update House"
        self.ids.subtitle.text = "Enter your details below to update house"
        self.ids.addbtn.text = "Update House"
    def on_last_name(self, inst, lname):
        self.ids.lname.text = lname
    def on_username(self, inst, uname):
        self.ids.uname.text = uname