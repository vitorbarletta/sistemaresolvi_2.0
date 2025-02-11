from qt_core import *
import requests
import json               
import pandas as pd

class RequestWorker(QThread):
    finished = Signal(list)
    progress = Signal(str)
    error = Signal(str)
    
    def __init__(self, quantidade, perfil, portais, consumir_planilha):
        super().__init__()
        self.quantidade = str(quantidade)
        self.perfil = int(perfil)
        self.portais = [int(p.strip()) for p in portais.split(',')] if portais else []
        self.consumir_planilha = consumir_planilha

    def run(self):
        
        idEffecti = 5628725
        try:
            self.progress.emit("Iniciando login...")

            urlLogin = "https://mdw.minha.effecti.com.br/users/login"
            payloadLogin = {
                "username": "resolvi.consultoria@gmail.com",
                "password": "Consultoria2023#"
            }
            headersLogin = {"Content-Type": "application/json"}
            
            responseLogin = requests.post(urlLogin, json=payloadLogin, headers=headersLogin)
            
            if responseLogin.status_code == 200:
                data = responseLogin.json()
                token = data.get("token")
                self.progress.emit("Login realizado com sucesso!")

                headers = {
                    "Authorization": f"Bearer {token}",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
                    "Accept": "application/json, text/plain, */*",
                    "Content-Type": "application/json"
                }
                
                if self.consumir_planilha == False:
                    payloadAvisos = {
                        "pagina": 0,
                        "interesse": True,
                        "favorito": False,
                        "orgaoFavorito": False,
                        "distribuidores": False,
                        "id": "",
                        "deserto": False,
                        "ordem": [{"orderBy": "dataEnvioEmail"}, {"order": "desc"}],
                        "tipo": [],
                        "dataPublicacao": {"equal": "", "less": "", "more": ""},
                        "dataInicial": {"equal": "", "less": "", "more": ""},
                        "dataFinal": {"equal": "", "less": "", "more": ""},
                        "dataEnvioEmail": {"equal": "", "less": "", "more": ""},
                        "portal": self.portais,
                        "perfil": [self.perfil],
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
                    
                    self.progress.emit("Buscando editais...")
                    urlData = "https://mdw.minha.effecti.com.br/aviso/minhas"
                    responseData = requests.post(urlData, headers=headers, json=payloadAvisos)

                    if responseData.status_code == 200:
                        response_json = responseData.json()
                        processed_data = []  # Initialize as list instead of dict
                        self.progress.emit("Buscando editais...")
                        
                        # Process each edital in the data array
                        for edital in response_json.get("data", []):
                            
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

                                # Process items
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

                        try:
                            with open('data.json', 'w', encoding='utf-8') as f:
                                json.dump(processed_data, f, indent=4, ensure_ascii=False)
                            self.progress.emit("Dados processados e salvos em data.json")
                        except Exception as e:
                            self.error.emit(f"Erro ao salvar arquivo: {str(e)}")

                        self.finished.emit(processed_data)
                    else:
                        self.error.emit(f"Erro ao buscar editais: {responseData.status_code} - {responseData.text}")
                else:
                    with open('user_settings.json', 'r', encoding='utf-8') as f:
                        user_settings = json.load(f)
                        sheet_ids = user_settings.get("sheet_ids")
                    
                    df = pd.read_excel(sheet_ids)

                    editais = []
                    self.progress.emit("Buscando editais...")
                    for index, row in df.iterrows():
                        if isinstance(row.iloc[1], int):
                            itens = [row.iloc[1]]
                        else:
                            itens = [int(item.strip()) for item in str(row.iloc[1]).split('-') if item.strip() and item.strip().isdigit()]
                        edital ={
                            'id': row.iloc[0],
                            'itens': itens,
                        }
                        editais.append(edital)
                    
                    processed_data = []
                        
                    for edital in editais:                   
                        urlData = f"https://mdw.minha.effecti.com.br/aviso/edital/{edital["id"]}"
                        
                        responseData = requests.get(urlData, headers=headers)

                        if responseData.status_code == 200:
                            data_content = responseData.json()  
                        
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

                            # Process items
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

                            # Process attachments
                            for anexo in data_content.get("attachments", []):
                                processed_anexo = {
                                    "codigo": anexo.get("id"),
                                    "nome": anexo.get("name", ""),
                                    "url": anexo.get("url", "")
                                }
                                processed_edital["anexo"].append(processed_anexo)

                            processed_data.append(processed_edital)
                        else:
                            self.error.emit(f"Erro ao pegar os dados: {responseData.status_code}")
                            
                    try:
                        with open('data.json', 'w', encoding='utf-8') as f:
                            json.dump(processed_data, f, indent=4, ensure_ascii=False)
                        self.progress.emit(f"Edital {edital['id']} processado e salvo")
                    except Exception as e:
                        self.error.emit(f"Erro ao salvar arquivo: {str(e)}")

                    self.finished.emit(processed_data)
            else:
                self.error.emit(f"Erro no login: {responseLogin.status_code} - {responseLogin.text}")

        except Exception as e:
            self.error.emit(str(e))