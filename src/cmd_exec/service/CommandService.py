from ..error.CmdExecError import CmdExecError
from ..command.CmdExecutor import CmdExecutor
from ..menu.Command import Command
from ..service.AppService import AppService
from ..service.ArgumentService import ArgumentService
from ..service.FieldService import FieldService
from ..util.FileUtil import FileUtil
from ..util.ModuleUtil import ModuleUtil
from ..util.ObjUtil import ObjUtil
from ..util.StrUtil import StrUtil
from ..util.ValidationUtil import ValidationUtil


class CommandService(AppService):
    __fieldService: FieldService
    __argService: ArgumentService

    def __init__(self, fieldService: FieldService, argService: ArgumentService):
        self.__fieldService = fieldService
        self.__argService = argService

    def __validateFields(self, cmd: Command):
        fields: dict = cmd.getFields()
        for fid, field in fields.items():
            field.validate()

    def buildCmdFromId(self, cid: str) -> Command:
        # 1) Search command file
        name = f"{cid}.py"
        files: list = FileUtil.findCmdFile(name)
        if len(files) > 1:
            raise CmdExecError('ERR82', {"fileName": name, "files": "\n".join(files)})
        path: str = files[0]
        # 2) Instantiate command object
        path = StrUtil.replaceStr(path, [FileUtil.getRootPath(), '\\', '.py'], ['', '.', ''])
        path = path[1:]
        clsName = f"{cid.capitalize()}"
        obj: Command = ObjUtil.initClassFromStr(path, clsName)
        ValidationUtil.failIfNotType(obj, Command, 'ERR82')
        obj.set_id(cid)
        return obj

    def __getFields(self, cmd: Command, fields: list) -> list:
        ValidationUtil.failIfNotType(fields, list, 'ERR45')
        retList = []
        for fieldProps in fields:
            field = self.__fieldService.buildField(cmd, fieldProps)
            retList.append(field)
        return retList

    def __getExecutor(self, cid: str, props: dict) -> CmdExecutor:
        # Set Executor
        execProps: dict = props.get('executor')
        ValidationUtil.failIfNotType(execProps, dict, 'ERR37', {'cid': cid})
        clsName = execProps.get('class')
        ValidationUtil.failIfStrNoneOrEmpty(clsName, 'ERR38', {'cid': cid})
        module = props.get('module')
        ValidationUtil.failIfStrNoneOrEmpty(module, 'ERR33', {'executor': clsName, 'file': cid + '.yaml'})
        clsPath = 'modules.{module}.src.executor.{cls}'.format(module=module, cls=clsName)
        ValidationUtil.failIfClassFileDoesNotExist(clsPath, 'ERR51', {'path': clsPath})
        method = execProps.get('method')
        if method is not None:
            ValidationUtil.failIfNotType(method, str, 'ERR39', {'cid': cid})
        cls = ObjUtil.getClassFromClsPath(clsPath, clsName)
        ValidationUtil.failIfNotSubClass(cls, CmdExecutor)
        executor = ObjUtil.initClassFromStr(clsPath, clsName, [method])
        ValidationUtil.failIfNotType(executor, CmdExecutor, 'ERR40', {'cid': cid})
        executor.setContextManager(self._contextManager)
        return executor

    def __validateExecutorSubClass(self, clsPath: str, clsName: str):
        # Child Class
        childCls = ObjUtil.getClassFromClsPath(clsPath, clsName)
        ValidationUtil.failIfNotSubClass(childCls, CmdExecutor)

    def __getCommand(self, cid: str, props: dict) -> Command:
        cmdId = props.get('id')
        ValidationUtil.failIfStrNoneOrEmpty(cmdId, 'ERR35', {'cid': cid})
        title = props.get('title')
        ValidationUtil.failIfStrNoneOrEmpty(title, 'ERR36', {'cid': cid})
        mid = props.get('module')
        ValidationUtil.failIfStrNoneOrEmpty(mid, 'ERR41', {'cid': cid})
        cmd: Command = Command(cmdId, title, mid)
        users = props.get('allowed_users')
        cmd.setAllowedUsers(users)
        users = props.get('denied_users')
        cmd.setDeniedUsers(users)
        groups = props.get('allowed_groups')
        cmd.setAllowedGroups(groups)
        groups = props.get('denied_groups')
        cmd.setDeniedGroups(groups)
        return cmd
