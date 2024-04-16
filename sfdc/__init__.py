import logging

import config

from sfdc.client import SFDC_Client

logging.debug('Starting SFDC client...')
vizier = SFDC_Client(config.Salesforce)

