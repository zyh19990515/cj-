import xlrd
import matplotlib.pyplot as plt
import numpy as np

def priceData(price_data):
    price_data_array = np.zeros(6, dtype=np.int)
    for i in range(0, len(price_data)):
        price_data[i] = price_data[i].replace(",", "", 1)#超过1000会写成1，000，使用replace()删除逗号
        price_data[i] = float(price_data[i])#将格式从str转为float
        #将价格分为6个区间，判断并计数，将计数结果放入price_data_array数组中
        if (price_data[i] > 0 and price_data[i] <= 20):
            price_data_array[0] += 1
        elif (price_data[i] > 20 and price_data[i] <= 40):
            price_data_array[1] += 1
        elif (price_data[i] > 40 and price_data[i] <= 60):
            price_data_array[2] += 1
        elif (price_data[i] > 60 and price_data[i] <= 80):
            price_data_array[3] += 1
        elif (price_data[i] > 80 and price_data[i] <= 100):
            price_data_array[4] += 1
        elif (price_data[i] > 100):
            price_data_array[5] += 1
    #转为百分比
    price_data_array = price_data_array / 250
    #饼状图中标签
    labal = ['0-20', '20-40', '40-60', '60-80', '80-100', '>100']
    plt.rcParams["font.family"] = 'Arial Unicode MS'
    plt.rcParams['axes.unicode_minus'] = False
    #饼状图
    plt.pie(price_data_array, labels=labal, autopct='%0.2f%%')
    plt.suptitle("price", fontsize=16, y=0.93)
    plt.show()

def fiveStarsData(fiveStars_data):
    y = np.linspace(0, 250, 250, dtype=np.int)
    fiveStars_data_array = np.zeros(6, dtype=np.int)



    for i in range(0, len(fiveStars_data)):
        fiveStars_data[i] = fiveStars_data[i].replace("次", "", 1)
        fiveStars_data[i] = float(fiveStars_data[i])
        if(fiveStars_data[i]>0 and fiveStars_data[i]<100):
            fiveStars_data_array[0] += 1
        elif(fiveStars_data[i]>100 and fiveStars_data[i]<500):
            fiveStars_data_array[1] += 1
        elif (fiveStars_data[i] > 500 and fiveStars_data[i] < 1000):
            fiveStars_data_array[2] += 1
        elif (fiveStars_data[i] > 1000 and fiveStars_data[i] < 5000):
            fiveStars_data_array[3] += 1
        elif (fiveStars_data[i] > 5000 and fiveStars_data[i] < 10000):
            fiveStars_data_array[4] += 1
        elif (fiveStars_data[i] > 10000):
            fiveStars_data_array[5] += 1
    fiveStars_data_array = fiveStars_data_array / 250
    labal = ['0-100', '100-500', '500-1000', '1000-5000', '5000-10000', '>10000']
    plt.rcParams["font.family"] = 'Arial Unicode MS'
    plt.rcParams['axes.unicode_minus'] = False
    plt.pie(fiveStars_data_array, labels=labal, autopct='%0.2f%%')
    plt.suptitle("fiveStars", fontsize=16, y=0.93)
    plt.show()

    plt.scatter(y, fiveStars_data)
    plt.show()

def dateData(date_data):
    date_data_array = np.zeros(16, dtype=np.int32)
    empty_index = []
    #print(len(date_data))
    for i in range(0, len(date_data)):
        if (len(date_data[i])==0):
            empty_index.append(i)
    cnt = 0
    for num in empty_index:
        #print(date_data[num-cnt])
        del date_data[num-cnt]
        cnt += 1
   
    for i in range(0, len(date_data)):
        date_data[i] = date_data[i][:-6]
        date_data[i] = int(float(date_data[i]))
    date_data = np.sort(date_data)
    print(date_data)
    cnt = 0
    for i in range(0, len(date_data)):
        if(i == 0):
            date_data_array[cnt]+=1
        else:
            if(date_data[i]==date_data[i-1]):
                date_data_array[cnt] += 1
            elif(date_data[i]!=date_data[i-1]):
                cnt += 1
                date_data_array[cnt] +=1
    x = [1991, 2006, 2007, 2009, 2010, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
    plt.bar(x, date_data_array)
    plt.show()



if __name__ == '__main__':
    #打开excel文件
    book = xlrd.open_workbook("dangdang.csv")
    data = book.sheets()[0]
    #获取文件中价格那一列的数据
    price_data = data.col_values(6)#提取价格数据
    #删除标题
    del price_data[0]
    #获取五星评价次数数据
    fiveStars_data = data.col_values(4)#提取五星数据
    # 删除标题
    del fiveStars_data[0]
    #获取出版日期数据
    date_data = data.col_values(5)
    # 删除标题
    del date_data[0]

    #处理价格数据并画图
    priceData(price_data)
    # 处理五星评价次数数据并画图
    fiveStarsData(fiveStars_data)
    # 处理出版日期数据并画图
    dateData(date_data)

