
HOST = 'https://abulaysov.ru'

NAME_DAYS = {'Понедельник': 'monday',
             'Вторник': 'tuesday',
             'Среда': 'wednesday',
             'Четверг': 'thursday',
             'Пятница': 'friday',
             'Суббота': 'saturday'}


def get_schedules(data: dict) -> tuple:
    first = [data['first_subject'][0],
             data['first_type_pair'][0],
             data['first_teacher'][0],
             data['first_aud'][0]]
    second = [data['second_subject'][0],
              data['second_type_pair'][0],
              data['second_teacher'][0],
              data['second_aud'][0]]
    third = [data['third_subject'][0],
             data['third_type_pair'][0],
             data['third_teacher'][0],
             data['third_aud'][0]]
    fourth = [data['fourth_subject'][0],
              data['fourth_type_pair'][0],
              data['fourth_teacher'][0],
              data['fourth_aud'][0]]

    return first, second, third, fourth


def schedules(data: dict) -> str:
    result = ''
    for i, value in enumerate(get_schedules(data), 1):
        if value[0].strip() == '':
            result += f'{i}) {"-" * 10}'
        else:
            result += f'{i}) {" ".join(value)}'
        result += '\n\n'
    return result


def get_url_for_update(pk):
    return f'{HOST}/api/v1/update-schedules/va312/ase4/{pk}/'

