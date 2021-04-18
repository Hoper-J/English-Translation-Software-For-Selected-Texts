import requests

from .baidu_translate import Dict


class Translator:
    """
    翻译，有疑惑的话请看下源码

    tip: 感觉这样写不易读，不过为了练习一下学的内容，暂时就不改了
    """
    def __init__(self):
        self.res = None
        self.baidu_dict = Dict() # 只获取一次html源码中的参数，加快翻译速度，如果每次都获取，速度差不多只有1/3

    @property
    def en_to_zh(self):
        """一个翻译的property"""
        return self.res

    @en_to_zh.setter
    def en_to_zh(self, string=' '):
        """翻译字符串"""
        self.raw_string = string
        self.__baidu_translation()
        # self.__youdao_translation()

    def __youdao_translation(self) -> str:
        """
        有道翻译，未反爬虫版，不建议使用
        """
        # print(self.raw_string)
        data = {
            'doctype': 'json',
            'type': 'AUTO',
            'i': self.raw_string,
        }
        url = "http://fanyi.youdao.com/translate"
        try:
            r = requests.get(url, params=data)
            result = r.json()
            # 注意translateResult返回的列表长度是根据翻译的行数而定
            self.res = self.__deal_with_yd_translation(result)
        except Exception as e:
            self.res = "翻译失败"
            print(e)

    def __baidu_translation(self):
        result = self.baidu_dict.dictionary(self.raw_string, dst='zh', src='en') # json
        self.res = self.__deal_with_bd_translation(result)
        # print(self.res)

    def __deal_with_yd_translation(self, result):
        """处理有道翻译"""
        res = ''
        for res_paragraph in result['translateResult']:
            for res_line in res_paragraph:
                res += res_line['tgt']
            res += '\n'

        return res

    def __deal_with_bd_translation(self, result):
        """处理百度翻译"""
        # todo: 对查询的特定单词进行格式处理 try: result['simple_means']
        res = ''
        try:
            simple_means = result['dict_result']['simple_means'] # 如果引起KeyError，代表查询的内容是句子

            dict = simple_means['symbols'][0]
            res += f"英 [{dict['ph_en']}]\n美 [{dict['ph_am']}]\n"

            means = dict['parts']
            for mean in means:
                res += mean['part'] + ';'.join(mean['means']) + '\n'

        except KeyError:
            for res_paragraph in result['trans_result']['data']:
                for res_line in res_paragraph['dst']:
                    res += res_line
                res += '\n'
        return res

if __name__ == '__main__':

    a = Translator()
    a.en_to_zh = """
    process
    """
    print(a.en_to_zh)
