import requests


class Translator:
    def __init__(self):
        self.res = None

    @property
    def en_to_zh(self):
        """一个翻译的property"""
        return self.res

    @en_to_zh.setter
    def en_to_zh(self, string=' '):
        """设置需翻译的字符串"""
        self.raw_string = string
        self.__youdao_translation()

    def __youdao_translation(self) -> str:
        """有道翻译"""
        data = {
            'doctype': 'json',
            'type': 'AUTO',
            'i': self.raw_string
        }
        url = "http://fanyi.youdao.com/translate"
        r = requests.get(url, params=data)
        result = r.json()

        # 注意这里translate的返回结果是根据行数而定
        self.res = ''
        for res_paragraph in result['translateResult']:
            for res_line in res_paragraph:
                self.res += res_line['tgt']
            self.res += '\n'


if __name__ == '__main__':

    a = Translator()
    a.en_to_zh = """
    The exact appearance of the interpreter 
    hello
    """
    print(a.en_to_zh)