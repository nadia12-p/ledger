import string
import time
from datetime import datetime

from read_files import connection

time_read_format = "%Y/%m/%d"


def convert_timestamp_to_string(processed_time):
    read_time = datetime.fromtimestamp(processed_time)
    return read_time.strftime(time_read_format)


def convert_to_time_stamp(original_time: string):
    element = datetime.strptime(original_time, time_read_format)
    element_tuple = element.timetuple()
    timestamp = time.mktime(element_tuple)
    return timestamp


with connection:
    connection.execute("""
    CREATE TABLE prices_history(
        date TIMESTAMP,
        time TEXT,
        currency TEXT,
        conversion_rate REAL
        );
    """)


def save_prices_history(date, conversion_time, currency, conversion_rate):
    query = """INSERT INTO prices_history 
    (date,time,currency,conversion_rate) 
    values(?,?,?,?)"""
    with connection:
        connection.execute(query, (date, conversion_time, currency, conversion_rate))


def get_all_conversion_rates():
    cursor = connection.cursor()
    cursor.execute('''SELECT currency,conversion_rate FROM prices_history''')
    result = cursor.fetchall()
    currencies = {}
    for conversion_rate in result:
        currency, value = conversion_rate
        currencies[currency] = currencies.get(currency, value)

    return currencies


def write_raw_info(raw_info):
    for row in raw_info:
        row = row.replace("\n", "")
        row = row.replace("$", "")
        values_divided = row.split(" ")
        pricedb_date = convert_to_time_stamp(values_divided[1])
        pricedb_time = values_divided[2]
        pricedb_currency = values_divided[3]
        pricedb_amount = float(values_divided[4])
        save_prices_history(pricedb_date, pricedb_time, pricedb_currency, pricedb_amount)


def load_prices(price_db):
    try:
        with open(price_db, 'r') as file:
            i = 0
            raw_info = []
            for line in file:
                if "P" in line:
                    raw_info.append(line)
            write_raw_info(raw_info)
            file.close()
    except:
        print("This file: {}, doesn't exist.".format(price_db))


def read_price_history(price_db):
    load_prices(price_db)