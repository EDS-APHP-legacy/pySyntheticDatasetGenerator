class NotCompatibleDistributionException(Exception):
    pass

class JobPoolDependencyTreeException(Exception):
    pass

class ConfigYamlException(Exception):
    pass

class ConfigYamlFKException(ConfigYamlException):
    pass
