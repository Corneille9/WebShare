from kivy.lang import Builder
from kivymd.app import MDApp

from app.dash import KV


# KV = """
# MDFloatLayout:
#     md_bg_color: 1,1,1,1
#     HoverButton:
#         text:"Hover Me"
#         font_size: "18sp"
#         size_hint: .5, .09
#         pos_hint: {"center_x": .5, "center_y": .5}
#         background_color: 1,1,1,0
#         color: 1,1, 1,1
#         canvas.before:
#             Color:
#                 rgb : self.background
#             RoundedRectangle:
#                 size: self.size
#                 pos: self.pos
#                 radius: [8]
#
# """
#
#
# class HoverButton(Button, HoverBehavior):
#     background = ListProperty((71 / 255, 100 / 255, 237 / 255))
#
#     def on_enter(self):
#         self.background = (251 / 255, 104 / 255, 23 / 255)
#         Animation(size_hint=(.6, .1), d=0.3).start(self)
#
#     def on_leave(self):
#         self.background = (71 / 255, 100 / 255, 237 / 255)
#         Animation(size_hint=(.5, .09), d=0.3).start(self)


class HoverEffect(MDApp):
    def build(self):
        return Builder.load_string(KV)


if __name__ == '__main__':
    HoverEffect().run()
