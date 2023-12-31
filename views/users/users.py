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

Builder.load_file("views/users/users.kv")
class Users(BoxLayout):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        Clock.schedule_once(self.render, .1)
        self.currentUser = None

    def render(self, _):
        t1 = Thread(target=self.get_users(), daemon=True)
        t1.start()
    def add_new(self):
        md = ModUser()
        md.callback = self.add_user
        md.open()
    def add_user(self, mv):
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
        user = {
                "firstName": fname.text.strip(),
                "lastName": lname.text.strip(),
                "username": uname.text.strip(),
                "password": upass,
                "Role": _date,
                "signedIn": "092344994"

            }
        self.set_users([user])

    def update_user(self, user):
        mv = ModUser()
        mv.first_name = user.first_name
        mv.last_name = user.last_name
        mv.username = user.username
        mv.callback = self.set_update

        mv.open()
    def set_update(self, mv):
        print("updating...")


    def get_users(self):
        users = [
            {
                "firstName": "Abdu",
                "lastName": "Haj",
                "username": "first.abdu",
                "password": "adhfakf2345",
                "Role": "system Admin",
                "signedIn": "092344994"
            },
            {
                "firstName": "Dawd",
                "lastName": "Fekd",
                "username": "first.dawd",
                "password": "adhfakf2345",
                "Role": "Desktop Recieptionest",
                "signedIn": "092344996"
            },
            {
                "firstName": "Awel",
                "lastName": "Jamel",
                "username": "first.awel",
                "password": "adhfakf2345",
                "Role": "system Admin",
                "signedIn": "092344994"
            },
        ]
        self.set_users(users)

    @mainthread
    def set_users(self, users:list):
        grid = self.ids.gl_users
        grid.clear_widgets()

        for u in users:
            ut = UserTile()
            ut.first_name = u['firstName']
            ut.last_name = u['lastName']
            ut.username = u['username']
            ut.password = u['password']
            ut.created = u['Role']
            ut.last_login = u['signedIn']
            ut.callback = self.delete_user
            ut.bind(on_release=self.update_user)

            grid.add_widget(ut)
    def delete_user(self, user):
        self.currentUser = user
        dl = ConfirmDialog()
        dl.title = "Delete User"
        dl.subtitle = "Are you sure you want to delete this user"
        dl.textConfirm = "Yes, Delete"
        dl.textCancel = "Cancel"
        dl.confirmColor = App.get_running_app().color_tertiary
        dl.cancelColor = App.get_running_app().color_primary
        dl.confirmCallback = self.delete_from_view
        dl.open()
    def delete_from_view(self, ConfirmDialog):

        if self.currentUser:
            self.currentUser.parent.remove_widget(self.currentUser)
class UserTile(ButtonBehavior,BoxLayout):
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
    def delete_user(self):
        if self.callback:
            self.callback(self)

class ModUser(ModalView):
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
        self.ids.title.text = "Update User"
        self.ids.subtitle.text = "Enter your details below to update user"
        self.ids.addbtn.text = "Update User"
    def on_last_name(self, inst, lname):
        self.ids.lname.text = lname
    def on_username(self, inst, uname):
        self.ids.uname.text = uname