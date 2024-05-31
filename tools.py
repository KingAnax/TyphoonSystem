import pymysql
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.basemap import Basemap


# 将pymysql的查询结果转化为json格式
def sql_fetch_json(cursor: pymysql.cursors.Cursor):
    keys = []
    for column in cursor.description:
        keys.append(column[0])
    key_number = len(keys)

    json_data = []
    for row in cursor.fetchall():
        item = dict()
        for q in range(key_number):
            item[keys[q]] = row[q]
        json_data.append(item)
    return json_data


class MySQLTools():
    # 初始化
    def __init__(self, host, user, password, db, charset):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset
        self.conn = pymysql.connect(host=host, user=user, password=password, db=db, charset=charset)
        self.cur = self.conn.cursor()


    # 占比统计
    def numStatic(self):
        sqlstr = "select count(*) as cnt from addition_info where rank = 'TD';"
        self.cur.execute(sqlstr)
        n1 = self.cur.fetchone()[0]
        sqlstr = "select count(*) as cnt from addition_info where rank = 'STD';"
        self.cur.execute(sqlstr)
        n2 = self.cur.fetchone()[0]
        sqlstr = "select count(*) as cnt from addition_info where rank = 'TS';"
        self.cur.execute(sqlstr)
        n3 = self.cur.fetchone()[0]
        sqlstr = "select count(*) as cnt from addition_info where rank = 'STS';"
        self.cur.execute(sqlstr)
        n4 = self.cur.fetchone()[0]
        sqlstr = "select count(*) as cnt from addition_info where rank = 'TY';"
        self.cur.execute(sqlstr)
        n5 = self.cur.fetchone()[0]
        sqlstr = "select count(*) as cnt from addition_info where rank = 'STY';"
        self.cur.execute(sqlstr)
        n6 = self.cur.fetchone()[0]
        n = n1 + n2 + n3 + n4 + n5 + n6
        return int(n1 / n * 100), int(n2 / n * 100), int(n3 / n * 100), int(n4 / n * 100), int(n5 / n * 100), int(
            n6 / n * 100)

    def addTy(self, ty_no, name):
        sqlstr = f"insert into basic_info(no, name) values('{ty_no}','{name}');"
        self.cur.execute(sqlstr)
        self.conn.commit()
        sqlstr = f"select * from basic_info "
        self.cur.execute(sqlstr)
        self.conn.commit()
        return

    def basicInfo(self):
        sqlstr = f"select * from basic_info "
        self.cur.execute(sqlstr)
        self.conn.commit()
        return sql_fetch_json(self.cur)

    def additionInfo(self):
        sqlstr = f"select * from addition_info "
        self.cur.execute(sqlstr)
        self.conn.commit()
        return sql_fetch_json(self.cur)

    def moveInfo(self, ty_no):
        sqlstr = f"select * from move_info " \
                 f"where ty_no = '{ty_no}' "
        self.cur.execute(sqlstr)
        self.conn.commit()
        return sql_fetch_json(self.cur)

    # 台风编号查询
    def ty_min(self):
        sqlstr = f"select no, name " \
                 f"from basic_info; "
        self.cur.execute(sqlstr)
        self.conn.commit()
        return sql_fetch_json(self.cur)


    # 绘制轨迹图
    def drawMap(self, tynm):
        # 绘制全球地图
        plt.figure(figsize=(20, 12))
        map = Basemap(llcrnrlon=70, llcrnrlat=2, urcrnrlon=170, urcrnrlat=58)
        map.etopo(scale=0.5, alpha=0.5)
        map.drawcoastlines()
        map.drawcountries()

        # 添加经纬线
        parallels = np.linspace(3, 55, 5)
        # print(parallels)
        map.drawparallels(parallels, labels=[False, True, False, False], fontsize=10)
        meridians = np.linspace(70, 170, 5)
        # print(meridians)
        map.drawmeridians(meridians, labels=[False, False, False, True], fontsize=10)

        sqlstr = f"SELECT longitude FROM move_info WHERE ty_no = '{tynm}'"
        self.cur.execute(sqlstr)
        lats = [row[0] for row in self.cur.fetchall()]  # Latitude values
        print(lats)

        sqlstr = f"SELECT latitude FROM move_info WHERE ty_no = '{tynm}'"
        self.cur.execute(sqlstr)
        lons = [row[0] for row in self.cur.fetchall()]  # Latitude values
        print(lons)

        x, y = map(lats, lons)
        map.plot(x, y, color='r', linewidth=1.5)

        # 显示地图
        plt.title('Typhoon Path')
        output_filename = './static/images/path_map.png'
        plt.savefig(output_filename, format='png')
        plt.show()
        plt.close()

    # 导入数据用
    def importData(self):
        columns_to_import = ['tfbh', 'strong', 'power', 'speed', 'pressure']  # 选择要导入的列名
        df = pd.read_csv('typhoon2022.csv', usecols=columns_to_import)
        df = df.drop_duplicates(subset='tfbh', keep='first')
        column_mapping = {
            'tfbh': 'ty_no',
            'strong': 'rank'
        }  # 列名映射关系
        df = df.rename(columns=column_mapping)
        df = df.fillna('-1')
        print(df)
        # 插入数据
        for index, row in df.iterrows():
            insert_query = f"INSERT INTO addition_info VALUES {tuple(row.values)};"
            self.cur.execute(insert_query)
            self.conn.commit()