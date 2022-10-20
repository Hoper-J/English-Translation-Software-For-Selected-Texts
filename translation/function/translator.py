import hashlib
import requests
import random
import time
# from .baidu_translate import Dict


class Translator:
    """
    翻译，有疑惑的话请看下源码

    tip: 感觉这样写不易读，不过为了练习一下学的内容，暂时就不改了
    """

    def __init__(self):
        self.res = None
        # self.baidu_dict = Dict()  # 只获取一次html源码中的参数，加快翻译速度，如果每次都获取，速度差不多只有1/3

    @property
    def en_to_zh(self):
        """一个翻译的property"""
        return self.res

    @en_to_zh.setter
    def en_to_zh(self, string=' '):
        """翻译字符串"""
        self.raw_string = string
        # self.__baidu_translation() # 暂时有bug
        self.__youdao_translation()

    def __youdao_translation(self) -> str:
        """
        有道翻译
        """
        lts = str(int(time.time() * 1000))
        salt = lts + str(random.randint(0, 9))
        i = self.raw_string
        sign_str = 'fanyideskweb' + i + salt + 'Ygy_4c=r#e#4EX^NUGUc5'
        m = hashlib.md5()
        m.update(sign_str.encode())
        sign = m.hexdigest()
        # print(self.raw_string)
        headers = {
            "Referer": "https://fanyi.youdao.com/",
            "Cookie": 'OUTFOX_SEARCH_USER_ID=-1124603977@10.108.162.139; JSESSIONID=aaamH0NjhkDAeAV9d28-x; OUTFOX_SEARCH_USER_ID_NCOO=1827884489.6445506; fanyi-ad-id=305426; fanyi-ad-closed=1; ___rl__test__cookies=1649216072438',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
        }
        data = {
            'doctype': 'json',
            'type': 'AUTO',
            'i': i,
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": salt,
            "sign": sign,
            "lts": lts,
            "bv": "a0d7903aeead729d96af5ac89c04d48e",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTlME",
        }
        url = "https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
        try:
            r = requests.post(url, headers=headers, data=data)
            result = r.json()
            # 注意translateResult返回的列表长度是根据翻译的行数而定
            self.res = self.__deal_with_yd_translation(result)
        except Exception as e:
            self.res = "翻译失败"
            print(e)

    def __baidu_translation(self):
        result = self.baidu_dict.dictionary(
            self.raw_string, dst='zh', src='en')  # json
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
            # 如果引起KeyError，代表查询的内容是句子
            simple_means = result['dict_result']['simple_means']

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
