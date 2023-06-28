import datetime

from migrate_kpis import MigrateKpis

file_name = "las_pulled_time.txt"


def set_last_pulled_time(str_time):
    f = open(file_name, "w")
    f.write(str_time)
    f.close()


def get_last_pulled_time():
    try:
        f = open(file_name, "r")
        time_str = f.read()
        # print(time_str)
        return time_str
    except Exception as e:
        return None


print('starting')
my_start_time = '2023-01-01'
my_end_time = '2023-01-03'
migrate_kpis_object = MigrateKpis()
print(migrate_kpis_object.config)
time_str = get_last_pulled_time()
print(time_str)
if time_str is None:
    print('create time here')
    my_end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    my_start_time = datetime.datetime.now().strftime("%Y-%m-%d 00:00:00")
    print(my_start_time + " - " + my_end_time)
    set_last_pulled_time(my_end_time)
    migrate_kpis_object.migrate_kpis(start_time=my_start_time, end_time=my_end_time)
else:
    # print(time_str)
    my_start_time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    my_end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    my_start_time = time_str
    print(my_start_time + " - " + my_end_time)
    set_last_pulled_time(my_end_time)
    migrate_kpis_object.migrate_kpis(start_time=my_start_time, end_time=my_end_time)
print('done')
