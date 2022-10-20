from setuptools import setup, find_packages

setup(
    name='Translation',
    version='0.0.1',
    author='hoper_j',
    author_email='hoper.hw@gmail.com',
    description='English Translation software for selected texts',
    url='https://github.com/Hoper-J/English-Translation-Software-For-Selected-Texts',
    packages=find_packages(include=["translation"]),
    install_requires=[
        "OCRmyPDF",
        "PyExecjs",
        "PyPDF2",
        "PyQt5",
        "PyQtWebEngine",
        "requests",
    ],
    keywords=['English Translation', 'selected text', 'OCR'],
   )
