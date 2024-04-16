import jsonpickle

from models import config


with open('./config.json', 'r') as config_file:
    _config = jsonpickle.decode(config_file.read())

Salesforce = config.SalesforceSettings(_config['salesforce-as'])
LogVerbose = False