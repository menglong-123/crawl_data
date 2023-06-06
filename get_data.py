# 根据URL爬取网页页面，然后根据正则表达式来得到乌尔都语，并根据句子长度来进行过滤

import requests
from tqdm import tqdm
import re
import time
import os

proxies = {
  'http': 'http://127.0.0.1:7890',
  'https': 'http://127.0.0.1:7890',
}

sentences = set()

def filter(s, fp):
    # 不重复
    # 保留句子长度为10-50之间的句子
    # 去除乌尔都单词 < 0.75的句子
    s = s.strip()
    n = len(s.split())
    # 重复过滤和句子长度过滤
    if s in sentences or n < 10 or n > 50:
        return 0
    
    # 有效词过滤
    p = re.compile('[\u0600-\u06ff]')
    cnt = 0
    for word in s:
        if len(p.findall(word)) > 0:
            cnt += 1
    if cnt / n < 0.75:
        return 0
    
    sentences.add(s)
    fp.write(s + '\n')
    return 1


prog = re.compile('[ !,.:?0-9|\u0600-\u06ff]+')
def helper(url, fp):
    try:
        data = requests.get(url, proxies=proxies)
    except :
        return 0
    if not data.ok:
        return 1
    data = data.text
    # 根据正则表达式找出所有匹配的结果
    result = prog.findall(data)
    # 对结果进行过滤
    result = [filter(i, fp) for i in result]
    print('\n' + str(sum(result)))    
        
    return 1

########################################
base_path = "url.txt"
########################################
files = os.listdir(base_path)

########################################
tgt_path = "xxx.txt"
########################################

for file in files:
    src_fp = open(os.path.join(base_path, file), encoding='utf-8')
    tgt_fp = open(os.path.join(tgt_path, file.split('_')[0] + ".txt"), 'w', encoding='utf-8', buffering=1)
    urls = src_fp.readlines()
    urls = list(set(urls))
    for url in tqdm(urls):
        url = url.strip('\n')
        flag = 0
        while flag != 1:
            flag = helper(url, tgt_fp)
            time.sleep(1)
