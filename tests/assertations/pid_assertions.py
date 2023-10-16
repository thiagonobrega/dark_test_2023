from assertpy import assert_that


def assert_external_pid(response, epids_values: list):
    for i in range(len(epids_values)):
        epid = str(epids_values[i])
        epid = epid.upper()
        repid = 'DOI:/'+response.as_dict['externa_pid_list'][i]['value']
        assert_that(repid).is_not_empty().contains(epid)

def assert_url(response, external_url: str):
    rurl = response.as_dict['externa_url']
    external_url = external_url.upper()
    assert_that(rurl).is_not_empty().contains(external_url)

# def assert_person_is_present(is_new_user_created):
#     assert_that(is_new_user_created).is_not_empty()