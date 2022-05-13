import string
from collections import deque
from copy import deepcopy

import texttable
from termcolor import colored

from command_register import MoneyValue
from read_files import get_accounts_and_amounts

table = texttable.Texttable()

test_table = ['Account', '100', '$']


def convert_currency(money: MoneyValue, prices: dict):
    currency_price = prices.get(money.currency, None)
    if money.currency != "$" and currency_price is not None:
        money.currency = "$"
        money.amount = money.amount * currency_price
    return money


class BalanceAccount:
    def __init__(self, raw_data,prices_history=None):
        self.account1 = raw_data[0]
        amount1 = raw_data[1]
        currency1 = raw_data[2]
        self.account2 = raw_data[3]
        amount2 = raw_data[4]
        currency2 = raw_data[5]
        if amount2 is None:
            amount2 = -1 * amount1
        self.money1 = MoneyValue(amount1, currency1)
        self.money2 = MoneyValue(amount2, currency2)
        if prices_history is not None:
            self.money1 = convert_currency(self.money1, prices_history)
            self.money2 = convert_currency(self.money2, prices_history)


def get_accounts_and_amounts_for_balance(prices_history=None):
    raw_data = get_accounts_and_amounts()
    accounts = AccountTree()
    for entry in raw_data:
        balance_account = BalanceAccount(entry,prices_history)
        names = balance_account.account1.split(":")
        queue_name = deque()
        for name in names:
            queue_name.append(name)
        accounts.addAccount(queue_name, balance_account.money1)
        names = balance_account.account2.split(":")
        queue_name = deque()
        [queue_name.append(name) for name in names]
        accounts.addAccount(queue_name, balance_account.money2)
    accounts.calculate_final_value()

    formatter = AccountFormater(accounts)
    formatter.format_tree()
    formatter.print()


class AccountTree:
    def sum_money(self, money: MoneyValue):
        working = deepcopy(self.value)
        existingMoney = list(filter(lambda m: m.currency == money.currency, working))
        if len(existingMoney) > 0:
            existingMoney = existingMoney[0]
            existingMoney += money
        else:
            working.append(money)
        return working

    def __init__(self):
        self.accounts_roots = []
        self.value = [MoneyValue()]

    def addAccount(self, account_queue: deque, account_money: MoneyValue):
        account_name = account_queue.popleft()
        found_account = list(filter(lambda account: account.name == account_name, self.accounts_roots))
        if len(found_account) == 0:
            if len(account_queue) == 0:
                new_account = AccountNode(account_name, account_money)
            else:
                new_account = AccountNode(account_name)
                new_account.addNewChild(account_queue, account_money)
            self.accounts_roots.append(new_account)
        else:
            account = found_account[0]
            account.updateValue(account_queue, account_money)

    def calculate_final_value(self):
        for account in self.accounts_roots:
            account.calculate_total_value(0)
            for account_value in account.value:
                self.value = self.sum_money(account_value)


class AccountNode:

    def sum_money(self, money: MoneyValue):
        working = deepcopy(self.value)
        existingMoney = list(filter(lambda m: m.currency == money.currency, working))
        if len(existingMoney) > 0:
            existingMoney = existingMoney[0]
            existingMoney += money
        else:
            working.append(money)
        return working

    def __init__(self, account: string, money: MoneyValue = None):
        self.name = account
        money = MoneyValue() if money is None else money
        self.value = [money]
        self.innerAccounts = []
        self.level = 0

    def addNewChild(self, account_queue: deque, childMoney: MoneyValue):
        account_name = account_queue.popleft()
        if len(account_queue) > 0:
            new_account = AccountNode(account_name)
            new_account.addNewChild(account_queue, childMoney)
        else:
            new_account = AccountNode(account_name, childMoney)
        self.innerAccounts.append(new_account)

    def getChildByName(self, account_name):
        account = list(filter(lambda account: account.name == account_name, self.innerAccounts))
        if len(account) == 0:
            return None
        return account[0]

    def updateValue(self, account_queue: deque, money: MoneyValue):
        remainin_names = len(account_queue)
        if remainin_names == 0:
            self.value = self.sum_money(money)
        else:
            account_name = account_queue.popleft()
            account = self.getChildByName(account_name)
            if account == None:
                account_queue.appendleft(account_name)
                self.addNewChild(account_queue, money)
            else:
                account.updateValue(account_queue, money)

    def calculate_total_value(self, level):
        self.level += level
        for child_account in self.innerAccounts:
            child_account.calculate_total_value(self.level + 1)
            for currency_value in child_account.value:
                self.value = self.sum_money(currency_value)


def color_blue(text, attribute=None):
    if attribute is None:
        return colored(text, 'blue')
    return colored(text, 'blue', attrs=attribute)


def color_red(text, attribute=None):
    if attribute is None:
        return colored(text, 'red')
    return colored(text, 'red', attrs=attribute)


def print_balance(test_table):
    table.reset()
    table.set_cols_align(["r", "l"])
    table.set_deco(0)
    table.set_cols_width([20, 50])
    table.add_row([test_table[0], color_blue(test_table[1], attribute=['bold'])])
    print(table.draw())


class AccountFormater:

    def __init__(self, accounts_tree: AccountTree):
        self.accounts = accounts_tree
        self.content = []

    def format_value(self, values: [MoneyValue]):
        str_value = ""
        for value in values:
            str_value += str(value) + "\n"
        return str_value.rstrip()

    def format_tree(self):
        for account in self.accounts.accounts_roots:
            self.recursive_format(account)

    def recursive_format(self, account_node: AccountNode):
        value = self.format_value(account_node.value)
        account = account_node.name
        self.content.append([value, account])
        for inner_account in account_node.innerAccounts:
            self.recursive_format(inner_account)

    def print(self):
        for content in self.content:
            print_balance(content)
        print("------------------------------")
        table.reset()
        final_row = [self.format_value(self.accounts.value),""]
        print_balance(final_row)