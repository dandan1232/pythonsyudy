from flask import Flask, render_template
import sqlalchemy
import pandas as pd
import json
import pymysql
import numpy

# 1.首先构建服务
app = Flask(__name__)


# 2.创建服务echarts可视化访问路径
@app.route("/")
def table():
    return render_template("show.html")


# 3.创建ajax获取后台数据的访问路径
# 以json文件的形式返回
@app.route("/data", methods=['POST', 'GET'])
def getdata():
    return (get_sql_data())


# 4.使用sqlalchemy获取后台数据库数据，整理成json数据
# (数据库产品名称+数据库操作模块名://数据库用户名:密码@数据库ip地址:数据库端口号/数据库名称)
def get_sql_data():
    engine = sqlalchemy.create_engine("mysql+pymysql://root:ldd123789dd@localhost:3306/bigdata")
    #     根据所需要的数据，选择read_sql_query,read_sql_table,read_sql方法查取数据。
    data_frame = pd.read_sql_table(table_name="bar", con=engine)
    # id,name,price.转换成json数据类型返回。
    names = data_frame['name'].values
    prices = data_frame['price'].values
    # 将数组转化为dict，然后转化为json字符串
    dict = {
        'names': names.tolist(),
        'prices': prices.tolist()
    }
    # print(dict)
    # print(json.dumps(dict, ensure_ascii=False))
    # print('....')
    return json.dumps(dict, ensure_ascii=False)


if __name__ == '__main__':
    app.run(debug=True, port='5000')
