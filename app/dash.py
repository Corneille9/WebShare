import asyncio
import ntpath
import socket
import sys

from kivy.animation import Animation
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.list import TwoLineAvatarListItem
# 16.75
from kivymd.uix.selectioncontrol import MDCheckbox, MDSwitch
from kivymd.uix.toolbar import MDToolbar

from app.utils.utilities import get_file_icon, get_icon_dir
from web.app import SharedFiles

KV = '''
#:import MagicBehavior kivymd.uix.behaviors.MagicBehavior

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
                 
                MDBottomAppBar:
                    height: 10
                    md_bg_color: 0, 0, 0, 1 
                
                    MDToolbar:
                        id: bottom_toolbar
                        icon: "git"
                        type: "bottom"
                        on_action_button: app.on_float_button_click(self)
                        icon_color: 0, 0, 0, 1
                        left_action_items: [["router-network", lambda x: app.show_custom_bottom_sheet(), "Paramètres du server"]]       
                
    MDNavigationDrawer:
        id: nav_drawer
        orientation:"vertical"
                
        MDToolbar:
            title: 'WebShare'
            elevation: 10    
            md_bg_color: 0, 0, 0, 1  
            
        ContentNavigationDrawer:  
            nav_drawer: nav_drawer                                    
          
<ContentCustomSheet@BoxLayout>:
    orientation: "vertical"
    size_hint_y: None
    height: "200dp"

    ScrollView:
        MDBoxLayout:
            orientation: "vertical"
            MDBoxLayout
                orientation: "horizontal"
                MDLabel:
                    padding: "20dp", "0dp"
                    bold: True
                    text: "Url :           http://192.168.43.214/SharedFiles"
                    adaptive_size: True
                    font_name: 'Kanit-SemiBold.ttf'
                    pos_hint: {'center_x': .9, 'center_y': .5}
                    
       
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


class WebShare(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.overlay_color = get_color_from_hex("#6042e4")
        self.custom_sheet = None
        self.other_task = None
        self.sharedFiles = SharedFiles(self)

    def add_files(self, file_path):
        for path in file_path:
            self.sharedFiles.files.append(path)
            self.root.ids.selection_list.add_widget(MyItem(path=path))

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
        btn = MyButton(self)
        self.root.ids.toolbar.add_widget(btn)

    def on_float_button_click(self, button):
        button.action_button.disabled = True

        def on_sccss(requests, result):
            button.action_button.disabled = False
            print(result)

        def on_fail(requests, result):
            button.action_button.disabled = False

        UrlRequest("http://" + self.sharedFiles.host + "/isConnected", on_success=on_sccss, on_failure=on_fail, on_error=on_fail)

    def show_custom_bottom_sheet(self):
        self.custom_sheet = MDCustomBottomSheet(screen=Factory.ContentCustomSheet(), radius_from="top")
        self.custom_sheet.open()

    def change_theme(self):
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
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
    def __init__(self, app=None, **kwargs):
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


class ContentNavigationDrawer(MDBoxLayout):
    icon = StringProperty()
    pass


class RightCheckbox(MDSwitch):
    pass
# https://www.youtube.com/watch?v=NZde8Xt78Iw
