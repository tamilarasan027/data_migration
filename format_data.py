import uuid
from datetime import datetime, timedelta
import traceback
import re


def get_time_in_utc(date_str):
    time_format = '%Y-%m-%dT%H:%M:%S'
    date_and_time = date_str.split('.')[0]
    # print(date_and_time)
    other_time = date_str.split('.')[1]
    date_obj = datetime.strptime(date_and_time, time_format)
    # print(str(date_obj))
    if '+' in other_time:
        offset_time = other_time.split('+')[1]
        # print(offset_time)
        date_obj = date_obj - timedelta(hours=int(offset_time[:2]))
        date_obj = date_obj - timedelta(minutes=int(offset_time[-2:]))
    if '-' in other_time:
        offset_time = other_time.split('-')[1]
        # print(offset_time)
        date_obj = date_obj + timedelta(hours=int(offset_time[:2]))
        date_obj = date_obj + timedelta(minutes=int(offset_time[-2:]))
    # print(str(date_obj))
    return str(date_obj)


def split_timestamp_timezone(timestamp):
    # Splitting timestamp and timezone using regular expression
    pattern = r'(?P<timestamp>[\d-]+T[\d:.]+)(?P<timezone>[+-]\d{2}(?::?\d{2})?)'
    match = re.match(pattern, timestamp)

    if match:
        extracted_timestamp = match.group('timestamp')
        extracted_timezone = match.group('timezone')
        return extracted_timestamp, extracted_timezone
    else:
        return "", ""


class FormatData:

    def __init__(self, test_id=None, test_obj=None, kpi_list=None):
        self.test_id = test_id
        self.test_obj = test_obj
        self.kpi_list = kpi_list

    # def format_analytics_data(self):
    #     analytics_data = []
    #     test_cases = self.test_obj['testCases']
    #     for test_case in test_cases:
    #         try:
    #             test_case_obj = {"uuid": str(uuid.uuid4()), 'test_id': self.test_id,
    #                              'test_case_name': test_case['testCaseName'],
    #                              'test_case_status': test_case['testCaseStatus']}
    #             test_case_obj = self.get_test_case_start_time(kpi_object={}, final_object=test_case_obj)
    #             test_case_obj = self.get_test_case_end_time(kpi_object={}, final_object=test_case_obj)
    #
    #             test_case_obj = self.get_test_start_time(kpi_object={}, final_object=test_case_obj)
    #             test_case_obj = self.get_test_end_time(kpi_object={}, final_object=test_case_obj)
    #             test_case_obj = self.get_test_status(kpi_object={}, final_object=test_case_obj)
    #             test_case_obj = self.get_project_name(kpi_object={}, final_object=test_case_obj)
    #             test_case_obj = self.get_application_name(kpi_object={}, final_object=test_case_obj)
    #             test_case_obj = self.get_application_package_name(kpi_object={}, final_object=test_case_obj)
    #             test_case_obj = self.get_application_package_version_name(kpi_object={}, final_object=test_case_obj)
    #             test_case_obj = self.get_test_script_name(kpi_object={}, final_object=test_case_obj)
    #             test_case_obj = self.get_device_make(kpi_object={}, final_object=test_case_obj)
    #             test_case_obj = self.get_device_model(kpi_object={}, final_object=test_case_obj)
    #             test_case_obj = self.get_device_platform(kpi_object={}, final_object=test_case_obj)
    #             test_case_obj = self.get_device_platform_version(kpi_object={}, final_object=test_case_obj)
    #             test_case_obj = self.get_device_city(kpi_object={}, final_object=test_case_obj)
    #             test_case_obj = self.get_device_country(kpi_object={}, final_object=test_case_obj)
    #             test_case_obj = self.get_device_location(kpi_object={}, final_object=test_case_obj)
    #             test_case_obj = self.get_user_name(kpi_object={}, final_object=test_case_obj)
    #             test_case_obj = self.get_browser_name(kpi_object={}, final_object=test_case_obj)
    #             test_case_obj = self.get_browser_version(kpi_object={}, final_object=test_case_obj)
    #             test_case_obj = self.get_device_network_type(kpi_object={}, final_object=test_case_obj)
    #             test_case_obj = self.get_device_mobile_operator(kpi_object={}, final_object=test_case_obj)
    #             test_case_obj = self.get_device_mobile_network_technology(kpi_object={}, final_object=test_case_obj)
    #             test_case_obj = self.get_device_city_from_geo_code(kpi_object={}, final_object=test_case_obj)
    #             test_case_obj = self.get_device_city_from_isp(kpi_object={}, final_object=test_case_obj)
    #             test_case_obj = self.get_device_cellular_network_id(kpi_object={}, final_object=test_case_obj)
    #             test_case_obj = self.get_device_serial(kpi_object={}, final_object=test_case_obj)
    #             analytics_data.append(test_case_obj)
    #         except Exception as e:
    #             print('Exception')
    #             traceback.print_exc()
    #             print(str(e))
    #     return analytics_data

    def format_data(self):
        my_final_list = []
        # column_names = ()
        for kpi_details in self.kpi_list:
            try:
                print(self.test_obj)
                # print(kpi_details)
                kpi_object = {"uuid": str(uuid.uuid4()), 'test_id': self.test_id}
                print(kpi_object)
                kpi_object = self.get_basic_kpi_data(kpi_object=kpi_details, final_object=kpi_object)
                kpi_object = self.get_test_start_time(kpi_object=kpi_details, final_object=kpi_object)
                kpi_object = self.get_test_end_time(kpi_object=kpi_details, final_object=kpi_object)
                kpi_object = self.get_test_status(kpi_object=kpi_details, final_object=kpi_object)
                kpi_object = self.get_project_name(kpi_object=kpi_details, final_object=kpi_object)
                kpi_object = self.get_application_name(kpi_object=kpi_details, final_object=kpi_object)
                kpi_object = self.get_application_package_name(kpi_object=kpi_details, final_object=kpi_object)
                kpi_object = self.get_application_package_version_name(kpi_object=kpi_details, final_object=kpi_object)
                kpi_object = self.get_test_script_name(kpi_object=kpi_details, final_object=kpi_object)
                kpi_object = self.get_device_make(kpi_object=kpi_details, final_object=kpi_object)
                kpi_object = self.get_device_model(kpi_object=kpi_details, final_object=kpi_object)
                kpi_object = self.get_device_platform(kpi_object=kpi_details, final_object=kpi_object)
                kpi_object = self.get_device_platform_version(kpi_object=kpi_details, final_object=kpi_object)
                kpi_object = self.get_device_city(kpi_object=kpi_details, final_object=kpi_object)
                kpi_object = self.get_device_country(kpi_object=kpi_details, final_object=kpi_object)
                kpi_object = self.get_device_location(kpi_object=kpi_details, final_object=kpi_object)
                kpi_object = self.get_user_name(kpi_object=kpi_details, final_object=kpi_object)
                kpi_object = self.get_browser_name(kpi_object=kpi_details, final_object=kpi_object)
                kpi_object = self.get_browser_version(kpi_object=kpi_details, final_object=kpi_object)
                kpi_object = self.get_device_network_type(kpi_object=kpi_details, final_object=kpi_object)
                kpi_object = self.get_device_mobile_operator(kpi_object=kpi_details, final_object=kpi_object)
                kpi_object = self.get_device_mobile_network_technology(kpi_object=kpi_details, final_object=kpi_object)
                kpi_object = self.get_device_city_from_geo_code(kpi_object=kpi_details, final_object=kpi_object)
                kpi_object = self.get_device_city_from_isp(kpi_object=kpi_details, final_object=kpi_object)
                kpi_object = self.get_device_cellular_network_id(kpi_object=kpi_details, final_object=kpi_object)
                kpi_object = self.get_device_serial(kpi_object=kpi_details, final_object=kpi_object)

                if 'mozarkEventAttributes_additional_info_6' in kpi_object:
                    kpi_object['additional_info_6'] = kpi_details['mozarkEventAttributes_additional_info_6']
                if 'mozarkEventAttributes_additional_info_7' in kpi_object:
                    kpi_object['additional_info_7'] = kpi_details['mozarkEventAttributes_additional_info_7']
                if 'mozarkEventAttributes_additional_info_8' in kpi_object:
                    kpi_object['additional_info_8'] = kpi_details['mozarkEventAttributes_additional_info_8']
                if 'mozarkEventAttributes_additional_info_9' in kpi_object:
                    kpi_object['additional_info_9'] = kpi_details['mozarkEventAttributes_additional_info_9']
                if 'mozarkEventAttributes_additional_info_10' in kpi_object:
                    kpi_object['additional_info_10'] = kpi_details['mozarkEventAttributes_additional_info_10']
                # print('------')
                # print(kpi_object)
                # my_final_list.append(tuple(kpi_object.values()))
                my_final_list.append(kpi_object)
                # column_names = tuple(kpi_object.keys())
            except Exception as e:
                print('Exception')
                traceback.print_exc()
                print(str(e))
        return my_final_list

    def get_test_start_time(self, kpi_object=None, final_object=None):
        if 'testStartTime' in self.test_obj:
            if self.test_obj['testStartTime'] is not None:
                extracted_timestamp, extracted_timezone = split_timestamp_timezone(self.test_obj['testStartTime'])
                final_object['test_start_date_time'] = get_time_in_utc(self.test_obj['testStartTime'])
                final_object['additional_info_1'] = extracted_timestamp
                final_object['additional_info_3'] = extracted_timezone
        elif 'starttime' in self.test_obj:
            if self.test_obj['starttime'] is not None:
                extracted_timestamp, extracted_timezone = split_timestamp_timezone(str(self.test_obj['starttime']))
                final_object['test_start_date_time'] = str(self.test_obj['starttime'])
                final_object['additional_info_1'] = extracted_timestamp
                final_object['additional_info_3'] = extracted_timezone
        elif 'testDate' in self.test_obj:
            if self.test_obj['testDate'] is not None:
                extracted_timestamp, extracted_timezone = split_timestamp_timezone(str(self.test_obj['testDate']))
                final_object['test_start_date_time'] = str(self.test_obj['testDate'])
                final_object['additional_info_1'] = extracted_timestamp
                final_object['additional_info_3'] = extracted_timezone
        elif 'mozarkEventAttributes_testStartDateTime' in kpi_object:
            if kpi_object['mozarkEventAttributes_testStartDateTime'] is not None:
                extracted_timestamp, extracted_timezone = split_timestamp_timezone(kpi_object['mozarkEventAttributes_testStartDateTime'])
                final_object['test_start_date_time'] = kpi_object['mozarkEventAttributes_testStartDateTime']
                final_object['additional_info_1'] = extracted_timestamp
                final_object['additional_info_3'] = extracted_timezone
        else:
            return final_object
        return final_object

    def get_test_end_time(self, kpi_object=None, final_object=None):
        if 'testEndTime' in self.test_obj:
            if self.test_obj['testEndTime'] is not None:
                extracted_timestamp, extracted_timezone = split_timestamp_timezone(self.test_obj['testEndTime'])
                final_object['test_end_date_time'] = get_time_in_utc(self.test_obj['testEndTime'])
                final_object['additional_info_2'] = extracted_timestamp
        elif 'endtime' in self.test_obj:
            if self.test_obj['endtime'] is not None:
                extracted_timestamp, extracted_timezone = split_timestamp_timezone(str(self.test_obj['endtime']))
                final_object['test_end_date_time'] = str(self.test_obj['endtime'])
                final_object['additional_info_2'] = extracted_timestamp
        elif 'testDate' in self.test_obj:
            if self.test_obj['testDate'] is not None:
                extracted_timestamp, extracted_timezone = split_timestamp_timezone(str(self.test_obj['testDate']))
                final_object['test_end_date_time'] = str(self.test_obj['testDate'])
                final_object['additional_info_2'] = extracted_timestamp
        elif 'mozarkEventAttributes_testEndDateTime' in kpi_object:
            extracted_timestamp, extracted_timezone = split_timestamp_timezone(kpi_object['mozarkEventAttributes_testEndDateTime'])
            if kpi_object['mozarkEventAttributes_testEndDateTime'] is not None:
                final_object['test_end_date_time'] = kpi_object['mozarkEventAttributes_testEndDateTime']
                final_object['additional_info_2'] = extracted_timestamp
        else:
            return final_object
        return final_object

    def get_test_case_start_time(self, kpi_object=None, final_object=None):
        if 'testStartTime' in self.test_obj:
            final_object['test_case_start_date_time'] = get_time_in_utc(self.test_obj['testStartTime'])
        elif 'starttime' in self.test_obj:
            final_object['test_case_start_date_time'] = str(self.test_obj['starttime'])
        elif 'testDate' in self.test_obj:
            final_object['test_case_start_date_time'] = str(self.test_obj['testDate'])
        elif 'mozarkEventAttributes_testStartDateTime' in kpi_object:
            final_object['test_case_start_date_time'] = kpi_object['mozarkEventAttributes_testStartDateTime']
        else:
            return final_object
        return final_object

    def get_test_case_end_time(self, kpi_object=None, final_object=None):
        if 'testEndTime' in self.test_obj:
            final_object['test_case_end_date_time'] = get_time_in_utc(self.test_obj['testEndTime'])
        elif 'endtime' in self.test_obj:
            final_object['test_case_end_date_time'] = str(self.test_obj['endtime'])
        elif 'testDate' in self.test_obj:
            final_object['test_case_end_date_time'] = str(self.test_obj['testDate'])
        elif 'mozarkEventAttributes_testEndDateTime' in kpi_object:
            final_object['test_case_end_date_time'] = kpi_object['mozarkEventAttributes_testEndDateTime']
        else:
            return final_object
        return final_object

    def get_test_status(self, kpi_object=None, final_object=None):
        if 'testStatus' in self.test_obj:
            final_object['test_status'] = self.test_obj['testStatus']
        elif 'status' in self.test_obj:
            final_object['test_status'] = self.test_obj['status']
        else:
            final_object['test_status'] = 'Completed'
        return final_object

    def get_project_name(self, kpi_object=None, final_object=None):
        if 'projectName' in self.test_obj:
            final_object['project_name'] = self.test_obj['projectName']
        elif 'mozarkEventAttributes_projectName' in kpi_object:
            final_object['project_name'] = kpi_object['mozarkEventAttributes_projectName']
        elif 'customerName' in self.test_obj:
            final_object['project_name'] = self.test_obj['customerName']
        else:
            final_object['project_name'] = 'default_project_name_1'
        return final_object

    def get_application_name(self, kpi_object=None, final_object=None):
        if 'applicationName' in self.test_obj:
            final_object['application_name'] = self.test_obj['applicationName']
        elif 'appname' in self.test_obj:
            final_object['application_name'] = self.test_obj['appname']
        else:
            final_object['application_name'] = 'default_application_name_1'
        return final_object

    def get_application_package_name(self, kpi_object=None, final_object=None):
        print(kpi_object)
        if 'package' in self.test_obj:
            final_object['application_package_name'] = self.test_obj['package']
        elif 'packageName' in self.test_obj:
            final_object['application_package_name'] = self.test_obj['packageName']
        elif 'mozarkEventAttributes_applicationId' in kpi_object:
            print('-----------------++++++++++++++++++++++++++++++++++++++++')
            final_object['application_package_name'] = kpi_object['mozarkEventAttributes_applicationId']
        else:
            final_object['application_package_name'] = 'default_application_package_name_1'
        return final_object

    def get_application_package_version_name(self, kpi_object=None, final_object=None):
        if 'appversion' in self.test_obj:
            final_object['application_package_version'] = self.test_obj['appversion']
        elif 'mozarkEventAttributes_applicationVersion' in kpi_object:
            final_object['application_package_version'] = kpi_object['mozarkEventAttributes_applicationVersion']
        else:
            final_object['application_package_version'] = 'default_application_package_version_1'
        return final_object

    def get_test_script_name(self, kpi_object=None, final_object=None):
        if 'scriptName' in self.test_obj:
            final_object['test_script_name'] = self.test_obj['scriptName']
        elif 'appname' in self.test_obj:
            final_object['test_script_name'] = self.test_obj['appname']
        else:
            final_object['test_script_name'] = 'default_test_script_name_1'
        return final_object

    def get_device_make(self, kpi_object=None, final_object=None):
        if 'deviceMake' in self.test_obj:
            final_object['device_make'] = self.test_obj['deviceMake']
        elif 'manufacturer' in self.test_obj:
            final_object['device_make'] = self.test_obj['manufacturer']
        else:
            final_object['device_make'] = 'default_device_make_1'
        return final_object

    def get_device_model(self, kpi_object=None, final_object=None):
        if 'devicename' in self.test_obj:
            final_object['device_model'] = self.test_obj['devicename']
        elif 'deviceName' in self.test_obj:
            final_object['device_model'] = self.test_obj['deviceName']
        elif 'model' in self.test_obj:
            final_object['device_model'] = self.test_obj['model']
        else:
            final_object['device_model'] = 'default_device_model_1'
        return final_object

    def get_device_platform(self, kpi_object=None, final_object=None):
        if 'devicePlatform' in self.test_obj:
            final_object['device_platform'] = self.test_obj['devicePlatform']
        elif 'platform' in self.test_obj:
            final_object['device_platform'] = self.test_obj['platform']
        else:
            final_object['device_platform'] = 'default_device_platform_1'
        return final_object

    def get_device_platform_version(self, kpi_object=None, final_object=None):
        if 'deviceOsVersion' in self.test_obj:
            final_object['device_platform_version'] = self.test_obj['deviceOsVersion']
        elif 'os' in self.test_obj:
            final_object['device_platform_version'] = self.test_obj['os']
        else:
            final_object['device_platform_version'] = 'default_device_platform_version_1'
        return final_object

    def get_device_city(self, kpi_object=None, final_object=None):
        if 'deviceLocation' in self.test_obj:
            final_object['device_city'] = self.test_obj['deviceLocation']
        elif 'city' in self.test_obj:
            final_object['device_city'] = self.test_obj['city']
        elif 'mozarkEventAttributes_deviceCity' in kpi_object:
            final_object['device_city'] = kpi_object['mozarkEventAttributes_deviceCity']
        else:
            final_object['device_city'] = 'default_device_city_1'
        return final_object

    def get_device_country(self, kpi_object=None, final_object=None):
        if 'deviceCountry' in self.test_obj:
            final_object['device_country'] = self.test_obj['deviceCountry']
        elif 'mozarkEventAttributes_country' in kpi_object:
            final_object['device_country'] = kpi_object['mozarkEventAttributes_country']
        else:
            final_object['device_country'] = 'default_device_country_1'
        return final_object

    def get_device_location(self, kpi_object=None, final_object=None):
        if 'mozarkEventAttributes_city' in kpi_object:
            final_object['device_location'] = kpi_object['mozarkEventAttributes_city']
        elif 'city' in self.test_obj:
            final_object['device_location'] = self.test_obj['city']
        else:
            final_object['device_location'] = 'default_device_location_1'
        return final_object

    def get_user_name(self, kpi_object=None, final_object=None):
        if 'userName' in self.test_obj:
            final_object['user_name'] = self.test_obj['userName']
        elif 'customerName' in self.test_obj:
            final_object['user_name'] = self.test_obj['customerName']
        else:
            final_object['user_name'] = 'default_user_name_1'
        return final_object

    def get_browser_name(self, kpi_object=None, final_object=None):
        if 'mozarkEventAttributes_browserName' in kpi_object:
            final_object['browser_name'] = kpi_object['mozarkEventAttributes_browserName']
        else:
            final_object['browser_name'] = 'default_browser_name_1'
        return final_object

    def get_browser_version(self, kpi_object=None, final_object=None):
        if 'mozarkEventAttributes_browserVersion' in kpi_object:
            final_object['browser_version'] = kpi_object['mozarkEventAttributes_browserVersion']
        else:
            final_object['browser_version'] = 'default_browser_version_1'
        return final_object

    def get_device_network_type(self, kpi_object=None, final_object=None):
        if 'deviceNetwork' in self.test_obj:
            final_object['device_network_type'] = self.test_obj['deviceNetwork']
        elif 'carrier' in self.test_obj:
            final_object['device_network_type'] = self.test_obj['carrier']
        elif 'mozarkEventAttributes_deviceNetworkType' in kpi_object:
            final_object['device_network_type'] = kpi_object['mozarkEventAttributes_deviceNetworkType']
        else:
            final_object['device_network_type'] = 'default_device_network_type_1'
        return final_object

    def get_device_mobile_operator(self, kpi_object=None, final_object=None):
        if 'operator' in self.test_obj and not self.test_obj['operator']:
            final_object['device_mobile_operator'] = self.test_obj['operator']
        elif 'deviceNetworkOperator' in kpi_object:
            final_object['device_mobile_operator'] = kpi_object['deviceNetworkOperator']
        elif 'operator' in kpi_object:
            final_object['device_mobile_operator'] = kpi_object['operator']
        elif 'mozarkEventAttributes_operator' in kpi_object:
            final_object['device_mobile_operator'] = kpi_object['mozarkEventAttributes_operator']
        else:
            final_object['device_mobile_operator'] = 'default_device_mobile_operator_1'
        return final_object

    def get_device_mobile_network_technology(self, kpi_object=None, final_object=None):
        if 'mozarkEventAttributes_deviceMobileNetworkTechnology' in kpi_object:
            final_object['device_mobile_network_technology'] = kpi_object[
                'mozarkEventAttributes_deviceMobileNetworkTechnology']
        else:
            final_object['device_mobile_network_technology'] = 'default_device_mobile_network_technology_1'
        return final_object

    def get_device_city_from_geo_code(self, kpi_object=None, final_object=None):
        if 'mozarkEventAttributes_deviceCityFromGeoCode' in kpi_object:
            final_object['device_city_from_geo_code'] = kpi_object['mozarkEventAttributes_deviceCityFromGeoCode']
        else:
            final_object['device_city_from_geo_code'] = 'default_device_city_from_geo_code_1'
        return final_object

    def get_device_city_from_isp(self, kpi_object=None, final_object=None):
        if 'mozarkEventAttributes_deviceCityFromIsp' in kpi_object:
            final_object['device_city_from_isp'] = kpi_object['mozarkEventAttributes_deviceCityFromIsp']
        else:
            final_object['device_city_from_isp'] = 'device_device_city_from_isp_1'
        return final_object

    def get_device_cellular_network_id(self, kpi_object=None, final_object=None):
        if 'mozarkEventAttributes_deviceCellularNetworkId' in kpi_object:
            final_object['device_cellular_network_id'] = kpi_object['mozarkEventAttributes_deviceCellularNetworkId']
        else:
            final_object['device_cellular_network_id'] = 'default_device_cellular_network_id_1'
        return final_object

    def get_device_serial(self, kpi_object=None, final_object=None):
        if 'mozarkEventAttributes_deviceId' in kpi_object:
            final_object['device_serial'] = kpi_object['mozarkEventAttributes_deviceId']
        elif 'mozarkEventAttributes_serialId' in kpi_object:
            final_object['device_serial'] = kpi_object['mozarkEventAttributes_serialId']
        elif 'deviceSerial' in self.test_obj:
            final_object['device_serial'] = self.test_obj['deviceSerial']
        else:
            final_object['device_serial'] = 'default_device_serial_1'
        return final_object

    def get_basic_kpi_data(self, kpi_object=None, final_object=None):
        if 'eventAttributes_testCaseName' in kpi_object:
            final_object['test_case_name'] = kpi_object['eventAttributes_testCaseName']
        else:
            final_object['test_case_name'] = ''
        final_object['kpi_name'] = kpi_object['name']
        final_object['kpi_value'] = kpi_object['value']
        final_object['kpi_status'] = kpi_object['status']
        return final_object
