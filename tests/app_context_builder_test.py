from tests.base_tester import TestBase
from tests.utils.TestModuleUtil import TestModuleUtil


class TestAppContextBuilder(TestBase):

    def test_build(self):
        self.prepareForTest()
        TestModuleUtil.generateModuleFiles('test', {}, {})
        True
