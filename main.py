# -*- coding: utf-8-*-

import sys
sys.dont_write_bytecode = True
import kivy
kivy.require('1.10.0')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.utils import get_color_from_hex, hex_colormap
from kivy.properties import ObjectProperty, StringProperty, ListProperty
try:
    from kivymd.theming import ThemeManager
    from kivymd.toolbar import Toolbar
    from kivymd.card import MDSeparator
    from kivymd.selectioncontrols import MDCheckbox 
except ImportError:
    raise ImportError('''Install package kivymd!''')

ACTIVITY_MANAGER = '''
#:import MDCheckbox kivymd.selectioncontrols.MDCheckbox
<mManager>:
    canvas:
        Rectangle:
            size: self.size
            pos: self.pos
            source: '%s/background.png' % root.home_path
    BoxLayout:
        size_hint_y: None
        height: dp(40)
        y: root.height - toolbar.height
        spacing: dp(5)
        Toolbar:
            id: toolbar
            title: 'Hello World'
            left_action_items: [['arrow-left', lambda x: root.exit_manager(1)]]
            right_action_items: [['information', lambda x: root.filter_manager(1)]] 
            elevation: 10
            md_bg_color: root.floating_button_color
    ScreenManager:
        id: manager
        Screen:
            name: 'mainlist'
            RecycleView:
                id: rv
                key_viewclass: 'viewclass'
                key_size: 'height'
                bar_width: dp(6)
                bar_color: root.floating_button_color
                y: -toolbar.height
                height: root.height - toolbar.height
                RecycleBoxLayout:
                    default_size_hint: 1, None
                    default_size: None, dp(72)
                    size_hint_y: None
                    height: self.minimum_height
                    orientation: 'vertical'
        Screen:
            name: 'assignment'
            MDCard:
                id: lic
                size_hint: 1, None 
                size: dp(360), root.height - toolbar.height
                pos_hint_y: None
                pos_hint_x: 0.5
                y: root.height - toolbar.height - lic.height   
                BoxLayout:
                    orientation:'vertical'
                    padding: dp(8)             
                    BoxLayout:
                        orientation:'horizontal'
                        size_hint: 1, None
                        size: dp(192), dp(48)
                        padding: dp(4)
                        MDLabel:
                            text: 'Порядок участия принимаю:'
                            size_hint: None, None
                            size: dp(192), dp(48)
                            theme_text_color: 'Primary' 
                        MDCheckbox:
                            id: licckeck
                            active: False
                            size_hint: None, None
                            size: dp(48), dp(48)
                            on_state: root.search_manager(1)
                    MDLabel:
                        text: root.lictext
                        theme_text_color: 'Primary' 
'''

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

class mManager(FloatLayout):
    home_path = StringProperty(os.path.split(__file__)[0])
    icon = StringProperty('qrcode-scan')
    '''Иконка, которая будет использована на кнопке выбора директории.'''
    exit_manager = ObjectProperty(lambda x: None)
    '''Функция, вызываемая при нажатии пользователем кнопки назад.'''
    filter_manager = ObjectProperty(lambda x: None)
    search_manager = ObjectProperty(lambda x: None)
    lictext = StringProperty(''' Eто проект. Порядок участия в проекте бесплатное. Сервис не содержит рекламы. Персональная информация не обрабатывается.''')  
    floating_button_color = ListProperty(get_color_from_hex(hex_colormap['teal']))
    '''Цвет кнопки.'''

    def __init__(self, **kwargs):
        super(mManager, self).__init__(**kwargs)
        toolbar_label = self.ids.toolbar.children[1].children[0]
        toolbar_label.font_style = 'Subhead' 

class HelloWorld(App):
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'BlueGrey'

    def build(self):
        self.manager_open = False
        self.islic = False
        Window.bind(on_keyboard=self.events)
        self.box = BoxLayout()
        self.main_manager = mManager(exit_manager=self.exit_manager
		, filter_manager=self.filter_manager, search_manager=self.search_manager)
        self.box.add_widget(self.main_manager)        
        return self.box

    def exit_manager(self, *args):
        if self.main_manager.ids.manager.current == 'mainlist':
            self.stop()
        else:
            self.main_manager.ids.toolbar.title = 'Hello World'
            self.main_manager.ids.manager.current = 'mainlist'

    def filter_manager(self, *args):
        '''Вызывается при достижении пользователем licence.'''
        self.main_manager.ids.toolbar.title = 'О сервисе'
        self.main_manager.ids.licckeck.active = self.islic 
        self.main_manager.ids.licckeck.disabled = self.islic 
        self.main_manager.ids.manager.current = 'assignment'

    def search_manager(self, *args):
        '''Вызывается при corLacuu c lic.'''
        if not self.islic:
            self.islic = True

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Вызывается при нажатии кнопок на мобильном устройстве.'''
        if keyboard in (1001, 27):
            if self.manager_open:
                self.stop() 
        return True

Builder.load_string(ACTIVITY_MANAGER)
HelloWorld().run()
