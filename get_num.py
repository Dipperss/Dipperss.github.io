'''
    此脚本用于对爬取下来的网页数据进行解析，主要获取网页中患者的信息，包括患者年龄和患者性别
'''
import json
import re
from pyecharts import options as opts
from pyecharts.charts import Bar, Page, Line, Pie
import time


def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False


def get_nums(strs, date):
    ''' 
        
        13岁男
        男，36岁
        女57岁
        女性，50岁
    '''

    if '新增' in strs:
        #正常顺序
        str_list = re.findall("([男女])性?，?(\d{1,2})岁", strs)
        str_list = [(se[0], se[1], date) for se in str_list]
        #相反顺序
        re_list = re.findall("(\d{1,2})岁，?([男女])", strs)
        re_list = [(e[1], e[0], date) for e in re_list]
    else : 
        str_list = []
        re_list = []

    return str_list + re_list

# 统计函数
def Tongji_1(data, lists):
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

# 
def Tongji_2(data):
    #横坐标为日期
    #纵坐标为不同性别新增人数
    #{新闻时间:{(性别,年龄):人数)}
    x_axis = []

    for e in data:
        if e[2] not in x_axis:
            x_axis.append(e[2])

    #收集的数据的时间是从当前时间到过去的时间，为了最后能够按时间顺序在坐标上展示，需要先对这个list逆序
    x_axis = x_axis[::-1]
    n = len(x_axis)
    ym_axis, yw_axis = [[0 for i in range(n)]for j in range(9)], [[0 for i in range(n)]for j in range(9)]

    for d in data:

        j = x_axis.index(d[2])

        if 1 <= int(d[1]) <= 10: i = 0
        elif 11 <= int(d[1]) <= 20: i = 1
        elif 21 <= int(d[1]) <= 30: i = 2
        elif 31 <= int(d[1]) <= 40: i = 3
        elif 41 <= int(d[1]) <= 50: i = 4
        elif 51 <= int(d[1]) <= 60: i = 5
        elif 61 <= int(d[1]) <= 70: i = 6
        elif 71 <= int(d[1]) <= 80: i = 7
        elif 81 <= int(d[1]) <= 90: i = 8
        # elif 91 <= int(d[1]) <= 100: i = 9
        # else : i = 10

        if d[0] == '男':
            ym_axis[i][j] += 1
        elif d[0] == '女':
            yw_axis[i][j] += 1

    return x_axis, ym_axis, yw_axis

#总数计算
def sum_all(men,women):

    all_list = [[0 for i in range(len(men[0]))]for j in range(len(men))]
    for i, m in enumerate(men):
        for j, mm in enumerate(m):
            all_list[i][j] = mm + women[i][j]

    return all_list

#逐行相加
def sum_row(lists):
    all_list = [0 for i in range(len(lists[0]))]
    for i in range(len(lists[0])):
        for j in range(len(lists)):
            all_list[i] += lists[j][i]
    return all_list       

# 绘制条形图
def paint_bar(data, latest_time):
    x_axis = ['1-10','11-20','21-30','31-40','41-50','51-60','61-70','71-80','80-90','91-100','100+']

    #男性数据与女性数据
    ym_axis, yw_axis = Tongji_1(data, x_axis)
    #男性数据与女性数据, 时间统计
    x_axis_t, ym_axis_t, yw_axis_t = Tongji_2(data)
    #计算每日人数总数
    y_axis_all_age = sum_all(ym_axis_t,yw_axis_t)
    y_axis_all = sum_row(y_axis_all_age)
    #计算男女比例 
    men_num, women_num = sum(ym_axis),sum(yw_axis)
    all_num = men_num + women_num
    
    # 
    #  武汉新型冠状病毒肺炎各性别患病年龄分布柱状图
    bar1=(
        Bar()
        .add_xaxis(x_axis)
        .add_yaxis(series_name="男性",yaxis_data=ym_axis)
        .add_yaxis(series_name="女性", yaxis_data=yw_axis) 
        .set_global_opts(title_opts=opts.TitleOpts(title="武汉新型冠状病毒肺炎各性别患病年龄分布图"+'(最新收集时间：{})'.format(latest_time)), xaxis_opts=opts.AxisOpts(name="年龄区间"), yaxis_opts=opts.AxisOpts(name="总人数"), legend_opts=opts.LegendOpts(pos_left="right"))#设置x轴可以拉动datazoom_opts=opts.DataZoomOpts()
    )

    # 每日新增患病者年龄分布柱状图与折线图
    bar2=(
        Bar()
        .add_xaxis(x_axis_t)
        .add_yaxis(series_name="1-10岁",yaxis_data=y_axis_all_age[0],stack="stack1")
        # .add_yaxis(series_name="1-10岁_女",yaxis_data=yw_axis_t[0],stack="stack1",color='red')
        .add_yaxis(series_name="11-20岁",yaxis_data=y_axis_all_age[1],stack="stack2")
        # .add_yaxis(series_name="11-20岁_女",yaxis_data=yw_axis_t[1],stack="stack2")
        .add_yaxis(series_name="21-30岁",yaxis_data=y_axis_all_age[2],stack="stack3")
        # .add_yaxis(series_name="21-30岁_女",yaxis_data=yw_axis_t[2],stack="stack3")
        .add_yaxis(series_name="31-40岁",yaxis_data=y_axis_all_age[3],stack="stack4")
        # .add_yaxis(series_name="31-40岁_女",yaxis_data=yw_axis_t[3],stack="stack4")
        .add_yaxis(series_name="41-50岁",yaxis_data=y_axis_all_age[4],stack="stack5")
        # .add_yaxis(series_name="41-50岁_女",yaxis_data=yw_axis_t[4],stack="stack5")
        .add_yaxis(series_name="51-60岁",yaxis_data=y_axis_all_age[5],stack="stack6")
        # .add_yaxis(series_name="51-60岁_女",yaxis_data=yw_axis_t[5],stack="stack6")
        .add_yaxis(series_name="61-70岁",yaxis_data=y_axis_all_age[6],stack="stack7")
        # .add_yaxis(series_name="61-70岁_女",yaxis_data=yw_axis_t[6],stack="stack7")
        .add_yaxis(series_name="71-80岁",yaxis_data=y_axis_all_age[7],stack="stack8")
        # .add_yaxis(series_name="71-80岁_女",yaxis_data=yw_axis_t[7],stack="stack8")
        .add_yaxis(series_name="81-90岁",yaxis_data=y_axis_all_age[8],stack="stack9")
        # .add_yaxis(series_name="81-90岁_女",yaxis_data=yw_axis_t[8],stack="stack9")
        .extend_axis(yaxis=opts.AxisOpts(name="新增总人数"))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="每日新增患病者年龄分布图(可通过鼠标滚轮以及拖动查看更多数据)"), xaxis_opts=opts.AxisOpts(name="时间"), yaxis_opts=opts.AxisOpts(name="新增人数"),legend_opts=opts.LegendOpts(pos_top="bottom"), datazoom_opts=opts.DataZoomOpts(range_start=40,range_end=100,type_="inside"))#设置x轴可以拉动datazoom_opts=opts.DataZoomOpts()

    )

    #每日新增患者数
    line2 = (
        Line()
        .add_xaxis(x_axis_t)
        .add_yaxis(series_name='日增',y_axis=y_axis_all,yaxis_index=1,is_smooth=True,color='red')
    )

    # 当前患者男女比例
    pie = (
        Pie()
        .add("",[list(z) for z in zip(["女性", "男性"], [women_num, men_num])] )
        .set_global_opts(title_opts=opts.TitleOpts(title="患者男女比例(总人数：{})".format(all_num)))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))

    )


    grid = (
        Page()
        .add(bar1)
        .add(bar2.overlap(line2))
        .add(pie)
    )

    grid.render("index.html")

    


if __name__ == "__main__":
    with open('./news.json') as f:
        htmls = json.load(f)
        f.close()
    res = []
    #最后更新的时间
    latest_time = htmls[0]['sendTime']
    for html in htmls:
        date = html['sendTime']
        date = re.match("(\d{4}-\d{1,2}-\d{1,2})", date).group()

        content = html['content']
        res += get_nums(content, date)

    # print(res)
    print('数量：',len(res))
    paint_bar(res, latest_time)

# print(get_nums(html))