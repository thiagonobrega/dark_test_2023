from json import dumps
from uuid import uuid4

from .base_client import BaseClient
from config import HYPERDRIVE_URI, RESOLVER_URI
from utils.request import APIRequest


class HyperDriveClient(BaseClient):
    def __init__(self, hyperdrive_version='sync'):
        super().__init__()

        if hyperdrive_version == 'sync':
            self.add_url_path = "/core/set/"
            self.set_url_path = "/core/set/"
        elif hyperdrive_version == 'async':
            self.add_url_path = "/core/add/"
            self.set_url_path = "/core/set/"
        else:
            raise ValueError(f"ERROR - hyperdriver version unknow [{hyperdrive_version}]")

        self.new_url_path = "/core/new"
        self.api_root_url = HYPERDRIVE_URI
        self.request = APIRequest()

    def request_pid(self, body=None):
        response = self.__request_pid(body)
        return response
    
    def add_url(self, pid:str, url:str):
        cmd_url = f"{self.api_root_url}{self.add_url_path}{pid}"
        payload = {
                    'external_url' : url
        }
        response = self.__update_pid(cmd_url,pid,payload)
        return pid, payload , response

    def add_external_pid(self, pid:str, external_pid:str):
        cmd_url = f"{self.api_root_url}{self.add_url_path}{pid}"
        payload = {
                    'external_pid' : external_pid
        }
        response = self.__update_pid(cmd_url,pid,payload)
        return pid, payload , response
    
    def set_payload(self, pid:str, payload:str):
        cmd_url = f"{self.api_root_url}{self.set_url_path}{pid}"
        post_payload = {
                    'payload' : payload
        }
        response = self.__update_pid(cmd_url,pid,post_payload)
        return pid, post_payload , response

    # private methods
    def __request_pid(self, body=None):
        cmd_url = f"{self.api_root_url}{self.new_url_path}"
        response = self.request.get(cmd_url)
        return response
    
    def __update_pid(self, cmd_url:str, pid:str, payload:dict):
        if isinstance(payload, dict):
            response = self.request.post(cmd_url, payload, self.headers)
        else:
            raise ValueError("ERROR - Parameter 'payload' should be of Type Dict")
        return response

class ResolverClient(BaseClient):
    def __init__(self):
        super().__init__()

        self.get_url_path = "/get/"
        self.api_root_url = RESOLVER_URI
        self.request = APIRequest()
    
    def get(self, pid, pid_type='ark'):
        response = self.__get_pid(f"{pid_type}:/{pid}")
        return response
    
    def __get_pid(self, pid):
        cmd_url = f"{self.api_root_url}{self.get_url_path}{pid}"
        response = self.request.get(cmd_url)
        return response