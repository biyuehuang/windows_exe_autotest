from typing import Union

class Assumption:
    def __init__(self, number: int, text: str) -> None:
        self.number = number
        self.text = text
        self.result = None
        self.info = None

    def set_result(self, result: Union[bool, str], info: str = '') -> None:
        self.result = result
        if info == '':
            print('Assumption: "{}" Result: {} '.format(self.text, self.result))
        else:
            print('Assumption: "{}" Result: {} Info: {}'.format(self.text, self.result, info))
