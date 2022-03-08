# WhatsApp-Chat-Analyser
Create visualizations and identify sentiments from the WhatsApp chats.

## Installing Package
pip install -i https://test.pypi.org/simple/ whatsapp-chat-analyser

## Usage
This pacakge can be used to perform text clearning, text visualisation and sentiment analysis for the WhatsApp conversation between individuals and/or group.
Accepted file format includes chats exported as txt files.

```
import whatsapp_chat_visualizer as wcv
wcv.pie(param = , data = )
# code for wordcloud
# code for sentiment analysis
```
Please refer to the following notebook to see how to use this package.

## Package Structure
```
WhatsApp-Chat-Analyser/
  |- .ipynb_checkpoints
     |- WhatsApp_analyser_ver3-checkpoint.ipynb
  |- WhatsappChatAnalyser/
     |- __init__.py 
     |- Sentiment.py
     |- author.py
     |- chat.py
     |- whatsapp_chat_sentiment.py
     |- whatsapp_chat_visualizer.py
     |- whatsapp_text_cleaner.py
     |- WhatsApp_analyser.ipynb
     |- WhatsApp Chat with UW MSDS Fall21.txt
  |- tests/
     |- __init__.py 
     |- author_tests.py
     |- chat_test.py
     |- whatsapp_chat_visualizer.py
     |- whatsapp_text_cleaner_test.py
  |- LISCENCE
  |- README.md
  |- pyproject.toml
  |- setup.py
```


## Installed Libraries and dependencies
```
python version 3.7 and above

Cython                             0.29.23
emoji                              1.6.3
entrypoints                        0.3
imagecodecs                        2021.3.31
imageio                            2.9.0
imagesize                          1.2.0
importlib-metadata                 3.10.0
iniconfig                          1.1.1
intervaltree                       3.1.0
ipykernel                          5.3.4
ipython                            7.22.0
ipython-genutils                   0.2.0
jupyter                            1.0.0
jupyter-client                     6.1.12
jupyter-console                    6.4.0
jupyter-core                       4.7.1
jupyter-packaging                  0.7.12
jupyter-server                     1.4.1
jupyterlab                         3.0.14
jupyterlab-pygments                0.1.2
jupyterlab-server                  2.4.0
jupyterlab-widgets                 1.0.0
matplotlib                         3.3.4
mistune                            0.8.4
mkl-fft                            1.3.0
mkl-random                         1.2.1
mkl-service                        2.3.0
mock                               4.0.3
more-itertools                     8.7.0
mpmath                             1.2.1
msgpack                            1.0.2
multipledispatch                   0.6.0
mypy-extensions                    0.4.3
nbformat                           5.1.3
nest-asyncio                       1.5.1
networkx                           2.5
nltk                               3.6.1
numpy                              1.20.1
numpydoc                           1.1.0
olefile                            0.46
openpyxl                           3.0.7
packaging                          20.9
pandas                             1.2.4
pandocfilters                      1.4.3
paramiko                           2.7.2
parso                              0.7.0
partd                              1.2.0
path                               15.1.2
pathlib2                           2.3.5
pathspec                           0.7.0
patsy                              0.5.1
pca                                1.5.2
pep8                               1.7.1
pip                                21.0.1
pkginfo                            1.7.0
plotly                             5.3.1
py                                 1.10.0
pycodestyle                        2.6.0
pycosat                            0.6.3
pycparser                          2.20
pycurl                             7.43.0.6
pydocstyle                         6.0.0
pyerfa                             1.7.3
pyflakes                           2.2.0
Pygments                           2.8.1
pylint                             2.7.4
pyls-black                         0.4.6
pyls-spyder                        0.3.2
pyodbc                             4.0.0-unsupported
pyOpenSSL                          20.0.1
pyparsing                          2.4.7
pyreadline                         2.1
pyrsistent                         0.17.3
PySocks                            1.7.1
pytest                             6.2.3
python-dateutil                    2.8.1
python-jsonrpc-server              0.4.0
python-language-server             0.36.2
regex                              2021.4.4
requests                           2.25.1
rope                               0.18.0
scikit-image                       0.18.1
scikit-learn                       0.24.1
scipy                              1.6.2
seaborn                            0.11.1
setuptools                         52.0.0.post20210125
simplegeneric                      0.8.1
singledispatch                     0.0.0
sip                                4.19.13
six                                1.15.0
sklearn                            0.0
statsmodels                        0.12.2
unicodecsv                         0.14.1
urllib3                            1.26.4
win-unicode-console                0.5
wincertstore                       0.2
wordcloud                          1.8.1
wrapt                              1.12.1
```

