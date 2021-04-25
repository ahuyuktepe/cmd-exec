from cmd_exec.context.AppContextManager import AppContextManager
from cmd_exec.builder.AppContextBuilder import AppContextBuilder
from cmd_exec.context.AppContext import AppContext
from cmd_exec.service.CoreTerminalService import CoreTerminalService
from tests.src.utils.TestUtil import TestUtil


class TestTerminalService:
    terminalService: CoreTerminalService

    def setup_method(self, method):
        TestUtil.setupTestingEnvironment()
        appContext: AppContext = AppContextBuilder.buildBaseAppContext()
        contextManager: AppContextManager = AppContextManager(appContext)
        terminalService = CoreTerminalService()
        terminalService.setContextManager(contextManager)
        self.terminalService = terminalService

    def teardown_method(self, method):
        TestUtil.destroyTestingEnvironment()

    def test_break_line_1(self, monkeypatch, capsys):
        text = "Test\n"
        self.terminalService.print(text)
        response = capsys.readouterr()
        assert response.out == 'Test\n\n'

    def test_break_line_2(self, monkeypatch, capsys):
        text = "Test[br]"
        self.terminalService.print(text)
        response = capsys.readouterr()
        assert response.out == 'Test\n\n'

    def test_color_import_1(self, monkeypatch, capsys):
        text = "[red]Test"
        self.terminalService.print(text)
        response = capsys.readouterr()
        assert response.out == '\033[1;31mTest\n'

    def test_color_import_2(self, monkeypatch, capsys):
        text = "[red]Test[rst]"
        self.terminalService.print(text)
        response = capsys.readouterr()
        assert response.out == '\033[1;31mTest\033[0;0m\n'

    def test_text_tag_1(self, monkeypatch, capsys):
        text = "[txt:10:left:Test]"
        self.terminalService.print(text)
        response = capsys.readouterr()
        assert response.out == 'Test      \n'

    def test_text_tag_2(self, monkeypatch, capsys):
        text = "[txt:10:right:Test]"
        self.terminalService.print(text)
        response = capsys.readouterr()
        assert response.out == '      Test\n'

    def test_text_tag_3(self, monkeypatch, capsys):
        text = "[txt:10:center:Test]"
        self.terminalService.print(text)
        response = capsys.readouterr()
        assert response.out == '   Test   \n'

    def test_repeat_tag(self, monkeypatch, capsys):
        text = "[rpt:5:-]"
        self.terminalService.print(text)
        response = capsys.readouterr()
        assert response.out == '-----\n'

    def test_string_interpolation(self, monkeypatch, capsys):
        text = "Test {{lastName}}"
        self.terminalService.print(text, {
            'lastName': 'User'
        })
        response = capsys.readouterr()
        assert response.out == 'Test User\n'
