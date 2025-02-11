
# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
import sys

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# LOAD UI MAIN
# ///////////////////////////////////////////////////////////////
from . ui_main import *

import requests
import json

from . worker import RequestWorker

from . workerAutomation import RequestWorkerAutomation

# FUNCTIONS
class MainFunctions():
    def __init__(self):
        super().__init__()
        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

    # SET MAIN WINDOW PAGES
    # ///////////////////////////////////////////////////////////////
    def set_page(self, page):
        self.ui.load_pages.pages.setCurrentWidget(page)
        
    def write_status_import(self, status):
        self.line_edit_status_import.setText(status)
        
    def write_status_settings(self, status):
        self.line_edit_status_settings.setText(status)
        
    def write_status_automation(self, status):
        current_text = self.line_edit_status_automation.toPlainText()
        new_text = f"{current_text}\n{status}" if current_text else status
        self.line_edit_status_automation.setPlainText(new_text)
        # Rola automaticamente para o final do texto
        self.line_edit_status_automation.verticalScrollBar().setValue(
            self.line_edit_status_automation.verticalScrollBar().maximum()
    )
        
    def select_save_path(self, text, element):
        directory = QFileDialog.getExistingDirectory(
        self,
        text,
        "", 
        QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        
        if directory:
            element.setText(directory)
        else:
            MainFunctions.write_status_settings(self, "Nenhuma pasta para salvar selecionado")
    
    def select_archive_path(self, text, element):
        archive = QFileDialog.getOpenFileName(
        self,
        text,
        "", 
        )
        
        if archive:
            element.setText(archive[0])
        else:
            MainFunctions.write_status_settings(self, "Nenhum arquivo selecionado")
    
    def save_settings(self):
        try:
            save_path = self.save_path_line_edit.text()
            sheet_ids = self.id_sheet_line_edit.text()
            document_archive = self.doc_line_edit.text()
            sheet_propouse = self.proposal_line_edit.text()
            declaration_document = self.declaration_line_edit.text()
            
            settings_data = {
                'save_path': save_path,
                'sheet_ids': sheet_ids,
                'document_archive': document_archive,
                'sheet_propouse': sheet_propouse,
                'declaration_document': declaration_document
            }
            
            with open('user_settings.json', 'w', encoding='utf-8') as settings_file:
                json.dump(settings_data, settings_file)
                
            MainFunctions.write_status_settings(self, "Configurações salvas com sucesso!")
        except Exception as e:
            MainFunctions.write_status_settings(self, f"Erro ao salvar configurações: {str(e)}")
            
    def user_settings(self):
        try: 
            
            with open('user_settings.json', 'r', encoding='utf-8') as settings_file:
                settings_data = json.load(settings_file)

            
            
            self.save_path = settings_data.get('save_path', '')
            self.sheet_ids = settings_data.get('sheet_ids', '')
            self.document_archive = settings_data.get('document_archive', '')
            self.sheet_propouse = settings_data.get('sheet_propouse', '')
            self.declaration_document = settings_data.get('declaration_document', '')
   
            
            
            self.save_path_line_edit.setText(self.save_path)
            self.id_sheet_line_edit.setText(self.sheet_ids)
            self.doc_line_edit.setText(self.document_archive)
            self.proposal_line_edit.setText(self.sheet_propouse)
            self.declaration_line_edit.setText(self.declaration_document)
        except Exception as e:
            MainFunctions.write_status_import(self, "Erro ao carregar configurações")
            print('Erro ao carregar configurações: ', str(e))
        
    def save_config_data(self):
        
        try:
            # Desabilita o botão
            self.push_button_importar_editais.setEnabled(False)
            
            quantidade = self.line_edit_quantidade.text()
            perfil = self.line_edit_perfil.text()
            portais = self.line_edit_portais.text()
            consumir_planilha = self.consumir_planiha_button.isChecked()
                        

            # Cria e configura o worker
            self.worker = RequestWorker(quantidade, perfil, portais, consumir_planilha)
            self.worker.progress.connect(lambda msg: MainFunctions.write_status_import(self,msg))
            self.worker.error.connect(lambda msg: MainFunctions.handle_error(self, msg))
            self.worker.finished.connect(lambda data: MainFunctions.handle_result(self, data))
            
            # Inicia o worker
            self.worker.start()

        except Exception as e:
            MainFunctions.write_status_import(self, f"Erro: {str(e)}")
            self.push_button_importar_editais.setEnabled(True)

    def start_automation(self):
        try:

            copy_docs = self.copy_docs_checkbox
            fill_word = self.fill_word_checkbox
            convert_pdf = self.convert_pdf_checkbox
            fill_proposal = self.fill_proposal_checkbox
            download_edital = self.download_editais_checkbox
            
            self.workerAutomation = RequestWorkerAutomation(copy_docs, fill_word, convert_pdf, fill_proposal, download_edital)
            
            self.workerAutomation.progress.connect(lambda msg: MainFunctions.write_status_automation(self,msg))
            self.workerAutomation.error.connect(lambda msg: MainFunctions.handle_error_automation(self, msg))
            self.workerAutomation.finished.connect(lambda: MainFunctions.handle_result_automation(self))
            
            self.start_automation_button.setText(" Parar Automação")
            self.start_automation_button.clicked.disconnect()
            self.start_automation_button.clicked.connect(lambda: MainFunctions.stop_automation(self))
            
            self.workerAutomation.start()
        except Exception as e:
            MainFunctions.write_status_automation(self, f"Erro: {str(e)}")
            MainFunctions.reset_automation_button(self)

    def stop_automation(self):
        try:
            if hasattr(self, 'workerAutomation'):
                self.workerAutomation.stop()
                self.workerAutomation.wait()
                MainFunctions.write_status_automation(self, "Automação interrompida pelo usuário")
            # Fix: Change to use lambda
            self.start_automation_button.clicked.disconnect()
            self.start_automation_button.clicked.connect(lambda: MainFunctions.start_automation(self))
            MainFunctions.reset_automation_button(self)
        except Exception as e:
            MainFunctions.write_status_automation(self, f"Erro ao parar automação: {str(e)}")
            MainFunctions.reset_automation_button(self)

    def reset_automation_button(self):
        self.start_automation_button.setText(" Iniciar Automação")
        self.start_automation_button.clicked.disconnect()
        # Fix: Change to use lambda 
        self.start_automation_button.clicked.connect(lambda: MainFunctions.start_automation(self))
        self.start_automation_button.setEnabled(True)

    def handle_result_automation(self):
        try:                
            MainFunctions.write_status_automation(self, f"Processo finalizado com sucesso!")
        except Exception as e:
            MainFunctions.write_status_automation(self, f"Erro ao processar dados: {str(e)}")
        finally:
            MainFunctions.reset_automation_button(self)
        
    def handle_error_automation(self, error_message):
        MainFunctions.write_status_automation(self, f"Erro: {error_message}")
        self.start_automation_button.setEnabled(True)
        
    
    def handle_error(self, error_message):
        MainFunctions.write_status_import(self, f"Erro: {error_message}")
        self.push_button_importar_editais.setEnabled(True)
        

    def handle_result(self, data):
        try:
            # Check if data exists
            if data is None:
                raise ValueError("Nenhum dado recebido")
                
            # Get length of data array directly since it's now a list of editais
            tamanho = len(data) if isinstance(data, list) else 0
            
            if tamanho > 0:
                MainFunctions.write_status_import(self, f"Dados importados com sucesso! {tamanho} editais encontrados")
            else:
                MainFunctions.write_status_import(self, "Nenhum edital encontrado")
                
        except Exception as e:
            MainFunctions.write_status_import(self, f"Erro ao processar dados: {str(e)}")
        finally:
            self.push_button_importar_editais.setEnabled(True)
        
        

    # SET LEFT COLUMN PAGES
    # ///////////////////////////////////////////////////////////////
    def set_left_column_menu(
        self,
        menu,
        title,
        icon_path
    ):
        self.ui.left_column.menus.menus.setCurrentWidget(menu)
        self.ui.left_column.title_label.setText(title)
        self.ui.left_column.icon.set_icon(icon_path)

    # RETURN IF LEFT COLUMN IS VISIBLE
    # ///////////////////////////////////////////////////////////////
    def left_column_is_visible(self):
        width = self.ui.left_column_frame.width()
        if width == 0:
            return False
        else:
            return True

    # RETURN IF RIGHT COLUMN IS VISIBLE
    # ///////////////////////////////////////////////////////////////
    def right_column_is_visible(self):
        width = self.ui.right_column_frame.width()
        if width == 0:
            return False
        else:
            return True

    # SET RIGHT COLUMN PAGES
    # ///////////////////////////////////////////////////////////////
    def set_right_column_menu(self, menu):
        self.ui.right_column.menus.setCurrentWidget(menu)

    # GET TITLE BUTTON BY OBJECT NAME
    # ///////////////////////////////////////////////////////////////
    def get_title_bar_btn(self, object_name):
        return self.ui.title_bar_frame.findChild(QPushButton, object_name)

    # GET TITLE BUTTON BY OBJECT NAME
    # ///////////////////////////////////////////////////////////////
    def get_left_menu_btn(self, object_name):
        return self.ui.left_menu.findChild(QPushButton, object_name)
    
    # LEDT AND RIGHT COLUMNS / SHOW / HIDE
    # ///////////////////////////////////////////////////////////////
    def toggle_left_column(self):
        # GET ACTUAL CLUMNS SIZE
        width = self.ui.left_column_frame.width()
        right_column_width = self.ui.right_column_frame.width()

        MainFunctions.start_box_animation(self, width, right_column_width, "left")

    def toggle_right_column(self):
        # GET ACTUAL CLUMNS SIZE
        left_column_width = self.ui.left_column_frame.width()
        width = self.ui.right_column_frame.width()

        MainFunctions.start_box_animation(self, left_column_width, width, "right")

    def start_box_animation(self, left_box_width, right_box_width, direction):
        right_width = 0
        left_width = 0
        time_animation = self.ui.settings["time_animation"]
        minimum_left = self.ui.settings["left_column_size"]["minimum"]
        maximum_left = self.ui.settings["left_column_size"]["maximum"]
        minimum_right = self.ui.settings["right_column_size"]["minimum"]
        maximum_right = self.ui.settings["right_column_size"]["maximum"]

        # Check Left Values        
        if left_box_width == minimum_left and direction == "left":
            left_width = maximum_left
        else:
            left_width = minimum_left

        # Check Right values        
        if right_box_width == minimum_right and direction == "right":
            right_width = maximum_right
        else:
            right_width = minimum_right       

        # ANIMATION LEFT BOX        
        self.left_box = QPropertyAnimation(self.ui.left_column_frame, b"minimumWidth")
        self.left_box.setDuration(time_animation)
        self.left_box.setStartValue(left_box_width)
        self.left_box.setEndValue(left_width)
        self.left_box.setEasingCurve(QEasingCurve.InOutQuart)

        # ANIMATION RIGHT BOX        
        self.right_box = QPropertyAnimation(self.ui.right_column_frame, b"minimumWidth")
        self.right_box.setDuration(time_animation)
        self.right_box.setStartValue(right_box_width)
        self.right_box.setEndValue(right_width)
        self.right_box.setEasingCurve(QEasingCurve.InOutQuart)

        # GROUP ANIMATION
        self.group = QParallelAnimationGroup()
        self.group.stop()
        self.group.addAnimation(self.left_box)
        self.group.addAnimation(self.right_box)
        self.group.start()