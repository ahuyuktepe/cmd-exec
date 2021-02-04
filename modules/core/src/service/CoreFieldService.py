from modules.core.src.field.TextField import TextField
from src.field.Field import Field
from src.field.FieldOption import FieldOption
from src.field.FieldType import FieldType
from src.service.ConfigService import ConfigService
from src.service.FieldService import FieldService
from src.util.ObjUtil import ObjUtil
from src.util.ValidationUtil import ValidationUtil


class CoreFieldService(FieldService):
    __configService: ConfigService

    def __init__(self, configService: ConfigService):
        self.__configService = configService

    def buildField(self, props: dict) -> Field:
        type = props.get('type')
        # Get Class Properties
        clsProps = self.__getFieldClassProps(type)
        path = clsProps.get('path')
        cls = clsProps.get('class')
        # Init Field Object
        id = props.get('id')
        ValidationUtil.failIfClassFileDoesNotExist(path, 'ERR49', {'path': path})
        field: Field = ObjUtil.initClassFromStr(path, cls, [id])
        field.setProperties(props)
        optionProps = props.get('options')
        if optionProps is not None:
            options = self.__getOptions(optionProps)
            field.setOptions(options)
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
