import mysql.connector


class GetMysqlTestDetails:

    def __init__(self, db_url=None, db_user=None, db_password=None, source_db=None):
        self.my_connection, self.my_cursor = self.get_mysql_cursor(db_url=db_url, db_user=db_user,
                                                                   db_password=db_password, source_db=source_db)

    def get_mysql_cursor(self, db_url=None, db_user=None, db_password=None, source_db=None):
        my_connection = mysql.connector.connect(
            host=db_url,
            user=db_user,
            password=db_password,
            database=source_db
        )
        mysql_cursor = my_connection.cursor(dictionary=True)
        return my_connection, mysql_cursor

    def get_details(self, table_name=None, identifier_key=None, identifier=None):
        # sql = 'select * from ' + table_name + ' where ' + identifier_key + ' = ' + identifier
        sql = 'select j.*,p.name as projectName, s.title as scriptName,dt.manufacturer as deviceMake,dt.platform as ' \
              'devicePlatform,dt.os as deviceOsVersion,dt.operator as deviceNetwork, dt.city as deviceLocation,' \
              'u.firstname as userName from ' \
              + table_name + ' j join project p on j.projectid=p.id join script s on j.scriptid=s.id join devicetray ' \
                             'dt on j.trayid=dt.trayid and j.deviceid=dt.deviceid join user u on j.userid=u.id where j.' \
              + identifier_key + ' = ' + identifier
        try:
            # print(sql)
            self.my_cursor.execute(sql)
            test_details = self.my_cursor.fetchone()
            # print(test_details)
            self.close_connection()
            return test_details
        except Exception as e:
            print("---------------error fetching data for this this--------------------------")
            print(sql)
            print(str(e))
            return None

    def close_connection(self):
        if self.my_connection is not None:
            print('closing connection')
            self.my_connection.close()
            print('connection closed')
        else:
            print('connection is closed already')
