class Config:
    healthcheckIntervalSeconds = 15
    requestTimeoutSeconds = 0.5

    @classmethod
    def getHealthcheckIntervalSeconds(cls):
        return cls.healthcheckIntervalSeconds
    
    @classmethod
    def getRequestTimeoutSeconds(cls):
        return cls.requestTimeoutSeconds