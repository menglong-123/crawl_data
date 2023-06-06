# 过滤掉重复句子和 根据长度过滤句子(太长或太短的删除)
import os
from tqdm import tqdm
import re

# 所以爬取数据的根目录
base_path = "xxx"
# 筛选后的根目录
tgt_path = "xxx"

files = os.listdir(base_path)
prog = re.compile('[\u0600-\u06ff]')
s = set()

# 筛选规则
def helper(line):
    # 重复句子
    if line in s:
        return False
    n = len(line.split())
    # 长度较短
    if n < 10 or n > 50:
        return False
    # 无效字符太多
    cnt = 0
    for word in line.split():
        if len(prog.findall(word)) > 0:
            cnt += 1
    if cnt / n < 0.75:
        return False
    
    return True


for file in files:
    src_fp = open(os.path.join(base_path, file), encoding='utf-8')
    tgt_fp = open(os.path.join(tgt_path, file.split('_')[0] + '.txt'), 'w', encoding='utf-8', buffering=1)
    content = src_fp.readlines()
    for line in tqdm(content):
        line = line.strip()
        if helper(line):
            s.add(line)
            tgt_fp.write(line + "\n")
    src_fp.close()
    tgt_fp.close()
