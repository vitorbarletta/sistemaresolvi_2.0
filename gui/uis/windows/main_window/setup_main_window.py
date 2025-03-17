from gui.widgets.py_table_widget.py_table_widget import PyTableWidget
import sys
import os
import json
from qt_core import *
from PySide6.QtWidgets import QSizePolicy, QSpacerItem
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap
from gui.core.json_settings import Settings
from gui.core.json_themes import Themes
from gui.widgets import *

from . ui_main import *
from . functions_main_window import MainFunctions
# Importe estas bibliotecas no início do arquivo
from PySide6.QtCharts import QChart, QChartView, QPieSeries, QBarSet, QBarSeries, QValueAxis, QBarCategoryAxis
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QLinearGradient
import datetime
import random  # Temporário para dados de exemplo
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QVBoxLayout
from PySide6.QtWidgets import QLineEdit, QPushButton, QTextEdit, QSpacerItem, QWidget, QGridLayout

# Substitua a classe CheckableComboBox inteira por esta implementação
# Substitua a classe CheckableComboBox com esta nova classe PerfilComboBox
class PerfilComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Configurar o estilo e comportamento
        self.setEditable(False)
        
        # Armazenar o ID do perfil selecionado e seu texto
        self.selected_id = None
        self.selected_text = ""
        
        # Mapeamento de índice para dados do perfil
        self.perfil_data = {}  # {índice: (id, nome)}
        
        # Conectar o sinal de seleção alterada
        self.currentIndexChanged.connect(self.handleSelectionChanged)
    
    def addPerfilItem(self, text, id_value):
        """Adiciona um perfil ao combobox"""
        # Armazenar o ID e nome do perfil pelo índice
        index = self.count()
        self.perfil_data[index] = (id_value, text)
        
        # Adicionar o item visível
        self.addItem(text)
    
    def handleSelectionChanged(self, index):
        """Manipula a mudança de seleção"""
        if index >= 0 and index in self.perfil_data:
            # Obter os dados do perfil selecionado
            self.selected_id, self.selected_text = self.perfil_data[index]
            
            # Imprimir informações do perfil selecionado
            print(f"\n=== Perfil Selecionado ===")
            print(f"Nome: '{self.selected_text}'")
            print(f"ID: {self.selected_id}")
            print("========================\n")
    
    def getSelectedId(self):
        """Retorna o ID do perfil selecionado"""
        return self.selected_id if self.selected_id is not None else ""
    
    def getSelectedText(self):
        """Retorna o nome do perfil selecionado"""
        return self.selected_text
    
# Adicione esta nova classe depois da classe PerfilComboBox
class PortalComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Configurar o estilo e comportamento
        self.setEditable(False)
        
        # Armazenar o ID do portal selecionado e seu texto
        self.selected_id = None
        self.selected_text = ""
        
        # Mapeamento de índice para dados do portal
        self.portal_data = {}  # {índice: (id, nome)}
        
        # Conectar o sinal de seleção alterada
        self.currentIndexChanged.connect(self.handleSelectionChanged)
    
    def addPortalItem(self, text, id_value):
        """Adiciona um portal ao combobox"""
        # Armazenar o ID e nome do portal pelo índice
        index = self.count()
        self.portal_data[index] = (id_value, text)
        
        # Adicionar o item visível
        self.addItem(text)
    
    def handleSelectionChanged(self, index):
        """Manipula a mudança de seleção"""
        if index >= 0 and index in self.portal_data:
            # Obter os dados do portal selecionado
            self.selected_id, self.selected_text = self.portal_data[index]
            
            # Imprimir informações do portal selecionado
            print(f"\n=== Portal Selecionado ===")
            print(f"Nome: '{self.selected_text}'")
            print(f"ID: {self.selected_id}")
            print("========================\n")
    
    def getSelectedId(self):
        """Retorna o ID do portal selecionado como string"""
        if self.selected_id is not None:
            return str(self.selected_id)
        return ""
    
    def getSelectedText(self):
        """Retorna o nome do portal selecionado"""
        return self.selected_text


class SetupMainWindow:
    def __init__(self):
        super().__init__()
       
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

# Modifique a lista add_left_menus adicionando um novo item:

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
        },
        {
            "btn_icon" : "icon_search.svg",
            "btn_id" : "btn_editais",
            "btn_text" : "Lista de Editais",
            "btn_tooltip" : "Visualizar Editais",
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

    def setup_btns(self):
        if self.ui.title_bar.sender() != None:
            return self.ui.title_bar.sender()
        elif self.ui.left_menu.sender() != None:
            return self.ui.left_menu.sender()
        elif self.ui.left_column.sender() != None:
            return self.ui.left_column.sender()

    def setup_gui(self):
        self.setWindowTitle(self.settings["app_name"])
        
        if self.settings["custom_title_bar"]:
            self.setWindowFlag(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

        if self.settings["custom_title_bar"]:
            self.left_grip = PyGrips(self, "left", self.hide_grips)
            self.right_grip = PyGrips(self, "right", self.hide_grips)
            self.top_grip = PyGrips(self, "top", self.hide_grips)
            self.bottom_grip = PyGrips(self, "bottom", self.hide_grips)
            self.top_left_grip = PyGrips(self, "top_left", self.hide_grips)
            self.top_right_grip = PyGrips(self, "top_right", self.hide_grips)
            self.bottom_left_grip = PyGrips(self, "bottom_left", self.hide_grips)
            self.bottom_right_grip = PyGrips(self, "bottom_right", self.hide_grips)


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


        MainFunctions.set_page(self, self.ui.load_pages.page_1)
        
        
        settings = Settings()
        self.settings = settings.items

        themes = Themes()
        self.themes = themes.items


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

        # # CIRCULAR PROGRESS 1
        # self.circular_progress_1 = PyCircularProgress(
        #     value = 80,
        #     progress_color = self.themes["app_color"]["context_color"],
        #     text_color = self.themes["app_color"]["text_title"],
        #     font_size = 14,
        #     bg_color = self.themes["app_color"]["dark_four"]
        # )
        # self.circular_progress_1.setFixedSize(200,200)

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


        # PY LINE EDIT - QUANTIDADE DE EDITAIS 
        self.line_edit_quantidade = PyLineEdit(
            text = "",
            place_holder_text = "Quantidade de editais",
            radius = 8,
            border_size = 2,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["white"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_active = self.themes["app_color"]["dark_three"],
            context_color = self.themes["app_color"]["context_color"],
        )
        quantidade_container = QWidget()
        quantidade_layout = QVBoxLayout(quantidade_container)
        quantidade_layout.setContentsMargins(0, 0, 0, 0)
        
        self.line_edit_quantidade.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.themes["app_color"]["dark_one"]};
                border-radius: 8px;
                border: 2px solid {self.themes["app_color"]["bg_three"]};
                padding: 5px;
                color: {self.themes["app_color"]["text_foreground"]};
            }}
        """)

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
        quantidade_container.setMaximumWidth(250)
        

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

        # Criar o combobox de portais
        self.portais_combo = PortalComboBox()
        self.portais_combo.setMinimumHeight(30)
        self.portais_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {self.themes["app_color"]["dark_one"]};
                border-radius: 8px;
                border: 2px solid {self.themes["app_color"]["bg_three"]};
                padding: 5px;
                color: {self.themes["app_color"]["text_foreground"]};
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: {self.themes["app_color"]["bg_three"]};
                border-left-style: solid;
            }}
            QListView {{
                background-color: {self.themes["app_color"]["dark_one"]};
                color: {self.themes["app_color"]["text_foreground"]};
                border: 1px solid {self.themes["app_color"]["bg_three"]};
                padding: 5px;
            }}
        """)

        # Carregar os portais do arquivo de dados
        try:
            with open('painel_data.json', 'r', encoding='utf-8') as f:
                painel_data = json.load(f)
                portais = painel_data.get("portais", [])
            
            # Primeiro, adicione um item padrão
            self.portais_combo.addItem("Selecione um portal")
            
            # Adicionar portais ao combobox
            for portal in portais:
                nome_portal = portal.get("nomePortal", "")
                id_portal = portal.get("idPortal", "")
                
                if nome_portal and id_portal:
                    self.portais_combo.addPortalItem(nome_portal, id_portal)
                else:
                    # Se não tiver o campo idPortal, usar o índice como ID
                    index = portais.index(portal)
                    self.portais_combo.addPortalItem(nome_portal, index)
                    print(f"Portal sem ID, usando índice {index}: {nome_portal}")
        except Exception as e:
            print(f"Erro ao carregar portais: {str(e)}")
            # Exibir o rastreamento completo do erro para debugging
            import traceback
            traceback.print_exc()

        portais_layout.addWidget(self.portais_combo)
        
        
        self.line_edit_perfil = PyLineEdit(
            text = "",
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
        perfil_container.setMinimumWidth(200)
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

        # Pelo código abaixo:
        perfil_container = QWidget()
        perfil_container.setMinimumWidth(200)
        perfil_layout = QVBoxLayout(perfil_container)
        perfil_layout.setContentsMargins(0, 0, 0, 0)

        self.perfil_label = QLabel("Perfis:")
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

        self.perfil_combo = PerfilComboBox()
        self.perfil_combo.setMinimumHeight(30)
        self.perfil_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {self.themes["app_color"]["dark_one"]};
                border-radius: 8px;
                border: 2px solid {self.themes["app_color"]["bg_three"]};
                padding: 5px;
                color: {self.themes["app_color"]["text_foreground"]};
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: {self.themes["app_color"]["bg_three"]};
                border-left-style: solid;
            }}
            QListView {{
                background-color: {self.themes["app_color"]["dark_one"]};
                color: {self.themes["app_color"]["text_foreground"]};
                border: 1px solid {self.themes["app_color"]["bg_three"]};
                padding: 5px;
            }}
        """)

        # E modifique a parte onde os perfis são carregados:
        try:
            with open('painel_data.json', 'r', encoding='utf-8') as f:
                painel_data = json.load(f)
                perfis = painel_data.get("perfis", [])
            
            # Primeiro, adicione um item padrão
            self.perfil_combo.addItem("Selecione um perfil")
            
            # Adicionar perfis ao combobox
            for perfil in perfis:
                nome_perfil = perfil.get("nomePerfil", "")
                id_perfil = perfil.get("idPerfil", "")
                
                if nome_perfil and id_perfil:
                    self.perfil_combo.addPerfilItem(nome_perfil, id_perfil)
                else:
                    # Se não tiver o campo idPerfil, usar o índice como ID
                    index = perfis.index(perfil)
                    self.perfil_combo.addPerfilItem(nome_perfil, index)
                    print(f"Perfil sem ID, usando índice {index}: {nome_perfil}")
        except Exception as e:
            print(f"Erro ao carregar perfis: {str(e)}")
            # Exibir o rastreamento completo do erro para debugging
            import traceback
            traceback.print_exc()

        perfil_layout.addWidget(self.perfil_combo)

        # Container para data inicial
        data_inicial_container = QWidget()
        data_inicial_container.setMinimumWidth(200)
        data_inicial_layout = QVBoxLayout(data_inicial_container)
        data_inicial_layout.setContentsMargins(0, 0, 0, 0)

        self.data_inicial_label = QLabel("Data Inicial:")
        self.data_inicial_label.setStyleSheet(f"""
            QLabel {{
                color: {self.themes["app_color"]["text_foreground"]};
                font-size: 14px;
                font-weight: bold;
                background-color: transparent;
                margin-bottom: 8px;
            }}
        """)
        data_inicial_layout.addWidget(self.data_inicial_label)

        self.data_inicial_picker = QDateEdit()
        self.data_inicial_picker.setCalendarPopup(True)
        self.data_inicial_picker.setDisplayFormat("dd/MM/yyyy")
        self.data_inicial_picker.setDate(QDate.currentDate())
        self.data_inicial_picker.setMinimumHeight(30)
        # Configurar valor especial para representar "vazio"
        self.data_inicial_picker.setSpecialValueText(" ")  # Texto especial quando a data é mínima
        self.data_inicial_picker.setMinimumDate(QDate(2000, 1, 1))  # Data mínima como indicador de "vazio"
        self.data_inicial_picker.setStyleSheet(f"""
            QDateEdit {{
                background-color: {self.themes["app_color"]["dark_one"]};
                border-radius: 8px;
                border: 2px solid {self.themes["app_color"]["bg_three"]};
                padding: 5px;
                color: {self.themes["app_color"]["text_foreground"]};
            }}
            QDateEdit::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: {self.themes["app_color"]["bg_three"]};
                border-left-style: solid;
            }}
        """)
        data_inicial_layout.addWidget(self.data_inicial_picker)

        # Container para data final
        data_final_container = QWidget()
        data_final_container.setMinimumWidth(200)
        data_final_layout = QVBoxLayout(data_final_container)
        data_final_layout.setContentsMargins(0, 0, 0, 0)

        self.data_final_label = QLabel("Data Final:")
        self.data_final_label.setStyleSheet(f"""
            QLabel {{
                color: {self.themes["app_color"]["text_foreground"]};
                font-size: 14px;
                font-weight: bold;
                background-color: transparent;
                margin-bottom: 8px;
            }}
        """)
        data_final_layout.addWidget(self.data_final_label)

        self.data_final_picker = QDateEdit()
        self.data_final_picker.setCalendarPopup(True)
        self.data_final_picker.setDisplayFormat("dd/MM/yyyy")
        self.data_final_picker.setDate(QDate.currentDate())
        self.data_final_picker.setMinimumHeight(30)
        # Configurar valor especial para representar "vazio"
        self.data_final_picker.setSpecialValueText(" ")  # Texto especial quando a data é mínima
        self.data_final_picker.setMinimumDate(QDate(2000, 1, 1))  # Data mínima como indicador de "vazio"
        self.data_final_picker.setStyleSheet(f"""
            QDateEdit {{
                background-color: {self.themes["app_color"]["dark_one"]};
                border-radius: 8px;
                border: 2px solid {self.themes["app_color"]["bg_three"]};
                padding: 5px;
                color: {self.themes["app_color"]["text_foreground"]};
            }}
            QDateEdit::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: {self.themes["app_color"]["bg_three"]};
                border-left-style: solid;
            }}
        """)
        data_final_layout.addWidget(self.data_final_picker)
        


        self.data_inicial_picker.setContextMenuPolicy(Qt.CustomContextMenu)
        self.data_inicial_picker.customContextMenuRequested.connect(
            lambda pos: MainFunctions.show_date_context_menu(self, self.data_inicial_picker, pos)
        )

        # Configurar menu de contexto para data final
        self.data_final_picker.setContextMenuPolicy(Qt.CustomContextMenu)
        self.data_final_picker.customContextMenuRequested.connect(
            lambda pos: MainFunctions.show_date_context_menu(self, self.data_final_picker, pos)
        )

        
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
        
        # Substitui a parte do código do toggle mode (linhas 663-693)
        self.consumir_planiha_button = PyToggle(
            width = 50,
            bg_color = self.themes["app_color"]["dark_two"],
            circle_color = self.themes["app_color"]["icon_color"],
            active_color = self.themes["app_color"]["dark_four"],
            animation_curve = QEasingCurve.OutBounce,
        )

        # Criar um toggle para favoritos
        self.favoritos_button = PyToggle(
            width = 50,
            bg_color = self.themes["app_color"]["dark_two"],
            circle_color = self.themes["app_color"]["icon_color"],
            active_color = self.themes["app_color"]["dark_four"],
            animation_curve = QEasingCurve.OutBounce,
        )

        # Criar um container principal para os toggles
        toggles_container = QWidget()
        toggles_layout = QHBoxLayout(toggles_container)
        toggles_layout.setContentsMargins(0, 0, 0, 0)
        toggles_layout.setSpacing(0)  # Espaçamento entre os toggles

        # Container para o toggle de planilha de ID
        planilha_id_container = QWidget()
        planilha_id_layout = QVBoxLayout(planilha_id_container)
        planilha_id_layout.setContentsMargins(0, 0, 0, 0)

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
        planilha_id_layout.addWidget(self.toggle_mode_label)

        toggle_mode_input_layout = QHBoxLayout()
        toggle_mode_input_layout.setContentsMargins(0, 0, 0, 0)
        toggle_mode_input_layout.addWidget(self.consumir_planiha_button)
        toggle_mode_input_layout.addStretch()  # Empurra o toggle para a esquerda

        planilha_id_layout.addLayout(toggle_mode_input_layout)

        # Container para o toggle de favoritos
        favoritos_container = QWidget()
        favoritos_layout = QVBoxLayout(favoritos_container)
        favoritos_layout.setContentsMargins(0, 0, 0, 0)

        self.favoritos_label = QLabel("Favoritos:")
        self.favoritos_label.setStyleSheet(f"""
            QLabel {{
                color: {self.themes["app_color"]["text_foreground"]};
                font-size: 14px;
                font-weight: bold;
                background-color: transparent;
                margin-bottom: 8px;
            }}
        """)
        favoritos_layout.addWidget(self.favoritos_label)

        favoritos_input_layout = QHBoxLayout()
        favoritos_input_layout.setContentsMargins(0, 0, 0, 0)
        favoritos_input_layout.addWidget(self.favoritos_button)
        favoritos_input_layout.addStretch()  # Empurra o toggle para a esquerda

        favoritos_layout.addLayout(favoritos_input_layout)

        # Adicionar ambos os containers ao layout horizontal
        toggles_layout.addWidget(planilha_id_container)
        toggles_layout.addWidget(favoritos_container)
        toggles_layout.addStretch()  # Isso empurra todos os toggles para a esquerda

        
        
        # Após adicionar os widgets
        self.ui.load_pages.row_1_layout.addWidget(quantidade_container)
        self.ui.load_pages.row_1_layout.addWidget(portais_container)
        self.ui.load_pages.row_1_layout.addWidget(perfil_container)
        self.ui.load_pages.row_1_layout.addWidget(data_inicial_container)
        self.ui.load_pages.row_1_layout.addWidget(data_final_container)
        self.ui.load_pages.row_2_layout.addWidget(toggles_container)
        self.ui.load_pages.row_3_layout.addWidget(self.push_button_importar_editais)
        self.ui.load_pages.row_4_layout.addWidget(self.line_edit_status_import)
        
        # self.ui.load_pages.row_4_layout.addWidget(self.label_title_portal_code)
        # self.ui.load_pages.row_4_layout.addWidget(self.label_description_portal_code)
        
        # self.ui.load_pages.row_4_layout.addWidget(self.label_title_perfil_code)
        # self.ui.load_pages.row_4_layout.addWidget(self.label_description_perfil_code)


        # CONFIGURAÇÕES ---------

        # Definir estilo para os títulos de seção
        section_style = f"""
            color: {self.themes["app_color"]["text_title"]};
            font-size: 16px;
            font-weight: bold;
            background-color: transparent;
            padding: 5px;
            border-bottom: 2px solid {self.themes["app_color"]["context_color"]};
            margin-top: 15px;
            margin-bottom: 10px;
        """

        # Estilo para labels
        label_style = f"""
            color: {self.themes["app_color"]["text_title"]};
            font-size: 14px;
            font-weight: bold;
            background-color: transparent;
            margin-bottom: 8px;
        """

        # Limpar os layouts existentes na página de configurações
        for layout in [
            self.ui.load_pages.row_1_layout_3,
            self.ui.load_pages.row_2_layout_3,
            self.ui.load_pages.row_3_layout_3,
            self.ui.load_pages.row_4_layout_3,
            self.ui.load_pages.row_5_layout_3
        ]:
            while layout.count():
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

        # Criar um container principal para todas as seções
        main_settings_container = QWidget()
        main_settings_layout = QVBoxLayout(main_settings_container)
        main_settings_layout.setContentsMargins(0, 0, 0, 0)
        main_settings_layout.setSpacing(15)

        # ===== SEÇÃO 1: DIRETÓRIO DE SAÍDA =====
        directory_section = QWidget()
        directory_layout = QVBoxLayout(directory_section)
        directory_layout.setContentsMargins(0, 0, 0, 0)

        # Título da seção
        directory_title = QLabel("DIRETÓRIO DE SAÍDA")
        directory_title.setStyleSheet(section_style)
        directory_layout.addWidget(directory_title)

        # Container do diretório de saída
        settings_save_path_container = QWidget()
        settings_save_path_layout = QVBoxLayout(settings_save_path_container)
        settings_save_path_layout.setContentsMargins(0, 0, 0, 0)

        self.save_path_label = QLabel("Selecione o diretório onde os editais serão salvos:")
        self.save_path_label.setStyleSheet(label_style)
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

        directory_layout.addWidget(settings_save_path_container)
        main_settings_layout.addWidget(directory_section)

        # ===== SEÇÃO 2: ARQUIVOS DE IMPORTAÇÃO =====
        import_files_section = QWidget()
        import_files_layout = QVBoxLayout(import_files_section)
        import_files_layout.setContentsMargins(0, 0, 0, 0)

        # Título da seção
        import_files_title = QLabel("ARQUIVO DE IMPORTAÇÃO")
        import_files_title.setStyleSheet(section_style)
        import_files_layout.addWidget(import_files_title)

        # Container para planilha de ID
        settings_id_sheet_container = QWidget() 
        settings_id_sheet_layout = QVBoxLayout(settings_id_sheet_container)
        settings_id_sheet_layout.setContentsMargins(0, 0, 0, 0)

        self.id_sheet_label = QLabel("Selecione a planilha de IDs:")
        self.id_sheet_label.setStyleSheet(label_style)
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

        import_files_layout.addWidget(settings_id_sheet_container)
        main_settings_layout.addWidget(import_files_section)

        # ===== SEÇÃO 3: DOCUMENTOS DE PROCESSO =====
        docs_section = QWidget()
        docs_layout = QVBoxLayout(docs_section)
        docs_layout.setContentsMargins(0, 0, 0, 0)

        # Título da seção
        docs_title = QLabel("DOCUMENTOS DE PROCESSO")
        docs_title.setStyleSheet(section_style)
        docs_layout.addWidget(docs_title)

        # Container para arquivo de documento
        settings_doc_container = QWidget()
        settings_doc_layout = QVBoxLayout(settings_doc_container)
        settings_doc_layout.setContentsMargins(0, 0, 0, 10)  # Adicionar margem inferior

        self.doc_label = QLabel("Selecione o arquivo de documento:")
        self.doc_label.setStyleSheet(label_style)
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
        docs_layout.addWidget(settings_doc_container)

        # Container para planilha de proposta
        settings_proposal_container = QWidget()
        settings_proposal_layout = QVBoxLayout(settings_proposal_container)
        settings_proposal_layout.setContentsMargins(0, 0, 0, 10)  # Adicionar margem inferior

        self.proposal_label = QLabel("Selecione a planilha de proposta:")
        self.proposal_label.setStyleSheet(label_style)
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
        docs_layout.addWidget(settings_proposal_container)

        # Container para documento de declaração
        settings_declaration_container = QWidget()
        settings_declaration_layout = QVBoxLayout(settings_declaration_container)
        settings_declaration_layout.setContentsMargins(0, 0, 0, 0)

        self.declaration_label = QLabel("Selecione o documento de declaração:")
        self.declaration_label.setStyleSheet(label_style)
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
        docs_layout.addWidget(settings_declaration_container)
        
        # ---- COTAÇÃO
        
        settings_cotacao_container = QWidget()
        settings_cotacao_layout = QVBoxLayout(settings_cotacao_container)
        settings_cotacao_layout.setContentsMargins(0, 0, 0, 0)

        self.cotacao_label = QLabel("Selecione o documento proposta de cotação:")
        self.cotacao_label.setStyleSheet(label_style)
        settings_cotacao_layout.addWidget(self.cotacao_label)

        cotacao_input_layout = QHBoxLayout()
        cotacao_input_layout.setContentsMargins(0, 0, 0, 0)

        self.cotacao_line_edit = PyLineEdit(
            text = "",
            place_holder_text = "Arquivo de cotação",
            radius = 8,
            border_size = 2,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["white"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_active = self.themes["app_color"]["dark_three"],
            context_color = self.themes["app_color"]["context_color"]
        )
        self.cotacao_line_edit.setMinimumHeight(30)

        self.cotacao_button = PyPushButton(
            text = "Escolher",
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_hover = self.themes["app_color"]["dark_three"],
            bg_color_pressed = self.themes["app_color"]["dark_four"]
        )
        self.cotacao_button.setMinimumHeight(30)
        self.cotacao_button.setMinimumWidth(200)
        self.cotacao_button.clicked.connect(lambda: MainFunctions.select_archive_path(self, "Selecione o arquivo de proposta de cotação", self.cotacao_line_edit))

        cotacao_input_layout.addWidget(self.cotacao_line_edit)
        cotacao_input_layout.addWidget(self.cotacao_button)
        settings_cotacao_layout.addLayout(cotacao_input_layout)
        docs_layout.addWidget(settings_cotacao_container)

        main_settings_layout.addWidget(docs_section)
        
        # Adicione este código após a seção de documentos e antes da seção de ações:

        # ===== SEÇÃO 4: ASSINATURA =====
        signature_section = QWidget()
        signature_layout = QVBoxLayout(signature_section)
        signature_layout.setContentsMargins(0, 0, 0, 0)

        # Título da seção
        signature_title = QLabel("ASSINATURA")
        signature_title.setStyleSheet(section_style)
        signature_layout.addWidget(signature_title)

        # Container para certificado digital
        settings_certificate_container = QWidget()
        settings_certificate_layout = QVBoxLayout(settings_certificate_container)
        settings_certificate_layout.setContentsMargins(0, 0, 0, 0)

        self.certificate_label = QLabel("Selecione o arquivo do certificado digital:")
        self.certificate_label.setStyleSheet(label_style)
        settings_certificate_layout.addWidget(self.certificate_label)

        certificate_input_layout = QHBoxLayout()
        certificate_input_layout.setContentsMargins(0, 0, 0, 0)

        self.certificate_line_edit = PyLineEdit(
            text = "",
            place_holder_text = "Arquivo de certificado digital",
            radius = 8,
            border_size = 2,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["white"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_active = self.themes["app_color"]["dark_three"],
            context_color = self.themes["app_color"]["context_color"]
        )
        self.certificate_line_edit.setMinimumHeight(30)

        self.certificate_button = PyPushButton(
            text = "Escolher",
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_hover = self.themes["app_color"]["dark_three"],
            bg_color_pressed = self.themes["app_color"]["dark_four"]
        )
        self.certificate_button.setMinimumHeight(30)
        self.certificate_button.setMinimumWidth(200)
        self.certificate_button.clicked.connect(lambda: MainFunctions.select_archive_path(self, "Selecione o arquivo de certificado digital", self.certificate_line_edit))

        certificate_input_layout.addWidget(self.certificate_line_edit)
        certificate_input_layout.addWidget(self.certificate_button)
        settings_certificate_layout.addLayout(certificate_input_layout)

        # Campo para senha do certificado
        self.certificate_password_label = QLabel("Senha do certificado digital:")
        self.certificate_password_label.setStyleSheet(label_style)
        settings_certificate_layout.addWidget(self.certificate_password_label)

        self.certificate_password_edit = PyLineEdit(
            text = "",
            place_holder_text = "Senha do certificado",
            radius = 8,
            border_size = 2,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["white"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_active = self.themes["app_color"]["dark_three"],
            context_color = self.themes["app_color"]["context_color"]
        )
        self.certificate_password_edit.setMinimumHeight(30)
        # self.certificate_password_edit.setEchoMode(QLineEdit.Password)  # Ocultar o texto da senha
        settings_certificate_layout.addWidget(self.certificate_password_edit)

        signature_layout.addWidget(settings_certificate_container)
        main_settings_layout.addWidget(signature_section)

        # Agora continua com a seção de ações...

        # ===== SEÇÃO 5: AÇÕES =====
        actions_section = QWidget()
        actions_layout = QVBoxLayout(actions_section)
        actions_layout.setContentsMargins(0, 0, 0, 0)

        # Título da seção
        actions_title = QLabel("AÇÕES")
        actions_title.setStyleSheet(section_style)
        actions_layout.addWidget(actions_title)

        # Botão de salvar configurações
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
        self.save_settings_button.setMinimumHeight(40)
        self.save_settings_button.setMaximumWidth(200)
        self.save_settings_button.clicked.connect(lambda: MainFunctions.save_settings(self))

        # Layout para centralizar o botão
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_settings_button)
        button_layout.addStretch()
        actions_layout.addLayout(button_layout)

        main_settings_layout.addWidget(actions_section)

        # ===== SEÇÃO 6: STATUS =====
        status_section = QWidget()
        status_layout = QVBoxLayout(status_section)
        status_layout.setContentsMargins(0, 0, 0, 0)

        # Título da seção
        status_title = QLabel("STATUS")
        status_title.setStyleSheet(section_style)
        status_layout.addWidget(status_title)

        # Campo de status
        self.line_edit_status_settings = QTextEdit()
        self.line_edit_status_settings.setStyleSheet(f"""
            QTextEdit {{
                background-color: {self.themes["app_color"]["dark_one"]};
                border-radius: 8px;
                padding: 5px;
                color: white;
                font-size: 12px;
            }}
        """)
        self.line_edit_status_settings.setMinimumHeight(100)
        self.line_edit_status_settings.setReadOnly(True)
        status_layout.addWidget(self.line_edit_status_settings)

        main_settings_layout.addWidget(status_section)

        # Adicionar um spacer para empurrar tudo para cima
        main_settings_layout.addStretch()

        # Configurar o scroll_area_3 para ter rolagem adequada
        self.ui.load_pages.scroll_area_3.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.ui.load_pages.scroll_area_3.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.load_pages.scroll_area_3.setWidgetResizable(True)
        self.ui.load_pages.scroll_area_3.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            QScrollBar:vertical {{
                width: 10px;
                background: transparent;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background: {self.themes["app_color"]["text_foreground"]};
                border-radius: 5px;
                min-height: 20px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)

        # Adicionar o container principal ao layout da página de configurações
        self.ui.load_pages.row_1_layout_3.addWidget(main_settings_container)
        
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
        
        cotacao_container = QWidget()
        cotacao_layout = QVBoxLayout(cotacao_container)  # Mudado para QVBoxLayout
        cotacao_layout.setContentsMargins(0, 0, 0, 0)
        self.cotacao_checkbox = QCheckBox("Preencher cotação")
        self.cotacao_checkbox.setChecked(False)
        cotacao_layout.addWidget(self.cotacao_checkbox)
        
        assign_pdf_container = QWidget()
        assign_pdf_layout = QVBoxLayout(assign_pdf_container)  # Mudado para QVBoxLayout
        assign_pdf_layout.setContentsMargins(0, 0, 0, 0)
        self.assign_pdf_checkbox = QCheckBox("Assinar PDF")
        self.assign_pdf_checkbox.setChecked(True)
        assign_pdf_layout.addWidget(self.assign_pdf_checkbox)

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
        main_layout.addWidget(self.cotacao_checkbox)
        main_layout.addWidget(self.assign_pdf_checkbox)

        # Adicionar o container principal ao layout da página
        self.ui.load_pages.row_1_layout_4.addWidget(main_container)
        self.ui.load_pages.row_1_layout_4.addWidget(self.line_edit_status_automation)
        self.ui.load_pages.row_2_layout_4.addWidget(self.start_automation_button)
        
        # === PÁGINA DE LISTA DE EDITAIS ===
        # Criando a tabela para a página 5
        self.editais_table = PyTableWidget(
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["context_color"],
            bg_color = self.themes["app_color"]["bg_two"],
            header_horizontal_color = self.themes["app_color"]["dark_two"],
            header_vertical_color = self.themes["app_color"]["bg_three"],
            bottom_line_color = self.themes["app_color"]["bg_three"],
            grid_line_color = self.themes["app_color"]["bg_one"],
            scroll_bar_bg_color = self.themes["app_color"]["bg_one"],
            scroll_bar_btn_color = self.themes["app_color"]["dark_four"],
            context_color = self.themes["app_color"]["context_color"]
        )

        # Configurar colunas da tabela
        columns = ["ID", "UASG", "Portal", "Data Final", "Perfil", "UF", "Situação"]
        self.editais_table.setColumnCount(len(columns))
        self.editais_table.setHorizontalHeaderLabels(columns)
        self.editais_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # Coluna "Objeto" expande

        # Adicionar a tabela ao layout
        self.ui.load_pages.table_layout_5.addWidget(self.editais_table)

        # Campo de filtro/pesquisa
        self.search_editais = PyLineEdit(
            text = "",
            place_holder_text = "Pesquisar editais...",
            radius = 8,
            border_size = 2,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["white"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_active = self.themes["app_color"]["dark_three"],
            context_color = self.themes["app_color"]["context_color"]
        )
        self.search_editais.setMinimumHeight(36)
        self.search_editais.textChanged.connect(self.filter_editais_table)

        # Botões de ação
        self.refresh_editais_btn = PyPushButton(
            text=" Atualizar",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.refresh_editais_btn.setIcon(QIcon(Functions.set_svg_icon("icon_send.svg")))
        self.refresh_editais_btn.setMinimumHeight(36)
        self.refresh_editais_btn.clicked.connect(self.populate_editais_table)

        # Layout para os controles de filtro e botões
        filter_widget = QWidget()
        filter_layout = QHBoxLayout(filter_widget)
        filter_layout.setContentsMargins(0, 0, 0, 0)
        filter_layout.addWidget(self.search_editais, 3)
        filter_layout.addWidget(self.refresh_editais_btn, 1)

        self.ui.load_pages.filters_layout_5.addWidget(filter_widget)

        # Carregar dados na inicialização
        self.populate_editais_table()
        
        self.editais_table.cellDoubleClicked.connect(self.show_edital_details)

        # Configurar o botão voltar na página de detalhes
        self.ui.load_pages.back_button_6.clicked.connect(self.back_to_editais_list)

        # Adicionar ícone ao botão voltar
        back_icon = QIcon(Functions.set_svg_icon("icon_arrow_left.svg"))
        self.ui.load_pages.back_button_6.setIcon(back_icon)
        

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