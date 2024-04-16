import logging

from simple_salesforce import Salesforce

from models.config import SalesforceSettings


class SFDC_Client:
    def __init__(self, cfg: SalesforceSettings):
        self.username = cfg.username
        self.password = cfg.password
        self.sec_token = cfg.security_token
        self.domain = 'test' if cfg.sandbox else 'login'
        self.client = self.init_client()

    def init_client(self):
        logging.debug('Initializing Salesforce API client...')

        return Salesforce(username=self.username, password=self.password, security_token=self.sec_token,
                          domain=self.domain, client_id='RevOps ECS Sync')

    def exec_soql(self, soql_query: str):
        return self.client.query_all(soql_query)['records']

    def exec_sosl(self, sosl_query: str):
        ...

    def get_existing_call(self, interview_id: str) -> str:
        soql = f"SELECT Id FROM Click_to_Talk_Request__c WHERE Stream_Interview_Id__c = '{interview_id}' LIMIT 1"
        call_reqs = self.exec_soql(soql)

        if call_reqs:
            return call_reqs[0]['Id']

        return ''

    def insert_apex_exception(self, err_payload: dict):
        self.client.Apex_Exception__c.create(err_payload)

    def insert_call_request(self, call_json: dict):
        self.client.Click_to_Talk_Request__c.create(call_json)

    def update_call_request(self, call_id: str, call_json: dict):
        self.client.Click_to_Talk_Request__c.update(call_id, call_json)