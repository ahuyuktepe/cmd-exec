from src.error.CmdExecError import CmdExecError
from src.field.Field import Field
from src.menu.Command import Command
from src.service.ArgumentService import ArgumentService
from src.service.ConfigService import ConfigService
from src.service.FieldService import FieldService
from src.util.FileUtil import FileUtil
from src.util.ObjUtil import ObjUtil
from src.util.ValidationUtil import ValidationUtil


class CoreFieldService(FieldService):
    __configService: ConfigService
    __argService: ArgumentService

    def __init__(self, configService: ConfigService, argService: ArgumentService):
        self.__configService = configService
        self.__argService = argService

    def buildField(self, cid: str, props: dict) -> Field:
        self.__validateRequiredProps(cid, props)
        fieldType = props.get('type')
        fid = props.get('id')
        if fieldType is None:
            raise CmdExecError('ERR53', {'cid': cid, 'type': type})
        clsProps: dict = self.__getFieldClassProps(fieldType)
        cls = clsProps.get('class')
        clsPath = clsProps.get('path')
        field: Field = ObjUtil.initClassFromStr(clsPath, cls, [fid])
        field.setProperties(props)
        return field

    def __getFieldClassProps(self, fieldType: str) -> dict:
        fieldClsProps = self.__configService.getFieldClassProps(fieldType)
        ValidationUtil.failIfNotType(fieldClsProps, dict, 'ERR50', {'type': type})
        cls = fieldClsProps.get('class')
        ValidationUtil.failIfStrNoneOrEmpty(cls, 'ERR47', {'type': type})
        mid = fieldClsProps.get('module')
        if mid is not None:
            ValidationUtil.failIfNotType(mid, str, 'ERR48', {'type': type})
        else:
            mid = 'core'
        path = 'modules.{module}.src.field.{cls}'.format(module=mid, cls=cls)
        return {'class': cls, 'path': path}

    def __validateRequiredProps(self, cid: str, props: dict):
        type = props.get('type')
        ValidationUtil.failIfStrNoneOrEmpty(type, 'ERR54', {'cid': cid, 'property': 'type'})
        fid = props.get('id')
        ValidationUtil.failIfStrNoneOrEmpty(fid, 'ERR54', {'cid': cid, 'property': 'id'})
        label = props.get('label')
        ValidationUtil.failIfStrNoneOrEmpty(label, 'ERR54', {'cid': cid, 'property': 'label'})

    def getFieldValuesFromArgumentFile(self, cmd: Command) -> dict:
        argFileName = cmd.getId() + '.args.yaml'
        path = ['resources', 'arguments', argFileName]
        if FileUtil.doesFileExist(path):
            return FileUtil.generateObjFromYamlFile(path)
        return {}

    def getFieldValuesFromCmdArgs(self, cmd: Command) -> dict:
        args: dict = {}
        fieldIds: list = cmd.getFieldIds()
        passedArgs: dict = self.__argService.getArgs()
        for fid in fieldIds:
            args[fid] = passedArgs.get(fid)
        return args
