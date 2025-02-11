from qt_core import *
import requests
import json               
import pandas as pd
import os
import shutil
import win32com.client as win32
from docx import Document
import xlwings as xw

class RequestWorkerAutomation(QThread):
    finished = Signal(list)
    progress = Signal(str)
    error = Signal(str)
    
    def __init__(self, copy_docs, fill_word, convert_pdf, fill_proposal, download_edital):
        super().__init__()
        self.copy_docs = copy_docs
        self.fill_word = fill_word
        self.convert_pdf = convert_pdf
        self.fill_proposal = fill_proposal
        self.download_edital = download_edital
        self._is_running = True
        self.initial_dir = os.getcwd()
    
    def stop(self):
        self._is_running = False
    

    def run(self):
        try:
            self.progress.emit("Iniciando automação...")
            
            settings_path = os.path.join(self.initial_dir, 'user_settings.json')
            data_path = os.path.join(self.initial_dir, 'data.json')
            
            try:
                with open(settings_path, 'r', encoding='utf-8') as f:
                    user_settings = json.load(f)
                with open(data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.progress.emit("Configurações carregadas com sucesso")
            except Exception as e:
                self.error.emit(f"Erro ao carregar configurações: {str(e)}")
                return
            
            for edital in data:
                if not self._is_running:
                    break
                
                self.progress.emit(f"\nProcessando edital {edital['id']}...")
                
                data_hora = edital["dataFinal"].split(' ')
                if len(data_hora) >= 2:
                    datasplit = data_hora[0].split('/')[:2]
                    dataPregao = ' '.join(datasplit)
                    
                    hora_split = data_hora[1].split(':')[:2]
                    horaPregao = ' '.join(hora_split)
                else:
                    dataPregao = "Data não disponível"
                    horaPregao = "Hora não disponível"

                numeroPregao = str(edital.get("pregao", ""))
                portalPregao = str(edital.get("portalNome", ""))
                uasgPregao = str(edital.get("uasg", ""))

                caracteres_proibidos = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
                
                numeroPregao_limpo = ''.join(caracter for caracter in numeroPregao if caracter not in caracteres_proibidos)
                portalPregao_limpo = ''.join(caracter for caracter in portalPregao if caracter not in caracteres_proibidos)
                portalPregao_limpo = portalPregao_limpo.upper()
                uasgPregao_limpo = ''.join(caracter for caracter in uasgPregao if caracter not in caracteres_proibidos)
                
                nome_pasta = f"{edital['id']} - {dataPregao} - {horaPregao}H - {portalPregao_limpo} {numeroPregao_limpo} - UASG {uasgPregao_limpo}"

                pasta_destino = os.path.join(user_settings["save_path"], nome_pasta)

                # Verifica se a pasta já existe
                if os.path.exists(pasta_destino):
                    self.progress.emit(f"Pasta já existe para o edital {edital['id']}, pulando para o próximo...")
                    continue

                try:
                    os.chdir(user_settings["save_path"])
                    os.mkdir(nome_pasta)
                    os.chdir(nome_pasta)
                    pathOriginal = os.getcwd()
                    for subpasta in ["DADOS DO PROCESSO", "PROPOSTA DE PREÇO", 
                                "DECLARACOES E ANEXOS", "DOCUMENTOS DE HABILITAÇAO"]:
                        os.mkdir(subpasta)

                    self.progress.emit(f"✔ Pastas criadas com sucesso para o edital {edital['id']}")
                
                
                    #DOCUMENTOS ----------------------------------------------------------------
                    if self.copy_docs.isChecked():
                        try:
                            os.chdir("DOCUMENTOS DE HABILITAÇAO")
                            shutil.copy(user_settings["document_archive"], os.getcwd())
                            self.progress.emit("✔ Documentos copiados com sucesso")
                        except Exception as e:
                            self.error.emit(f"❌ Erro na cópia dos documentos: {str(e)}")
                        finally:
                            os.chdir(pathOriginal)
                    
                    if self.fill_word.isChecked():
                        try:
                            os.chdir("DECLARACOES E ANEXOS")
                            caminho_modificado = os.getcwd()
                            nomeDeclaracao, extensao = os.path.splitext(os.path.basename(user_settings["declaration_document"]))

                            declaracaoWord = os.path.join(caminho_modificado,nomeDeclaracao + '.docx')
                            declaracaoPDF = os.path.join(caminho_modificado,nomeDeclaracao + '.pdf')
                            shutil.copy(user_settings["declaration_document"], os.getcwd())

                            declaracao = Document(nomeDeclaracao + '.docx')

                            declaracao.core_properties.author = edital["uasgNome"]
                            declaracao.core_properties.subject = numeroPregao
                            self.progress.emit("✔ Declaração preenchida com sucesso")
                            declaracao.save(nomeDeclaracao + '.docx')

                        except Exception as e:
                            self.error.emit(f"❌ Erro no preenchimento da declaração: {str(e)}")
                        finally:
                            os.chdir(pathOriginal)

                    try:
                        cache_dir = os.path.join(os.path.dirname(win32.__file__), "gen_py")
                        if os.path.exists(cache_dir):
                            shutil.rmtree(cache_dir)
                    except Exception as e:
                        pass
                        
                    if self.convert_pdf.isChecked():                 
                        try:
                            word = win32.Dispatch('Word.Application')
                            doc = word.Documents.Open(declaracaoWord)
                            doc.SaveAs(declaracaoPDF, FileFormat=17) 
                            doc.Close()
                            word.Quit()
                            self.progress.emit("✔ Arquivo convertido para PDF com sucesso")
                        except Exception as e:
                            self.error.emit(f"❌ Erro na conversão para PDF: {str(e)}")
                        finally:
                            os.chdir(pathOriginal)
                    
                    if self.fill_proposal.isChecked():
                        try:
                            os.chdir("PROPOSTA DE PREÇO")
                            shutil.copy(user_settings["sheet_propouse"], os.getcwd())
                            
                            caminho_planilha = os.path.basename(user_settings["sheet_propouse"])
                            
                            app = xw.App(visible=False)
                            workbook = app.books.open(caminho_planilha)
                            sheet = workbook.sheets[0]
                            sheet.range("B11").value = edital["uasgNome"]
                            sheet.range("C13").value = numeroPregao
                            
                            if edital["planilhaConsumida"] == True:
                                try: 
                                    linha_inicial = 21
                                    linha_primeiro_item = linha_inicial
                                    editaisValidos = edital["editaisValidos"]

                                    for item in edital["item"]:
                                        for editalValido in editaisValidos:
                                            if editalValido["id"] == edital["id"] and item["codigo"] in editalValido["itens"]:

                                                
                                                sheet[f"A{linha_inicial}"].value = item["codigo"]
                                                sheet[f"B{linha_inicial}"].value = item["descricao"]
                                                sheet[f"C{linha_inicial}"].value = item["unidade"]
                                                sheet[f"E{linha_inicial}"].value = item["quantidade"]
                                                sheet[f"G{linha_inicial}"].formula = f"=F{linha_inicial}*E{linha_inicial}"

                                                intervalo = f"A{linha_inicial}:G{linha_inicial}"
                                                for cell in sheet.range(intervalo):
                                                    for border_id in range(7, 13):
                                                        cell.api.Borders(border_id).LineStyle = 1
                                                        cell.api.Borders(border_id).Weight = 2
                                                linha_inicial += 1

                                    linha_total = linha_inicial
                                    range_total = f"A{linha_total}:F{linha_total}"
                                    sheet.range(range_total).merge()
                                    sheet[f"A{linha_total}"].value = "Total:"
                                    sheet[f"A{linha_total}"].font.bold = True
                                    sheet[f"A{linha_total}"].api.HorizontalAlignment = -4152

                                    sheet[f"G{linha_total}"].formula = f"=SUM(G{linha_primeiro_item}:G{linha_inicial - 1})"
                                    sheet[f"G{linha_total}"].font.bold = True
                                    self.progress.emit("✔ Proposta preenchida com sucesso")
                                except Exception as e:
                                    self.error.emit(f"❌ Erro no preenchimento da proposta: {str(e)}")
                                finally:
                                    workbook.save(caminho_planilha)
                                    workbook.close()
                                    app.quit()
                                    os.chdir(pathOriginal)
                            else:
                                try: 
                                    linha_inicial = 21
                                    linha_primeiro_item = linha_inicial

                                    for item in edital["item"]:
                                        sheet[f"A{linha_inicial}"].value = item["codigo"]
                                        sheet[f"B{linha_inicial}"].value = item["descricao"]
                                        sheet[f"C{linha_inicial}"].value = item["unidade"]
                                        sheet[f"E{linha_inicial}"].value = item["quantidade"]
                                        sheet[f"G{linha_inicial}"].formula = f"=F{linha_inicial}*E{linha_inicial}"

                                        intervalo = f"A{linha_inicial}:G{linha_inicial}"
                                        for cell in sheet.range(intervalo):
                                            for border_id in range(7, 13):
                                                cell.api.Borders(border_id).LineStyle = 1
                                                cell.api.Borders(border_id).Weight = 2
                                        linha_inicial += 1

                                    linha_total = linha_inicial
                                    range_total = f"A{linha_total}:F{linha_total}"
                                    sheet.range(range_total).merge()
                                    sheet[f"A{linha_total}"].value = "Total:"
                                    sheet[f"A{linha_total}"].font.bold = True
                                    sheet[f"A{linha_total}"].api.HorizontalAlignment = -4152

                                    sheet[f"G{linha_total}"].formula = f"=SUM(G{linha_primeiro_item}:G{linha_inicial - 1})"
                                    sheet[f"G{linha_total}"].font.bold = True
                                    self.progress.emit("✔ Proposta preenchida com sucesso")
                                except Exception as e:
                                    self.error.emit(f"❌ Erro no preenchimento da proposta: {str(e)}")
                                finally:
                                    workbook.save(caminho_planilha)
                                    workbook.close()
                                    app.quit()
                                    os.chdir(pathOriginal)
                        except Exception as e:
                            self.error.emit(f"❌ Erro no preenchimento da proposta: {str(e)}")

                    if self.download_edital.isChecked():
                        try:
                            os.chdir("DADOS DO PROCESSO")
                            self.progress.emit("\nIniciando download dos anexos...")
                            
                            for anexo in edital["anexo"]:
                                if not self._is_running:
                                    break
                                try:
                                    # Pega a URL e nome do arquivo
                                    url = anexo["url"]
                                    filename = anexo["nome"]
                                    
                                    self.progress.emit(f"Baixando anexo: {filename}")
                                    
                                    # Faz a requisição com stream=True para arquivos grandes
                                    response = requests.get(url, stream=True)
                                    response.raise_for_status()
                                    
                                    # Verifica se tem nome do arquivo no cabeçalho da resposta
                                    if 'Content-Disposition' in response.headers:
                                        content_disposition = response.headers['Content-Disposition']
                                        if 'filename=' in content_disposition:
                                            filename = content_disposition.split('filename=')[1].strip('"')
                                    
                                    # Adiciona extensão .pdf se não tiver extensão
                                    if not os.path.splitext(filename)[1]:
                                        filename = f"{filename}.pdf"
                                    
                                    # Salva o arquivo
                                    file_path = os.path.join(os.getcwd(), filename)
                                    with open(file_path, 'wb') as f:
                                        for chunk in response.iter_content(chunk_size=8192):
                                            if chunk:
                                                f.write(chunk)
                                    
                                    self.progress.emit(f"Baixado: {filename}")
                                    
                                except Exception as e:
                                    self.error.emit(f"Erro ao baixar {anexo['url']}: {str(e)}")
                            
                            self.progress.emit("✔ Download dos anexos concluído")
                        except Exception as e:
                            self.error.emit(f"❌ Erro geral no download: {str(e)}")
                        finally:
                            os.chdir(pathOriginal)
                    self.progress.emit(f"✔ Processamento do edital {edital['id']} concluído\n")
                except Exception as e: 
                    self.error.emit(f"❌ Erro no processamento do edital {edital['id']}: {str(e)}")
                    continue
                finally:
                    os.chdir(self.initial_dir)
                
            self.progress.emit("\n✔ Automação concluída com sucesso!")
        except Exception as e:
            self.error.emit(f"❌ Erro crítico na automação: {str(e)}")
        finally:
            self._is_running = False
            os.chdir(self.initial_dir)
            self.finished.emit([])