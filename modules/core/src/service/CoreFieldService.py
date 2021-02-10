from modules.core.src.field.DateTimeField import DateTimeField
from modules.core.src.field.DateField import DateField
from modules.core.src.field.FileField import FileField
from modules.core.src.field.MultiSelectField import MultiSelectField
from modules.core.src.field.NumberField import NumberField
from modules.core.src.field.SingleSelectField import SingleSelectField
from modules.core.src.field.TextField import TextField
from src.error.CmdExecError import CmdExecError
from src.field.Field import Field
from src.field.FieldOption import FieldOption
from src.field.FieldType import FieldType
from src.menu.Command import Command
from src.service.ArgumentService import ArgumentService
from src.service.ConfigService import ConfigService
from src.service.FieldService import FieldService
from src.util.FileUtil import FileUtil
from src.util.ValidationUtil import ValidationUtil


class CoreFieldService(FieldService):
    __configService: ConfigService
    __argService: ArgumentService

    def __init__(self, configService: ConfigService, argService: ArgumentService):
        self.__configService = configService
        self.__argService = argService

    def buildField(self, cid: str, props: dict) -> Field:
        self.__validateRequiredProps(cid, props)
        type = props.get('type')
        fid = props.get('id')
        if type == FieldType.DATE:
            return self.__buildDateField(fid, props)
        elif type == FieldType.DATE_TIME:
            return self.__buildDateTimeField(fid, props)
        elif type == FieldType.FILE:
            return self.__buildFileField(fid, props)
        elif type == FieldType.MULTI_SELECT:
            return self.__buildMultiSelectField(fid, props)
        elif type == FieldType.NUMBER:
            return self.__buildNumberField(fid, props)
        elif type == FieldType.SINGLE_SELECT:
            return self.__buildSingleSelectField(fid, props)
        elif type == FieldType.TEXT:
            return self.__buildTextField(fid, props)
        else:
            raise CmdExecError('ERR53', {'cid': cid, 'type': type})

    def __validateRequiredProps(self, cid: str, props: dict):
        type = props.get('type')
        ValidationUtil.failIfStrNoneOrEmpty(type, 'ERR54', {'cid': cid, 'property': 'type'})
        fid = props.get('id')
        ValidationUtil.failIfStrNoneOrEmpty(fid, 'ERR54', {'cid': cid, 'property': 'id'})
        label = props.get('label')
        ValidationUtil.failIfStrNoneOrEmpty(label, 'ERR54', {'cid': cid, 'property': 'label'})

    def __buildDateField(self, fid: str, props: dict) -> DateField:
        field = DateField(fid)
        field.setProperties(props)
        return field

    def __buildDateTimeField(self, fid: str, props: dict) -> DateTimeField:
        field = DateTimeField(fid)
        field.setProperties(props)
        return field

    def __buildFileField(self, fid: str, props: dict) -> FileField:
        field = FileField(fid)
        field.setProperties(props)
        return field

    def __buildMultiSelectField(self, fid: str, props: dict) -> MultiSelectField:
        field = MultiSelectField(fid)
        field.setProperties(props)
        return field

    def __buildNumberField(self, fid: str, props: dict) -> NumberField:
        field = NumberField(fid)
        field.setProperties(props)
        return field

    def __buildSingleSelectField(self, fid: str, props: dict) -> SingleSelectField:
        field = SingleSelectField(fid)
        field.setProperties(props)
        return field

    def __buildTextField(self, fid: str, props: dict) -> TextField:
        field = TextField(fid)
        field.setProperties(props)
        return field

    def __getOptions(self, options: list) -> list:
        retList = []
        for optProps in options:
            option = FieldOption(**optProps)
            retList.append(option)
        return retList

    def __getFieldClassProps(self, type: str) -> dict:
        fieldClsProps = self.__configService.getFieldClassProps(type)
        ValidationUtil.failIfNotType(fieldClsProps, dict, 'ERR50', {'type': type})
        cls = fieldClsProps.get('class')
        ValidationUtil.failIfStrNoneOrEmpty(cls, 'ERR47', {'type': type})
        mid = fieldClsProps.get('module')
        if mid is not None:
            ValidationUtil.failIfNotType(mid, str, 'ERR48', {'type': type})
        else:
            mid = 'core'
        path = 'modules.{module}.src.field.{cls}'.format(module=mid, cls=cls)
        return {
            'class': cls,
            'path': path
        }

    def getFieldValuesFromArgumentFile(self, cmd: Command) -> dict:
        argFileName = cmd.getId() + '.args.yaml'
        path = ['resources', 'arguments', argFileName]
        if FileUtil.doesFileExist(path):
            return FileUtil.generateObjFromYamlFile(path)
        return {}

    def getFieldValuesFromCmdArgs(self, cmd: Command) -> dict:
        args: dict = {}
        fieldIds: list = cmd.getRequiredFieldIdsWithoutValue()
        passedArgs: dict = self.__argService.getArgs()
        for fid in fieldIds:
            args[fid] = passedArgs.get(fid)
        return args

    def getFieldValuesFromUser(self, cmd: Command) -> dict:
        return {}
