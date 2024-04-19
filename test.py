import logging
import sys
import traceback

import sfdc

def test_connection():

    logging.info('Testing access to SFDC API...')

    soql = "SELECT count(id) FROM Account"

    try:
        records = sfdc.vizier.exec_soql(soql)

        account_count = records[0]['expr0']
        logging.info(f'Test successful! Number of Accounts: {account_count}')

    except Exception as ex:
        ex_type, ex_value, ex_traceback = sys.exc_info()


        logging.error(f'There was a problem connecting to Salesforce.')
        logging.error(ex_value)