import pytest
import logging
import sys
from clients import HyperDriveClient, ResolverClient

@pytest.fixture(scope="session")
def client():
    hyperdrive_api = HyperDriveClient()
    return hyperdrive_api

@pytest.fixture(scope="session")
def resolver():
    resolver_api = ResolverClient()
    return resolver_api


@pytest.fixture(scope="session")
def logger(request):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    return logger


# import logging
# # import random
# # import sys

# import pytest
# # from pytest_reportportal import RPLogger #, RPLogHandler
# from reportportal_client import RPLogger

# from utils.file_reader import read_file

# import logging
# import sys

# import pytest

# from reportportal_client import RPLogger

# @pytest.fixture(scope="session")
# def rp_logger():
#     logger = logging.getLogger(__name__)
#     logger.setLevel(logging.DEBUG)
#     logging.setLoggerClass(RPLogger)
#     return logger

# @pytest.fixture
# def create_data():
#     payload = read_file('create_person.json')

#     random_no = random.randint(0, 1000)
#     last_name = f'Olabini{random_no}'

#     payload['lname'] = last_name
#     yield payload

# @pytest.fixture(scope="session")
# def logger(request):
#     logger = logging.getLogger(__name__)
#     logger.setLevel(logging.DEBUG)

#     # Create handler for Report Portal if the service has been
#     # configured and started.
#     if hasattr(request.node.config, 'py_test_service'):
#         # Import Report Portal logger and handler to the test module.
#         logging.setLoggerClass(RPLogger)
#         rp_handler = RPLogHandler(request.node.config.py_test_service)

#         # Add additional handlers if it is necessary
#         console_handler = logging.StreamHandler(sys.stdout)
#         console_handler.setLevel(logging.INFO)
#         logger.addHandler(console_handler)
#     else:
#         rp_handler = logging.StreamHandler(sys.stdout)

#     # Set INFO level for Report Portal handler.
#     rp_handler.setLevel(logging.INFO)
#     return logger