import datetime
from time import strftime, strptime
from insert_kpis import InsertKpis

from get_test_details import GetTestDetails
from migrate_kpis import MigrateKpis

print('starting')
my_start_time = '2023-01-17'
my_end_time = '2023-01-25'
migrate_kpis_object = MigrateKpis()
print(migrate_kpis_object.config)

if ' ' not in my_start_time and ' ' not in my_end_time:
    start_date = datetime.datetime.strptime(my_start_time, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(my_end_time, '%Y-%m-%d')
    day_count = (end_date - start_date).days + 1
    print(day_count)
    while day_count > 0:
        end_date = start_date + datetime.timedelta(days=1)
        print(str(start_date) + " - " + str(end_date))
        migrate_kpis_object.migrate_kpis(start_time=str(start_date), end_time=str(end_date))

        start_date = start_date + datetime.timedelta(days=1)
        day_count -= 1

print('done')

