import ijson
import zipfile
import pandas as pd


def extract_itens_from_json(input_file_path, target_inst=None):
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
                    # Faça algo com o documento, por exemplo, imprimir ou processar
                    # i+=1
                    # if i > limit:
                    #     break
                        if target_inst!= None:
                            try:
                                if target_inst.get(doc['instacron_str']) != None:
                                    set_of_itens.append(doc)
                            except KeyError:
                                pass
                        else:
                            set_of_itens.append(doc)
                    else:
                        short_prexif = prefix.split('.')[-1]
                        if short_prexif != 'item':
                            doc[short_prexif] = value
                elif prefix == 'response.docs':
                    in_docs = True

    # Certifique-se de fechar o arquivo após a leitura
    zip_file.close()
    json_file.close()
    return set_of_itens