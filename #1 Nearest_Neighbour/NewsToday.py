from NewsSample import news
from random import randint

text = open("ChatRecord/20200306.txt", "r")
news_amounts = 20
# 读取的消息记录，改这里

textlist = text.readlines()
classified = {}
attribute = {}
# [-9: -4]是时间
# [-22: -12]是QQ号

time = "00:00"
qq = "1234567890"
for line in textlist:
    if len(line) >= 23 and line[-4] == ':':
        time = line[-9: -4]
        qq = line[-22: -12]
        if not classified.__contains__(line[-9: -4]):
            classified[line[-9: -4]] = []
    # 创建时间标签，如08：04
    else:
        classified[time].append(line[:-1])
        # 创建消息时间表，如{'00:04' : ['XXX']}
        attribute[line[:-1]] = [qq]
        # 创建消息标签

for item in classified.items():
    for chatline in item[1]:
        # attribute[chatline].append()
        attribute[chatline].append(len(chatline) * 10)
        # 属性1：消息长度 *10
        if len(chatline) > 0:
            attribute[chatline].append(ord(chatline[0]) / 100)
        else:
            attribute[chatline].append(0)
        # 属性2：第一个字符的ASCII码 /100
        current_time = item[0]
        current_qq = attribute[chatline][0]
        next_index = classified[current_time].index(chatline) + 1
        heat = len(classified[current_time][next_index:])
        # 这一分钟从该语句开始的语句条数
        discussion = 1
        for i in classified[current_time][next_index:]:
            if attribute[i][0] != current_qq:
                discussion += 1
                current_qq = attribute[i][0]
        # 这一分钟从该语句开始不同的用户数
        for n in range(4):
            current_time = current_time[:-1] + str(int(current_time[-1]) + 1)
            if int(current_time[3:5]) > 59:
                current_time = str(int(current_time[0:2]) + 1) + ':' + str(int(current_time[3:5] - 60))
            if classified.__contains__(current_time):
                heat += len(classified[current_time])
                for i in classified[current_time]:
                    if attribute[i][0] != current_qq:
                        discussion += 1
                        current_qq = attribute[i][0]
        attribute[chatline].append(heat * 10)
        attribute[chatline].append(discussion * 10)
        # 属性3：热度(heat) *10，即该消息后5分钟的消息数
        # 属性4：讨论度(discussion) *10，即即该消息后5分钟讨论的用户数，说话人改变一次计一次

unlikelyhood = []
key = {}
for i in attribute.items():
    current_unlikelyhood = 0
    for j in news:
        if j[-1] > 0:
            current_unlikelyhood += j[-1] * ((i[1][1] - j[1]) ** 2 + (i[1][2] - j[2]) ** 2 + (i[1][3] - j[3]) ** 2 + (i[1][4] - j[4]) ** 2) ** 0.5
        else:
            current_unlikelyhood += 40000 * (-j[-1]) / (((i[1][1] - j[1]) ** 2 + (i[1][2] - j[2]) ** 2 + (i[1][3] - j[3]) ** 2 + (i[1][4] - j[4]) ** 2) ** 0.5 + 100)
    unlikelyhood.append(current_unlikelyhood)
    key[current_unlikelyhood] = i[0]
# 计算每条消息是新闻的可能性，变量unlikelyhood值越小可能性越大
# 比对NewsSample中每个样本，计算其欧拉距离d
# 对于标签为+的样本，距离越小，即相似度越低，可能性越大，因此current_unlikelyhood直接加上 倍数*d
# 对于标签为-的样本，距离越小，即相似度越低，可能性越低，因此current_unlikelyhood加上 倍数*40000/d
# 将current_unlikelyhood作为key，指向其对应的消息文本


unlikelyhood.sort()
count = 1
print("#1 Nearest_Neighbour")
for k in unlikelyhood[:news_amounts]:
    random1 = randint(1, 10)
    random2 = randint(1, 8)
    print(f"{count}. ", end="")
    print(f"{key[k]}")
    count += 1
# 可能性排序，unlikelyhood从小到大，作为key寻找对应消息，排序输出


print()
for k in unlikelyhood[:news_amounts]:
    attribute[key[k]].append(-1.5)
    print(f'    {attribute[key[k]]},      #{key[k]}')
print()
# 排名前20消息
for k in unlikelyhood[int(len(unlikelyhood)/3): int(len(unlikelyhood)/3) + news_amounts]:
    attribute[key[k]].append(-1.8)
    print(f'    {attribute[key[k]]},      #{key[k]}')
print()
print(unlikelyhood)
# 排名1/3处消息
# 方便NewsSample打标签