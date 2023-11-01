from functools import wraps
from typing import List

from cmd_exec.command.CmdExecutor import CmdExecutor
from cmd_exec.command.CmdRequest import CmdRequest
from cmd_exec.service.ArgumentService import ArgumentService
from cmd_exec.service.ConfigurationService import ConfigurationService


def config(params: dict):
    def config_decorator(func):
        @wraps(func)
        def wrapped_config(executor: CmdExecutor, req: CmdRequest):
            service: ConfigurationService = executor._contextManager.getService('configService')
            for key, path in params.items():
                executor.__setattr__(key, service.getValue(path))
            func(executor, req)
        return wrapped_config
    return config_decorator

def arg(params: dict):
    def config_decorator(func):
        @wraps(func)
        def wrapped_config(executor: CmdExecutor, req: CmdRequest):
            service: ArgumentService = executor._contextManager.getService('argService')
            for key, val in params.items():
                executor.__setattr__(key, service.getArgVal(val))
            func(executor, req)
        return wrapped_config
    return config_decorator

def service(sids: List[str]):
    def config_decorator(func):
        @wraps(func)
        def wrapped_config(executor: CmdExecutor, req: CmdRequest):
            for sid in sids:
                executor.__setattr__(sid, executor._contextManager.getService(sid))
            func(executor, req)
        return wrapped_config
    return config_decorator