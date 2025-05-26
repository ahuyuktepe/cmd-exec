from cmd_exec.menu.Command import Command
from cmd_exec.service.TerminalService import TerminalService
from temp.modules.sample.src.cls.ListCmdFields import ListCmdFields

class Delete(Command):
    # ============================================================================================
    # Injecting Fields
    # ============================================================================================
    #@fields
    fields: dict                # Injects all fields into dict
                                # TODO: This should be automatically imported into CmdExecutor
    #@fields
    fields: ListCmdFields       # Injects all fields into object
    #@fields(id="first_name")
    first_name: str             # Injects single field value to variable
    #@field_value
    first_name: str             # Injects single field value to variable
    # ============================================================================================
    # Injecting Configuration Values
    # ============================================================================================
    #@config(key="app.version")
    version: str
    # ============================================================================================
    # Injecting Services
    # ============================================================================================
    #@service
    terminalService: TerminalService
    #@service(key="core.terminalService")
    terminalService: TerminalService
    # ============================================================================================
    # Injecting Setting Values
    # ============================================================================================
    #@settings
    setting: dict                   #TODO: This should be automatically imported into CmdExecutor
    #@settings(key="desc")
    desc: str

    # @settings(
    #     desc="Listing command",
    #     args=[
    #         { id: "first_name", type: "string" },
    #         { id: "last_name", type: "string" }
    #     ]
    # )
    # def __init__(self):
    #     super.__init__()

    def execute(self):
        print("delete")
