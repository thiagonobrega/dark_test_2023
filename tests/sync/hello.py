import pytest
import requests
from assertpy import assert_that
from tests.assertations.pid_assertions import *
from clients import HyperDriveClient
import datetime


# from clients import HyperDriveClient
# from tests.assertions.people_assertions import *
# from tests.helpers.people_helpers import *
# client = HyperDriveClient()

# @pytest.fixture
def gen_pid() -> str:
    cc = HyperDriveClient()
    response = cc.request_pid()
    return response.as_dict['ark']

# @pytest.fixture
def valid_metada():
    now_unix_timestamp = str(datetime.datetime.timestamp(datetime.datetime.now())*1000)
    valid_ext_url = 'http://dark.io/'+now_unix_timestamp
    valid_epid = 'doi:/116.dark.' + str(now_unix_timestamp)
    valid_payload = '{' + f'name : name_{str(now_unix_timestamp)}, time : {str(now_unix_timestamp)}' + '}'

    return [valid_ext_url , valid_epid , valid_payload]

valid_ext_url , valid_epid , valid_payload = valid_metada()
pid_a = gen_pid()
print(pid_a)

def test_create_pid(client,logger) -> None:
    response = client.request_pid()
    # print(response)
    # print(response.status_code)
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    logger.info(f"PID successfully generater ::: {response.as_dict['ark']}")

def test_add_external_pid_wrong(client,logger) -> None:
    pid, payload, response = client.add_external_pid(pid_a,'doi:/1239.1233')
    assert_that(response.status_code).is_equal_to(requests.codes.bad)
    logger.info(f"Unable to load external PID to a draft dARK::: {pid} ")

def test_set_payload_wrong(client,logger) -> None:
    data = '{' + f'name : xpto' + '}'
    pid, payload, response = client.set_payload(pid_a, data)
    assert_that(response.status_code).is_equal_to(requests.codes.bad)
    logger.info(f"Unable to set a payload to a draft dARK::: {pid} ")
  
def test_add_url(client,logger) ->  None:
    pid, payload, response = client.add_url(pid_a, valid_ext_url)
    assert_that(response.status_code).is_equal_to(requests.codes.ok)

# nao ativado
# def test_external_pid_invalid(client) ->  None:
#     pid, payload, response = client.add_external_pid(pid_a, 'mb:/asdas')
#     assert_that(response.status_code).is_equal_to(requests.codes.bad)

def test_external_pid(client,logger) ->  None:
    pid, payload, response = client.add_external_pid(pid_a, valid_epid)
    assert_that(response.status_code).is_equal_to(requests.codes.ok)

def test_set_payload(client,logger) ->  None:
    pid, payload, response = client.set_payload(pid_a, valid_payload)
    assert_that(response.status_code).is_equal_to(requests.codes.ok)

def test_confirm_value_resolver(resolver) -> None:
    response = resolver.get(pid_a)
    assert_external_pid(response,[valid_epid])
    assert_url(response,valid_ext_url)