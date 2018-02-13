# 8:42 PM, Feb 12, 2018 @ home, Shangyu
# 爬取看准网 IT/互联网行业公司的排行和基本信息
# 爬取的内容：
# 公司名称、排名、业务范围、地点、人数规模、网址、评分、平均工资
# urls:
# http://www.kanzhun.com/plc52p1.html?ka=paging1
# http://www.kanzhun.com/plc52p2.html?ka=paging2
# ...
# http://www.kanzhun.com/plc52p10.html?ka=paging10
# 共 10 个页面
# url 构造, 注意有两个 page 变量
# http://www.kanzhun.com/plc52p{page}.html?ka=paging{page}

# 1.使用 Beautiful 库的 select 方法，没抓到任何东西，奇怪
# 2.改用正则表达式，成功
# 10:07 PM, Feb 12, 2018 @ home, Shangyu

# To do:
# 1.问题
# 这个页面的甲骨文公司没有网址，导致后面的公司网址错位
# http://www.kanzhun.com/plc52p4.html?ka=paging4
# for 循环中，zip() 函数匹配列表长度最短的
# 由于漏掉了甲骨文的网址，该页面的最后一个公司信息没有打印
# 2.如何修复
# 业务范围、地点、人数规模、网址尝试用一个正则式同时抓取

import requests
import time
import re


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

def get_info(url):
    global count
    global file
    print(url)
    file.write('on page:' + url + '\n')
    res = requests.get(url, headers=headers)
    # 根据网页源代码，推导每个元素的正则表达式, (.*?)经常用到
    companys = re.findall('<a ka="com\d+-title" href="/.*?.html" target="_blank">(.*?)</a>', res.text)

    kinds = re.findall('<p>(.*?)<em>', res.text)
    addresses = re.findall('<p>.*?<em>\|</em>(.*?)<em>\|', res.text)
    people = re.findall('<p>.*?<em>\|</em>.*?<em>\|</em>(.*?)<em>\|', res.text)
    websites = re.findall('<span class="urladdress">(.*?)</span>', res.text)
    reviews = re.findall('<dd><span class="grade_star ps_start mr10"><i style="width:.*?;"></i></span>(.*?)</dd>', res.text)
    salarys = re.findall('<dd class="grey_99">.*?&nbsp;&nbsp;.(.*?)</dd>', res.text)
    for company, kind, address, person, website, review, salary in zip(companys,kinds,addresses,people,websites,reviews,salarys):
        count += 1
        print('Top:{}'.format(count))
        print('公司:'+company)
        print('行业:'+kind)
        print('地址:'+address)
        print('人数:'+person)
        print('主页:'+website)
        print('评分:'+review)
        print('平均月薪:'+salary)
        print()
        file.write('Top:{}'.format(count) + '\n')
        file.write('公司:'+company + '\n')
        file.write('行业:'+kind + '\n')
        file.write('地址:'+address + '\n')
        file.write('人数:'+person + '\n')
        file.write('主页:'+website + '\n')
        file.write('评分:'+review + '\n')
        file.write('平均月薪:'+salary + '\n')
        file.write('\n')

def main():
    global file
    global count
    count = 0
    file = open('E:\AllPrj\PyCharmPrj\py-crawler\kanzhun-jobs-crawler-test\kanzhun-jobs-results.txt', 'a+', encoding='utf-8')
    # 列表推倒式, 生成 urls, 注意有两个 page 变量
    urls = ['http://www.kanzhun.com/plc52p{page}.html?ka=paging{page}'.format(page=page) for page in range(1, 11)]
    for url in urls:
        get_info(url)
        time.sleep(1)
    file.close()

if __name__ == '__main__':
    main()
