from elasticsearch import Elasticsearch
from datetime import datetime, timedelta

class GetElastAlerts:
    def __init__(self, hosts, index, protocol = 'http', username=None, password=None, verify_certs = False, ca_certs = None):
        assert protocol == 'http' or protocol == 'https'
        self.hosts = hosts
        self.index = index
        self.protocol = protocol
        self.username = username
        self.password = password
        self.verify_certs = verify_certs
        self.ca_certs = ca_certs
        self.time_last = datetime.utcnow() - timedelta(0,5)
    
    @staticmethod
    def get_result_timedelta(es_connect, index, time_start, time_end, size=500):
        #TODO: add sort by time
        query = {
            "bool": {
                "filter":
                [
                    {"range": { "timestamp": { 
                        "gte": time_start.strftime('%Y-%m-%dT%H:%M:%S'), 
                        "lte": time_end.strftime('%Y-%m-%dT%H:%M:%S') } } }
                ]
            }
        }
        return es_connect.search(index=index, body = {'size':size, 'query':query})['hits']['hits']
    
    def get_elastic_connect(self):
        protocol = 'http://' if self.protocol == 'http' else 'https://'
        creds = f"{self.username}:{self.password}@" if self.username and self.password else ""
        es = Elasticsearch(
            [protocol + creds + host for host in self.hosts],
            verify_certs = self.verify_certs,
            ca_certs = self.ca_certs
        )
        return es
    
    def get_elastic_alerts(self):
        es_connect = self.get_elastic_connect()
        time_now = (datetime.utcnow() - timedelta(0,5))
        result_timedelta = self.get_result_timedelta(es_connect=es_connect, index=self.index, time_start=self.time_last, time_end=time_now)
        self.time_last = time_now
        return result_timedelta