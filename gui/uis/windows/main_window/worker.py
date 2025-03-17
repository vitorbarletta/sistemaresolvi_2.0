from qt_core import *
import requests
import json               
import pandas as pd
import os
from typing import List, Dict, Any, Optional
import traceback

class RequestWorker(QThread):
    finished = Signal(list)
    progress = Signal(str)
    error = Signal(str)
    
    def __init__(self, quantidade, perfil, portais, consumir_planilha, data_inicial=None, data_final=None, favoritos=True):
        super().__init__()
        # Mantém o valor original da quantidade (pode ser vazio)
        self.quantidade_original = quantidade
        # Se quantidade estiver vazia, inicializa com "1" para a primeira requisição
        self.quantidade = str(quantidade) if quantidade and quantidade.strip() else "1"
        self.perfil = (perfil) if perfil else None
        self.portais = (portais) if portais else None
        self.consumir_planilha = consumir_planilha
        self.data_inicial = data_inicial if data_inicial else ""
        self.data_final = data_final if data_final else ""
        self.token = None
        self.headers = None
        self.favoritos = favoritos
        # Indica se é necessário fazer uma segunda requisição com o recordsTotal
        self.necessita_segunda_requisicao = not (quantidade and quantidade.strip())

    def run(self):
        try:
            if not self._realizar_login():
                return
            
            if self.consumir_planilha:
                self._processar_planilha()
            else:
                self._buscar_editais_regulares()
        except Exception as e:
            self.error.emit(f"Erro crítico: {str(e)}")
    
    def _realizar_login(self) -> bool:
        """Realiza o login na API e retorna True se bem-sucedido"""
        self.progress.emit("Iniciando login...")

        try:
            url_login = "https://mdw.minha.effecti.com.br/users/login"
            payload_login = {
                "username": "resolvi.consultoria@gmail.com",
                "password": "Consultoria2023#"
            }
            headers_login = {"Content-Type": "application/json"}
            
            response_login = requests.post(url_login, json=payload_login, headers=headers_login, timeout=30)
            
            if response_login.status_code == 200:
                data = response_login.json()
                self.token = data.get("token")
                
                if not self.token:
                    self.error.emit("Token não encontrado na resposta de login")
                    return False
                    
                self.headers = {
                    "Authorization": f"Bearer {self.token}",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
                    "Accept": "application/json, text/plain, */*",
                    "Content-Type": "application/json"
                }
                self.progress.emit("Login realizado com sucesso!")
                return True
            else:
                self.error.emit(f"Erro no login: {response_login.status_code} - {response_login.text}")
                return False
        except requests.RequestException as e:
            self.error.emit(f"Erro de conexão durante login: {str(e)}")
            return False
        except json.JSONDecodeError:
            self.error.emit("Erro ao processar resposta do servidor")
            return False
        except Exception as e:
            self.error.emit(f"Erro inesperado durante login: {str(e)}")
            return False
    
    def _buscar_editais_regulares(self):
        """Busca editais conforme configuração básica"""
        self.progress.emit("Buscando editais...")
        
        try:
            # Primeira requisição para obter o recordsTotal quando quantidade original estiver vazia
            if self.necessita_segunda_requisicao:
                self.progress.emit("Realizando consulta preliminar para determinar total de registros...")
                payload_preliminar = self._criar_payload_busca()
                url_data = "https://mdw.minha.effecti.com.br/aviso/minhas"
                
                response_preliminar = requests.post(
                    url_data, 
                    headers=self.headers, 
                    json=payload_preliminar,
                    timeout=60
                )
                
                if response_preliminar.status_code != 200:
                    self.error.emit(f"Erro na consulta preliminar: {response_preliminar.status_code} - {response_preliminar.text}")
                    return
                    
                response_json_preliminar = response_preliminar.json()
                records_total = response_json_preliminar.get("recordsTotal", 0)
                
                if records_total <= 0:
                    self.progress.emit("Nenhum edital encontrado.")
                    self.finished.emit([])
                    return
                    
                self.progress.emit(f"Encontrados {records_total} editais no total. Buscando dados completos...")
                # Atualiza a quantidade para a segunda requisição
                self.quantidade = str(records_total)
            
            # Continua com a requisição normal (a segunda, se necessário)
            payload_avisos = self._criar_payload_busca()
            url_data = "https://mdw.minha.effecti.com.br/aviso/minhas"
            
            response_data = requests.post(
                url_data, 
                headers=self.headers, 
                json=payload_avisos,
                timeout=60
            )
            
            if response_data.status_code != 200:
                self.error.emit(f"Erro ao buscar editais: {response_data.status_code} - {response_data.text}")
                return
                
            response_json = response_data.json()
            editais_data = response_json.get("data", [])
            
            if not editais_data:
                self.progress.emit("Nenhum edital encontrado.")
                self.finished.emit([])
                return
                
            processed_data = self._processar_editais(editais_data)
            self._salvar_dados(processed_data)
            self.finished.emit(processed_data)
            
        except requests.RequestException as e:
            self.error.emit(f"Erro de conexão ao buscar editais: {str(e)}")
        except json.JSONDecodeError:
            self.error.emit("Erro ao interpretar resposta do servidor")
        except Exception as e:
            self.error.emit(f"Erro ao buscar editais: {str(e)}")
    
    def _criar_payload_busca(self) -> Dict:
        """Cria o payload para busca de editais"""
        return {
            "pagina": 0,
            "interesse": True,
            "favorito": self.favoritos,
            "orgaoFavorito": False,
            "distribuidores": False,
            "id": "",
            "deserto": False,
            "ordem": [{"orderBy": "dataEnvioEmail"}, {"order": "desc"}],
            "tipo": [],
            "dataPublicacao": {"equal": "", "less": "", "more": ""},
            "dataInicial": {"equal": "", "less": "", "more": ""},
            "dataFinal": {"equal": "", 
                        "less": self.data_final if self.data_final else "", 
                        "more": self.data_inicial if self.data_inicial else ""},
            "dataEnvioEmail": {"equal": "", "less": "", "more": ""},
            "portal": [self.portais] if self.portais is not None else [],
            "perfil": [self.perfil] if self.perfil is not None else [],
            "pregao": "",
            "uasg": "",
            "uasgNome": "",
            "uf": [],
            "esferas": [],
            "cidades": [],
            "palavrasChave": [],
            "exclusivoMeEpp": [],
            "keywordsGroupSelected": {"items": []},
            "comunicadoSelected": [],
            "tamanho": self.quantidade,
            "search": "",
            "modificado": False,
            "grupoPalavras": []
        }
    
    def _processar_editais(self, editais: List[Dict]) -> List[Dict]:
        """Processa os editais recebidos da API"""
        processed_data = []
        
        for edital in editais:
            try:
                processed_edital = {
                    "id": edital.get("id"),
                    "objeto": edital.get("objeto", ""),
                    "portal": edital.get("portal"),
                    "portalNome": edital.get("portalNome", ""),
                    "perfil": edital.get("perfil", ""),
                    "pregao": edital.get("pregao", ""),
                    "uasgNome": edital.get("uasgNome", ""),
                    "url": edital.get("url", ""),
                    "item": [],
                    "anexo": [],
                    "dataInicial": edital.get("dataInicial", ""),
                    "dataFinal": edital.get("dataFinal", ""),
                    "uasg": edital.get("uasg", ""),
                    "orgao": edital.get("orgao"),
                    "uf": edital.get("uf", ""),
                    "tipo": edital.get("tipo", ""),
                    "anotacoes": edital.get("anotacoes", []),
                    "planilhaConsumida": False
                }

                # Processa itens
                for item in edital.get("item", []):
                    processed_item = {
                        "codigo": item.get("codigo"),
                        "tipo": item.get("tipo", 2),
                        "grupo": item.get("grupo", ""),
                        "objeto": item.get("objeto", ""),
                        "unidade": item.get("unidade", "UNIDADE"),
                        "exclusivoMeEpp": item.get("exclusivoMeEpp", 0),
                        "quantidade": item.get("quantidade", ""),
                        "decreto7174": item.get("decreto7174", 0),
                        "descricao": item.get("descricao", "")
                    }
                    processed_edital["item"].append(processed_item)

                # Processa anexos
                for anexo in edital.get("anexo", []):
                    processed_anexo = {
                        "codigo": anexo.get("codigo"),
                        "nome": anexo.get("nome", ""),
                        "url": anexo.get("url", "")
                    }
                    processed_edital["anexo"].append(processed_anexo)

                processed_data.append(processed_edital)

            except Exception as e:
                self.error.emit(f"Erro ao processar edital: {str(e)}")
                continue
                
        return processed_data
    
    def _processar_planilha(self):
        """Processa os editais através de uma planilha"""
        try:
            # Carrega configurações do usuário
            with open('user_settings.json', 'r', encoding='utf-8') as f:
                user_settings = json.load(f)
                sheet_path = user_settings.get("sheet_ids")
                
            if not os.path.exists(sheet_path):
                self.error.emit(f"Arquivo de planilha não encontrado: {sheet_path}")
                return
                
            # Carrega a planilha
            try:
                df = pd.read_excel(sheet_path)
                self.progress.emit("Planilha carregada com sucesso.")
            except Exception as e:
                self.error.emit(f"Erro ao carregar planilha: {str(e)}")
                return
                
            # Extrai IDs dos editais e itens
            editais = []
            for index, row in df.iterrows():
                try:
                    edital_id = row.iloc[0]
                    if pd.isna(edital_id):
                        continue
                        
                    if isinstance(row.iloc[1], int):
                        itens = [row.iloc[1]]
                    else:
                        itens = [int(item.strip()) for item in str(row.iloc[1]).split('-') 
                                if item.strip() and item.strip().isdigit()]
                                
                    editais.append({
                        'id': edital_id,
                        'itens': itens,
                    })
                except Exception as e:
                    self.error.emit(f"Erro ao processar linha {index+1} da planilha: {str(e)}")
            
            if not editais:
                self.error.emit("Nenhum edital válido encontrado na planilha")
                return
                
            self.progress.emit(f"Encontrados {len(editais)} editais na planilha")
            processed_data = self._obter_detalhes_editais_planilha(editais)
            
            if processed_data:
                self._salvar_dados(processed_data)
                self.finished.emit(processed_data)
            else:
                self.error.emit("Não foi possível processar os editais da planilha")
                
        except Exception as e:
            self.error.emit(f"Erro ao processar planilha: {str(e)}")
            
    def _obter_detalhes_editais_planilha(self, editais: List[Dict]) -> List[Dict]:
        """Obtém detalhes dos editais especificados na planilha"""
        processed_data = []
        
        for edital in editais:
            try:
                self.progress.emit(f"Buscando detalhes do edital {edital['id']}...")
                url_data = f"https://mdw.minha.effecti.com.br/aviso/edital/{edital['id']}"
                
                response = requests.get(url_data, headers=self.headers, timeout=30)
                
                if response.status_code != 200:
                    self.error.emit(f"Erro ao buscar edital {edital['id']}: {response.status_code}")
                    continue
                    
                data_content = response.json()
                
                processed_edital = {
                    "id": data_content.get("id"),
                    "objeto": data_content.get("object", ""),
                    "portal": data_content.get("portalCode"),
                    "portalNome": data_content.get("portal", ""),
                    "perfil": data_content.get("perfil", ""),
                    "pregao": data_content.get("tradding", ""),
                    "uasgNome": data_content.get("uasgName", ""),
                    "url": data_content.get("url", ""),
                    "item": [],
                    "anexo": [],
                    "dataInicial": data_content.get("dateInitial", ""),
                    "dataFinal": data_content.get("dateFinal", ""),
                    "uasg": data_content.get("uasg", ""),
                    "orgao": data_content.get("organ"),
                    "uf": data_content.get("uf", ""),
                    "tipo": data_content.get("modality", ""),
                    "anotacoes": data_content.get("extra", []),
                    "orgaoDetalhe": data_content.get("organDetails", {}),
                    "planilhaConsumida": True,
                    "editaisValidos": editais
                }
                
                # Processa itens
                for item in data_content.get("items", []):
                    processed_item = {
                        "codigo": item.get("id"),
                        "tipo": 2,  # Default value for material
                        "grupo": item.get("group", ""),
                        "objeto": item.get("object", ""),
                        "unidade": item.get("unity", "UNIDADE"),
                        "exclusivoMeEpp": item.get("exclusiveMeEpp", 0),
                        "quantidade": str(item.get("amount", "")),
                        "decreto7174": 1 if item.get("decree7174") else 0,
                        "descricao": item.get("object", "")
                    }
                    processed_edital["item"].append(processed_item)
                
                # Processa anexos
                for anexo in data_content.get("attachments", []):
                    processed_anexo = {
                        "codigo": anexo.get("id"),
                        "nome": anexo.get("name", ""),
                        "url": anexo.get("url", "")
                    }
                    processed_edital["anexo"].append(processed_anexo)
                
                processed_data.append(processed_edital)
                self.progress.emit(f"Edital {edital['id']} processado com sucesso")
                
            except requests.RequestException as e:
                self.error.emit(f"Erro de conexão ao buscar edital {edital['id']}: {str(e)}")
            except json.JSONDecodeError:
                self.error.emit(f"Erro ao processar resposta do edital {edital['id']}")
            except Exception as e:
                self.error.emit(f"Erro ao processar edital {edital['id']}: {str(e)}")
                
        return processed_data
    
    def _salvar_dados(self, data: List[Dict]) -> None:
        """Salva os dados processados em um arquivo JSON"""
        try:
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            self.progress.emit(f"Dados processados e salvos em data.json ({len(data)} editais)")
        except Exception as e:
            self.error.emit(f"Erro ao salvar arquivo: {str(e)}")