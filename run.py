import time, sys , os
import configparser
import argparse


import pandas as pd

from dark import DarkGateway

from utils.oasis_reader import extract_itens_from_json
from clients import CrossrefClient, HyperDriveClient


def getDarkGateway():
    PROJECT_ROOT = "./"
    bc_config = configparser.ConfigParser()
    deployed_contracts_config = configparser.ConfigParser()
    
    bc_config.read(os.path.join(PROJECT_ROOT, "notebooks"+os.sep+"config.ini"))
    deployed_contracts_config.read(os.path.join(PROJECT_ROOT, "notebooks"+os.sep+"deployed_contracts.ini"))
    dark_gw = DarkGateway(bc_config, deployed_contracts_config)
    return dark_gw

def measure_response_time(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    response_time = end_time - start_time
    return result, response_time

def measure_tx_params(dark_gw, cost_flag, func, *args, **kwargs):
    if cost_flag != False:
        initial_amount = dark_gw.get_account_balance()

    result, response_time = measure_response_time(func, *args, **kwargs)
    if cost_flag != False:
        final_amount = dark_gw.get_account_balance()
        tx_value = initial_amount - final_amount
    else:
        tx_value = 0
    
    return result, response_time , tx_value

##########

def get_pids(input_df,cost_flag):

    dark_gw = getDarkGateway()
    cc = HyperDriveClient()

    oasis_dark_map = {}

    for index, row in input_df.iterrows():

        oasis_id = row['id']
        oai_id   = row['oai_identifier_str']
        title    = row.get('title')
        tipo     = row.get('format')
        url      = row.get('url')
        # print(index)
        # request, resp_time = measure_response_time(cc.request_pid)
        try:
            request, resp_time, amount = measure_tx_params(dark_gw,cost_flag,cc.request_pid)
            try:
                ark = request.as_dict['ark']
                status = 'ok'
            except KeyError:
                ark = '-'
                status = 'error'
        
            oasis_dark_map[oasis_id] = {'dark' : ark, 'status' :  status , 'exec_time' : resp_time , 'amount' : amount , 'action' : 'assign_pid'}
        except Exception as e:
            print(f'\t\t > error ao salvar {oasis_id}')
            oasis_dark_map[oasis_id] = {'dark' : '-', 'status' :  'error' , 'exec_time' : 999 , 'amount' : 0 , 'action' : 'assign_pid' , 'error_detail' : e}

    return oasis_dark_map

def call_pid_method(cmd,input_df,pid_map,cost_flag):

    dark_gw = getDarkGateway()
    cc = HyperDriveClient(hyperdrive_version='async')
    cr_client = CrossrefClient()

    action_map = {}
    
    if cmd == 'add_url':
        call_func = cc.add_url
    elif cmd == 'add_external_pid':
        call_func = cc.add_external_pid
    elif cmd == 'set_payload':
        call_func = cc.set_payload
    else:
        raise Exception("Unknow Param")

    for index, row in input_df.iterrows():

        oasis_id = row['id']
        oai_id   = row['oai_identifier_str']
        title    = row.get('title')
        tipo     = row.get('format')
        url      = row.get('url')
        pdate    = row.get('publishDate')
        lang     = row.get('language')
        authors  = row.get('author')
        
        exec_flag = True


        dark_pid = pid_map[oasis_id]['dark']
        if cmd == 'add_url':
            request, resp_time, amount = measure_tx_params(dark_gw,cost_flag,call_func,dark_pid,url)
        elif cmd == 'add_external_pid':
            if tipo == 'article':
                doi = cr_client.get_doi_by_title(title)
                if doi != None:
                    doi = 'doi:/' + doi
                    request, resp_time, amount = measure_tx_params(dark_gw,cost_flag,call_func,dark_pid,doi)
                else:
                    exec_flag = False
            else:
                exec_flag = False

        elif cmd == 'set_payload':
            payload_data = '{' + f'title : {title}, authors : {authors}, publish_data: {pdate}, oai: {oai_id} , language: {lang}' + '}'
            request, resp_time, amount = measure_tx_params(dark_gw,cost_flag,call_func,dark_pid,payload_data)
            

        
        if exec_flag == True:
            # print(request[2])
            if request[2].status_code == 200:
                status = 'ok'
                action_map[oasis_id] = {'dark' : dark_pid, 'status' :  status , 'exec_time' : resp_time , 'amount' : amount , 'action' : cmd }
            else:
                status = 'error'
                action_map[oasis_id] = {'dark' : dark_pid, 'status' :  status , 'exec_time' : resp_time , 'amount' : amount , 'action' : cmd , 'error_detail' : request[2]}
            #
            
        
    
    
        

    return action_map




if __name__ == "__main__":
    # Configurar o parser de argumentos
    
    parser = argparse.ArgumentParser(description="HyperDrive Experiment Runner")
    parser.add_argument("name", type=str, help="Nome do experimento")
    parser.add_argument("file", type=str, help="Path do arquivo")
    parser.add_argument("sample_size", type=int, help="Tamanho do sample")
    parser.add_argument('--get-gas-cost', default=False, action='store_true',
                            help='Ativar o cálculo do custo de gás')

    args = parser.parse_args()
    
    name = args.name
    file = args.file
    get_gas_cost = args.get_gas_cost
    sample_size = args.sample_size

    

    if not name:
        sys.exit("Erro: O nome é obrigatório. Utilize o argumento 'name'.")
    if not file:
        sys.exit("Erro: O nome é obrigatório. Utilize o argumento 'file'.")
    if not sample_size:
        sys.exit("Erro: O nome é obrigatório. Utilize o argumento 'sample_size'.")
    
    sample_size = int(sample_size)

    print(f"Running {name} [ {sample_size} samples]")
    # df=pd.read_json('notebooks/pb-data.json')
    df=pd.read_json(file)

    sample_df = df.sample(sample_size)
    
    ##
    ## executar experimento
    ##
    print("\t Generating Pids")
    pid_map = get_pids(sample_df,get_gas_cost)

    print("\t Adding url")
    urls = call_pid_method('add_url',sample_df,pid_map,get_gas_cost)
    print("\t Adding External Pid")
    pids = call_pid_method('add_external_pid',sample_df,pid_map,get_gas_cost)
    print("\t Adding Payload")
    payl = call_pid_method('set_payload',sample_df,pid_map,get_gas_cost)

    ##
    ## save outpur
    ##
    a = pd.concat([pd.DataFrame(pid_map).T, pd.DataFrame(urls).T, pd.DataFrame(pids).T, pd.DataFrame(payl).T])
    a['oasis_id'] = a.index
    a.reset_index(inplace=True)
    a.to_csv(name+'.csv',index=False,sep=';')