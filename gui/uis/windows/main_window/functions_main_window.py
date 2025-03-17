import sys
import os
import json
from typing import Optional, Dict, Any, Union, Callable

# IMPORT QT CORE
from qt_core import *

# LOAD UI MAIN
from .ui_main import *

# IMPORT WORKERS
from .worker import RequestWorker
from .workerAutomation import RequestWorkerAutomation
import datetime

class MainFunctions():
    """
    Classe que gerencia as funções principais da aplicação
    """
    def __init__(self):
        super().__init__()
        # Remover estas linhas que causam o conflito
        # self.ui = UI_MainWindow()
        # self.ui.setup_ui(self)
        
        # Verificação de configurações na inicialização
        self._load_user_settings()

    # MÉTODOS DE INTERFACE
    # ///////////////////////////////////////////////////////////////
    def set_page(self, page):
        """Alterna para a página especificada"""
        if hasattr(self.ui, 'load_pages') and hasattr(self.ui.load_pages, 'pages'):
            self.ui.load_pages.pages.setCurrentWidget(page)
        else:
            print("Erro: Interface não inicializada corretamente")
            
    # Adicione este método à classe MainFunctions:

    def get_title_bar_btn(self, object_name):
        """
        Retorna um botão da barra de título pelo seu nome de objeto
        """
        if hasattr(self, 'ui') and hasattr(self.ui, 'title_bar'):
            return self.ui.title_bar.findChild(QPushButton, object_name)
        return None

    # Adicione também estes métodos que podem ser necessários:

    def left_column_is_visible(self):
        """
        Verifica se a coluna esquerda está visível
        """
        width = self.ui.left_column_frame.width()
        if width == 0:
            return False
        else:
            return True

    def right_column_is_visible(self):
        """
        Verifica se a coluna direita está visível
        """
        width = self.ui.right_column_frame.width()
        if width == 0:
            return False
        else:
            return True

    def toggle_left_column(self):
        """
        Alterna a visibilidade da coluna esquerda
        """
        # Get current left column width
        width = self.ui.left_column_frame.width()
        MinWidth = self.ui.left_column_frame.minimumWidth()

        if width == 0:
            # Show left column
            newWidth = MinWidth
        else:
            # Restore left column
            newWidth = 0

        # Animate left column
        self.animation_left_column = QPropertyAnimation(self.ui.left_column_frame, b"minimumWidth")
        self.animation_left_column.setDuration(self.settings["time_animation"])
        self.animation_left_column.setStartValue(width)
        self.animation_left_column.setEndValue(newWidth)
        self.animation_left_column.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation_left_column.start()

    def toggle_right_column(self):
        """
        Alterna a visibilidade da coluna direita
        """
        # Get current right column width
        width = self.ui.right_column_frame.width()
        MinWidth = self.ui.right_column_frame.minimumWidth()

        if width == 0:
            # Show right column
            newWidth = MinWidth
        else:
            # Restore right column
            newWidth = 0

        # Animate right column
        self.animation_right_column = QPropertyAnimation(self.ui.right_column_frame, b"minimumWidth")
        self.animation_right_column.setDuration(self.settings["time_animation"])
        self.animation_right_column.setStartValue(width)
        self.animation_right_column.setEndValue(newWidth)
        self.animation_right_column.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation_right_column.start()
        
    def write_status_import(self, status: str):
        """Atualiza o status no campo de importação"""
        if hasattr(self, 'line_edit_status_import'):
            self.line_edit_status_import.setText(str(status))
        
    def write_status_settings(self, status: str):
        """Atualiza o status no campo de configurações"""
        if hasattr(self, 'line_edit_status_settings'):
            self.line_edit_status_settings.setText(str(status))
        
    def write_status_automation(self, status: str):
        """Adiciona texto ao campo de status de automação com rolagem automática"""
        if not hasattr(self, 'line_edit_status_automation'):
            return
            
        current_text = self.line_edit_status_automation.toPlainText()
        new_text = f"{current_text}\n{status}" if current_text else str(status)
        self.line_edit_status_automation.setPlainText(new_text)
        
        # Rolagem automática para o final do texto
        scrollbar = self.line_edit_status_automation.verticalScrollBar()
        if scrollbar:
            scrollbar.setValue(scrollbar.maximum())
    
    # MÉTODOS DE SELEÇÃO DE ARQUIVOS E DIRETÓRIOS
    # ///////////////////////////////////////////////////////////////
    def select_save_path(self, text: str, element: QLineEdit):
        """Abre diálogo para seleção de diretório"""
        if not element:
            self.write_status_settings("Erro: Elemento inválido")
            return
            
        directory = QFileDialog.getExistingDirectory(
            self,
            text,
            "", 
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        
        if directory:
            element.setText(directory)
        else:
            self.write_status_settings("Nenhuma pasta selecionada")
    
    def select_archive_path(self, text: str, element: QLineEdit):
        """Abre diálogo para seleção de arquivo"""
        if not element:
            self.write_status_settings("Erro: Elemento inválido")
            return
            
        archive = QFileDialog.getOpenFileName(
            self,
            text,
            "", 
        )
        
        if archive and archive[0]:
            element.setText(archive[0])
        else:
            self.write_status_settings("Nenhum arquivo selecionado")
    
    # MÉTODOS DE CONFIGURAÇÃO
    # ///////////////////////////////////////////////////////////////
    def save_settings(self):
        """Salva as configurações do usuário em arquivo JSON"""
        try:
            # Verificar se os elementos da interface existem
            if not all(hasattr(self, attr) for attr in [
                'save_path_line_edit', 'id_sheet_line_edit', 'doc_line_edit',
                'proposal_line_edit', 'declaration_line_edit', 'cotacao_line_edit', 'certificate_line_edit', 'certificate_password_edit'
            ]):
                raise AttributeError("Elementos da interface não encontrados")
            
            # Obter valores dos campos
            save_path = self.save_path_line_edit.text().strip()
            sheet_ids = self.id_sheet_line_edit.text().strip()
            document_archive = self.doc_line_edit.text().strip()
            sheet_propouse = self.proposal_line_edit.text().strip()
            declaration_document = self.declaration_line_edit.text().strip()
            cotacao_document = self.cotacao_line_edit.text().strip()
            certificate_path = self.certificate_line_edit.text().strip()
            certificate_password = self.certificate_password_edit.text().strip()
            
            # Validar caminhos de diretórios e arquivos
            if save_path and not os.path.isdir(save_path):
                self.write_status_settings("Aviso: Caminho de salvamento inválido")
            
            for path in [sheet_ids, document_archive, sheet_propouse, declaration_document]:
                if path and not os.path.isfile(path):
                    self.write_status_settings(f"Aviso: Arquivo não encontrado: {path}")
            
            # Preparar e salvar dados
            settings_data = {
                'save_path': save_path,
                'sheet_ids': sheet_ids,
                'document_archive': document_archive,
                'sheet_propouse': sheet_propouse,
                'declaration_document': declaration_document,
                'cotacao_document': cotacao_document,
                'certificate_path': certificate_path,
                'certificate_password': certificate_password
            }
            
            with open('user_settings.json', 'w', encoding='utf-8') as settings_file:
                json.dump(settings_data, settings_file, indent=4)
                
            self.write_status_settings("Configurações salvas com sucesso!")
            
        except Exception as e:
            self.write_status_settings(f"Erro ao salvar configurações: {str(e)}")
            
    def _load_user_settings(self):
        """Carrega as configurações do usuário do arquivo JSON (usado internamente)"""
        try:
            if not os.path.exists('user_settings.json'):
                # Cria arquivo de configurações vazio se não existir
                with open('user_settings.json', 'w', encoding='utf-8') as f:
                    json.dump({}, f, indent=4)
                return {}
                
            with open('user_settings.json', 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            print(f"Erro ao carregar configurações: {str(e)}")
            return {}
            
    def user_settings(self):
        """Carrega as configurações do usuário e preenche os campos da interface"""
        try:
            # Verificar se os elementos da interface existem
            if not all(hasattr(self, attr) for attr in [
                'save_path_line_edit', 'id_sheet_line_edit', 'doc_line_edit',
                'proposal_line_edit', 'declaration_line_edit', 'cotacao_line_edit',
                'certificate_line_edit', 'certificate_password_edit'
            ]):
                raise AttributeError("Elementos da interface não encontrados")
            
            settings_data = self._load_user_settings()
            
            # Armazenar valores em atributos da classe
            self.save_path = settings_data.get('save_path', '')
            self.sheet_ids = settings_data.get('sheet_ids', '')
            self.document_archive = settings_data.get('document_archive', '')
            self.sheet_propouse = settings_data.get('sheet_propouse', '')
            self.declaration_document = settings_data.get('declaration_document', '')
            self.cotacao_document = settings_data.get('cotacao_document', '')
            self.certificate_path = settings_data.get('certificate_path', '')
            self.certificate_password = settings_data.get('certificate_password', '')
            
            # Preencher campos da interface
            self.save_path_line_edit.setText(self.save_path)
            self.id_sheet_line_edit.setText(self.sheet_ids)
            self.doc_line_edit.setText(self.document_archive)
            self.proposal_line_edit.setText(self.sheet_propouse)
            self.declaration_line_edit.setText(self.declaration_document)
            self.cotacao_line_edit.setText(self.cotacao_document)
            self.certificate_line_edit.setText(self.certificate_path)
            self.certificate_password_edit.setText(self.certificate_password)
        
        except Exception as e:
            self.write_status_settings(f"Erro ao carregar configurações: {str(e)}")
            
    def show_date_context_menu(self, date_edit, pos):
        """Exibe menu de contexto para campos de data"""
        context_menu = QMenu()
        clear_action = context_menu.addAction("Limpar data")
        today_action = context_menu.addAction("Hoje")
        
        action = context_menu.exec_(date_edit.mapToGlobal(pos))
        
        if action == clear_action:
            # Definir para a data mínima e configurar para exibir o texto especial
            date_edit.setSpecialValueText(" ")  # Usar espaço em branco como texto especial
            date_edit.setDate(date_edit.minimumDate())
        elif action == today_action:
            # Restaurar texto normal (nenhum texto especial) e definir data para hoje
            date_edit.setSpecialValueText("")
            date_edit.setDate(QDate.currentDate())
    
    # MÉTODOS DE EXECUÇÃO DE TAREFAS
    # ///////////////////////////////////////////////////////////////
    def save_config_data(self):
        """Inicia a importação de editais via worker thread"""
        try:
            # Validar elementos de interface
            if not hasattr(self, 'push_button_importar_editais'):
                raise AttributeError("Botão de importação não encontrado")
                
            if not all(hasattr(self, attr) for attr in [
                'line_edit_quantidade', 'line_edit_perfil', 
                'line_edit_portais', 'consumir_planiha_button',
                'data_inicial_picker', 'data_final_picker'
            ]):
                raise AttributeError("Elementos da interface não encontrados")
            
            # Desabilitar o botão para evitar múltiplas chamadas
            self.push_button_importar_editais.setEnabled(False)
            
            # Obter e validar parâmetros - apenas quantidade é obrigatória
            quantidade = self.line_edit_quantidade.text().strip()
            perfil = self.perfil_combo.getSelectedId()
            portais = self.portais_combo.getSelectedId()
            consumir_planilha = self.consumir_planiha_button.isChecked()
            favoritos = self.favoritos_button.isChecked()
            
            # Substitua o trecho de código da verificação de data por este:
            # Obter datas selecionadas
            data_inicial = ""
            data_final = ""

            # Verificar se a data não é a data mínima (usada para representar "vazio")
            if self.data_inicial_picker.date() != self.data_inicial_picker.minimumDate():
                data_inicial = self.data_inicial_picker.date().toString("dd/MM/yyyy")

            if self.data_final_picker.date() != self.data_final_picker.minimumDate():
                data_final = self.data_final_picker.date().toString("dd/MM/yyyy")
            
            # Verificar se planilha existe quando opção está marcada
            if consumir_planilha:
                settings = self._load_user_settings()
                sheet_path = settings.get('sheet_ids', '')
                if not sheet_path or not os.path.isfile(sheet_path):
                    raise FileNotFoundError("Planilha de IDs não configurada ou não encontrada")
            
            # Criar e configurar o worker com as datas
            self.worker = RequestWorker(
                quantidade, perfil, portais, consumir_planilha, 
                data_inicial, data_final, favoritos
            )
            
            # Conectar sinais
            self.worker.progress.connect(self.write_status_import)
            self.worker.error.connect(self.handle_error)
            self.worker.finished.connect(self.handle_result)
            
            # Iniciar o worker
            self.worker.start()
            self.write_status_import("Iniciando importação...")
            
            # Mostrar mensagem sobre período de busca apenas se houver datas definidas
            if data_inicial or data_final:
                periodo = f"{data_inicial if data_inicial else 'início'} a {data_final if data_final else 'hoje'}"
                self.write_status_import(f"Período de busca: {periodo}")
            else:
                self.write_status_import("Buscando editais sem filtro de data")

        except ValueError as e:
            self.handle_error(f"Erro de validação: {str(e)}")
        except FileNotFoundError as e:
            self.handle_error(f"Arquivo não encontrado: {str(e)}")
        except Exception as e:
            self.handle_error(f"Erro: {str(e)}")

    def start_automation(self):
        """Inicia o processo de automação via worker thread"""
        try:
            # Validar elementos de interface
            required_elements = [
                'copy_docs_checkbox', 'fill_word_checkbox', 'convert_pdf_checkbox', 
                'fill_proposal_checkbox', 'download_editais_checkbox', 'start_automation_button', 'cotacao_checkbox', 'assign_pdf_checkbox'
            ]
            
            if not all(hasattr(self, elem) for elem in required_elements):
                raise AttributeError("Elementos da interface não encontrados")
            
            # Verificar configurações necessárias
            settings = self._load_user_settings()
            save_path = settings.get('save_path', '')
            
            if not save_path or not os.path.isdir(save_path):
                raise ValueError("Pasta de destino não configurada ou inválida")
                
            # Verificar se existem dados para processar
            if not os.path.exists('data.json'):
                raise FileNotFoundError("Nenhum edital importado para processar")
                
            # Obter opções selecionadas
            copy_docs = self.copy_docs_checkbox
            fill_word = self.fill_word_checkbox
            convert_pdf = self.convert_pdf_checkbox
            fill_proposal = self.fill_proposal_checkbox
            download_edital = self.download_editais_checkbox
            cotacao_document = self.cotacao_checkbox
            assign_pdf = self.assign_pdf_checkbox
            
            # # Verificar se pelo menos uma opção está selecionada
            # if not any([copy_docs.isChecked(), fill_word.isChecked(), 
            #            convert_pdf.isChecked(), fill_proposal.isChecked(), 
            #            download_edital.isChecked()]):
            #     raise ValueError("Selecione pelo menos uma opção de automação")
            
            # Criar e configurar worker
            self.workerAutomation = RequestWorkerAutomation(
                copy_docs, fill_word, convert_pdf, fill_proposal, download_edital, cotacao_document, assign_pdf
            )
            
            # Conectar sinais
            self.workerAutomation.progress.connect(self.write_status_automation)
            self.workerAutomation.error.connect(self.handle_error_automation)
            self.workerAutomation.finished.connect(self.handle_result_automation)
            
            # Configurar botão para parar automação
            self.start_automation_button.setText(" Parar Automação")
            self.start_automation_button.clicked.disconnect()
            self.start_automation_button.clicked.connect(self.stop_automation)
            
            # Iniciar worker
            self.workerAutomation.start()
            self.write_status_automation("Iniciando automação...")
            
        except Exception as e:
            self.write_status_automation(f"Erro ao iniciar automação: {str(e)}")
            self.reset_automation_button()

    def stop_automation(self):
        """Para o processo de automação em andamento"""
        try:
            if not hasattr(self, 'workerAutomation'):
                raise AttributeError("Worker de automação não encontrado")
                
            if not hasattr(self, 'start_automation_button'):
                raise AttributeError("Botão de automação não encontrado")
                
            # Parar o worker e aguardar finalização
            self.workerAutomation.stop()  
            self.workerAutomation.wait()
            self.write_status_automation("Automação interrompida pelo usuário")
            
            # Reconectar o botão para iniciar nova automação
            self.reset_automation_button()
            
        except Exception as e:
            self.write_status_automation(f"Erro ao parar automação: {str(e)}")
            self.reset_automation_button()

    def reset_automation_button(self):
        """Reseta o botão de automação para o estado inicial"""
        try:
            if not hasattr(self, 'start_automation_button'):
                return
                
            self.start_automation_button.setText(" Iniciar Automação")
            
            if self.start_automation_button.receivers(self.start_automation_button.clicked) > 0:
                self.start_automation_button.clicked.disconnect()
                
            self.start_automation_button.clicked.connect(self.start_automation)
            self.start_automation_button.setEnabled(True)
            
        except Exception as e:
            print(f"Erro ao resetar botão de automação: {str(e)}")
    
    def populate_editais_table(self):
        """Carrega os dados dos editais na tabela"""
        try:
            # Limpar tabela
            self.editais_table.setRowCount(0)
            
            # Carregar dados do arquivo JSON
            if not os.path.exists('data.json'):
                return
                
            with open('data.json', 'r', encoding='utf-8') as f:
                editais = json.load(f)
                
            # Preencher a tabela
            for edital in editais:
                row_position = self.editais_table.rowCount()
                self.editais_table.insertRow(row_position)
                
                # ID
                id_item = QTableWidgetItem(str(edital.get('id', '')))
                id_item.setTextAlignment(Qt.AlignCenter)
                self.editais_table.setItem(row_position, 0, id_item)
                
                # Objeto (limitar tamanho e remover tags HTML)
                perfil = edital.get('perfil', '')
                self.editais_table.setItem(row_position, 4, QTableWidgetItem(perfil))
                
                # Portal
                self.editais_table.setItem(row_position, 2, QTableWidgetItem(edital.get('portalNome', '')))
                
                # Data Final (formatar como data legível)
                data_final = edital.get('dataFinal', '')
                if data_final:
                    data_final = data_final.split(' ')[0]  # Remover a parte da hora
                self.editais_table.setItem(row_position, 3, QTableWidgetItem(data_final))
                
                # UASG
                self.editais_table.setItem(row_position, 1, QTableWidgetItem(edital.get('uasgNome', '')))
                
                # UF
                self.editais_table.setItem(row_position, 5, QTableWidgetItem(edital.get('uf', '')))
                
                # Situação (baseado na data final)
                try:
                    if data_final:
                        data_final_obj = datetime.datetime.strptime(data_final, '%d/%m/%Y')
                        hoje = datetime.datetime.now()
                        situacao = "Aberto" if data_final_obj > hoje else "Encerrado"
                        
                        # Definir cor com base na situação
                        situacao_item = QTableWidgetItem(situacao)
                        if situacao == "Aberto":
                            situacao_item.setForeground(QColor("#4CAF50"))  # Verde para aberto
                        else:
                            situacao_item.setForeground(QColor("#F44336"))  # Vermelho para encerrado
                            
                        situacao_item.setTextAlignment(Qt.AlignCenter)
                        self.editais_table.setItem(row_position, 6, situacao_item)
                    else:
                        self.editais_table.setItem(row_position, 6, QTableWidgetItem("Desconhecida"))
                except Exception as e:
                    print(f"Erro ao processar data: {str(e)}")
                    self.editais_table.setItem(row_position, 6, QTableWidgetItem("Erro"))
                    
            # Ajustar largura das colunas
            self.editais_table.resizeColumnsToContents()
            self.editais_table.setColumnWidth(1, 300)  # Fixar largura da coluna Objeto
                
        except Exception as e:
            print(f"Erro ao carregar editais: {str(e)}")

    def filter_editais_table(self):
        """Filtra a tabela de editais com base no texto de pesquisa"""
        search_text = self.search_editais.text().lower()
        
        for row in range(self.editais_table.rowCount()):
            match_found = False
            
            # Verificar todas as colunas para o texto de pesquisa
            for column in range(self.editais_table.columnCount()):
                item = self.editais_table.item(row, column)
                if item and search_text in item.text().lower():
                    match_found = True
                    break
                    
            # Mostrar/esconder a linha com base no resultado da pesquisa
            self.editais_table.setRowHidden(row, not match_found)
            
    # Dentro da classe MainWindow, adicione estes métodos:

    def show_edital_details(self, row, column):
        """Mostra os detalhes do edital selecionado"""
        try:
            # Obter o ID do edital da primeira coluna
            id_item = self.editais_table.item(row, 0)
            if not id_item:
                return
            
            edital_id = id_item.text()
            
            # Carregar dados do edital do arquivo JSON
            if not os.path.exists('data.json'):
                return
                
            with open('data.json', 'r', encoding='utf-8') as f:
                editais = json.load(f)
            
            # Encontrar o edital pelo ID
            edital = None
            for e in editais:
                if str(e.get('id', '')) == edital_id:
                    edital = e
                    break
            
            if not edital:
                QMessageBox.warning(self, "Erro", f"Edital ID {edital_id} não encontrado")
                return
            
            # Limpar o layout existente
            self.clear_layout(self.ui.load_pages.edital_details_layout)
            
            # Criar widgets para mostrar os detalhes do edital
            self.populate_edital_details(edital)
            
            # Mudar para a página de detalhes
            MainFunctions.set_page(self, self.ui.load_pages.page_6)
            
        except Exception as e:
            print(f"Erro ao mostrar detalhes do edital: {str(e)}")
            import traceback
            traceback.print_exc()

    def back_to_editais_list(self):
        """Retornar para a lista de editais"""
        MainFunctions.set_page(self, self.ui.load_pages.page_5)

    def clear_layout(self, layout):
        """Remove todos os widgets de um layout"""
        if not layout:
            return
        
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def populate_edital_details(self, edital):
        """Preenche a página de detalhes com os dados do edital"""
        try:
            # Adicionar estilo para títulos e valores
            title_style = f"""
                color: {self.themes["app_color"]["text_title"]};
                font-size: 14px;
                font-weight: bold;
                background-color: transparent;
                margin-top: 10px;
            """
            
            value_style = f"""
                color: {self.themes["app_color"]["text_title"]};
                font-size: 12px;
                background-color: transparent;
                border: 1px solid {self.themes["app_color"]["bg_three"]};
                border-radius: 5px;
                padding: 8px;
            """
            
            section_style = f"""
                color: {self.themes["app_color"]["text_title"]};
                font-size: 16px;
                font-weight: bold;
                background-color: transparent;
                padding: 5px;
                border-bottom: 2px solid {self.themes["app_color"]["context_color"]};
                margin-top: 15px;
                margin-bottom: 5px;
            """
            
            # Container principal
            main_container = QWidget()
            main_layout = QVBoxLayout(main_container)
            main_layout.setContentsMargins(0, 0, 0, 0)
            main_layout.setSpacing(5)
            
            # ===== SEÇÃO: INFORMAÇÕES GERAIS =====
            section_label = QLabel("INFORMAÇÕES GERAIS")
            section_label.setStyleSheet(section_style)
            main_layout.addWidget(section_label)
            
            # ID e Portal
            row_layout = QHBoxLayout()
            
            # ID
            id_container = QWidget()
            id_layout = QVBoxLayout(id_container)
            id_layout.setContentsMargins(0, 0, 10, 0)
            
            id_title = QLabel("ID:")
            id_title.setStyleSheet(title_style)
            id_layout.addWidget(id_title)
            
            id_value = QLabel(str(edital.get('id', 'N/A')))
            id_value.setStyleSheet(value_style)
            id_layout.addWidget(id_value)
            
            row_layout.addWidget(id_container)
            
            # Portal
            portal_container = QWidget()
            portal_layout = QVBoxLayout(portal_container)
            portal_layout.setContentsMargins(0, 0, 0, 0)
            
            portal_title = QLabel("Portal:")
            portal_title.setStyleSheet(title_style)
            portal_layout.addWidget(portal_title)
            
            portal_value = QLabel(f"{edital.get('portalNome', 'N/A')} ({edital.get('portal', 'N/A')})")
            portal_value.setStyleSheet(value_style)
            portal_layout.addWidget(portal_value)
            
            row_layout.addWidget(portal_container)
            main_layout.addLayout(row_layout)
            
            # Objeto
            objeto_container = QWidget()
            objeto_layout = QVBoxLayout(objeto_container)
            objeto_layout.setContentsMargins(0, 0, 0, 0)
            
            objeto_title = QLabel("Objeto:")
            objeto_title.setStyleSheet(title_style)
            objeto_layout.addWidget(objeto_title)
            
            objeto_text = edital.get('objeto', 'N/A')
            objeto_text = objeto_text.replace('<mark>', '').replace('</mark>', '').replace('<em>', '').replace('</em>', '')
            
            objeto_value = QTextEdit()
            objeto_value.setHtml(objeto_text)
            objeto_value.setReadOnly(True)
            objeto_value.setMaximumHeight(100)
            objeto_value.setStyleSheet(value_style)
            objeto_layout.addWidget(objeto_value)
            
            main_layout.addWidget(objeto_container)
            
            # Datas, UASG, UF e Tipo em grade de 3x2
            grid_widget = QWidget()
            grid_layout = QGridLayout(grid_widget)
            grid_layout.setContentsMargins(0, 0, 0, 0)
            
            # Data Inicial
            data_inicial_title = QLabel("Data Inicial:")
            data_inicial_title.setStyleSheet(title_style)
            grid_layout.addWidget(data_inicial_title, 0, 0)
            
            data_inicial_value = QLabel(edital.get('dataInicial', 'N/A'))
            data_inicial_value.setStyleSheet(value_style)
            grid_layout.addWidget(data_inicial_value, 1, 0)
            
            # Data Final
            data_final_title = QLabel("Data Final:")
            data_final_title.setStyleSheet(title_style)
            grid_layout.addWidget(data_final_title, 0, 1)
            
            data_final_value = QLabel(edital.get('dataFinal', 'N/A'))
            data_final_value.setStyleSheet(value_style)
            grid_layout.addWidget(data_final_value, 1, 1)
            
            # UASG
            uasg_title = QLabel("UASG:")
            uasg_title.setStyleSheet(title_style)
            grid_layout.addWidget(uasg_title, 0, 2)
            
            uasg_value = QLabel(f"{edital.get('uasgNome', 'N/A')} ({edital.get('uasg', 'N/A')})")
            uasg_value.setStyleSheet(value_style)
            grid_layout.addWidget(uasg_value, 1, 2)
            
            # UF
            uf_title = QLabel("UF:")
            uf_title.setStyleSheet(title_style)
            grid_layout.addWidget(uf_title, 2, 0)
            
            uf_value = QLabel(edital.get('uf', 'N/A'))
            uf_value.setStyleSheet(value_style)
            grid_layout.addWidget(uf_value, 3, 0)
            
            # Tipo
            tipo_title = QLabel("Tipo:")
            tipo_title.setStyleSheet(title_style)
            grid_layout.addWidget(tipo_title, 2, 1)
            
            tipo_value = QLabel(edital.get('tipo', 'N/A'))
            tipo_value.setStyleSheet(value_style)
            grid_layout.addWidget(tipo_value, 3, 1)
            
            # Pregão
            pregao_title = QLabel("Pregão:")
            pregao_title.setStyleSheet(title_style)
            grid_layout.addWidget(pregao_title, 2, 2)
            
            pregao_value = QLabel(edital.get('pregao', 'N/A'))
            pregao_value.setStyleSheet(value_style)
            grid_layout.addWidget(pregao_value, 3, 2)
            
            main_layout.addWidget(grid_widget)
            
            # URL
            url_container = QWidget()
            url_layout = QVBoxLayout(url_container)
            url_layout.setContentsMargins(0, 0, 0, 0)
            
            url_title = QLabel("URL:")
            url_title.setStyleSheet(title_style)
            url_layout.addWidget(url_title)
            
            url_text = edital.get('url', 'N/A')
            url_value = QLineEdit(url_text)
            url_value.setReadOnly(True)
            url_value.setStyleSheet(value_style)
            url_layout.addWidget(url_value)
            
            # Botão para abrir URL
            url_button = QPushButton("Abrir URL")
            url_button.setStyleSheet(f"""
                background-color: {self.themes["app_color"]["dark_one"]};
                color: {self.themes["app_color"]["text_foreground"]};
                border-radius: 5px;
                padding: 5px 10px;
            """)
            url_button.setCursor(QCursor(Qt.PointingHandCursor))
            
            if url_text != 'N/A':
                url_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(url_text)))
            else:
                url_button.setEnabled(False)
                
            url_layout.addWidget(url_button)
            main_layout.addWidget(url_container)
            
            # ===== SEÇÃO: ITENS =====
            itens = edital.get('item', [])
            if itens:
                section_label = QLabel("ITENS")
                section_label.setStyleSheet(section_style)
                main_layout.addWidget(section_label)
                
                # Tabela de itens
                itens_table = QTableWidget()
                # Definir uma altura mínima maior para a tabela
                itens_table.setMinimumHeight(300)  # Aumento significativo na altura mínima
                
                itens_table.setStyleSheet(f"""
                    QTableWidget {{
                        background-color: {self.themes["app_color"]["bg_two"]};
                        border-radius: 5px;
                        color: white;  /* Texto branco para os itens da tabela */
                    }}
                    QTableWidget::item {{
                        padding: 5px;
                        color: white;  /* Garantir que os itens da tabela tenham texto branco */
                    }}
                    QHeaderView::section {{
                        background-color: {self.themes["app_color"]["dark_two"]};
                        color: white;  /* Cabeçalho com texto branco */
                        font-weight: bold;
                        padding: 5px;
                        border: none;
                    }}
                    /* Melhorar visibilidade da seleção */
                    QTableWidget::item:selected {{
                        background-color: {self.themes["app_color"]["context_color"]};
                        color: white;
                    }}
                """)
                
                # Configurar colunas
                columns = ["Código", "Grupo", "Descrição", "Unidade", "Quantidade", "ME/EPP"]
                itens_table.setColumnCount(len(columns))
                itens_table.setHorizontalHeaderLabels(columns)
                itens_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)  # Coluna descrição expande
                
                # Preencher linhas
                for item in itens:
                    row = itens_table.rowCount()
                    itens_table.insertRow(row)
                    
                    # Código
                    codigo_item = QTableWidgetItem(str(item.get('codigo', '')))
                    codigo_item.setTextAlignment(Qt.AlignCenter)
                    itens_table.setItem(row, 0, codigo_item)
                    
                    # Grupo
                    grupo_item = QTableWidgetItem(item.get('grupo', '-'))
                    grupo_item.setTextAlignment(Qt.AlignCenter)
                    itens_table.setItem(row, 1, grupo_item)
                    
                    # Descrição (sem tags HTML)
                    descricao = item.get('descricao', item.get('objeto', ''))
                    descricao = descricao.replace('<mark>', '').replace('</mark>', '').replace('<em>', '').replace('</em>', '')
                    itens_table.setItem(row, 2, QTableWidgetItem(descricao))
                    
                    # Unidade
                    itens_table.setItem(row, 3, QTableWidgetItem(item.get('unidade', '-')))
                    
                    # Quantidade
                    qtd_item = QTableWidgetItem(item.get('quantidade', '0'))
                    qtd_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    itens_table.setItem(row, 4, qtd_item)
                    
                    # ME/EPP
                    me_epp = item.get('exclusivoMeEpp', -1)
                    me_epp_text = "Sim" if me_epp == 1 else "Não" if me_epp == 0 else "N/D"
                    me_epp_item = QTableWidgetItem(me_epp_text)
                    me_epp_item.setTextAlignment(Qt.AlignCenter)
                    itens_table.setItem(row, 5, me_epp_item)
                
                itens_table.resizeColumnsToContents()
                main_layout.addWidget(itens_table)
            
            # ===== SEÇÃO: ANEXOS =====
            anexos = edital.get('anexo', [])
            if anexos:
                section_label = QLabel("ANEXOS")
                section_label.setStyleSheet(section_style)
                main_layout.addWidget(section_label)
                
                anexos_container = QWidget()
                anexos_layout = QVBoxLayout(anexos_container)
                anexos_layout.setContentsMargins(0, 0, 0, 0)
                
                for anexo in anexos:
                    anexo_widget = QWidget()
                    anexo_layout = QHBoxLayout(anexo_widget)
                    anexo_layout.setContentsMargins(0, 5, 0, 5)
                    
                    nome = anexo.get('nome', 'Sem nome')
                    url = anexo.get('url', '')
                    
                    # Ícone para o anexo
                    anexo_icon = QLabel()
                    anexo_icon.setText("📄")
                    anexo_icon.setStyleSheet("font-size: 20px; padding: 0 10px;")
                    
                    anexo_layout.addWidget(anexo_icon)
                    
                    # Nome do anexo
                    anexo_name = QLabel(nome)
                    anexo_name.setStyleSheet(f"color: {self.themes['app_color']['text_description']};")
                    anexo_layout.addWidget(anexo_name)
                    
                    # Botão para baixar
                    download_btn = QPushButton("Baixar")
                    download_btn.setMinimumWidth(80)
                    download_btn.setMaximumWidth(80)
                    download_btn.setStyleSheet(f"""
                        background-color: {self.themes["app_color"]["dark_one"]};
                        color: {self.themes["app_color"]["text_foreground"]};
                        border-radius: 5px;
                        padding: 5px;
                    """)
                    download_btn.setCursor(QCursor(Qt.PointingHandCursor))
                    
                    if url:
                        download_btn.clicked.connect(lambda checked, u=url: QDesktopServices.openUrl(QUrl(u)))
                    else:
                        download_btn.setEnabled(False)
                    
                    anexo_layout.addWidget(download_btn)
                    
                    anexos_layout.addWidget(anexo_widget)
                
                main_layout.addWidget(anexos_container)
            
            # Adicionar tudo ao layout da página
            self.ui.load_pages.edital_details_layout.addWidget(main_container)
            
            # Adicionar espaço na parte inferior
            spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.ui.load_pages.edital_details_layout.addItem(spacer)
            
        except Exception as e:
            print(f"Erro ao popular detalhes do edital: {str(e)}")
            import traceback
            traceback.print_exc()

    # MÉTODOS DE TRATAMENTO DE RESULTADOS
    # ///////////////////////////////////////////////////////////////
    def handle_result_automation(self):
        """Manipula o resultado do processo de automação"""
        try:                
            self.write_status_automation("Processo finalizado com sucesso!")
        except Exception as e:
            self.write_status_automation(f"Erro ao processar resultado: {str(e)}")
        finally:
            self.reset_automation_button()
        
    def handle_error_automation(self, error_message: str):
        """Manipula erros do processo de automação"""
        self.write_status_automation(f"Erro: {str(error_message)}")
        self.reset_automation_button()
        
    def handle_error(self, error_message: str):
        """Manipula erros do processo de importação"""
        self.write_status_import(f"Erro: {str(error_message)}")
        if hasattr(self, 'push_button_importar_editais'):
            self.push_button_importar_editais.setEnabled(True)

    def handle_result(self, data):
        """Manipula o resultado do processo de importação"""
        try:
            if not hasattr(self, 'push_button_importar_editais'):
                raise AttributeError("Botão de importação não encontrado")
                
            # Verificar dados recebidos
            if data is None:
                self.write_status_import("Nenhum dado recebido")
                return
                
            # Processar dados recebidos
            tamanho = len(data) if isinstance(data, list) else 0
            
            if tamanho > 0:
                self.write_status_import(f"Dados importados com sucesso! {tamanho} editais encontrados")
            else:
                self.write_status_import("Nenhum edital encontrado")
                
        except Exception as e:
            self.write_status_import(f"Erro ao processar dados: {str(e)}")
        finally:
            # Garantir que o botão seja reativado
            self.push_button_importar_editais.setEnabled(True)