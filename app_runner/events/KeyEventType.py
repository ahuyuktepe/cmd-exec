
class KeyEventType:
    UP_KEY_PRESSED = 'upKeyPressed'
    DOWN_KEY_PRESSED = 'downKeyPressed'
    LEFT_KEY_PRESSED = 'leftKeyPressed'
    RIGHT_KEY_PRESSED = 'rightKeyPressed'
    ENTER_KEY_PRESSED = 'enterKeyPressed'
    SPACE_KEY_PRESSED = 'spaceKeyPressed'

    @staticmethod
    def getAll() -> list:
        return [
            KeyEventType.UP_KEY_PRESSED,
            KeyEventType.DOWN_KEY_PRESSED,
            KeyEventType.LEFT_KEY_PRESSED,
            KeyEventType.RIGHT_KEY_PRESSED,
            KeyEventType.ENTER_KEY_PRESSED,
            KeyEventType.SPACE_KEY_PRESSED
        ]
