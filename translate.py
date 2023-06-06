# 对一个txt数据文件进行翻译
import os
import time
from tqdm import tqdm
from pygtrans import Translate
os.environ['http_proxy'] = "http://127.0.0.1:7890"
os.environ['https_proxy'] = "http://127.0.0.1:7890"

client = Translate()
text = client.translate('I love China, China is my home', target='zh')
print(text.translatedText)  # 谷歌翻译

src_fp = open("xxx.txt", 'r', encoding='utf-8')
tgt_fp = open("translation.txt", 'a', encoding='utf-8')
document = src_fp.readlines()
batch_size = 128
for i in tqdm(range(0, len(document), batch_size)):
    text = document[i : i+batch_size]
    # 指定target语言
    ans = client.translate(text, target='zh')
    time.sleep(1)
    for line in ans:
        tgt_fp.write(str(line.translatedText) + '\n')
    