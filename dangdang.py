import requests
import re
import json
import xlwt

'''
函数名：request_dandan(url):
url为网页链接，通过request.get(url)请求访问网站，获得网页代码信息，通过return.text返回
'''
def request_dandan(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None

'''
函数名：paser_result(html)
获取到的网页代码数据，通过re.compile(),使用正则表达式提取需要的数据，最后使用for循环将获取的信息打包
'''
def parse_result(html):
    #pattern = re.compile('<li>.*?list_num.*?(\d+).</div>.*?<img src="(.*?)".*?class="name".*?title="(.*?)">.*?class="star">.*?class="tuijian">(.*?)</span>.*?class="publisher_info">.*?target="_blank">(.*?)</a>.*?class="biaosheng">.*?<span>(.*?)</span></div>.*?<p><span\sclass="price_n">&yen;(.*?)</span>.*?</li>',re.S)
    pattern = re.compile('<li>.*?list_num.*?(\d+).</div>.*?class="name".*?title="(.*?)">.*?class="star">.*?class="tuijian">(.*?)</span>.*?class="publisher_info">.*?target="_blank">(.*?)</a>.*?class="biaosheng">.*?<span>(.*?)</span></div>.*?class="publisher_info"><span>(.*?)</span>.*?<p><span\sclass="price_n">&yen;(.*?)</span>.*?</li>',re.S)
    items = re.findall(pattern, html)
    #print(items)
    for item in items:
        #print(item)
        yield {
            'range': item[0],
            'title': item[1],
            'recommend': item[2],
            'author': item[3],
            'stars' : item[4],
            'time': item[5],
            'price': item[6]
        }

'''
文件名：write_item_to_file(item,count_num)
使用xlrd库，将爬到的信息写入excel
'''
def write_item_to_file(item, count_num):
    print('开始写入数据 ====> ' + str(item))
    # with open('book.txt', 'a', encoding='UTF-8') as f:
    #     f.write(json.dumps(item, ensure_ascii=False) + '\n')
    #     f.close()
    #print(item['range'])
    #print(count_num)
    sheet.write(count_num, 0, item['range'])
    sheet.write(count_num, 1, item['title'])
    sheet.write(count_num, 2, item['recommend'])
    sheet.write(count_num, 3, item['author'])
    sheet.write(count_num, 4, item['stars'])
    sheet.write(count_num, 5, item['time'])
    sheet.write(count_num, 6, item['price'])



def main(page, count_num):
    url = 'http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-' + str(page)
    html = request_dandan(url)
    items = parse_result(html) # 解析过滤我们想要的信息

    #写excel文件中的标题信息
    sheet.write(0, 0, '排名')
    sheet.write(0, 1, '书名')
    sheet.write(0, 2, '推荐')
    sheet.write(0, 3, '作者')
    sheet.write(0, 4, '五星评价数')
    sheet.write(0, 5, '出版时间')
    sheet.write(0, 6, '价格')

    for item in items:
        write_item_to_file(item, count_num)
        count_num +=1


if __name__ == "__main__":
    '''
    创建excel文件
    '''
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)

    #创建excel文件sheet
    sheet = book.add_sheet('当当Top250', cell_overwrite_ok=True)
    for i in range(1, 26):
        main(i, count_num=(i-1)*10+1)

    book.save(u'豆瓣最受欢迎的250部电影.csv')