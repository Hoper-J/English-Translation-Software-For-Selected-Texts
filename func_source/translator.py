import requests


class Translator:
    """
    翻译，有疑惑的话请看下源码

    tip: 感觉这样写不易读，不过为了练习一下学的内容，暂时就不改了
    """
    def __init__(self):
        self.res = None

    @property
    def en_to_zh(self):
        """一个翻译的property"""
        return self.res

    @en_to_zh.setter
    def en_to_zh(self, string=' '):
        """翻译字符串"""
        self.raw_string = string
        self.__youdao_translation()

    def __youdao_translation(self) -> str:
        """有道翻译"""
        try:
            data = {
                'doctype': 'json',
                'type': 'AUTO',
                'i': self.raw_string
            }
            url = "http://fanyi.youdao.com/translate"
            r = requests.get(url, params=data)
            result = r.json()
            # 注意translateResult返回的列表长度是根据翻译的行数而定
            self.res = ''
            for res_paragraph in result['translateResult']:
                for res_line in res_paragraph:
                    self.res += res_line['tgt']
                self.res += '\n'
        except:
            self.res = "翻译失败"
            print("请检查网络")


if __name__ == '__main__':

    a = Translator()
    a.en_to_zh = """
    The exact appearance of the interpreter 
    hello
    """
    print(a.en_to_zh)