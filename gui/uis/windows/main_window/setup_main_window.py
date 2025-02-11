# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
from gui.widgets.py_table_widget.py_table_widget import PyTableWidget
import sys
import os
import json

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

from PySide6.QtWidgets import QSizePolicy, QSpacerItem
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap
# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from gui.core.json_settings import Settings

# IMPORT THEME COLORS
# ///////////////////////////////////////////////////////////////
from gui.core.json_themes import Themes

# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
from gui.widgets import *

# LOAD UI MAIN
# ///////////////////////////////////////////////////////////////
from . ui_main import *

# MAIN FUNCTIONS 
# ///////////////////////////////////////////////////////////////
from . functions_main_window import MainFunctions

# PY WINDOW
# ///////////////////////////////////////////////////////////////
class SetupMainWindow:
    def __init__(self):
        super().__init__()
        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

    # ADD LEFT MENUS
    # ///////////////////////////////////////////////////////////////
    add_left_menus = [
        {
            "btn_icon" : "icon_home.svg",
            "btn_id" : "btn_home",
            "btn_text" : "Home",
            "btn_tooltip" : "Home page",
            "show_top" : True,
            "is_active" : True
        },
        {
            "btn_icon" : "icon_widgets.svg",
            "btn_id" : "btn_widgets",
            "btn_text" : "Importar editais",
            "btn_tooltip" : "Importação de editais",
            "show_top" : True,
            "is_active" : False
        },
        {
            "btn_icon" : "icon_settings.svg",
            "btn_id" : "btn_config",
            "btn_text" : "Configurações",
            "btn_tooltip" : "Abrir configurações",
            "show_top" : False,
            "is_active" : False
        },
        {
            "btn_icon" : "icon_send.svg",
            "btn_id" : "btn_automation",
            "btn_text" : "Robô Montador",
            "btn_tooltip" : "Robô Montador",
            "show_top" : True,
            "is_active" : False
        }
    ]

    add_title_bar_menus = [
        {
            "btn_icon" : "icon_settings.svg",
            "btn_id" : "btn_top_settings",
            "btn_tooltip" : "Top settings",
            "is_active" : False
        }
    ]

    # SETUP CUSTOM BTNs OF CUSTOM WIDGETS
    # Get sender() function when btn is clicked
    # ///////////////////////////////////////////////////////////////
    def setup_btns(self):
        if self.ui.title_bar.sender() != None:
            return self.ui.title_bar.sender()
        elif self.ui.left_menu.sender() != None:
            return self.ui.left_menu.sender()
        elif self.ui.left_column.sender() != None:
            return self.ui.left_column.sender()

    # SETUP MAIN WINDOW WITH CUSTOM PARAMETERS
    # ///////////////////////////////////////////////////////////////
    def setup_gui(self):
        # APP TITLE
        # ///////////////////////////////////////////////////////////////
        self.setWindowTitle(self.settings["app_name"])
        
        # REMOVE TITLE BAR
        # ///////////////////////////////////////////////////////////////
        if self.settings["custom_title_bar"]:
            self.setWindowFlag(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

        # ADD GRIPS
        # ///////////////////////////////////////////////////////////////
        if self.settings["custom_title_bar"]:
            self.left_grip = PyGrips(self, "left", self.hide_grips)
            self.right_grip = PyGrips(self, "right", self.hide_grips)
            self.top_grip = PyGrips(self, "top", self.hide_grips)
            self.bottom_grip = PyGrips(self, "bottom", self.hide_grips)
            self.top_left_grip = PyGrips(self, "top_left", self.hide_grips)
            self.top_right_grip = PyGrips(self, "top_right", self.hide_grips)
            self.bottom_left_grip = PyGrips(self, "bottom_left", self.hide_grips)
            self.bottom_right_grip = PyGrips(self, "bottom_right", self.hide_grips)

        # LEFT MENUS / GET SIGNALS WHEN LEFT MENU BTN IS CLICKED / RELEASED
        # ///////////////////////////////////////////////////////////////
        # ADD MENUS
        self.ui.left_menu.add_menus(SetupMainWindow.add_left_menus)

        # SET SIGNALS
        self.ui.left_menu.clicked.connect(self.btn_clicked)
        self.ui.left_menu.released.connect(self.btn_released)

        # TITLE BAR / ADD EXTRA BUTTONS
        # ///////////////////////////////////////////////////////////////
        # ADD MENUS
        self.ui.title_bar.add_menus(SetupMainWindow.add_title_bar_menus)

        # SET SIGNALS
        self.ui.title_bar.clicked.connect(self.btn_clicked)
        self.ui.title_bar.released.connect(self.btn_released)

        # ADD Title
        if self.settings["custom_title_bar"]:
            self.ui.title_bar.set_title(self.settings["app_name"])
        else:
            self.ui.title_bar.set_title("Welcome to PyOneDark")

        # LEFT COLUMN SET SIGNALS
        # ///////////////////////////////////////////////////////////////
        self.ui.left_column.clicked.connect(self.btn_clicked)
        self.ui.left_column.released.connect(self.btn_released)

        # SET INITIAL PAGE / SET LEFT AND RIGHT COLUMN MENUS
        # ///////////////////////////////////////////////////////////////
        MainFunctions.set_page(self, self.ui.load_pages.page_1)
        MainFunctions.set_left_column_menu(
            self,
            menu = self.ui.left_column.menus.menu_1,
            title = "Settings Left Column",
            icon_path = Functions.set_svg_icon("icon_settings.svg")
        )
        MainFunctions.set_right_column_menu(self, self.ui.right_column.menu_1)
        
        

        # ///////////////////////////////////////////////////////////////
        # EXAMPLE CUSTOM WIDGETS
        # Here are added the custom widgets to pages and columns that
        # were created using Qt Designer.
        # This is just an example and should be deleted when creating
        # your application.
        #
        # OBJECTS FOR LOAD PAGES, LEFT AND RIGHT COLUMNS
        # You can access objects inside Qt Designer projects using
        # the objects below:
        #
        # <OBJECTS>
        # LEFT COLUMN: self.ui.left_column.menus
        # RIGHT COLUMN: self.ui.right_column
        # LOAD PAGES: self.ui.load_pages
        # </OBJECTS>
        # ///////////////////////////////////////////////////////////////

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # LOAD THEME COLOR
        # ///////////////////////////////////////////////////////////////
        themes = Themes()
        self.themes = themes.items

        # LEFT COLUMN
        # ///////////////////////////////////////////////////////////////

        # BTN 1
        self.left_btn_1 = PyPushButton(
            text="Btn 1",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.left_btn_1.setMaximumHeight(40)
        self.ui.left_column.menus.btn_1_layout.addWidget(self.left_btn_1)

        # BTN 2
        self.left_btn_2 = PyPushButton(
            text="Btn With Icon",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.icon = QIcon(Functions.set_svg_icon("icon_settings.svg"))
        self.left_btn_2.setIcon(self.icon)
        self.left_btn_2.setMaximumHeight(40)
        self.ui.left_column.menus.btn_2_layout.addWidget(self.left_btn_2)

        # BTN 3 - Default QPushButton
        self.left_btn_3 = QPushButton("Default QPushButton")
        self.left_btn_3.setMaximumHeight(40)
        self.ui.left_column.menus.btn_3_layout.addWidget(self.left_btn_3)

        # PAGES
        # ///////////////////////////////////////////////////////////////

        # PAGE 1 - ADD LOGO TO MAIN PAGE
        # PAGE 1 - ADD LOGO TO MAIN PAGE
        self.logo_png = QLabel()
        logo_pixmap = QPixmap(Functions.set_image("resolvi_logo_2.png"))

        # Definir tamanho máximo desejado
        desired_width = 300  # ajuste este valor conforme necessário
        desired_height = 100  # ajuste este valor conforme necessário

        # Redimensionar mantendo proporção
        scaled_pixmap = logo_pixmap.scaled(
            desired_width, 
            desired_height,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.logo_png.setPixmap(scaled_pixmap)
        self.logo_png.setAlignment(Qt.AlignCenter)

        # Configurar política de dimensionamento
        self.logo_png.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.logo_png.setMaximumSize(desired_width, desired_height)

        self.ui.load_pages.logo_layout.addWidget(self.logo_png, Qt.AlignCenter, Qt.AlignCenter)

        # PAGE 2
        # # CIRCULAR PROGRESS 1
        # self.circular_progress_1 = PyCircularProgress(
        #     value = 80,
        #     progress_color = self.themes["app_color"]["context_color"],
        #     text_color = self.themes["app_color"]["text_title"],
        #     font_size = 14,
        #     bg_color = self.themes["app_color"]["dark_four"]
        # )
        # self.circular_progress_1.setFixedSize(200,200)

        # CIRCULAR PROGRESS 2
        # self.circular_progress_2 = PyCircularProgress(
        #     value = 45,
        #     progress_width = 4,
        #     progress_color = self.themes["app_color"]["context_color"],
        #     text_color = self.themes["app_color"]["context_color"],
        #     font_size = 14,
        #     bg_color = self.themes["app_color"]["bg_three"]
        # )
        # self.circular_progress_2.setFixedSize(160,160)

        # # CIRCULAR PROGRESS 3
        # self.circular_progress_3 = PyCircularProgress(
        #     value = 75,
        #     progress_width = 2,
        #     progress_color = self.themes["app_color"]["pink"],
        #     text_color = self.themes["app_color"]["white"],
        #     font_size = 14,
        #     bg_color = self.themes["app_color"]["bg_three"]
        # )
        # self.circular_progress_3.setFixedSize(140,140)

        # # PY SLIDER 1
        # self.vertical_slider_1 = PySlider(
        #     margin=8,
        #     bg_size=10,
        #     bg_radius=5,
        #     handle_margin=-3,
        #     handle_size=16,
        #     handle_radius=8,
        #     bg_color = self.themes["app_color"]["dark_three"],
        #     bg_color_hover = self.themes["app_color"]["dark_four"],
        #     handle_color = self.themes["app_color"]["context_color"],
        #     handle_color_hover = self.themes["app_color"]["context_hover"],
        #     handle_color_pressed = self.themes["app_color"]["context_pressed"]
        # )
        # self.vertical_slider_1.setMinimumHeight(100)

        # # PY SLIDER 2
        # self.vertical_slider_2 = PySlider(
        #     bg_color = self.themes["app_color"]["dark_three"],
        #     bg_color_hover = self.themes["app_color"]["dark_three"],
        #     handle_color = self.themes["app_color"]["context_color"],
        #     handle_color_hover = self.themes["app_color"]["context_hover"],
        #     handle_color_pressed = self.themes["app_color"]["context_pressed"]
        # )
        # self.vertical_slider_2.setMinimumHeight(100)

        # # PY SLIDER 3
        # self.vertical_slider_3 = PySlider(
        #     margin=8,
        #     bg_size=10,
        #     bg_radius=5,
        #     handle_margin=-3,
        #     handle_size=16,
        #     handle_radius=8,
        #     bg_color = self.themes["app_color"]["dark_three"],
        #     bg_color_hover = self.themes["app_color"]["dark_four"],
        #     handle_color = self.themes["app_color"]["context_color"],
        #     handle_color_hover = self.themes["app_color"]["context_hover"],
        #     handle_color_pressed = self.themes["app_color"]["context_pressed"]
        # )
        # self.vertical_slider_3.setOrientation(Qt.Horizontal)
        # self.vertical_slider_3.setMinimumWidth(200)

        # # PY SLIDER 4
        # self.vertical_slider_4 = PySlider(
        #     bg_color = self.themes["app_color"]["dark_three"],
        #     bg_color_hover = self.themes["app_color"]["dark_three"],
        #     handle_color = self.themes["app_color"]["context_color"],
        #     handle_color_hover = self.themes["app_color"]["context_hover"],
        #     handle_color_pressed = self.themes["app_color"]["context_pressed"]
        # )
        # self.vertical_slider_4.setOrientation(Qt.Horizontal)
        # self.vertical_slider_4.setMinimumWidth(200)

        # # ICON BUTTON 1
        # self.icon_button_1 = PyIconButton(
        #     icon_path = Functions.set_svg_icon("icon_heart.svg"),
        #     parent = self,
        #     app_parent = self.ui.central_widget,
        #     tooltip_text = "Icon button - Heart",
        #     width = 40,
        #     height = 40,
        #     radius = 20,
        #     dark_one = self.themes["app_color"]["dark_one"],
        #     icon_color = self.themes["app_color"]["icon_color"],
        #     icon_color_hover = self.themes["app_color"]["icon_hover"],
        #     icon_color_pressed = self.themes["app_color"]["icon_active"],
        #     icon_color_active = self.themes["app_color"]["icon_active"],
        #     bg_color = self.themes["app_color"]["dark_one"],
        #     bg_color_hover = self.themes["app_color"]["dark_three"],
        #     bg_color_pressed = self.themes["app_color"]["pink"]
        # )

        # # ICON BUTTON 2
        # self.icon_button_2 = PyIconButton(
        #     icon_path = Functions.set_svg_icon("icon_add_user.svg"),
        #     parent = self,
        #     app_parent = self.ui.central_widget,
        #     tooltip_text = "BTN with tooltip",
        #     width = 40,
        #     height = 40,
        #     radius = 8,
        #     dark_one = self.themes["app_color"]["dark_one"],
        #     icon_color = self.themes["app_color"]["icon_color"],
        #     icon_color_hover = self.themes["app_color"]["icon_hover"],
        #     icon_color_pressed = self.themes["app_color"]["white"],
        #     icon_color_active = self.themes["app_color"]["icon_active"],
        #     bg_color = self.themes["app_color"]["dark_one"],
        #     bg_color_hover = self.themes["app_color"]["dark_three"],
        #     bg_color_pressed = self.themes["app_color"]["green"],
        # )

        # # ICON BUTTON 3
        # self.icon_button_3 = PyIconButton(
        #     icon_path = Functions.set_svg_icon("icon_add_user.svg"),
        #     parent = self,
        #     app_parent = self.ui.central_widget,
        #     tooltip_text = "BTN actived! (is_actived = True)",
        #     width = 40,
        #     height = 40,
        #     radius = 8,
        #     dark_one = self.themes["app_color"]["dark_one"],
        #     icon_color = self.themes["app_color"]["icon_color"],
        #     icon_color_hover = self.themes["app_color"]["icon_hover"],
        #     icon_color_pressed = self.themes["app_color"]["white"],
        #     icon_color_active = self.themes["app_color"]["icon_active"],
        #     bg_color = self.themes["app_color"]["dark_one"],
        #     bg_color_hover = self.themes["app_color"]["dark_three"],
        #     bg_color_pressed = self.themes["app_color"]["context_color"],
        #     is_active = True
        # )
        
        # # PUSH BUTTON 1
        # self.push_button_1 = PyPushButton(
        #     text = "Importar",
        #     radius = 8,
        #     color = self.themes["app_color"]["text_foreground"],
        #     bg_color = self.themes["app_color"]["dark_one"],
        #     bg_color_hover = self.themes["app_color"]["dark_three"],
        #     bg_color_pressed = self.themes["app_color"]["dark_four"]
        # )
        # self.push_button_1.setMinimumHeight(30)
        # self.push_button_1.setMinimumWidth(300)

        

        # PY LINE EDIT - QUANTIDADE DE EDITAIS 
        self.line_edit_quantidade = PyLineEdit(
            text = "",
            place_holder_text = "Quantidade de editais (obrigatório)",
            radius = 8,
            border_size = 2,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["white"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_active = self.themes["app_color"]["dark_three"],
            context_color = self.themes["app_color"]["context_color"]
        )
        quantidade_container = QWidget()
        quantidade_layout = QVBoxLayout(quantidade_container)
        quantidade_layout.setContentsMargins(0, 0, 0, 0)

        self.quantidade_label = QLabel("Quantidade de editais:")
        self.quantidade_label.setStyleSheet(f"""
            QLabel {{
                color: {self.themes["app_color"]["text_foreground"]};
                font-size: 14px;
                font-weight: bold;
                background-color: transparent;
                margin-bottom: 8px;
            }}
        """)
        quantidade_layout.addWidget(self.quantidade_label)

        self.line_edit_quantidade.setMinimumHeight(30)
        quantidade_layout.addWidget(self.line_edit_quantidade)
        

        # PY LINE EDIT - PORTAIS 
        self.line_edit_portais = PyLineEdit(
            text = "",
            place_holder_text = "Portais (Ex: 1,41,12)",
            radius = 8,
            border_size = 2,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["white"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_active = self.themes["app_color"]["dark_three"],
            context_color = self.themes["app_color"]["context_color"]
        )
        portais_container = QWidget()
        portais_layout = QVBoxLayout(portais_container)
        portais_layout.setContentsMargins(0, 0, 0, 0)

        self.portais_label = QLabel("Portais:")
        self.portais_label.setStyleSheet(f"""
            QLabel {{
                color: {self.themes["app_color"]["text_foreground"]};
                font-size: 14px;
                font-weight: bold;
                background-color: transparent;
                margin-bottom: 8px;
            }}
        """)
        portais_layout.addWidget(self.portais_label)

        self.line_edit_portais.setMinimumHeight(30)
        portais_layout.addWidget(self.line_edit_portais)
        
        
        self.line_edit_perfil = PyLineEdit(
            text = "4821",
            place_holder_text = "Perfil (Ex: 4821)",
            radius = 8,
            border_size = 2,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["white"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_active = self.themes["app_color"]["dark_three"],
            context_color = self.themes["app_color"]["context_color"]
        )
        perfil_container = QWidget()
        perfil_layout = QVBoxLayout(perfil_container)
        perfil_layout.setContentsMargins(0, 0, 0, 0)

        self.perfil_label = QLabel("Perfil:")
        self.perfil_label.setStyleSheet(f"""
            QLabel {{
                color: {self.themes["app_color"]["text_foreground"]};
                font-size: 14px;
                font-weight: bold;
                background-color: transparent;
                margin-bottom: 8px;
            }}
        """)
        perfil_layout.addWidget(self.perfil_label)

        self.line_edit_perfil.setMinimumHeight(30)
        perfil_layout.addWidget(self.line_edit_perfil)
        
        # PUSH BUTTON 2
        self.push_button_importar_editais = PyPushButton(
            text = " Importar",
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_hover = self.themes["app_color"]["dark_three"],
            bg_color_pressed = self.themes["app_color"]["dark_four"]
        )
        self.icon_2 = QIcon(Functions.set_svg_icon("icon_settings.svg"))
        self.push_button_importar_editais.setMinimumHeight(40)
        self.push_button_importar_editais.setIcon(self.icon_2)
        self.push_button_importar_editais.setMinimumWidth(200)
        self.push_button_importar_editais.clicked.connect(lambda: MainFunctions.save_config_data(self))
        
        self.line_edit_status_import = QTextEdit()
        self.line_edit_status_import.setStyleSheet(f"""
            QTextEdit {{
                background-color: {self.themes["app_color"]["dark_one"]};
                border-radius: {8}px;
                padding: 5px;
                color: {self.themes["app_color"]["text_foreground"]};
            }}
        """)
        self.line_edit_status_import.setMinimumHeight(200)
        self.line_edit_status_import.setReadOnly(True)
        
        self.label_title_portal_code = QLabel("Códigos de Portais")
        self.label_title_portal_code.setStyleSheet(f"""
            QLabel {{
                color: {self.themes["app_color"]["text_foreground"]};
                font-size: 14px;
                font-weight: bold;
                background-color: transparent;
            }}
        """)
        
        portal_list = """
            5 - BEC / Imprensa Oficial / Pregão SP
            24 - BLL - Bolsa de Licitações e Leilões
            1362 - BNC - Bolsa Nacional de Compras
            19 - Banrisul
            29 - Compras Amazonas
            898 - Compras BR
            35 - Compras Mato Grosso
            9 - Compras Minas Gerais
            58 - Compras Pernambuco Integrado
            3 - Compras Públicas
            11 - Compras Santa Catarina
            1 - ComprasNet
            25 - ComprasNet - Cotação Eletrônica
            20 - ComprasNet Goiás
            769 - ComprasNet Simulador
            18 - ComprasRS
            28 - Licitanet
            1236 - Licitar Digital
            2 - Licitações-e
            17 - Procergs
            26 - Publinexo
            7 - Siga Espírito Santo
            6 - Siga Rio de Janeiro
            """

        # Create description label with different style
        self.label_description_portal_code = QLabel(portal_list)
        self.label_description_portal_code.setStyleSheet(f"""
            QLabel {{
                color: {self.themes["app_color"]["text_description"]};
                font-size: 13px;
                background-color: transparent;
                margin-top: -15px;
                margin-left: -30px;
            }}
        """)
        
        self.label_title_perfil_code = QLabel("Códigos de Perfis")
        self.label_title_perfil_code.setStyleSheet(f"""
            QLabel {{
                color: {self.themes["app_color"]["text_foreground"]};
                font-size: 14px;
                font-weight: bold;
                background-color: transparent;
            }}
        """)
        
        perfil_list = """
            4824 - ANE CARE
            4529 - AVANI - BRASIL PROTEC
            4822 - GAIA
            4823 - GX2
            4821 - SNACK BORDO
            """

        # Create description label with different style
        self.label_description_perfil_code = QLabel(perfil_list)
        self.label_description_perfil_code.setStyleSheet(f"""
            QLabel {{
                color: {self.themes["app_color"]["text_description"]};
                font-size: 13px;
                background-color: transparent;
                margin-top: -15px;
                margin-left: -30px;
            }}
        """)
        
        self.consumir_planiha_button = PyToggle(
            width = 50,
            bg_color = self.themes["app_color"]["dark_two"],          # Background when off
            circle_color = self.themes["app_color"]["icon_color"],      # Circle color (#FF7A01)
            active_color = self.themes["app_color"]["dark_four"],       # Background when on
            animation_curve = QEasingCurve.OutBounce,                  # Animation curve    
        )
        
        toggle_mode_container = QWidget()
        toggle_mode_container.setMaximumWidth(200)
        toggle_mode_layout = QVBoxLayout(toggle_mode_container)
        toggle_mode_layout.setContentsMargins(0, 0, 0, 0)

        self.toggle_mode_label = QLabel("Consumir planilha de ID:")
        self.toggle_mode_label.setStyleSheet(f"""
            QLabel {{
                color: {self.themes["app_color"]["text_foreground"]};
                font-size: 14px;
                font-weight: bold;
                background-color: transparent;
                margin-bottom: 8px;
            }}
        """)
        toggle_mode_layout.addWidget(self.toggle_mode_label)

        toggle_mode_input_layout = QHBoxLayout()
        toggle_mode_input_layout.setContentsMargins(0, 0, 0, 0)
        toggle_mode_input_layout.addWidget(self.consumir_planiha_button)
        toggle_mode_input_layout.addStretch()

        toggle_mode_layout.addLayout(toggle_mode_input_layout)

        
        
        # Após adicionar os widgets
        self.ui.load_pages.row_1_layout.addWidget(quantidade_container)
        self.ui.load_pages.row_1_layout.addWidget(portais_container)
        self.ui.load_pages.row_1_layout.addWidget(perfil_container)
        self.ui.load_pages.row_1_layout.addWidget(toggle_mode_container)
        self.ui.load_pages.row_2_layout.addWidget(self.push_button_importar_editais)
        self.ui.load_pages.row_3_layout.addWidget(self.line_edit_status_import)
        
        self.ui.load_pages.row_4_layout.addWidget(self.label_title_portal_code)
        self.ui.load_pages.row_4_layout.addWidget(self.label_description_portal_code)
        
        self.ui.load_pages.row_4_layout.addWidget(self.label_title_perfil_code)
        self.ui.load_pages.row_4_layout.addWidget(self.label_description_perfil_code)


        # CONFIGURAÇÕES ---------
        
        
        
        settings_save_path_container = QWidget()
        settings_save_path_layout = QVBoxLayout(settings_save_path_container)
        settings_save_path_layout.setContentsMargins(0, 0, 0, 0)

        self.save_path_label = QLabel("Selecione o diretório onde os editais serão salvos:")
        self.save_path_label.setStyleSheet(f"""
            QLabel {{
                color: {self.themes["app_color"]["text_foreground"]};
                font-size: 14px;
                font-weight: bold;
                background-color: transparent;
                margin-bottom: 8px;
            }}
        """)
        settings_save_path_layout.addWidget(self.save_path_label)

        save_path_input_layout = QHBoxLayout()
        save_path_input_layout.setContentsMargins(0, 0, 0, 0)

        self.save_path_line_edit = PyLineEdit(
            text = "",
            place_holder_text = "Diretório para salvar os editais",
            radius = 8,
            border_size = 2,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["white"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_active = self.themes["app_color"]["dark_three"],
            context_color = self.themes["app_color"]["context_color"]
        )
        self.save_path_line_edit.setMinimumHeight(30)

        self.save_path_button = PyPushButton(
            text = "Escolher",
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_hover = self.themes["app_color"]["dark_three"],
            bg_color_pressed = self.themes["app_color"]["dark_four"]
        )
        self.save_path_button.setMinimumHeight(30)
        self.save_path_button.setMinimumWidth(200)
        self.save_path_button.clicked.connect(lambda: MainFunctions.select_save_path(self, "Selecione a pasta para salvar os editais", self.save_path_line_edit))

        save_path_input_layout.addWidget(self.save_path_line_edit)
        save_path_input_layout.addWidget(self.save_path_button)
        settings_save_path_layout.addLayout(save_path_input_layout)

        # Container para planilha de ID
        settings_id_sheet_container = QWidget() 
        settings_id_sheet_layout = QVBoxLayout(settings_id_sheet_container)
        settings_id_sheet_layout.setContentsMargins(0, 0, 0, 0)

        self.id_sheet_label = QLabel("Selecione a planilha de IDs:")
        self.id_sheet_label.setStyleSheet(f"""
            QLabel {{
                color: {self.themes["app_color"]["text_foreground"]};
                font-size: 14px;
                font-weight: bold;
                background-color: transparent;
                margin-bottom: 8px;
            }}
        """)
        settings_id_sheet_layout.addWidget(self.id_sheet_label)

        id_sheet_input_layout = QHBoxLayout()
        id_sheet_input_layout.setContentsMargins(0, 0, 0, 0)

        self.id_sheet_line_edit = PyLineEdit(
            text = "",
            place_holder_text = "Arquivo de planilha de IDs",
            radius = 8,
            border_size = 2,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["white"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_active = self.themes["app_color"]["dark_three"],
            context_color = self.themes["app_color"]["context_color"]
        )
        self.id_sheet_line_edit.setMinimumHeight(30)

        self.id_sheet_button = PyPushButton(
            text = "Escolher",
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_hover = self.themes["app_color"]["dark_three"],
            bg_color_pressed = self.themes["app_color"]["dark_four"]
        )
        self.id_sheet_button.setMinimumHeight(30)
        self.id_sheet_button.setMinimumWidth(200)
        self.id_sheet_button.clicked.connect(lambda: MainFunctions.select_archive_path(self, "Selecione a planilha de IDs", self.id_sheet_line_edit))

        id_sheet_input_layout.addWidget(self.id_sheet_line_edit)
        id_sheet_input_layout.addWidget(self.id_sheet_button)
        settings_id_sheet_layout.addLayout(id_sheet_input_layout)
        
        settings_doc_container = QWidget()
        settings_doc_layout = QVBoxLayout(settings_doc_container)
        settings_doc_layout.setContentsMargins(0, 0, 0, 0)

        self.doc_label = QLabel("Selecione o arquivo de documento:")
        self.doc_label.setStyleSheet(f"""
            QLabel {{
                color: {self.themes["app_color"]["text_foreground"]};
                font-size: 14px;
                font-weight: bold;
                background-color: transparent;
                margin-bottom: 8px;
            }}
        """)
        settings_doc_layout.addWidget(self.doc_label)

        doc_input_layout = QHBoxLayout()
        doc_input_layout.setContentsMargins(0, 0, 0, 0)

        self.doc_line_edit = PyLineEdit(
            text = "",
            place_holder_text = "Arquivo de documento",
            radius = 8,
            border_size = 2,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["white"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_active = self.themes["app_color"]["dark_three"],
            context_color = self.themes["app_color"]["context_color"]
        )
        self.doc_line_edit.setMinimumHeight(30)

        self.doc_button = PyPushButton(
            text = "Escolher",
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_hover = self.themes["app_color"]["dark_three"],
            bg_color_pressed = self.themes["app_color"]["dark_four"]
        )
        self.doc_button.setMinimumHeight(30)
        self.doc_button.setMinimumWidth(200)
        self.doc_button.clicked.connect(lambda: MainFunctions.select_archive_path(self, "Selecione o arquivo de documento", self.doc_line_edit))

        doc_input_layout.addWidget(self.doc_line_edit)
        doc_input_layout.addWidget(self.doc_button)
        settings_doc_layout.addLayout(doc_input_layout)

        # Container para planilha de proposta
        settings_proposal_container = QWidget()
        settings_proposal_layout = QVBoxLayout(settings_proposal_container)
        settings_proposal_layout.setContentsMargins(0, 0, 0, 0)

        self.proposal_label = QLabel("Selecione a planilha de proposta:")
        self.proposal_label.setStyleSheet(f"""
            QLabel {{
                color: {self.themes["app_color"]["text_foreground"]};
                font-size: 14px;
                font-weight: bold;
                background-color: transparent;
                margin-bottom: 8px;
            }}
        """)
        settings_proposal_layout.addWidget(self.proposal_label)

        proposal_input_layout = QHBoxLayout()
        proposal_input_layout.setContentsMargins(0, 0, 0, 0)

        self.proposal_line_edit = PyLineEdit(
            text = "",
            place_holder_text = "Arquivo de planilha de proposta",
            radius = 8,
            border_size = 2,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["white"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_active = self.themes["app_color"]["dark_three"],
            context_color = self.themes["app_color"]["context_color"]
        )
        self.proposal_line_edit.setMinimumHeight(30)

        self.proposal_button = PyPushButton(
            text = "Escolher",
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_hover = self.themes["app_color"]["dark_three"],
            bg_color_pressed = self.themes["app_color"]["dark_four"]
        )
        self.proposal_button.setMinimumHeight(30)
        self.proposal_button.setMinimumWidth(200)
        self.proposal_button.clicked.connect(lambda: MainFunctions.select_archive_path(self, "Selecione a planilha de proposta", self.proposal_line_edit))

        proposal_input_layout.addWidget(self.proposal_line_edit)
        proposal_input_layout.addWidget(self.proposal_button)
        settings_proposal_layout.addLayout(proposal_input_layout)

        settings_declaration_container = QWidget()
        settings_declaration_layout = QVBoxLayout(settings_declaration_container)
        settings_declaration_layout.setContentsMargins(0, 0, 0, 0)

        self.declaration_label = QLabel("Selecione o documento de declaração:")
        self.declaration_label.setStyleSheet(f"""
            QLabel {{
                color: {self.themes["app_color"]["text_foreground"]};
                font-size: 14px;
                font-weight: bold;
                background-color: transparent;
                margin-bottom: 8px;
            }}
        """)
        settings_declaration_layout.addWidget(self.declaration_label)

        declaration_input_layout = QHBoxLayout()
        declaration_input_layout.setContentsMargins(0, 0, 0, 0)

        self.declaration_line_edit = PyLineEdit(
            text = "",
            place_holder_text = "Arquivo de declaração",
            radius = 8,
            border_size = 2,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["white"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_active = self.themes["app_color"]["dark_three"],
            context_color = self.themes["app_color"]["context_color"]
        )
        self.declaration_line_edit.setMinimumHeight(30)

        self.declaration_button = PyPushButton(
            text = "Escolher",
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_hover = self.themes["app_color"]["dark_three"],
            bg_color_pressed = self.themes["app_color"]["dark_four"]
        )
        self.declaration_button.setMinimumHeight(30)
        self.declaration_button.setMinimumWidth(200)
        self.declaration_button.clicked.connect(lambda: MainFunctions.select_archive_path(self, "Selecione o arquivo de declaração", self.declaration_line_edit))

        declaration_input_layout.addWidget(self.declaration_line_edit)
        declaration_input_layout.addWidget(self.declaration_button)
        settings_declaration_layout.addLayout(declaration_input_layout)
        
        
        
        self.save_settings_button = PyPushButton(
            text=" Salvar Configurações",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
        )
        self.save_settings_button_icon = QIcon(Functions.set_svg_icon("icon_save.svg"))

        self.save_settings_button.setIcon(self.save_settings_button_icon)
        self.save_settings_button.setMinimumHeight(30)
        self.save_settings_button.setMaximumWidth(200)
        
        self.save_settings_button.clicked.connect(lambda: MainFunctions.save_settings(self))
        
        self.line_edit_status_settings = QTextEdit()
        self.line_edit_status_settings.setStyleSheet(f"""
            QTextEdit {{
                background-color: {self.themes["app_color"]["dark_one"]};
                border-radius: {8}px;
                padding: 5px;
                color: {self.themes["app_color"]["text_foreground"]};
            }}
        """)
        self.line_edit_status_settings.setMinimumHeight(200)
        self.line_edit_status_settings.setReadOnly(True)
        


        # Adicione todos os containers ao layout principal
        self.ui.load_pages.row_1_layout_3.addWidget(settings_save_path_container)
        self.ui.load_pages.row_1_layout_3.addWidget(settings_id_sheet_container)
        self.ui.load_pages.row_2_layout_3.addWidget(settings_doc_container)
        self.ui.load_pages.row_2_layout_3.addWidget(settings_proposal_container)
        self.ui.load_pages.row_3_layout_3.addWidget(settings_declaration_container)
        
        self.ui.load_pages.row_4_layout_3.addWidget(self.save_settings_button)
        self.ui.load_pages.row_5_layout_3.addWidget(self.line_edit_status_settings)
        
        self.line_edit_status_automation = QTextEdit()
        self.line_edit_status_automation.setStyleSheet(f"""
            QTextEdit {{
                background-color: {self.themes["app_color"]["dark_one"]};
                border-radius: {8}px;
                padding: 5px;
                color: {self.themes["app_color"]["text_foreground"]};
            }}
        """)
        self.line_edit_status_automation.setMinimumHeight(200)
        self.line_edit_status_automation.setReadOnly(True)

        
        self.start_automation_button = PyPushButton(
            text=" Iniciar Automação",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
        )
        self.start_automation_button_icon = QIcon(Functions.set_svg_icon("icon_send.svg"))

        self.start_automation_button.setIcon(self.start_automation_button_icon)
        self.start_automation_button.setMinimumHeight(30)
        self.start_automation_button.setMaximumWidth(200)
        self.start_automation_button.clicked.connect(lambda: MainFunctions.start_automation(self))
        
        

        # Segundo checkbox
        copy_docs_container = QWidget()
        copy_docs_layout = QVBoxLayout(copy_docs_container)  # Mudado para QVBoxLayout
        copy_docs_layout.setContentsMargins(0, 0, 0, 0)
        self.copy_docs_checkbox = QCheckBox("Copiar documentos de habilitação")
        self.copy_docs_checkbox.setChecked(True)
        copy_docs_layout.addWidget(self.copy_docs_checkbox)

        # Terceiro checkbox
        fill_word_container = QWidget()
        fill_word_layout = QVBoxLayout(fill_word_container)  # Mudado para QVBoxLayout
        fill_word_layout.setContentsMargins(0, 0, 0, 0)
        self.fill_word_checkbox = QCheckBox("Preencher declaração do Word")
        self.fill_word_checkbox.setChecked(True)
        fill_word_layout.addWidget(self.fill_word_checkbox)

        # Quarto checkbox
        convert_pdf_container = QWidget()
        convert_pdf_layout = QVBoxLayout(convert_pdf_container)  # Mudado para QVBoxLayout
        convert_pdf_layout.setContentsMargins(0, 0, 0, 0)
        self.convert_pdf_checkbox = QCheckBox("Converter declaração em PDF")
        self.convert_pdf_checkbox.setChecked(True)
        convert_pdf_layout.addWidget(self.convert_pdf_checkbox)

        # Quinto checkbox 
        fill_proposal_container = QWidget()
        fill_proposal_layout = QVBoxLayout(fill_proposal_container)  # Mudado para QVBoxLayout
        fill_proposal_layout.setContentsMargins(0, 0, 0, 0)
        self.fill_proposal_checkbox = QCheckBox("Preencher proposta de preço")
        self.fill_proposal_checkbox.setChecked(True)
        fill_proposal_layout.addWidget(self.fill_proposal_checkbox)
        
        download_editais_container = QWidget()
        download_editais_layout = QVBoxLayout(download_editais_container)  # Mudado para QVBoxLayout
        download_editais_layout.setContentsMargins(0, 0, 0, 0)
        self.download_editais_checkbox = QCheckBox("Baixar os arquivos do edital")
        self.download_editais_checkbox.setChecked(True)
        download_editais_layout.addWidget(self.download_editais_checkbox)

        # Criar um container principal para todos os checkboxes
        main_container = QWidget()
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)  # Espaçamento entre os elementos

        # Adicionar todos os checkboxes ao container principal
        main_layout.addWidget(self.copy_docs_checkbox)
        main_layout.addWidget(self.fill_word_checkbox)
        main_layout.addWidget(self.convert_pdf_checkbox)
        main_layout.addWidget(self.fill_proposal_checkbox)
        main_layout.addWidget(self.download_editais_checkbox)

        # Adicionar o container principal ao layout da página
        self.ui.load_pages.row_1_layout_4.addWidget(main_container)
        self.ui.load_pages.row_1_layout_4.addWidget(self.line_edit_status_automation)
        self.ui.load_pages.row_2_layout_4.addWidget(self.start_automation_button)
        
        
        

        # # Adicionar spacer vertical para empurrar widgets para cima
        # verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # self.ui.load_pages.row_4_layout_3.addItem(verticalSpacer)

        MainFunctions.user_settings(self)

    # RESIZE GRIPS AND CHANGE POSITION
    # Resize or change position when window is resized
    # ///////////////////////////////////////////////////////////////
    def resize_grips(self):
        if self.settings["custom_title_bar"]:
            self.left_grip.setGeometry(5, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 15, 10, 10, self.height())
            self.top_grip.setGeometry(5, 5, self.width() - 10, 10)
            self.bottom_grip.setGeometry(5, self.height() - 15, self.width() - 10, 10)
            self.top_right_grip.setGeometry(self.width() - 20, 5, 15, 15)
            self.bottom_left_grip.setGeometry(5, self.height() - 20, 15, 15)
            self.bottom_right_grip.setGeometry(self.width() - 20, self.height() - 20, 15, 15)