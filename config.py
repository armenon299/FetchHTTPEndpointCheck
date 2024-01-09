class Config:
    def __init__(self):
        self.healthcheckIntervalSeconds = 15
        self.requestTimeoutSeconds = 0.5

    def getHealthcheckIntervalSeconds(self):
        return self.healthcheckIntervalSeconds
    
    def getRequestTimeoutSeconds(self):
        return self.requestTimeoutSeconds