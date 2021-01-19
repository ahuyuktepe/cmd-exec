import pytest

from src.error.CmdExecError import CmdExecError
from src.util.FileUtil import FileUtil


class TestFileUtil:

    def test_delete_directory(self):
        with pytest.raises(CmdExecError) as errInfo:
            path = ['modules']
            FileUtil.deleteDir(path)
        error: CmdExecError = errInfo.value
        assert error.getCode() == 'ERR21'
