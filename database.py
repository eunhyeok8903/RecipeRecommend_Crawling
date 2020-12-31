import pymysql

class MysqlController:
    def __init__(self, host, id, pw, db_name):
        try:
            self.conn = pymysql.connect(host=host, user=id, password=pw, db=db_name, charset='utf8')
            self.curs = self.conn.cursor(pymysql.cursors.DictCursor)
        except self.conn.DatabaseError as e:
            print(e)
            self.conn.close()

    # 메뉴 insert
    def insert_menu(self, mname, url):
        try:
            sql = 'INSERT INTO menu(mname, url) VALUES (%s, %s)'
            self.curs.execute(sql, (mname, url))
            self.conn.commit()
            return self.curs.lastrowid
        except self.conn.DatabaseError as e:
            print(e)

    # 재료 insert
    def insert_ingredient(self, menuId, iname):
        try:
            sql = 'INSERT INTO ingredient(menuId, iname) VALUES (%s, %s)'
            self.curs.execute(sql, (menuId, iname))
            self.conn.commit()
        except self.conn.DatabaseError as e:
            print(e)

    # def insert_recipeOrder(self, context, menuId):
    #     try:
    #         sql = 'INSERT INTO recipeorder(context, menuId) VALUES (%s, %s)'
    #         self.curs.execute(sql, (context, menuId))
    #         self.conn.commit()
    #     except self.conn.DatabaseError as e:
    #         print(e)

    # def insert_sauce(self, menuId, sname):
    #     try:
    #         sql = 'INSERT INTO sauce(menuId, sname) VALUES (%s, %s)'
    #         self.curs.execute(sql, (menuId, sname))
    #         self.conn.commit()
    #     except self.conn.DatabaseError as e:
    #         print(e)

    def select_ingredient_iname(self):
        try:
            sql = 'SELECT (iname) FROM ingredient'
            self.curs.execute(sql)
            self.conn.commit()
            res = self.curs.fetchall()
            return res
        except self.conn.DatabaseError as e:
            print(e)