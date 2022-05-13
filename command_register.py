from copy import deepcopy

import texttable
from termcolor import colored
from read_files import convert_timestamp_to_string

register_first_line = texttable.Texttable()


def color_blue(text, attribute=None):
    if attribute is None:
        return colored(text, 'blue')
    return colored(text, 'blue', attrs=attribute)


def text_bold(text):
    return colored(text, attrs=['bold'])


def color_red(text, attribute=None):
    if attribute is None:
        return colored(text, 'red')
    return colored(text, 'red', attrs=attribute)


def print_register(first_line, second_line):
    register_first_line.reset()
    register_first_line.set_cols_align(["l", "l", "r", "r"])
    register_first_line.set_deco(0)
    register_first_line.set_cols_width([60, 60, 20, 20])

    register_first_line.add_row(first_line)
    register_first_line.add_row(second_line)
    print(register_first_line.draw())


class MoneyValue():
    def __init__(self, quantity=None, currency=None):
        self.amount = 0 if quantity is None else quantity
        self.currency = "$" if currency is None else currency

    def __add__(self, other):
        self.amount += other.amount

    def __str__(self):
        amount = self.amount
        format_amount = "{:.2f}".format(amount)
        if self.currency == "$":
            raw_string = self.currency + format_amount
        else:
            raw_string = format_amount + " " + self.currency
        if self.amount < 0:
            raw_string = color_red(raw_string)
        return raw_string


class Transaction:

    def __init__(self, entry):
        self.date = convert_timestamp_to_string(entry[0], "%y-%b-%d")
        self.concept = entry[1]
        self.account1 = entry[2]
        self.amount1 = entry[3]
        self.currency1 = entry[4]
        self.account2 = entry[5]
        self.amount2 = entry[6]
        self.currency2 = entry[7]

        if self.amount2 is None:
            self.amount2 = -1 * self.amount1

    def get_accounts(self):
        return color_blue(self.account1, ['bold']), color_blue(self.account2, ['bold'])

    def convert_currency(self, money: MoneyValue, prices: dict):
        currency_price = prices.get(money.currency, None)
        if money.currency != "$" and currency_price is not None:
            money.currency = "$"
            money.amount = money.amount * currency_price
        return money

    def get_moneys(self, prices_history: dict = None):
        money1 = MoneyValue(self.amount1, self.currency1)
        money2 = MoneyValue(self.amount2, self.currency2)
        if prices_history is not None:
            money1 = self.convert_currency(money1, prices_history)
            money2 = self.convert_currency(money2, prices_history)
        return money1, money2


class Register:
    before_transaction = [MoneyValue()]
    after_transaction = [MoneyValue()]

    def format_money_values(self, moneys: [MoneyValue]):
        formatted_money = ""
        for money in moneys:
            formatted_money += str(money) + "\n"

        return formatted_money.rstrip()

    def formatted_date_concept(self, date, concept):
        return date + " " + text_bold(concept)

    def print_register(self, entry, prices_history=None):
        incoming_register = Transaction(entry)
        date = incoming_register.date
        concept = incoming_register.concept
        account1, account2 = incoming_register.get_accounts()
        incoming_money1, incoming_money2 = incoming_register.get_moneys(prices_history)
        self.before_transaction = self.sum_money(incoming_money1, self.after_transaction)
        self.after_transaction = self.sum_money(incoming_money2, self.before_transaction)
        formatted_date_concept = self.formatted_date_concept(date, concept)
        first_line = [formatted_date_concept, account1, str(incoming_money1),
                      self.format_money_values(self.before_transaction)]
        second_line = ["", account2, str(incoming_money2),
                       self.format_money_values(self.after_transaction)]
        print_register(first_line, second_line)

    def sum_money(self, money: MoneyValue, set_of_money: [MoneyValue]):
        working = deepcopy(set_of_money)
        existing_money = list(filter(lambda m: m.currency == money.currency, working))
        if len(existing_money) > 0:
            existing_money = existing_money[0]
            existing_money += money
        else:
            working.append(money)
        return working