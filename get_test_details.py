from get_data_from_mongo import GetMongoData
from get_mysql_test_details import GetMysqlTestDetails


class GetTestDetails:

    def __init__(self, db_host_type=None, data_base_type=None):
        self.db_host_type = db_host_type
        self.data_base_type = data_base_type

    def get_test_data(self, db_url=None, db_user=None, db_password=None, source_db=None, table_name=None,
                      test_id_key=None, test_id=None):
        if self.data_base_type == 'mongodb':
            get_kpis_object = GetMongoData(host_type=self.db_host_type, db_url=db_url, db_user=db_user,
                                           db_password=db_password, source_db=source_db)
            test_details = get_kpis_object.get_test_details(collection_name=table_name, identifier_key=test_id_key,
                                                            identifier=test_id)
            return test_details

        elif self.data_base_type == 'mysql':
            get_test_details = GetMysqlTestDetails(db_url=db_url, db_user=db_user, db_password=db_password,
                                                   source_db=source_db)
            test_details = get_test_details.get_details(table_name=table_name, identifier_key=test_id_key,
                                                        identifier=test_id)
            return test_details

        elif self.data_base_type == 'postgresql':
            pass
        else:
            pass
