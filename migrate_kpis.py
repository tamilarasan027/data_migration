import json
from format_data import FormatData
from get_data_from_mongo import GetMongoData
from insert_kpis import InsertKpis
from get_test_details import GetTestDetails


class MigrateKpis:

    def __init__(self):
        self.config = None
        print("initiating...")
        self.load_config()
        print("initiated...")

    def load_config(self):
        self.config = json.load(open("config.json"))
        if type(self.config) is dict:
            return self.config
        else:
            print("There is no valid configuration file")
            return None

    def migrate_kpis(self, start_time=None, end_time=None):
        for tenant in self.config['tenants']:
            print('running for :- ' + tenant['name'])
            tenant_details = tenant['details']
            host_type = None
            if 'host_type' in tenant:
                host_type = tenant['host_type']
            get_kpis_object = GetMongoData(host_type=host_type, db_url=tenant['source_db_url'],
                                           db_user=tenant['source_db_user'], db_password=tenant['source_db_password'],
                                           source_db=tenant_details['kpi_source_db'])
            my_test_list = []
            try:
                my_test_list = get_kpis_object.get_test_list1(collection_name=tenant_details['kpi_source_collection'],
                                                              required_key=tenant_details['kpi_test_identifier_key'],
                                                              start_time=start_time, end_time=end_time,
                                                              time_key=tenant_details['kpi_date_time_key'])
            except Exception as e:
                print('----------incorrect date format ---------------')
                print(start_time)
                print(end_time)
                print(str(e))
            # print(my_test_list)
            print(len(my_test_list))
            tenant_kpi_destination_details = tenant['details']['kpi_destination_details']
            insert_kpis_object = InsertKpis(db_url=tenant['destination_db_url'],
                                            db_user=tenant['destination_db_user'],
                                            db_password=tenant['destination_db_password'],
                                            source_db=tenant_kpi_destination_details['db'])
            tenant_test_source_db_details = tenant['details']['test_source_db_details']
            for test_id in my_test_list:
                test_id = str(test_id)
                print("for tenant :- " + tenant['name'] + "testId is :- " + test_id)
                test_details_host_type = None
                if 'host_type' in tenant_test_source_db_details:
                    test_details_host_type = tenant_test_source_db_details['host_type']

                get_test_details_object = GetTestDetails(db_host_type=test_details_host_type,
                                                         data_base_type=tenant_test_source_db_details['type'])

                test_details = get_test_details_object.get_test_data(db_url=tenant_test_source_db_details['url'],
                                                                     db_user=tenant_test_source_db_details['user'],
                                                                     db_password=tenant_test_source_db_details
                                                                     ['password'],
                                                                     source_db=tenant_test_source_db_details['db'],
                                                                     table_name=tenant_test_source_db_details['table'],
                                                                     test_id_key=tenant_test_source_db_details
                                                                     ['test_identifier_key'],
                                                                     test_id=test_id)

                # Added This condition if exception occurs while fetching test id
                if test_details is None:
                    try:
                        tenant_test_source_db_details_mongo = tenant['details']['test_source_db_details_mongo']
                        get_test_details_object = GetTestDetails(db_host_type=test_details_host_type,
                                                                 data_base_type=tenant_test_source_db_details_mongo[
                                                                     'type'])
                        test_details = get_test_details_object.get_test_data(
                            db_url=tenant_test_source_db_details_mongo['url'],
                            db_user=tenant_test_source_db_details_mongo['user'],
                            db_password=tenant_test_source_db_details_mongo
                            ['password'],
                            source_db=tenant_test_source_db_details_mongo['db'],
                            table_name=tenant_test_source_db_details_mongo[
                                'table'],
                            test_id_key=tenant_test_source_db_details_mongo
                            ['test_identifier_key'],
                            test_id=test_id)
                    except Exception as e:
                        print("some error in fetching this test id -----------------")
                        print(test_id)
                        print(str(e))

                temp_test_details = test_details
                kpi_test_id = test_id
                if tenant_details['kpi_test_identifier_type'] == 'int':
                    kpi_test_id = int(kpi_test_id)

                my_kpi_list = []

                # Special case for app-xp
                if test_details is not None and 'kpis' in test_details:
                    if type(test_details['kpis']) is dict:
                        print(str(test_details['kpis'].keys()))
                        for key in test_details['kpis'].keys():
                            my_kpi_list.append({"name": key, "value": test_details['kpis'][key], "status": "Completed"})
                    else:
                        my_kpi_list = test_details['kpis']
                else:
                    my_kpi_list = get_kpis_object.get_kpi_list(collection_name=tenant_details['kpi_source_collection'],
                                                               identifier_key=tenant_details['kpi_test_identifier_key'],
                                                               identifier=kpi_test_id)
                # print(test_details)
                print(len(my_kpi_list))
                if test_details is not None and 'info' in test_details:
                    user_name = test_details['uuid']['username']
                    test_details = test_details['info']
                    test_details['userName'] = user_name
                    test_details['devicePlatform'] = test_details['deviceOsVersion'].split(' ')[0]
                    test_details['deviceOsVersion'] = test_details['deviceOsVersion'].split(' ')[1]
                    if 'mozarkEventAttributes_applicationName' in my_kpi_list[0]:
                        test_details['applicationName'] = my_kpi_list[0]['mozarkEventAttributes_applicationName']
                    if 'mozarkEventAttributes_deviceMake' in my_kpi_list[0]:
                        test_details['deviceMake'] = my_kpi_list[0]['mozarkEventAttributes_deviceMake']
                else:
                    try:
                        test_details = {'userName': my_kpi_list[0]['mozarkEventAttributes_userName'],
                                        'devicePlatform': my_kpi_list[0]['mozarkEventAttributes_devicePlatform'],
                                        'deviceOsVersion': my_kpi_list[0][
                                            'mozarkEventAttributes_devicePlatformVersion'],
                                        'applicationName': my_kpi_list[0]['mozarkEventAttributes_applicationName'],
                                        'scriptName': my_kpi_list[0]['mozarkEventAttributes_scriptId'],
                                        'deviceMake': my_kpi_list[0]['mozarkEventAttributes_deviceMake'],
                                        'devicename': my_kpi_list[0]['mozarkEventAttributes_deviceModel']}
                    except Exception as e:
                        print(str(e))
                        test_details = temp_test_details
                print(test_details)
                format_data_obj = FormatData(test_id=test_id, test_obj=test_details, kpi_list=my_kpi_list)
                my_final_list = format_data_obj.format_data()
                # # add analytics data in RDS
                # try:
                #     my_analytics_list = format_data_obj.format_analytics_data()
                #     print(my_analytics_list)
                #     for my_analytics in my_analytics_list:
                #         check_test_id = insert_kpis_object.check_data_in_analytics_table(
                #             table_name=tenant_kpi_destination_details
                #             ['analytics_table'], test_id=test_id, test_case_name=my_analytics['test_case_name'],
                #             test_case_status=my_analytics['test_case_status'])
                #
                #         if check_test_id is None:
                #             print('inserting')
                #             insert_kpis_object.insert_data(table_name=tenant_kpi_destination_details['analytics_table'],
                #                                            kpi_object=my_analytics)
                #         else:
                #             my_kpi.pop('test_id')
                #             my_kpi.pop('uuid')
                #             print('updating')
                #             insert_kpis_object.update_analytics_data(table_name=
                #                                                      tenant_kpi_destination_details['analytics_table'],
                #                                                      my_analytics=my_analytics, test_id=test_id)
                # except Exception as e:
                #     print("-------------some error in migrating analytics data---------------------")
                #     print(str(e))

                for my_kpi in my_final_list:
                    check_test_id = insert_kpis_object.check_data_in_table(table_name=tenant_kpi_destination_details
                    ['table'], test_id=test_id, kpi_name=my_kpi['kpi_name'], test_case_name=my_kpi['test_case_name'])

                    if check_test_id is None:
                        print('inserting')
                        # insert_kpis_object.delete_data(table_name=tenant_kpi_destination_details['table'],
                        # test_id=test_id, kpi_name=my_kpi['kpi_name'], test_case_name=my_kpi['test_case_name'])
                        insert_kpis_object.insert_data(table_name=tenant_kpi_destination_details['table'],
                                                       kpi_object=my_kpi)
                    else:
                        my_kpi.pop('test_id')
                        my_kpi.pop('uuid')
                        print('updating')
                        insert_kpis_object.update_data(table_name=tenant_kpi_destination_details['table'],
                                                       kpi_object=my_kpi, test_id=test_id)
            insert_kpis_object.close_connection()
