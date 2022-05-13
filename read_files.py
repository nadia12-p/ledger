import re
import sqlite3 as sql
import string
import time
from datetime import datetime

time_read_format = "%Y/%m/%d"


def convert_timestamp_to_string(processed_time, date_format=None):
    read_time = datetime.fromtimestamp(processed_time)
    if date_format is None:
        return read_time.strftime(time_read_format)
    else:
        return read_time.strftime(date_format)


def convert_to_time_stamp(original_time: string):
    element = datetime.strptime(original_time, time_read_format)
    element_tuple = element.timetuple()
    timestamp = time.mktime(element_tuple)
    return timestamp


connection = sql.connect(":memory:")

with connection:
    connection.execute("""
    CREATE TABLE transactions(
        date TIMESTAMP,
        concept TEXT,
        account1 TEXT,
        amount1 REAL,
        currency1 TEXT,
        account2 TEXT,
        amount2 REAL,
        currency2 TEXT
        );
    """)


def save_transaction(date, concept, account1, amount1, currency1, account2, amount2, currency2):
    query = """INSERT INTO transactions 
    (date,concept,account1,amount1,currency1,account2,amount2,currency2) 
    values(?,?,?,?,?,?,?,?)"""
    with connection:
        connection.execute(query, (date, concept, account1, amount1, currency1, account2, amount2, currency2))


def get_all_transactions():
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM transactions''')
    result = cursor.fetchall()
    return result


def get_all_transactions_sorted_by_date():
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM transactions ORDER BY date ASC''')
    result = cursor.fetchall()
    return result


def get_accounts_and_amounts():
    cursor = connection.cursor()
    cursor.execute('''SELECT account1,amount1,currency1,account2,amount2,currency2 FROM transactions''')
    result = cursor.fetchall()
    return result


def get_date_concept(first_line):
    values_divided = first_line.split(" ", 1)
    date = convert_to_time_stamp(values_divided[0])
    concept = values_divided[1].replace("\n", "")
    return date, concept


def get_account_amount(second_line):
    values_divided = second_line.split("\t")
    account_amount = []
    for value in values_divided:
        if value == "":
            continue
        account_amount.append(value.rstrip())
    return account_amount


def get_currency_amount(raw_amount):
    sign = 1
    currency = ""
    amount = 0
    if "-" in raw_amount:
        sign = -1
        raw_amount = raw_amount.replace("-", "")
    values_divided = re.split("([0-9.]+)", raw_amount)
    values_divided = list(filter(lambda x: x != '', values_divided))
    if "$" in values_divided:
        amount = float(values_divided[1]) * sign
        currency = values_divided[0].strip()
    else:
        amount = float(values_divided[0]) * sign
        currency = values_divided[1].strip()
    return amount, currency


def write_raw_info(raw_info):
    [date, concept] = get_date_concept(raw_info[0])
    [account1, raw_amount1] = get_account_amount(raw_info[1])
    [amount1, currency1] = get_currency_amount(raw_amount1)
    account_amount2 = get_account_amount(raw_info[2])
    account2 = account_amount2[0]
    if len(account_amount2) == 1:
        amount2 = None
        currency2 = currency1
    else:
        [amount2, currency2] = get_currency_amount(account_amount2[1])
    save_transaction(date, concept, account1, amount1, currency1, account2, amount2, currency2)


def load_files(path):
    parent_lines = []
    try:
        with open(path, 'r') as file:
            i = 0
            raw_info = []
            for line in file:
                if "!include " in line:
                    line = line.replace('!include ', '')
                    line = line.replace('\n', '')
                    parent_lines.append(line)
                    continue
                if ";" in line:
                    continue
                raw_info.append(line)
                i += 1
                if i == 3:
                    write_raw_info(raw_info)
                    i = 0
                    raw_info = []
            file.close()
    except:
        print("This file: {}, doesn't exist.".format(path))
    for p in parent_lines:
        load_files(p)


def read(paths):
    for f in paths:
        load_files(f)
