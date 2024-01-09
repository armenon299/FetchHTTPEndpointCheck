import yaml
import requests
import sys
import time
from threading import Thread
from urllib.parse import urlparse
from requests import RequestException
from config import Config

domainStatusDict = {}


class HttpEndpoint:
    def __init__(self, endPoint):
        self.name = endPoint["name"]
        self.url = endPoint["url"]
        self.domain = urlparse(self.url).netloc
        self.method = endPoint["method"] if "method" in endPoint else "GET"
        self.headers = endPoint["headers"] if "headers" in endPoint else None
        self.body = endPoint["body"] if "body" in endPoint else None


class DomainStatus:
    def __init__(self, domain):
        self.domain = domain
        self.successfulRequests = 0
        self.totalRequests = 0

    def successfulRequest(self):
        self.successfulRequests += 1
        self.totalRequests += 1
    
    def unsuccessfulRequest(self):
        self.totalRequests += 1

    def getDomainAvailability(self):
        return round(100 * (self.successfulRequests / self.totalRequests)) if self.totalRequests != 0 else 0



def loadEndpointData(fileName):
    # Returns a list of type HttpEndpoint
    with open(fileName, "r") as inputFile:
        endpointData = yaml.safe_load(inputFile)
        allEndpoints = []
        for endpoint in endpointData:
            newdomainRecord = HttpEndpoint(endpoint)
            domainStatusDict[newdomainRecord.domain] = DomainStatus(newdomainRecord.domain)
            allEndpoints.append(newdomainRecord)
        return allEndpoints

def updateStatus(endpoint):
    response = None
    url = endpoint.url
    headers = endpoint.headers
    data = endpoint.body
    method = endpoint.method
    domain = endpoint.domain
    try:
        response = requests.request(method=method, url=url, headers=headers, data=data, timeout=Config.getRequestTimeoutSeconds())
        if not response:
            domainStatusDict[domain].unsuccessfulRequest()
        else:
            responseStatus = response.status_code
            if 200 < responseStatus or responseStatus > 299:
                domainStatusDict[domain].unsuccessfulRequest()
            else:
                domainStatusDict[domain].successfulRequest()
    except RequestException:
        pass


def startThreads(allEndpoints):
    threads = []
    for endpoint in allEndpoints:
        t = Thread(target=updateStatus, args=(endpoint,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()


def displayDomainAvailability():
    print("---------------------------")
    for domainRecord in domainStatusDict.values():
        print(f'{domainRecord.domain} has {domainRecord.getDomainAvailability()}% availability percentage')
    print("---------------------------")


def main(argv):
    if len(argv) < 1:
        print("Invalid Argument: Please provide one input YAML file")
    elif len(argv) > 1:
        print("Invalid Arguments: Only one input YAML file is expected")
    else:
        try:
            allEndpoints = loadEndpointData(argv[0])
            while True:
                startThreads(allEndpoints)
                displayDomainAvailability()
                time.sleep(Config.getHealthcheckIntervalSeconds())
        except KeyboardInterrupt:
            print("\nProgram terminated by user (Ctrl+C). Exiting gracefully...")
        except yaml.YAMLError:
            print("\nInvalid YAML Format: Please reformat the input file")
        except FileNotFoundError:
            print("\nInvalid Argument: Input YAML file not found")
        except Exception as e:
            print(f"\nException Thrown: {str(e)}")


if __name__ == "__main__":
    main(sys.argv[1:])