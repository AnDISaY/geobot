from excel import initialize_sheet, add_attendance
from database_connect import get_managers, get_employees, get_employee, get_manager_by_employee
import datetime


def start_of_the_day():
    managers = get_managers()
    managers_id = []
    for m in managers:
        managers_id.append(m[0])
    for m in managers_id:
        employees = get_employees(m)
        employees_fullname = []
        for e in employees:
            employees_fullname.append(f'{e[1]} {e[2]}')
        initialize_sheet(m, employees_fullname)


def check_attendance(time, location, tg_id):
    latitude = location['latitude']
    longitude = location['longitude']
    location_link = f'https://www.google.com/maps/search/?api=1&query={latitude},{longitude}'
    # data = {2: 'Присутствие', 3: 'Опоздания', 4: 'Пропуски', 6: location_link}
    if time is not None:
        if time < datetime.time(8):
            data = {2: '✓', 3: '—', 6:location_link}
        elif time > datetime.time(8) and time < datetime.time(16, 30):
            hour = time.hour
            minute = time.minute
            if len(str(time.hour)) == 1:
                hour = f'0{time.hour}'
            if len(str(time.minute)) == 1:
                minute = f'0{time.minute}'
            now = f'{hour}:{minute}'
            data = {2: '✓', 3: now, 6:location_link}
        else:
            data = {2: '—', 6:location_link}
    else:
        data = {2: '—', 6:location_link}
    name = get_employee(tg_id)[0].strip('(').strip(')').split(',')
    name = f'{name[0]} {name[1]}'
    add_attendance(get_manager_by_employee(tg_id)[0], data, name)


# def start_of_the_day():
    # managers = get_managers()
    # for m in managers:
    #     send_sheet(m[0], f'sheets/Отчет -- {m[0]}.xlsx')


def insert_time():
    pass


check_attendance(datetime.time(11, 00), {'latitude': 38.272112, 'longitude': -95.980005}, 1260539121)
# start_of_the_day()