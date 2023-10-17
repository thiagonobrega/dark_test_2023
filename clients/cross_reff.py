import requests

# Título da publicação que você deseja pesquisar
titulo_publicacao = "Incremental Entity Blocking over Heterogeneous Streaming Data"


class CrossrefClient():
    def __init__(self):
        self.__crossref_base_url = "https://api.crossref.org"
        self.__doi_query_url = "/works?query.title="

    def get_doi_by_title(self, title: str) -> str:
        query_url = self.__crossref_base_url + self.__doi_query_url + title
        response = requests.get(query_url)

        if response.status_code == 200:
            data = response.json()['message']
            
            if "items" in data and len(data["items"]) > 0:
                doi = data["items"][0]["DOI"]
                return doi
        
        return None
