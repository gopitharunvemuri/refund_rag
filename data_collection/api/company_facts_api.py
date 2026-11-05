from Loggers.logging import Custom_logger
from Exceptions.Exceptions import CustomExcpetion
from data_collection.api.used_functions import request_get_data

logger_class = Custom_logger()
logger = logger_class.get_logger("new_logger")

class Company_facts:
    def __init__(self, url, filename):
        self.url=url
        self.filename = filename

    def reframe_data(self):
        pass

    def get_data(self):
        request_get_data(self.url, self.filename)
    
obj = Company_facts(url="https://data.sec.gov/api/xbrl/companyconcept/CIK0000789019/us-gaap/Revenues.json", filename = "Company_facts.json")
obj.get_data()