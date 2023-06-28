import mysql.connector


class InsertKpis:

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
        mysql_cursor = my_connection.cursor(dictionary=True, buffered=True)
        return my_connection, mysql_cursor

    def insert_kpis(self, table_name=None, test_id=None, column_names=None, values=None):
        for value in values:
            # print(value)
            try:
                query = 'insert into ' + table_name + ' ' + str(column_names).replace('\'', '') + ' values ' + str(
                    value)
                # print(query)
                self.my_cursor.execute(query)
            except Exception as e:
                print('Exception')
                print(str(e))
        print('done for test :- ' + str(test_id))
        # print('committing to db')
        self.my_connection.commit()

    def close_connection(self):
        if self.my_connection is not None:
            # print('closing connection')
            self.my_connection.close()
            # print('connection closed')
        else:
            print('connection is closed already')

    def check_data_in_table(self, table_name=None, test_id=None, kpi_name=None, test_case_name=None):
        try:
            sql = 'select test_id from ' + table_name + ' where test_id = \'' + test_id + '\' and kpi_name = \'' + \
                  kpi_name + '\' and test_case_name = \'' + test_case_name + '\''
            print(sql)
            self.my_cursor.execute(sql)
            db_test_id = self.my_cursor.fetchone()
            print(db_test_id)
            return db_test_id
        except Exception as e:
            return None

    def check_data_in_analytics_table(self, table_name=None, test_id=None, test_case_name=None, test_case_status=None):
        try:
            sql = 'select test_id from ' + table_name + ' where test_id = \'' + test_id + '\' and test_case_name = \'' + \
                  test_case_name + '\' and test_case_status = \'' + test_case_status + '\''
            print(sql)
            self.my_cursor.execute(sql)
            db_test_id = self.my_cursor.fetchone()
            print(db_test_id)
            return db_test_id
        except Exception as e:
            print(str(e))
            return None

    def insert_data(self, table_name=None, kpi_object=None):
        try:
            query = 'insert into ' + table_name + ' ' + str(tuple(kpi_object.keys())).replace('\'', '') + ' values ' + \
                    str(tuple(kpi_object.values()))
            # print(query)
            self.my_cursor.execute(query)
            self.my_connection.commit()
        except Exception as e:
            print('Exception')
            print(str(e))
        # print('committing to db')

    def update_data(self, table_name=None, kpi_object=None, test_id=None):
        try:
            query = 'UPDATE ' + table_name + ' SET {}'.format(', '.join('{}=%s'.format(key) for key in kpi_object)) + \
                    ' where test_id = \'' + test_id + '\' and kpi_name = \'' + \
                    kpi_object['kpi_name'] + '\' and test_case_name = \'' + kpi_object['test_case_name'] + '\''
            print(query)
            self.my_cursor.execute(query, tuple(kpi_object.values()))
            self.my_connection.commit()
        except Exception as e:
            print('Exception')
            print(str(e))
        # print('committing to db')

    def update_analytics_data(self, table_name=None, my_analytics=None, test_id=None):
        try:
            query = 'UPDATE ' + table_name + ' SET {}'.format(', '.join('{}=%s'.format(key) for key in my_analytics)) + \
                    ' where test_id = \'' + test_id + '\' and test_case_name = \'' + \
                    my_analytics['test_case_name'] + '\' and test_case_status = \'' + my_analytics['test_case_status'] + '\''
            print(query)
            self.my_cursor.execute(query, tuple(my_analytics.values()))
            self.my_connection.commit()
        except Exception as e:
            print('Exception')
            print(str(e))

    def delete_data(self, table_name=None, test_id=None, kpi_name=None, test_case_name=None):
        try:
            sql = 'delete from ' + table_name + ' where test_id = \'' + test_id + '\' and kpi_name = \'' + \
                  kpi_name + '\' and test_case_name = \'' + test_case_name + '\''
            print(sql)
            self.my_cursor.execute(sql)
            self.my_connection.commit()
        except Exception as e:
            print('Exception in delete')
            print(str(e))
        # print('committing to db')

    def get_empty_project_test_ids(self, table_name=None):
        try:
            sql = 'select distinct(test_id) from ' + table_name + ' where project_name = \'\' or project_name is null'
            print(sql)
            self.my_cursor.execute(sql)
            db_test_id = self.my_cursor.fetchall()
            print(db_test_id)
            return db_test_id
        except Exception as e:
            return None
