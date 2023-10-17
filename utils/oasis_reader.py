import ijson
import zipfile
import pandas as pd

def processar_item(doc,remove_att_list, att_name_list):
    for att in remove_att_list:
        try:
            del doc[att]
        except KeyError:
            pass
                            
                            #converte as listas
    for att in att_name_list:
        try:
            if len(doc[att]) > 1:
                doc[att] =';'.join(doc[att])
            else:
                doc[att] = doc[att][0]     
        except KeyError:
            pass
    
    return doc

def extract_itens_from_json(input_file_path, filtro_inst=None, remove_att_list=None):
    """
    - id - o id do documento no Oasisbr
    - oai_identifier_str - id externo que vem do repositório de origem
    - instname_str - nome da instituição de origem
    - instacron_str - acrônimo da instituição de origem
    - network_acronym_str - acrônimo da rede de origem (pode descartar)
    - network_name_str - nome da rede origem (pode descartar)
    - title - título
    - author - autores
    - publishDate  - data da publicação
    - format - tipo de documento (article, masterThesis, doctoralThesis, …)
    - description - abstract
    - topic - keywords
    - language - idioma do documento
    - eu_rights_str_mv - tipo de acesso (openAccess, closed, …)
    - url - url externa para o documento
    """
    set_of_itens = []
    i = 0

    # lista de atributos que sao lista
    att_name_list = ['author', 'format', 'url', 'language', 'eu_rights_str_mv', 'publishDate', 'topic']

    with zipfile.ZipFile(input_file_path, "r") as zip_file:
        filename= zip_file.namelist()[0]
    
        with zip_file.open(filename) as json_file:
            parser = ijson.parse(json_file)

        # Inicie o parsing do JSON
            in_docs = False
            for prefix, event, value in parser:
                if in_docs:
                    if event == 'start_map':
                        doc = {}  # Inicie um novo dicionário para cada documento "docs"
                    elif event == 'end_map':
                        # leu tudo
                        
                        doc_clean = processar_item(doc,remove_att_list, att_name_list)

                        if filtro_inst!= None:
                            try:
                                if filtro_inst.get(doc_clean['instacron_str']) != None:
                                    set_of_itens.append(doc_clean)
                            except KeyError:
                                pass
                        else:
                            set_of_itens.append(doc_clean)
                            

                    else:
                        # processa o json
                        short_prefix = prefix.split('.item.')[-1]
                        if (short_prefix != 'response.docs.item' and value != None):
                            short_prefix = short_prefix.split('.')[0]
                            # print("\t ",short_prefix,value)
                            # verifica se o atributo e do tipo lista
                            if short_prefix in att_name_list:
                                if short_prefix not in doc:
                                    doc[short_prefix] = []
                                    doc[short_prefix].append(value)
                                else:
                                    doc[short_prefix].append(value)
                            else: # adiciona valores que nao sao lista
                                doc[short_prefix] =  value              

                elif prefix == 'response.docs':
                    in_docs = True

    # Certifique-se de fechar o arquivo após a leitura
    zip_file.close()
    json_file.close()
    return set_of_itens

