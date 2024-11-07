import logging, random
import jwt
from datetime import datetime, timedelta
from flask_sqlalchemy import inspect
from flask import jsonify
from itertools import groupby
from operator import itemgetter


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


def dict_as_json(dictionary):
    return jsonify(dictionary)


def object_as_json(row):
    return dict_as_json(object_as_dict(row))


def str_to_bool(s):
    if s == 'True':
        return True
    elif s == 'False':
        return False
    else:
        raise ValueError


def jwt_decode(dictionary, key):
    return jwt.decode(dictionary, key)


def group_by_keys(iterable, keys):
    key_func = itemgetter(*keys)
    # For groupby() to do what we want, the iterable needs to be sorted
    # by the same key function that we're grouping by.
    sorted_iterable = sorted(iterable, key=key_func)
    return [list(group) for key, group in groupby(sorted_iterable, key_func)]


def replace_string(string_replace, before=None):
    repl = {
        '%': '~',
        ':': '',
        ' ': '_',
        '(': '',
        ')': '',
        '_~_': '_',
        '~': '',
        '.': '',
        '/': '',
        '__': '_',
    }
    if not string_replace:
        return string_replace
    before = before or str.lower
    t = before(string_replace)
    for key, value in repl.items():
        t = t.replace(key, value)
        for value2 in string_replace:
            if value2 == key:
                replace_string(t)
    return t


def add_business_days(from_date, ndays):
    if ndays < 1:
        ndays = 1
    business_days_to_add = abs(ndays)
    # print(type(from_date))
    current_date = datetime.strptime(from_date, '%Y-%m-%d')
    # print(type(current_date))
    sign = ndays / abs(ndays)
    while business_days_to_add > 0:
        current_date += timedelta(sign * 1)
        weekday = current_date.weekday()
        if weekday >= 5:  # sunday = 6
            continue
        business_days_to_add -= 1
    current_date = current_date.strftime('%Y-%m-%d')
    return current_date


def ordereddict_to_dict(value):
    for k, v in value.items():
        if isinstance(v, dict):
            value[k] = ordereddict_to_dict(v)
    return dict(value)


def generate_initials(value):
    try:
        arra = value.split(' ')
        if arra[0]:
            first = arra[0]
            letter_one = first[:1]
        else:
            letter_one = ''

        if len(arra) > 1 and arra[1]:
            second = arra[1]
            letter_two = second[:1].upper()
        else:
            letter_two = ''

        return f'{letter_one} {letter_two}'
    except Exception as e:
        return 'NN'
    


def generate_hex():
    random_number = random.randint(0, 16777215)
    hex_number = format(random_number, 'x')
    if hex_number in ['fff','ffff','fffff','ffffff']:
        generate_hex()
    return '#' + hex_number


def date_tranform(date):
    return str(date['year']) + '-' + str(date['month']) + '-' + str(date['day'])


def remove_dupes(l):
    b = []
    try:
        for i, val in l.items():
            # print(i)
            for e in range(0, len(val)):
                if val[e] not in val[e + 1 :]:
                    b.append({i: [val[e]]})

    except Exception as e:
        print(e, 'El')
    return b
