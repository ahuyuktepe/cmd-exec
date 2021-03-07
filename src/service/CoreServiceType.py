
class CoreServiceType:
    ARG_SERVICE: str = 'argService'
    CMD_SERVICE: str = 'cmdService'
    CONF_SERVICE: str = 'configService'
    FIELD_SERVICE: str = 'fieldService'
    LOG_SERVICE: str = 'logService'

    __SERVICES: list = [
        ARG_SERVICE,
        CMD_SERVICE,
        CONF_SERVICE,
        FIELD_SERVICE,
        LOG_SERVICE
    ]

    @staticmethod
    def isCoreService( sid: str) -> bool:
        return sid in CoreServiceType.__SERVICES

    @staticmethod
    def isArgService(sid: str) -> bool:
        return sid == CoreServiceType.ARG_SERVICE

    @staticmethod
    def isCmdService(sid: str) -> bool:
        return sid == CoreServiceType.CMD_SERVICE

    @staticmethod
    def isConfService(sid: str) -> bool:
        return sid == CoreServiceType.CONF_SERVICE

    @staticmethod
    def isFieldService(sid: str) -> bool:
        return sid == CoreServiceType.FIELD_SERVICE

    @staticmethod
    def isLogService(sid: str) -> bool:
        return sid == CoreServiceType.LOG_SERVICE
