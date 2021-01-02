from src.app.CmdExecApp import CmdExecApp
from src.builder.AppBuilder import AppBuilder

application: CmdExecApp = AppBuilder.build()
application.run()
