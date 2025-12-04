from typing import List
import logging
logger = logging.getLogger(__name__)
"""
controller generated to handled auth operation described at:
https://connexion.readthedocs.io/en/latest/security.html
"""
def check_bearerAuth(token):
    logger.debug("Bearer token received")
    return {'test_key': 'test_value'}


