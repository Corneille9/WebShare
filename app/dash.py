import asyncio
import ntpath
import sys
import textwrap

from kivy.animation import Animation
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.material_resources import dp
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import TwoLineAvatarListItem
# 16.75
from kivymd.uix.selectioncontrol import MDCheckbox, MDSwitch
from kivymd.uix.snackbar import Snackbar

from app.utils.database_manager import DbManager
from app.utils.utilities import get_file_icon, get_icon_dir
from web.app import SharedFiles

KV = '''
#:import MagicBehavior kivymd.uix.behaviors.MagicBehavior
#:import get_color_from_hex kivy.utils.get_color_from_hex

<ContentNavigationDrawer>:
    nav_drawer: root.nav_drawer
            
    ScrollView:

        MDList:
            OneLineAvatarIconListItem:
                text: "Mode nuit"
                _no_ripple_effect: True     
                divider: "Inset"             
                
                IconLeftWidget:
                    icon:"theme-light-dark"
                    
                RightCheckbox:   
                    pos_hint: {"center_x": .9, "center_y": .5}    
                    on_active: app.change_theme()


            OneLineAvatarIconListItem:
                text: "Aide"
                divider: "Inset"
                
                IconLeftWidget:
                    icon:"help"
                
            OneLineAvatarIconListItem:
                text: "Quitter" 
                divider: "Inset"
                
                IconLeftWidget:
                    icon:"exit-to-app"                          
           

<MyItem>
    source: "file.png"
    ImageLeftWidget:
        source: root.source

MDNavigationLayout:   
    
    ScreenManager:
    
        MDScreen: 
        
            MDBoxLayout:
                orientation: "vertical"
                        
                MDToolbar:
                    id: toolbar
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open"), "Menu"]]
                    right_action_items: [["magnify"], ["dots-vertical"], ]   
            
                MDGridLayout:
                    id: box
                    cols: 2
                    adaptive_height: True
                    height: '60dp'
            
                    MDLabel:
                        bold: True
                        text: "Application list"
                        font_name: 'Kanit-SemiBold.ttf'
                        padding: "20dp", "5dp"
                        color: "62acce"
                    
                    MDBoxLayout:   
                        halign: 'right'
                        
                        MDLabel:
                            padding: "20dp", "0dp"
                            bold: True
                            text: "Select all"
                            font_name: 'Kanit-SemiBold.ttf'
                            halign: 'right'
                            color: "62acce"
                                
                        MDCheckbox:
                            size_hint: None, None
                            size: "48dp", "48dp"
                            on_active: app.on_checkbox_active(*args)  
                            pos_hint: {'center_x': .5, 'center_y': .5}    
                            active: True
                            halign: 'center'
                        
                ScrollView:
                    do_scroll_x: False
            
                    MDSelectionList:
                        id: selection_list
                        spacing: "12dp"
                        overlay_color: app.overlay_color[:-1] + [.2]
                        icon_bg_color: app.overlay_color
                        on_selected: app.on_selected(*args)
                        on_unselected: app.on_unselected(*args)
                        on_selected_mode: app.set_selection_mode(*args)
                 
                MDBottomAppBar:
                    id : bottom_Appbar
                
                    MDToolbar:
                        id: bottom_toolbar
                        icon: "git"
                        margin: 110, 100
                        type: "bottom"
                        on_action_button: app.on_float_button_click(self)
                        icon_color: 0, 0, 0, 1
                        left_action_items: [["router-network", lambda x: app.show_custom_bottom_sheet(), "Paramètres du server"]]     
                        elevation : 8  
                
    MDNavigationDrawer:
        id: nav_drawer
        orientation:"vertical"
            
        ContentNavigationDrawer:  
            nav_drawer: nav_drawer                                    
          
<ContentCustomSheet@BoxLayout>:
    orientation: "vertical"
    size_hint_y: None
    height: "200dp"        
'''


class MyItem(TwoLineAvatarListItem):
    all_items = []

    def __init__(self, path, **kwargs):
        super().__init__(**kwargs)
        self.source = get_icon_dir() + get_file_icon(path)
        self.path = path
        self.text = textwrap.shorten(ntpath.basename(path), width=80, placeholder="...")
        self.secondary_text = textwrap.shorten(path, width=50, placeholder="...")
        self._no_ripple_effect = True
        self.check = MDCheckbox(
            pos_hint={"center_x": .9, "center_y": .5},
            size_hint=[None, None],
            size=["48dp", "48dp"]
        )
        self.check.active = True
        self.add_widget(self.check)
        self.all_items.append(self.check)


class WebShare(MDApp):
    db_manager = DbManager()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.overlay_color = get_color_from_hex("#6042e4")
        self.custom_sheet = None
        self.other_task = None
        self.sharedFiles = SharedFiles(self)

    def colors_definition(self):
        self.theme_cls.colors["Dark"]["Background"] = "1C2028"
        # self.theme_cls.colors["Dark"]["AppBar"] = "1C2028"
        self.theme_cls.colors["Dark"]["StatusBar"] = "1C2028"
        self.theme_cls.colors["Dark"]["CardsDialogs"] = "1C2028"
        # self.theme_cls.colors["Dark"]["FlatButtonDown"] = "1C2028"
        self.root.ids.toolbar.md_bg_color = get_color_from_hex("1C2028")
        self.root.ids.bottom_Appbar.md_bg_color = get_color_from_hex("1C2028")
        self.root.ids.nav_drawer.md_bg_color = get_color_from_hex("1C2028")

    def add_files(self, path_list):
        for file in self.db_manager.insertFiles(path_list):
            self.sharedFiles.files.append(file)
            self.root.ids.selection_list.add_widget(MyItem(path=file[0]))

    @classmethod
    def loadFiles(cls, self):
        for file in cls.db_manager.getAllFiles():
            self.sharedFiles.files.append((file[1], file[2]))
            self.root.ids.selection_list.add_widget(MyItem(path=file[1]))

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

    def app_func(self):
        self.other_task = asyncio.ensure_future(self.waste_time_freely())

        async def run_wrapper():
            # we don't actually need to set asyncio as the lib because it is
            # the default, but it doesn't hurt to be explicit
            await self.async_run(async_lib='asyncio')
            print('App done')
            self.other_task.cancel()

        return asyncio.gather(run_wrapper(), self.other_task)

    async def waste_time_freely(self):
        try:
            await (self.sharedFiles.run())
        except asyncio.CancelledError as e:
            print('Wasting time was canceled', e)
        finally:
            print('Done wasting time')

    def on_start(self):
        self.root.ids.nav_drawer.set_state("close")
        self.root.ids.toolbar.add_widget(MyButton(self))
        self.root.ids.toolbar.title = "[color=#62acce]Webshare[/color]"
        self.colors_definition()
        self.loadFiles(self)

    def on_float_button_click(self, button):
        button.action_button.disabled = True

        def on_success(requests, result):
            button.action_button.disabled = False
            Snackbar(
                text="[color=#ddbb34]Server is running![/color]",
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_x=(Window.width - (dp(10) * 2)) / Window.width
            ).open()

        def on_failure(requests, result):
            button.action_button.disabled = False
            Snackbar(
                text="[color=#ddbb34]Server is not running![/color]",
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_x=(Window.width - (dp(10) * 2)) / Window.width
            ).open()

        UrlRequest("http://" + self.sharedFiles.host + "/isConnected", on_success=on_success, on_failure=on_failure,
                   on_error=on_failure)

    def show_custom_bottom_sheet(self):
        self.custom_sheet = MDCustomBottomSheet(screen=Factory.ContentCustomSheet(), radius_from="top")
        self.custom_sheet.open()

    def change_theme(self):
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
            self.colors_definition()
        elif self.theme_cls.theme_style == "Dark":
            self.theme_cls.theme_style = "Light"

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
            self.root.ids.toolbar.title = "Webshare"

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

    def on_checkbox_active(self, checkbox, value):
        if value:
            for check in MyItem.all_items:
                check.active = True
        else:
            for check in MyItem.all_items:
                check.active = False


class MyButton(MDFillRoundFlatButton, TouchBehavior):
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self._radius = 6
        self.text = "Add new File"
        self.bold = True
        self.pos_hint = {"center_x": .5, "center_y": .5}
        self.font_name = 'Kanit-SemiBold.ttf'

    def on_enter(self):
        Animation(size_hint=(.6, .1), d=0.3).start(self)

    def on_leave(self):
        Animation(size_hint=(.5, .09), d=0.3).start(self)

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


class ContentNavigationDrawer(MDBoxLayout):
    icon = StringProperty()
    pass


class RightCheckbox(MDSwitch):
    pass


class ContentCustomSheet(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.custom()

    def custom(self):
        layout = MDGridLayout(cols=2)
        layout.padding = (dp(20), dp(20))

        # 1st row
        layout.add_widget(
            MDLabel(
                text="Settings",
                halign="left",
                size_hint_x=None,
                width=100,
                font_name='Kanit-SemiBold.ttf',
                color="62acce"
            )
        )
        layout.add_widget(
            MDLabel(
                halign="left",
            ))

        # 2nd row
        layout.add_widget(
            MDLabel(
                text="Server status : ",
                halign="left",
                size_hint_x=None,
                width=200,
                padding=(dp(20), dp(5))
            )
        )
        layout.add_widget(MDLabel(
            text="active",
            halign="left",
        ))

        # 3rd row
        layout.add_widget(
            MDLabel(
                text="Url : ",
                halign="left",
                size_hint_x=None,
                width=200,
                padding=(dp(20), dp(5))
            )
        )
        layout.add_widget(MDLabel(
            text=SharedFiles.get_url(),
            halign="left",
            color=get_color_from_hex("#91cee3")
        ))

        # 4th row
        layout.add_widget(
            MDLabel(
                text="Enable authentication",
                halign="left",
                size_hint_x=None,
                width=200,
                padding=(dp(20), dp(5))
            )
        )
        layout.add_widget(MDSwitch(
            pos_hint={"center_x": .5, "center_y": .5}
        ))

        self.add_widget(layout)

# https://www.youtube.com/watch?v=NZde8Xt78Iw
