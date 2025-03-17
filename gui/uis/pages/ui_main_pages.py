# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *


class Ui_MainPages(object):
    def setupUi(self, MainPages):
        if not MainPages.objectName():
            MainPages.setObjectName(u"MainPages")
        MainPages.resize(860, 600)
        self.main_pages_layout = QVBoxLayout(MainPages)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setObjectName(u"main_pages_layout")
        self.main_pages_layout.setContentsMargins(5, 5, 5, 5)
        self.pages = QStackedWidget(MainPages)
        self.pages.setObjectName(u"pages")
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        self.page_1.setStyleSheet(u"font-size: 14pt")
        self.page_1_layout = QVBoxLayout(self.page_1)
        self.page_1_layout.setSpacing(5)
        self.page_1_layout.setObjectName(u"page_1_layout")
        self.page_1_layout.setContentsMargins(5, 5, 5, 5)
        self.welcome_base = QFrame(self.page_1)
        self.welcome_base.setObjectName(u"welcome_base")
        self.welcome_base.setMinimumSize(QSize(300, 150))
        self.welcome_base.setMaximumSize(QSize(300, 150))
        self.welcome_base.setFrameShape(QFrame.NoFrame)
        self.welcome_base.setFrameShadow(QFrame.Raised)
        self.center_page_layout = QVBoxLayout(self.welcome_base)
        self.center_page_layout.setSpacing(10)
        self.center_page_layout.setObjectName(u"center_page_layout")
        self.center_page_layout.setContentsMargins(0, 0, 0, 0)
        self.logo = QFrame(self.welcome_base)
        self.logo.setObjectName(u"logo")
        self.logo.setMinimumSize(QSize(300, 120))
        self.logo.setMaximumSize(QSize(300, 120))
        self.logo.setFrameShape(QFrame.NoFrame)
        self.logo.setFrameShadow(QFrame.Raised)
        self.logo_layout = QVBoxLayout(self.logo)
        self.logo_layout.setSpacing(0)
        self.logo_layout.setObjectName(u"logo_layout")
        self.logo_layout.setContentsMargins(0, 0, 0, 0)

        self.center_page_layout.addWidget(self.logo)

        self.label = QLabel(self.welcome_base)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.center_page_layout.addWidget(self.label)


        self.page_1_layout.addWidget(self.welcome_base, 0, Qt.AlignHCenter)

        self.pages.addWidget(self.page_1)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2_layout = QVBoxLayout(self.page_2)
        self.page_2_layout.setSpacing(5)
        self.page_2_layout.setObjectName(u"page_2_layout")
        self.page_2_layout.setContentsMargins(5, 5, 5, 5)
        self.scroll_area = QScrollArea(self.page_2)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setStyleSheet(u"background: transparent;")
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.contents = QWidget()
        self.contents.setObjectName(u"contents")
        self.contents.setGeometry(QRect(0, 0, 840, 580))
        self.contents.setStyleSheet(u"background: transparent;")
        self.verticalLayout = QVBoxLayout(self.contents)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.title_label = QLabel(self.contents)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setMaximumSize(QSize(16777215, 40))
        font = QFont()
        font.setPointSize(16)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet(u"font-size: 16pt; font-weight: bold;")
        self.verticalLayout.addWidget(self.title_label)

        self.description_label = QLabel(self.contents)
        self.description_label.setObjectName(u"description_label")
        self.description_label.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.description_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.description_label)

        self.row_1_layout = QHBoxLayout()
        self.row_1_layout.setObjectName(u"row_1_layout")

        self.verticalLayout.addLayout(self.row_1_layout)

        self.row_2_layout = QHBoxLayout()
        self.row_2_layout.setObjectName(u"row_2_layout")

        self.verticalLayout.addLayout(self.row_2_layout)

        self.row_3_layout = QHBoxLayout()
        self.row_3_layout.setObjectName(u"row_3_layout")

        self.verticalLayout.addLayout(self.row_3_layout)

        self.row_4_layout = QVBoxLayout()
        self.row_4_layout.setObjectName(u"row_4_layout")

        self.verticalLayout.addLayout(self.row_4_layout)

        self.row_5_layout = QVBoxLayout()
        self.row_5_layout.setObjectName(u"row_5_layout")

        self.verticalLayout.addLayout(self.row_5_layout)

        self.scroll_area.setWidget(self.contents)

        self.page_2_layout.addWidget(self.scroll_area)

        self.pages.addWidget(self.page_2)
        
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.page_3_layout = QVBoxLayout(self.page_3)
        self.page_3_layout.setSpacing(5)
        self.page_3_layout.setObjectName(u"page_3_layout")
        self.page_3_layout.setContentsMargins(5, 5, 5, 5)

        self.scroll_area_3 = QScrollArea(self.page_3)
        self.scroll_area_3.setObjectName(u"scroll_area_3")
        self.scroll_area_3.setStyleSheet(u"background: transparent;")
        self.scroll_area_3.setFrameShape(QFrame.NoFrame)
        self.scroll_area_3.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area_3.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area_3.setWidgetResizable(True)

        self.contents_3 = QWidget()
        self.contents_3.setObjectName(u"contents_3")
        self.contents_3.setGeometry(QRect(0, 0, 840, 580))
        self.contents_3.setStyleSheet(u"background: transparent;")

        self.verticalLayout_3 = QVBoxLayout(self.contents_3)
        self.verticalLayout_3.setSpacing(15)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)

        self.title_label_3 = QLabel(self.contents_3)
        self.title_label_3.setObjectName(u"title_label_3")
        self.title_label_3.setMaximumSize(QSize(16777215, 40))
        self.title_label_3.setFont(font)
        self.title_label_3.setStyleSheet(u"font-size: 18pt; font-weight: bold;")
        self.verticalLayout_3.addWidget(self.title_label_3)

        self.description_label_3 = QLabel(self.contents_3)
        self.description_label_3.setObjectName(u"description_label_3")
        self.description_label_3.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.description_label_3.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.description_label_3)

        self.row_1_layout_3 = QHBoxLayout()
        self.row_1_layout_3.setObjectName(u"row_1_layout_3")
        self.verticalLayout_3.addLayout(self.row_1_layout_3)

        self.row_2_layout_3 = QHBoxLayout()
        self.row_2_layout_3.setObjectName(u"row_2_layout_3")
        self.verticalLayout_3.addLayout(self.row_2_layout_3)

        self.row_3_layout_3 = QHBoxLayout()
        self.row_3_layout_3.setObjectName(u"row_3_layout_3")
        self.verticalLayout_3.addLayout(self.row_3_layout_3)

        self.row_4_layout_3 = QHBoxLayout()
        self.row_4_layout_3.setObjectName(u"row_4_layout_3")
        self.verticalLayout_3.addLayout(self.row_4_layout_3)
        
        self.row_5_layout_3 = QHBoxLayout()
        self.row_5_layout_3.setObjectName(u"row_5_layout_3")
        self.verticalLayout_3.addLayout(self.row_5_layout_3)

        self.scroll_area_3.setWidget(self.contents_3)
        self.page_3_layout.addWidget(self.scroll_area_3)

        self.pages.addWidget(self.page_3)
        
                # PAGE 4
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.page_4_layout = QVBoxLayout(self.page_4)
        self.page_4_layout.setSpacing(5)
        self.page_4_layout.setObjectName(u"page_4_layout")
        self.page_4_layout.setContentsMargins(5, 5, 5, 5)

        self.scroll_area_4 = QScrollArea(self.page_4)
        self.scroll_area_4.setObjectName(u"scroll_area_4")
        self.scroll_area_4.setStyleSheet(u"background: transparent;")
        self.scroll_area_4.setFrameShape(QFrame.NoFrame)
        self.scroll_area_4.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area_4.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area_4.setWidgetResizable(True)

        self.contents_4 = QWidget()
        self.contents_4.setObjectName(u"contents_4")
        self.contents_4.setGeometry(QRect(0, 0, 840, 580))
        self.contents_4.setStyleSheet(u"background: transparent;")

        self.verticalLayout_4 = QVBoxLayout(self.contents_4)
        self.verticalLayout_4.setSpacing(15)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(5, 5, 5, 5)

        self.title_label_4 = QLabel(self.contents_4)
        self.title_label_4.setObjectName(u"title_label_4")
        self.title_label_4.setMaximumSize(QSize(16777215, 40))
        self.title_label_4.setFont(font)
        self.title_label_4.setStyleSheet(u"font-size: 18pt; font-weight: bold;")
        self.verticalLayout_4.addWidget(self.title_label_4)

        self.description_label_4 = QLabel(self.contents_4)
        self.description_label_4.setObjectName(u"description_label_4")
        self.description_label_4.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.description_label_4.setWordWrap(True)
        self.verticalLayout_4.addWidget(self.description_label_4)

        # Create layout rows
        self.row_1_layout_4 = QHBoxLayout()
        self.row_1_layout_4.setObjectName(u"row_1_layout_4")
        self.verticalLayout_4.addLayout(self.row_1_layout_4)

        self.row_2_layout_4 = QHBoxLayout()
        self.row_2_layout_4.setObjectName(u"row_2_layout_4")
        self.verticalLayout_4.addLayout(self.row_2_layout_4)

        self.row_3_layout_4 = QHBoxLayout()
        self.row_3_layout_4.setObjectName(u"row_3_layout_4")
        self.verticalLayout_4.addLayout(self.row_3_layout_4)

        self.row_4_layout_4 = QHBoxLayout()
        self.row_4_layout_4.setObjectName(u"row_4_layout_4")
        self.verticalLayout_4.addLayout(self.row_4_layout_4)
        
        self.row_5_layout_4 = QHBoxLayout()
        self.row_5_layout_4.setObjectName(u"row_5_layout_4")
        self.verticalLayout_4.addLayout(self.row_5_layout_4)

        # Set scroll area widget and add to page layout
        self.scroll_area_4.setWidget(self.contents_4)
        self.page_4_layout.addWidget(self.scroll_area_4)

        # Add page 4 to stacked widget
        self.pages.addWidget(self.page_4)
        
        # Adicione após a página 4, antes do trecho que adiciona o widget "pages" ao layout principal:

        # PAGE 5 - LISTA DE EDITAIS
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.page_5_layout = QVBoxLayout(self.page_5)
        self.page_5_layout.setSpacing(5)
        self.page_5_layout.setObjectName(u"page_5_layout")
        self.page_5_layout.setContentsMargins(5, 5, 5, 5)

        self.scroll_area_5 = QScrollArea(self.page_5)
        self.scroll_area_5.setObjectName(u"scroll_area_5")
        self.scroll_area_5.setStyleSheet(u"background: transparent;")
        self.scroll_area_5.setFrameShape(QFrame.NoFrame)
        self.scroll_area_5.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area_5.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area_5.setWidgetResizable(True)

        self.contents_5 = QWidget()
        self.contents_5.setObjectName(u"contents_5")
        self.contents_5.setGeometry(QRect(0, 0, 840, 580))
        self.contents_5.setStyleSheet(u"background: transparent;")

        self.verticalLayout_5 = QVBoxLayout(self.contents_5)
        self.verticalLayout_5.setSpacing(15)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(5, 5, 5, 5)

        self.title_label_5 = QLabel(self.contents_5)
        self.title_label_5.setObjectName(u"title_label_5")
        self.title_label_5.setMaximumSize(QSize(16777215, 40))
        self.title_label_5.setFont(font)
        self.title_label_5.setStyleSheet(u"font-size: 18pt; font-weight: bold;")
        self.verticalLayout_5.addWidget(self.title_label_5)

        self.description_label_5 = QLabel(self.contents_5)
        self.description_label_5.setObjectName(u"description_label_5")
        self.description_label_5.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.description_label_5.setWordWrap(True)
        self.verticalLayout_5.addWidget(self.description_label_5)

        # Layout para os filtros
        self.filters_layout_5 = QHBoxLayout()
        self.filters_layout_5.setObjectName(u"filters_layout_5")
        self.verticalLayout_5.addLayout(self.filters_layout_5)

        # Layout para a tabela
        self.table_layout_5 = QVBoxLayout()
        self.table_layout_5.setObjectName(u"table_layout_5")
        self.verticalLayout_5.addLayout(self.table_layout_5)

        # Set scroll area widget and add to page layout
        self.scroll_area_5.setWidget(self.contents_5)
        self.page_5_layout.addWidget(self.scroll_area_5)

        # Add page 5 to stacked widget
        self.pages.addWidget(self.page_5)
        
        # Adicione após o código da página 5 (antes do main_pages_layout.addWidget(self.pages)):

        # PAGE 6 - DETALHES DO EDITAL
        self.page_6 = QWidget()
        self.page_6.setObjectName(u"page_6")
        self.page_6_layout = QVBoxLayout(self.page_6)
        self.page_6_layout.setSpacing(5)
        self.page_6_layout.setObjectName(u"page_6_layout")
        self.page_6_layout.setContentsMargins(5, 5, 5, 5)

        self.scroll_area_6 = QScrollArea(self.page_6)
        self.scroll_area_6.setObjectName(u"scroll_area_6")
        self.scroll_area_6.setStyleSheet(u"background: transparent;")
        self.scroll_area_6.setFrameShape(QFrame.NoFrame)
        self.scroll_area_6.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area_6.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area_6.setWidgetResizable(True)

        self.contents_6 = QWidget()
        self.contents_6.setObjectName(u"contents_6")
        self.contents_6.setGeometry(QRect(0, 0, 840, 580))
        self.contents_6.setStyleSheet(u"background: transparent;")

        self.verticalLayout_6 = QVBoxLayout(self.contents_6)
        self.verticalLayout_6.setSpacing(15)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(5, 5, 5, 5)

        # Header da página com botão de voltar
        self.header_layout_6 = QHBoxLayout()
        self.header_layout_6.setObjectName(u"header_layout_6")

        self.back_button_6 = QPushButton()
        self.back_button_6.setObjectName(u"back_button_6")
        self.back_button_6.setMinimumSize(QSize(40, 40))
        self.back_button_6.setMaximumSize(QSize(40, 40))
        self.back_button_6.setCursor(QCursor(Qt.PointingHandCursor))
        self.back_button_6.setStyleSheet(u"background-color: transparent;")

        self.title_label_6 = QLabel(self.contents_6)
        self.title_label_6.setObjectName(u"title_label_6")
        self.title_label_6.setMaximumSize(QSize(16777215, 40))
        self.title_label_6.setFont(font)
        self.title_label_6.setStyleSheet(u"font-size: 18pt; font-weight: bold;")

        self.header_layout_6.addWidget(self.back_button_6)
        self.header_layout_6.addWidget(self.title_label_6)
        self.header_layout_6.addStretch()

        self.verticalLayout_6.addLayout(self.header_layout_6)

        # Conteúdo dos detalhes do edital
        self.edital_details_layout = QVBoxLayout()
        self.edital_details_layout.setObjectName(u"edital_details_layout")
        self.verticalLayout_6.addLayout(self.edital_details_layout)

        # Set scroll area widget and add to page layout
        self.scroll_area_6.setWidget(self.contents_6)
        self.page_6_layout.addWidget(self.scroll_area_6)

        # Add page 6 to stacked widget
        self.pages.addWidget(self.page_6)
        
        
        

        self.main_pages_layout.addWidget(self.pages)


        self.retranslateUi(MainPages)

        self.pages.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainPages)
    # setupUi

    def retranslateUi(self, MainPages):
        MainPages.setWindowTitle(QCoreApplication.translate("MainPages", u"Form", None))
        self.label.setText(QCoreApplication.translate("MainPages", u"Bem vindo(a) ao Sistema Resolvi", None))
        self.title_label.setText(QCoreApplication.translate("MainPages", u"Importar editais", None))
        self.title_label_3.setText(QCoreApplication.translate("MainPages", u"Configurações", None))
        self.title_label_4.setText(QCoreApplication.translate("MainPages", u"Robô Montador", None))
        # No método retranslateUi(), adicione:
        self.title_label_5.setText(QCoreApplication.translate("MainPages", u"Lista de Editais", None))
        self.description_label_5.setText(QCoreApplication.translate("MainPages", u"Visualize todos os editais importados", None))
        # Adicione ao método retranslateUi:
        self.title_label_6.setText(QCoreApplication.translate("MainPages", u"Detalhes do Edital", None))
        self.back_button_6.setText(QCoreApplication.translate("MainPages", u"←", None))
    # retranslateUi

