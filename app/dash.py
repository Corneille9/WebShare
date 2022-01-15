import ntpath
import sys

from kivy.animation import Animation
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.list import TwoLineAvatarListItem
# 16.75
from kivymd.uix.selectioncontrol import MDCheckbox

from app.utils.utilities import get_file_icon, get_icon_dir

KV = '''
#:import MagicBehavior kivymd.uix.behaviors.MagicBehavior

<MyItem>
    source: "file.png"
    ImageLeftWidget:
        source: root.source
        
MDBoxLayout:
    orientation: "vertical"

    MDToolbar:
        id: toolbar
        left_action_items: [["menu"]]
        right_action_items: [["magnify"], ["dots-vertical"], ]
        md_bg_color: 0, 0, 0, 1   

    MDBoxLayout:
        id: box
        padding: "24dp", "8dp", 0, "8dp"
        adaptive_size: True

        MDLabel:
            bold: True
            text: "Application list"
            adaptive_size: True
            font_name: 'Kanit-SemiBold.ttf'
            pos_hint: {'center_x': .5, 'center_y': .5}
            
        MDLabel:
            padding: "20dp", "0dp"
            bold: True
            text: "Tout Cocher"
            adaptive_size: True
            font_name: 'Kanit-SemiBold.ttf'
            pos_hint: {'center_x': .9, 'center_y': .5}
                
        MDCheckbox:
            size_hint: None, None
            size: "48dp", "48dp"
            pos_hint: {'center_x': .5, 'center_y': .5}    
            
    ScrollView:

        MDSelectionList:
            id: selection_list
            spacing: "12dp"
            overlay_color: app.overlay_color[:-1] + [.2]
            icon_bg_color: app.overlay_color
            on_selected: app.on_selected(*args)
            on_unselected: app.on_unselected(*args)
            on_selected_mode: app.set_selection_mode(*args)
'''


class MyItem(TwoLineAvatarListItem):
    def __init__(self, path, **kwargs):
        super().__init__(**kwargs)
        self.source = get_icon_dir() + get_file_icon(path)
        self.path = path
        self.text = ntpath.basename(path)
        self.secondary_text = path
        self._no_ripple_effect = True
        self.check = MDCheckbox(
            pos_hint={"center_x": .9, "center_y": .5},
            size_hint=[None, None],
            size=["48dp", "48dp"]
        )
        self.check.active = True
        self.add_widget(self.check)


class AppInstaller(MDApp):
    overlay_color = get_color_from_hex("#6042e4")
    files = []

    def add_files(self, file_path):
        for path in file_path:
            self.files.append(path)
            self.root.ids.selection_list.add_widget(MyItem(path=path))

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

    def on_start(self):
        self.root.ids.toolbar.add_widget(MyButton(self))

    def set_selection_mode(self, instance_selection_list, mode):
        if mode:
            md_bg_color = self.overlay_color
            left_action_items = [
                [
                    "close",
                    lambda x: self.root.ids.selection_list.unselected_all(),
                ]
            ]
            right_action_items = [["trash-can"], ["dots-vertical"]]
        else:
            md_bg_color = (0, 0, 0, 1)
            left_action_items = [["menu"]]
            right_action_items = [["magnify"], ["dots-vertical"]]
            self.root.ids.toolbar.title = "Inbox"

        Animation(md_bg_color=md_bg_color, d=0.2).start(self.root.ids.toolbar)
        self.root.ids.toolbar.left_action_items = left_action_items
        self.root.ids.toolbar.right_action_items = right_action_items

    def on_selected(self, instance_selection_list, instance_selection_item):
        self.root.ids.toolbar.title = str(
            len(instance_selection_list.get_selected_list_items())
        )

    def on_unselected(self, instance_selection_list, instance_selection_item):
        if instance_selection_list.get_selected_list_items():
            self.root.ids.toolbar.title = str(
                len(instance_selection_list.get_selected_list_items())
            )

    # @staticmethod
    # def get_icon_from_filename(path):
    #     if os.path.isfile(path):
    #         # Get icon name
    #         file = Gio.File(path)
    #         file_info = file.query_info("standard::icon")
    #         file_icon = file_info.get_icon().get_names()[0]
    #         icon_theme = gtk.icon_theme_get_default()
    #         icon_filename = icon_theme.lookup_icon(file_icon, 50, 0)
    #         if icon_filename is not None:
    #             return icon_filename.get_filename()


class MyButton(MDFillRoundFlatButton, TouchBehavior):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self._radius = 6
        self.text = "Ajouter"
        self.bold = True
        self.pos_hint = {"center_x": .5, "center_y": .5}
        self.font_name = 'Kanit-SemiBold.ttf'

    def on_press(self):
        file_chooser = None
        if sys.platform == "linux":
            from plyer.platforms.linux.filechooser import LinuxFileChooser
            file_chooser = LinuxFileChooser()
        elif sys.platform == "win32":
            from plyer.platforms.win.filechooser import WinFileChooser
            file_chooser = WinFileChooser()
        if file_chooser is not None:
            self.app.add_files(file_chooser.open_file(multiple=True))

    def on_long_touch(self, touch, *args):
        print("<on_long_touch> event")

    def on_double_tap(self, touch, *args):
        print("<on_double_tap> event")

    def on_triple_tap(self, touch, *args):
        print("<on_triple_tap> event")

# https://www.youtube.com/watch?v=NZde8Xt78Iw
