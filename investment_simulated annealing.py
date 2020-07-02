"""
债券组合投资方案设计

# 目标函数
# 约束条件
# 动态绘制柱状图

Author:张森
"""
import sys
from math import exp

import numpy as np
from random import random
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

#
amount_money = 8000
# init_args
args = [700, 800, 300, 800, 500, 400, 500, 600, 300, 500, 500, 500, 800, 600, 200]
#
#
x_labels = ['医药健康', '交通运输', '科技研发', '装备制造', '国民福利']
step = len(args) // 5  # 每个债券领域中的产品个数
x = range(5)  # 横坐标 #5个债券领域
x = np.arange(len(x))  # 首先用第一个的长度作为横坐标
width = 0.1  # 设置柱与柱之间的宽度
fig, ax = plt.subplots(figsize=(12, 5))
#
ax.set_ylabel('单位/万元')
ax.set_title('债券组合投资方案')
ax.set_xticks(x)
ax.set_xticks(x + width / 2)  # 将坐标设置在指定位置
ax.set_xticklabels(x_labels)  # 将横坐标替换成
# ax.legend()
fig.tight_layout()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


# pre_data 编码
income_before_taxes = [0.0445, 0.3989, 2.3211, 0.08, 0.5827, 3.0054, 0.1255, 1.8009, 2.3211,
                       0.1255, 0.3989, 2.0612,
                       0.0445, 0.1877, 2.0612]
# tax = [1, 1, 1, 0.2, 0.2, 0.2, 1, 1, 1, 0.1, 0.1, 0.1, 0.3, 0.3, 0.3]
tax_convert_percent = [1, 1, 1, 0.8, 0.8, 0.8, 1, 1, 1, 0.9, 0.9, 0.9, 0.7, 0.7, 0.7]

# restrict_1
# sum(args) == amount_money
# restrict_2
# sum(args[:3]) >= amount_money * 0.2
restrict_3 = [5, 5, 5, 2, 2, 2, 4, 4, 4, 3, 3, 3, 1, 1, 1]
restrict_4 = [2, 9, 20, 3, 12, 25, 4, 15, 20, 4, 9, 18, 2, 5, 18]


# judge risk level
def fun_restrict_3(args):
    _sum = 0
    # step = 3
    # for i in range(5):
    #     _sum += sum(restrict_3[i] * args[3 * i:3 * i + step])
    for i in range(len(args)):
        _sum += restrict_3[i] * args[i]

    if _sum / amount_money >= 2.5:
        return True
    else:
        return False


# judge  average bond age limit
def fun_restrict_4(args):
    _sum = 0
    # for i in range(15):
    #     _sum += restrict_4[i] * args[i]
    for i in range(len(args)):
        _sum += restrict_4[i] * args[i]
    if _sum / amount_money <= 10:
        return True
    else:
        return False


# judge args列表中的元素全部大于0
def fun_restrict_5(args):
    # for i in range(len(args)):
    #     if (i >= 0):
    #         pass
    #     else:
    if len([i for i in args if i > 0]) < len(args):
        return False
    else:
        return True


# judge_restrict
def judge_restrict(args):
    if abs(sum(args) - amount_money) <= 1e-1 and sum(args[:3]) >= amount_money * 0.2 and fun_restrict_3(
            args) and fun_restrict_4(args) and fun_restrict_5(args):
        return True
    else:
        return False


# 目标函数
np_args = np.array(args)
np_tax = np.array(tax_convert_percent)
np_income_before_taxes = np.array(income_before_taxes)
f = sum(np_args * np_tax * np_income_before_taxes)

# 模拟退火
num = 300000  # 每个温度下迭代次数
T_max = 300000  # 初始最大温度1000
T_min = 0.01  # 结尾最小温度0.01
Trate = 0.95  # 温度下降速率0.95
n = 0
#
while T_max > T_min:
    while n < num:
        np_args_tmp = np.zeros(len(np_args))
        #
        for i in range(len(np_args)):
            # np_args_tmp[i] = np.around(np_args[i],2) + round(random() - 0.5, 2)
            np_args_tmp[i] = np.around(np_args[i] + random() - 0.5, 2)

        # np_args_tmp = np_args + round(random()-0.5, 2)
        # print(np_args_tmp)
        if judge_restrict(np_args_tmp):
            f_tmp = sum(np_args_tmp * np_tax * np_income_before_taxes)
            res = f_tmp - f

            # 更新args
            if res > 0:
                np_args = np_args_tmp
                f = f_tmp
            # 概率点: 没找到更大的值，看概率
            else:
                p = exp(-res / T_max)
                if random() > p:
                    np_args = np_args_tmp
                    f = f_tmp
        # n = n + 1
        #
        #
        if n % 2000 == 0:
            y1 = np_args[::step]  # 第一个纵坐标
            y2 = np_args[1::step]
            y3 = np_args[2::step]
            ax.cla()
            rects1 = ax.bar(x, y1, width, alpha=0.9,label='产品1')
            rects2 = ax.bar(x + width, y2, width, alpha=0.9, color='red',label='产品2')
            rects3 = ax.bar(x + 2 * width, y3, width, alpha=0.9, color='green',label='产品3')
            ax.legend()
            ax.set_xticks(x + width / 2)
            ax.set_xticklabels(x_labels)  # 将横坐标替换成
            ax.set_ylabel('单位/万元')
            ax.set_title('债券组合投资方案 最大收益:%.2f 万元' % f)

            autolabel(rects1)
            autolabel(rects2)
            autolabel(rects3)
            plt.pause(0.01)
        #
        #
        n = n + 1

        #
        #
    T_max = T_max * Trate

plt.show()
print(np_args)
print(sum(np_args))
print('最大收益', f)
