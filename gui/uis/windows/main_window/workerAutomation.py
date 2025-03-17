from qt_core import *
import requests
import json               
import pandas as pd
import os
import shutil
import win32com.client as win32
from docx import Document
import xlwings as xw
import time
import urllib.parse
import ssl
from urllib3.exceptions import InsecureRequestWarning
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import subprocess
import glob
from pathlib import Path
from pypdf import PdfReader, PdfWriter
import shutil
import datetime

class RequestWorkerAutomation(QThread):
    finished = Signal(list)
    progress = Signal(str)
    error = Signal(str)
    
    def __init__(self, copy_docs, fill_word, convert_pdf, fill_proposal, download_edital, cotacao_document, assign_pdf):
        super().__init__()
        self.copy_docs = copy_docs
        self.fill_word = fill_word
        self.convert_pdf = convert_pdf
        self.fill_proposal = fill_proposal
        self.download_edital = download_edital
        self.cotacao_document = cotacao_document
        self.assign_pdf = assign_pdf
        self._is_running = True
        self.initial_dir = os.getcwd()
        
    def abreviar_nome_portal(self, nome_portal):
        """Converte o nome completo do portal para sua abreviação"""
        
        # Dicionário de mapeamento de nomes de portais para abreviações
        abreviacoes = {
            "BEC / Imprensa Oficial / Pregão SP": "BEC",
            "BLL - Bolsa de Licitações e Leilões": "BLL",
            "BNC - Bolsa Nacional de Compras": "BNC",
            "Banrisul": "BR",
            "Compras Amazonas": "CAM",
            "Compras BR": "CBR",
            "Compras Mato Grosso": "CMT",
            "Compras Minas Gerais": "CMG",
            "Compras Pernambuco Integrado": "CPE",
            "Compras Públicas": "CP",
            "Compras Santa Catarina": "CSC",
            "ComprasNet": "CN",
            "ComprasNet - Cotação Eletrônica": "CNCE",
            "ComprasNet Goiás": "CNG",
            "ComprasNet Simulador": "CNS",
            "ComprasRS": "CRS",
            "Licitanet": "LN",
            "Licitar Digital": "LD",
            "Licitações-e": "LE",
            "Procergs": "PRG",
            "Publinexo": "PNX",
            "Siga Espírito Santo": "SES",
            "Siga Rio de Janeiro": "SRJ"
        }
        
        # Retorna a abreviação ou o próprio nome se não encontrar no dicionário
        return abreviacoes.get(nome_portal, nome_portal)
    
    def separar_pdf(self, pdf_entrada, diretorio_saida):
        """
        Separa um arquivo PDF em páginas individuais
        """
        os.makedirs(diretorio_saida, exist_ok=True)
        
        pdf = PdfReader(pdf_entrada)
        total_paginas = len(pdf.pages)
        
        nome_arquivo = Path(pdf_entrada).stem
        
        arquivos_separados = []
        
        for i in range(total_paginas):
            writer = PdfWriter()
            writer.add_page(pdf.pages[i])
            
            arquivo_saida = os.path.join(diretorio_saida, f"{nome_arquivo}_pagina_{i+1}.pdf")
            with open(arquivo_saida, "wb") as f:
                writer.write(f)
            
            arquivos_separados.append(arquivo_saida)
            self.progress.emit(f"✓ Página {i+1}/{total_paginas} separada: {arquivo_saida}")
        
        self.progress.emit(f"Total de {len(arquivos_separados)} páginas separadas.")
        return arquivos_separados

    def limpar_diretorios_temporarios(self, diretorios):
        """
        Remove os diretórios temporários e seus conteúdos
        """
        for diretorio in diretorios:
            if os.path.exists(diretorio):
                try:
                    shutil.rmtree(diretorio)
                    self.progress.emit(f"✓ Diretório temporário removido: {diretorio}")
                except Exception as e:
                    self.error.emit(f"✗ Erro ao remover diretório {diretorio}: {str(e)}")

    def assinar_pdfs(self, diretorio_entrada, diretorio_saida, certificado_pfx, senha):
        """
        Assina todos os PDFs em um diretório usando JSignPdf
        """
        os.makedirs(diretorio_saida, exist_ok=True)
        
        arquivos_pdf = glob.glob(os.path.join(diretorio_entrada, "*.pdf"))
        
        # Verificar se a pasta JSignPdf está no diretório do projeto
        jsignpdf_jar = os.path.join(self.initial_dir, "JSignPdf.jar")
        
        # Verificar se o arquivo JAR existe
        if not os.path.exists(jsignpdf_jar):
            self.error.emit(f"❌ Arquivo JSignPdf.jar não encontrado em: {jsignpdf_jar}")
            return []
        
        arquivos_assinados = []
        
        for i, arquivo in enumerate(arquivos_pdf):
            nome_arquivo = Path(arquivo).name
            nome_base = Path(nome_arquivo).stem
            arquivo_saida = os.path.join(diretorio_saida, f"{nome_base}_assinado.pdf")
            
            self.progress.emit(f"Processando {i+1}/{len(arquivos_pdf)}: {nome_arquivo}")
            
            # Data atual formatada
            data_atual = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S BRT")
            
            # Texto personalizado para a camada 2 da assinatura (descrição principal)
            texto_l2 = f"Assinado digitalmente por ${{signer}}\nC=BR, O=ICP-Brasil, OU=12517704000115, OU=Secretaria da Receita Federal do Brasil - RFB\nRazão: ${{reason}}\nLocalização: ${{location}}\nData: {data_atual}"
            
            # Texto para a camada 4 (status)
            texto_l4 = "Documento assinado digitalmente"
            
            # Comando para JSignPdf para assinar o PDF com informações detalhadas
            comando = [
                "java", "-jar", jsignpdf_jar,
                arquivo,
                "-kst", "PKCS12",
                "-ksf", certificado_pfx,
                "-ksp", senha,
                "-d", diretorio_saida,
                "-fs", "8.0",
                "-llx", "45", "-lly", "0",
                "-urx", "250", "-ury", "220",
                "-V",
                "-r", "Eu estou aprovando este documento com minha assinatura de vinculação legal",
                "-l", "Minas Gerais",
                "--l2-text", texto_l2,
                "--l4-text", texto_l4,
                "--render-mode", "DESCRIPTION_ONLY"
            ]
            
            try:
                subprocess.run(comando, check=True)
                
                # Depois de assinar, o JSignPdf provavelmente cria um arquivo com nome padrão
                possivel_arquivo = os.path.join(diretorio_saida, f"{nome_base}_signed.pdf")
                if os.path.exists(possivel_arquivo):
                    # Verifica se o arquivo de destino já existe e o remove
                    if os.path.exists(arquivo_saida):
                        os.remove(arquivo_saida)
                    os.rename(possivel_arquivo, arquivo_saida)
                    
                arquivos_assinados.append(arquivo_saida)
                self.progress.emit(f"✓ Arquivo assinado com sucesso: {arquivo_saida}")
            except subprocess.CalledProcessError as e:
                self.error.emit(f"✗ Erro ao assinar {nome_arquivo}: {str(e)}")
                
                # Se falhar com as opções avançadas, tenta uma versão simplificada
                self.progress.emit("Tentando com opções simplificadas...")
                comando_simplificado = [
                    "java", "-jar", jsignpdf_jar,
                    arquivo,
                    "-kst", "PKCS12",
                    "-ksf", certificado_pfx,
                    "-ksp", senha,
                    "-d", diretorio_saida,
                    "-fs", "8.0",
                    "-llx", "45", "-lly", "350",
                    "-urx", "250", "-ury", "450",
                    "-V",
                    "-r", "Eu estou aprovando este documento com minha assinatura de vinculação legal",
                    "-l", "Minas Gerais",
                    "-c", "C=BR, O=ICP-Brasil, OU=12517704000115, OU=Secretaria da Receita Federal do Brasil - RFB"
                ]
                
                try:
                    subprocess.run(comando_simplificado, check=True)
                    
                    # Verificar e renomear o arquivo se necessário
                    possivel_arquivo = os.path.join(diretorio_saida, f"{nome_base}_signed.pdf")
                    if os.path.exists(possivel_arquivo):
                        if os.path.exists(arquivo_saida):
                            os.remove(arquivo_saida)
                        os.rename(possivel_arquivo, arquivo_saida)
                        
                    arquivos_assinados.append(arquivo_saida)
                    self.progress.emit(f"✓ Arquivo assinado com sucesso (modo simplificado): {arquivo_saida}")
                except subprocess.CalledProcessError as e2:
                    self.error.emit(f"✗ Erro ao assinar {nome_arquivo} (modo simplificado): {str(e2)}")
        
        self.progress.emit(f"Total de {len(arquivos_assinados)} arquivos assinados.")
        return arquivos_assinados

    def juntar_pdfs(self, lista_pdfs, pdf_saida):
        """
        Junta uma lista de PDFs em um único arquivo
        """
        # Garantir que os arquivos estão ordenados pelo número de página
        lista_pdfs.sort(key=lambda x: int(Path(x).stem.split('_pagina_')[1].split('_')[0]))
        
        writer = PdfWriter()
        
        for pdf_file in lista_pdfs:
            pdf = PdfReader(pdf_file)
            for page in pdf.pages:
                writer.add_page(page)
        
        with open(pdf_saida, "wb") as f:
            writer.write(f)
        
        self.progress.emit(f"✓ Arquivo final criado com sucesso: {pdf_saida}")
        return pdf_saida

    def processar_assinatura_pdf(self, pdf_entrada, user_settings):
        """
        Processa a assinatura digital de um arquivo PDF
        """
        if not os.path.exists(pdf_entrada):
            self.error.emit(f"❌ Arquivo PDF não encontrado: {pdf_entrada}")
            return None
        
        # Obter o certificado e senha do user_settings
        certificado_pfx = user_settings.get('certificate_path', '')
        senha = user_settings.get('certificate_password', '')
        
        # Verificar se o certificado existe
        if not certificado_pfx or not os.path.exists(certificado_pfx):
            self.error.emit("❌ Certificado digital não configurado ou não encontrado")
            return None
        
        # Verificar se a senha foi fornecida
        if not senha:
            self.error.emit("❌ Senha do certificado digital não configurada")
            return None
        
        # Criar diretórios temporários
        dir_base = os.path.dirname(pdf_entrada)
        nome_arquivo = Path(pdf_entrada).stem
        diretorio_paginas = os.path.join(dir_base, f"{nome_arquivo}_paginas_temp")
        diretorio_assinados = os.path.join(dir_base, f"{nome_arquivo}_assinados_temp")
        pdf_final = os.path.join(dir_base, f"{nome_arquivo}_assinado.pdf")
        
        try:
            self.progress.emit("\n=== ETAPA 1: SEPARANDO PDF EM PÁGINAS INDIVIDUAIS ===")
            paginas_separadas = self.separar_pdf(pdf_entrada, diretorio_paginas)
            
            self.progress.emit("\n=== ETAPA 2: ASSINANDO PÁGINAS INDIVIDUAIS ===")
            paginas_assinadas = self.assinar_pdfs(diretorio_paginas, diretorio_assinados, certificado_pfx, senha)
            
            if not paginas_assinadas:
                self.error.emit("❌ Nenhuma página foi assinada com sucesso")
                return None
            
            self.progress.emit("\n=== ETAPA 3: JUNTANDO PÁGINAS ASSINADAS EM UM ÚNICO PDF ===")
            pdf_resultado = self.juntar_pdfs(paginas_assinadas, pdf_final)
            
            self.progress.emit("\n=== ETAPA 4: LIMPANDO DIRETÓRIOS TEMPORÁRIOS ===")
            self.limpar_diretorios_temporarios([diretorio_paginas, diretorio_assinados])
            
            self.progress.emit("\n=== PROCESSO DE ASSINATURA CONCLUÍDO COM SUCESSO! ===")
            self.progress.emit(f"Arquivo final: {pdf_resultado}")
            
            return pdf_resultado
            
        except Exception as e:
            self.error.emit(f"❌ Erro no processo de assinatura: {str(e)}")
            # Tentar limpar os diretórios temporários mesmo em caso de erro
            try:
                self.limpar_diretorios_temporarios([diretorio_paginas, diretorio_assinados])
            except:
                pass
            return None
    
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
                portalPregao_abreviado = self.abreviar_nome_portal(portalPregao)
                caracteres_proibidos = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
                
                numeroPregao_limpo = ''.join(caracter for caracter in numeroPregao if caracter not in caracteres_proibidos)
                portalPregao_limpo = ''.join(caracter for caracter in portalPregao_abreviado if caracter not in caracteres_proibidos)
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
                            sheet.range("B5").value = edital["uasgNome"]
                            sheet.range("C7").value = numeroPregao
                            
                            if edital["planilhaConsumida"] == True:
                                try: 
                                    linha_inicial = 15
                                    linha_primeiro_item = linha_inicial
                                    editaisValidos = edital["editaisValidos"]

                                    for item in edital["item"]:
                                        for editalValido in editaisValidos:
                                            if editalValido["id"] == edital["id"] and item["codigo"] in editalValido["itens"]:

                                                
                                                sheet[f"A{linha_inicial}"].value = item["codigo"]
                                                sheet[f"B{linha_inicial}"].value = item["descricao"]
                                                sheet[f"C{linha_inicial}"].value = item["unidade"]
                                                sheet[f"F{linha_inicial}"].value = item["quantidade"]
                                                sheet[f"H{linha_inicial}"].formula = f"=F{linha_inicial}*G{linha_inicial}"

                                                intervalo = f"A{linha_inicial}:G{linha_inicial}"
                                                for cell in sheet.range(intervalo):
                                                    for border_id in range(7, 13):
                                                        cell.api.Borders(border_id).LineStyle = 1
                                                        cell.api.Borders(border_id).Weight = 2
                                                linha_inicial += 1

                                    linha_total = linha_inicial
                                    range_total = f"A{linha_total}:G{linha_total}"
                                    sheet.range(range_total).merge()
                                    sheet[f"A{linha_total}"].value = "Total:"
                                    sheet[f"A{linha_total}"].font.bold = True
                                    sheet[f"A{linha_total}"].api.HorizontalAlignment = -4152

                                    sheet[f"H{linha_total}"].formula = f"=SUM(H{linha_primeiro_item}:H{linha_inicial - 1})"
                                    sheet[f"H{linha_total}"].font.bold = True
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
                                    linha_inicial = 15
                                    linha_primeiro_item = linha_inicial

                                    for item in edital["item"]:
                                        sheet[f"A{linha_inicial}"].value = item["codigo"]
                                        sheet[f"B{linha_inicial}"].value = item["descricao"]
                                        sheet[f"C{linha_inicial}"].value = item["unidade"]
                                        sheet[f"F{linha_inicial}"].value = item["quantidade"]
                                        sheet[f"H{linha_inicial}"].formula = f"=F{linha_inicial}*G{linha_inicial}"


                                        intervalo = f"A{linha_inicial}:G{linha_inicial}"
                                        for cell in sheet.range(intervalo):
                                            for border_id in range(7, 13):
                                                cell.api.Borders(border_id).LineStyle = 1
                                                cell.api.Borders(border_id).Weight = 2
                                        linha_inicial += 1

                                    linha_total = linha_inicial
                                    range_total = f"A{linha_total}:G{linha_total}"
                                    sheet.range(range_total).merge()
                                    sheet[f"A{linha_total}"].value = "Total:"
                                    sheet[f"A{linha_total}"].font.bold = True
                                    sheet[f"A{linha_total}"].api.HorizontalAlignment = -4152

                                    sheet[f"H{linha_total}"].formula = f"=SUM(H{linha_primeiro_item}:H{linha_inicial - 1})"
                                    sheet[f"H{linha_total}"].font.bold = True
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
                                
                                for i, anexo in enumerate(edital["anexo"]):
                                    if not self._is_running:
                                        break
                                    
                                    try:
                                        # Informações básicas do anexo
                                        url = anexo["url"]
                                        original_filename = anexo.get("nome", f"anexo_{i+1}")
                                        
                                        self.progress.emit(f"Baixando anexo: {original_filename}")
                                        
                                        # Configurar sessão com retry automático
                                        session = requests.Session()
                                        
                                        # Configurar retry com backoff exponencial
                                        retries = Retry(
                                            total=5,  # Número total de tentativas
                                            backoff_factor=1,  # Fator de backoff entre tentativas
                                            status_forcelist=[429, 500, 502, 503, 504],  # Códigos de erro para retry
                                            allowed_methods=["GET", "POST"]  # Métodos permitidos para retry
                                        )
                                        
                                        # Aplicar configuração de retry ao adapter
                                        adapter = HTTPAdapter(max_retries=retries)
                                        session.mount("http://", adapter)
                                        session.mount("https://", adapter)
                                        
                                        # Headers universais que simulam um navegador completo
                                        headers = {
                                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                                            'Accept': '*/*',  # Aceita qualquer tipo de conteúdo
                                            'Accept-Encoding': 'gzip, deflate, br',
                                            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                                            'Connection': 'keep-alive',
                                            'Sec-Fetch-Dest': 'document',
                                            'Sec-Fetch-Mode': 'navigate',
                                            'Sec-Fetch-Site': 'cross-site',
                                            'Sec-Fetch-User': '?1',
                                            'Upgrade-Insecure-Requests': '1',
                                            'Cache-Control': 'max-age=0'
                                        }
                                        
                                        # Fazer a requisição com opções avançadas
                                        try:
                                            self.progress.emit("Iniciando requisição de download...")
                                            response = session.get(
                                                url, 
                                                headers=headers,
                                                stream=True,  # Importante para arquivos grandes
                                                timeout=(10, 60),  # (timeout de conexão, timeout de leitura)
                                                allow_redirects=True,  # Seguir redirecionamentos
                                                verify=True  # Verificar SSL por padrão
                                            )
                                            
                                            # Se falhar com SSL, tentar novamente sem verificar
                                            if response.status_code >= 400:
                                                self.progress.emit("Tentando download sem verificação de SSL...")
                                                response = session.get(
                                                    url, 
                                                    headers=headers,
                                                    stream=True,
                                                    timeout=(10, 60),
                                                    allow_redirects=True,
                                                    verify=False  # Ignorar erros de SSL
                                                )
                                            
                                            response.raise_for_status()
                                            
                                            # Log do sucesso da requisição
                                            self.progress.emit(f"Requisição bem-sucedida: {response.status_code}")
                                            
                                            # Processa o filename
                                            filename = original_filename
                                            caracteres_proibidos = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
                                            
                                            # Verificar se há um nome de arquivo no header Content-Disposition
                                            if 'Content-Disposition' in response.headers:
                                                content_disp = response.headers['Content-Disposition']
                                                if 'filename=' in content_disp:
                                                    parts = content_disp.split('filename=')
                                                    if len(parts) > 1:
                                                        extracted = parts[1].strip()
                                                        if extracted.startswith('"') and extracted.endswith('"'):
                                                            extracted = extracted[1:-1]
                                                        elif extracted.startswith("'") and extracted.endswith("'"):
                                                            extracted = extracted[1:-1]
                                                        
                                                        if extracted:
                                                            filename = extracted
                                            
                                            # Se filename ainda não tem extensão, tentar determinar pelo Content-Type
                                            if not os.path.splitext(filename)[1]:
                                                content_type = response.headers.get('Content-Type', '').lower()
                                                
                                                if 'pdf' in content_type:
                                                    filename = f"{filename}.pdf"
                                                elif any(x in content_type for x in ['excel', 'spreadsheet', 'xlsx']):
                                                    filename = f"{filename}.xlsx"
                                                elif any(x in content_type for x in ['word', 'document', 'docx']):
                                                    filename = f"{filename}.docx"
                                                elif any(x in content_type for x in ['zip', 'compressed']):
                                                    filename = f"{filename}.zip"
                                                elif 'image/jpeg' in content_type:
                                                    filename = f"{filename}.jpg"
                                                elif 'image/png' in content_type:
                                                    filename = f"{filename}.png"
                                                else:
                                                    # Para outros casos, o mais comum costuma ser PDF
                                                    filename = f"{filename}.pdf"
                                            
                                            # Limpar caracteres inválidos do nome do arquivo
                                            filename = ''.join(c for c in filename if c not in caracteres_proibidos)
                                            
                                            # Verificar tamanho do arquivo antes de baixar
                                            total_size = int(response.headers.get('content-length', 0))
                                            if total_size > 0:
                                                self.progress.emit(f"Tamanho do arquivo: {total_size / (1024*1024):.2f} MB")
                                            
                                            # Definir o caminho de destino
                                            file_path = os.path.join(os.getcwd(), filename)
                                            
                                            # Salvar o arquivo em chunks para melhor gerenciamento de memória
                                            with open(file_path, 'wb') as f:
                                                downloaded = 0
                                                for chunk in response.iter_content(chunk_size=8192):
                                                    if chunk:
                                                        f.write(chunk)
                                                        downloaded += len(chunk)
                                                        # Log opcional de progresso para arquivos grandes
                                                        if total_size > 10*1024*1024 and downloaded % (1024*1024) < 8192:  # Log a cada ~1MB 
                                                            self.progress.emit(f"Baixando... {downloaded / (1024*1024):.1f}MB / {total_size / (1024*1024):.1f}MB")
                                            
                                            # Verificar se arquivo foi salvo e possui conteúdo
                                            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                                                self.progress.emit(f"✓ Download concluído: {filename} ({os.path.getsize(file_path) / 1024:.1f} KB)")
                                            else:
                                                raise Exception("Arquivo vazio ou não foi salvo corretamente")
                                                
                                        except Exception as e:
                                            self.error.emit(f"❌ Erro no download do anexo: {str(e)}")
                                        
                                    except Exception as e:
                                        self.error.emit(f"❌ Erro ao processar anexo {original_filename}: {str(e)}")
                                
                                self.progress.emit("✔ Processo de download dos anexos concluído")
                                
                            except Exception as e:
                                self.error.emit(f"❌ Erro geral no sistema de download: {str(e)}")
                            finally:
                                os.chdir(pathOriginal)
                    
                    if self.cotacao_document.isChecked():
                        try:
                            os.chdir("PROPOSTA DE PREÇO")
                            
                            # Obter nome e extensão do arquivo original
                            nome_original = os.path.basename(user_settings["cotacao_document"])
                            nome_sem_ext, extensao = os.path.splitext(nome_original)
                            
                            # Criar novo nome com o ID do edital
                            novo_nome = f"{nome_sem_ext}_{edital['id']}{extensao}"
                            
                            # Copiar arquivo para a pasta com o novo nome
                            shutil.copy(user_settings["cotacao_document"], novo_nome)
                            
                            # Usar o novo nome para o resto do processamento
                            caminho_planilha = novo_nome
                            
                            app = xw.App(visible=False)
                            workbook = app.books.open(caminho_planilha)
                            sheet = workbook.sheets[0]
                            sheet.range("C4").value = edital["id"]
                            
                            try: 
                                linha_inicial = 8
                                linha_primeiro_item = linha_inicial

                                for item in edital["item"]:
                                    sheet[f"A{linha_inicial}"].value = item["codigo"]
                                    sheet[f"B{linha_inicial}"].value = item["descricao"]
                                    sheet[f"C{linha_inicial}"].value = item["unidade"]
                                    sheet[f"F{linha_inicial}"].value = item["quantidade"]
                                    sheet[f"H{linha_inicial}"].formula = f"=F{linha_inicial}*G{linha_inicial}"

                                    intervalo = f"A{linha_inicial}:G{linha_inicial}"
                                    for cell in sheet.range(intervalo):
                                        for border_id in range(7, 13):
                                            cell.api.Borders(border_id).LineStyle = 1
                                            cell.api.Borders(border_id).Weight = 2
                                    linha_inicial += 1

                                linha_total = linha_inicial
                                range_total = f"A{linha_total}:G{linha_total}"
                                sheet.range(range_total).merge()
                                sheet[f"A{linha_total}"].value = "Total:"
                                sheet[f"A{linha_total}"].font.bold = True
                                sheet[f"A{linha_total}"].api.HorizontalAlignment = -4152

                                sheet[f"H{linha_total}"].formula = f"=SUM(H{linha_primeiro_item}:H{linha_inicial - 1})"
                                sheet[f"H{linha_total}"].font.bold = True
                                self.progress.emit(f"✔ Cotação preenchida com sucesso e salva como {novo_nome}")
                            except Exception as e:
                                self.error.emit(f"❌ Erro no preenchimento da cotação: {str(e)}")
                            finally:
                                workbook.save()
                                workbook.close()
                                app.quit()
                                os.chdir(pathOriginal)
                            
                        except Exception as e:
                            self.error.emit(f"❌ Erro no preenchimento da cotação: {str(e)}")
                        
                    if self.assign_pdf.isChecked():
                        try:
                            self.progress.emit("\nIniciando processo de assinatura digital de PDFs...")
                            
                            # Verificar se existe o PDF convertido da declaração
                            os.chdir("DECLARACOES E ANEXOS")
                            pdf_files = glob.glob("*.pdf")
                            
                            if not pdf_files:
                                self.error.emit("❌ Nenhum arquivo PDF encontrado para assinar na pasta DECLARACOES E ANEXOS")
                            else:
                                # Para cada PDF na pasta de declarações, assinar o documento
                                for pdf_file in pdf_files:
                                    self.progress.emit(f"\nProcessando assinatura do arquivo: {pdf_file}")
                                    pdf_path = os.path.join(os.getcwd(), pdf_file)
                                    
                                    # Processar a assinatura
                                    resultado = self.processar_assinatura_pdf(pdf_path, user_settings)
                                    
                                    if resultado:
                                        self.progress.emit(f"✅ Assinatura do arquivo {pdf_file} concluída com sucesso!")
                                    else:
                                        self.error.emit(f"❌ Falha ao assinar o arquivo {pdf_file}")
                            
                            # Voltar ao diretório original
                            os.chdir(pathOriginal)
                            
                        except Exception as e:
                            self.error.emit(f"❌ Erro no processo de assinatura digital: {str(e)}")
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