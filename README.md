# PDF划线翻译（支持扫描版）
感谢以下三个仓库给我提供的帮助：
1. [English-Document-translation-software](https://github.com/zhangcf0110/English-Document-translation-software)提供的鼠标事件捕获思路
2. [百度翻译 API 破解](https://github.com/ZCY01/BaiduTranslate) 提供的翻译帮助（暂时不可用）
3. [pdf.js](https://github.com/mozilla/pdf.js) 的pdf浏览支持

软件使用的第三方库：PyExecjs, OCRmyPDF, PyPDF2, PyQt5, PyQtWebEngine, requests

## 搭建虚拟环境以及安装依赖
```bash
cd Translation
# Python Preparation
virtualenv venv
source venv/bin/activate
# Install translation and other dependencies
pip install -e .
```
## 用法
```bash
cd translation
python main.py
```
## 功能

- 划词/句翻译 [√]
- 从文件导入 PDF [√]
- 拉拽分割线调节布局 [√]
- 简单的调节字号大小 [√]
- 简单的翻译记录（每个PDF独立）[√]
- 简单的单词记录 (所有PDF共享) [√]
- 备份当前文件 & OCR (in place) 文字层覆盖[√]
  
## Todo（估计得等一年后了）
- 重构代码逻辑
- 重命名各变量以增加代码易读性
- 完善以上简单功能
- 美化界面

## 界面一览（未截菜单栏）
- 句子翻译
![句子翻译](https://blogby.oss-cn-guangzhou.aliyuncs.com/20210418170605.png)
- 单词翻译
<img width="1393" alt="image" src="https://user-images.githubusercontent.com/79922894/115140196-97473000-a068-11eb-9bcb-1d8e581b04c7.png">
- 记录
<img width="494" alt="image" src="https://user-images.githubusercontent.com/79922894/115140422-d2962e80-a069-11eb-95a6-9ec6819d7ef5.png">

