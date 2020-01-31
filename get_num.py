'''
    此脚本用于对爬取下来的网页数据进行解析，主要获取网页中患者的信息，包括患者年龄和患者性别
'''
import json
import re
from pyecharts import options as opts
from pyecharts.charts import Bar

def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False


def get_nums(strs):
    ''' 
        
        13岁男
        男，36岁
        女57岁
        女性，50岁
    '''

    if '新增' in strs:
        #正常顺序
        str_list = re.findall("([男女])性?，?(\d{1,2})岁", strs)
        #相反顺序
        re_list = re.findall("(\d{1,2})岁，?([男女])", strs)

        re_list = [(e[1], e[0]) for e in re_list]
    else : 
        str_list = []
        re_list = []

    return str_list + re_list

#统计函数
def Tongji(data, lists):
    n = len(lists)
    ym_axis, yw_axis = [0]*n, [0]*n

    for d in data:
        i = None

        if 1 <= int(d[1]) <= 10: i = 0
        elif 11 <= int(d[1]) <= 20: i = 1
        elif 21 <= int(d[1]) <= 30: i = 2
        elif 31 <= int(d[1]) <= 40: i = 3
        elif 41 <= int(d[1]) <= 50: i = 4
        elif 51 <= int(d[1]) <= 60: i = 5
        elif 61 <= int(d[1]) <= 70: i = 6
        elif 71 <= int(d[1]) <= 80: i = 7
        elif 81 <= int(d[1]) <= 90: i = 8
        elif 91 <= int(d[1]) <= 100: i = 9
        else : i = 10

        if d[0] == '男':
            ym_axis[i] += 1
        elif d[0] == '女':
            yw_axis[i] += 1

    return ym_axis, yw_axis
            



#绘制条形图
def paint_bar(data):
    x_axis = ['1-10','11-20','21-30','31-40','41-50','51-60','61-70','71-80','80-90','91-100','100+']

    #男性数据与女性数据
    ym_axis, yw_axis = Tongji(data, x_axis)

    bar=(
        Bar()
        .add_xaxis(x_axis)
        .add_yaxis("男性", ym_axis)
        .add_yaxis("女性", yw_axis)
        .set_global_opts(title_opts=opts.TitleOpts(title="武汉新型冠状病毒肺炎各性别患病年龄分布图"))
     )
 
    bar.render()

    


if __name__ == "__main__":
    with open('./news.json') as f:
        htmls = json.load(f)
        f.close()
    res = []
    for html in htmls:
        content = html['content']
        res += get_nums(content)

    print(res)
    print('数量：',len(res))
    paint_bar(res)

# print(get_nums(html))