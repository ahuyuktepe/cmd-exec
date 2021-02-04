from src.command.CmdExecutor import CmdExecutor
from src.menu.Command import Command
from src.service.CommandService import CommandService
from src.util.ModuleUtil import ModuleUtil
from src.util.ValidationUtil import ValidationUtil


class CoreCmdService(CommandService):

    def buildCmdFromId(self, cid: str) -> Command:
        props = ModuleUtil.getModuleCommandProps(cid)
        # Init Command Object
        cmd: Command = self.__getCommand(cid, props)
        # Init Executor Object
        executor: CmdExecutor = self.__getExecutor(cid, props)
        cmd.setExecutor(executor)
        return cmd

    def __getExecutor(self, cid: str, props: dict) -> CmdExecutor:
        # Set Executor
        execProps: dict = props.get('executor')
        ValidationUtil.failIfNotType(execProps, dict, 'ERR37', {'cid': cid})
        cls = execProps.get('class')
        executor = CmdExecutor(cls)
        ValidationUtil.failIfStrNoneOrEmpty(cls, 'ERR38', {'cid': cid})
        method = execProps.get('method')
        if method is not None:
            ValidationUtil.failIfStrNoneOrEmpty(cls, 'ERR39', {'cid': cid})
            executor.setMethod(method)
        ValidationUtil.failIfNotType(executor, CmdExecutor, 'ERR40', {'cid': cid})
        executor.setContextManager(self._contextManager)
        return executor

    def __getCommand(self, cid: str, props: dict) -> Command:
        cmdId = props.get('id')
        ValidationUtil.failIfStrNoneOrEmpty(cmdId, 'ERR35', {'cid': cid})
        title = props.get('title')
        ValidationUtil.failIfStrNoneOrEmpty(title, 'ERR36', {'cid': cid})
        mid = props.get('module')
        ValidationUtil.failIfStrNoneOrEmpty(mid, 'ERR41', {'cid': cid})
        return Command(props.get('id'), props.get('title'))
