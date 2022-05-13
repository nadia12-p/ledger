import texttable
from read_files import convert_timestamp_to_string

table = texttable.Texttable()


class printable_transaction:
    def __init__(self, date, concept, account1, amount1, currency1, account2, amount2, currency2):
        self.date = convert_timestamp_to_string(date)
        self.concept = concept
        self.account1 = account1
        self.account2 = account2

        self.money1 = self.read_money(amount1, currency1)
        if amount2 is None:
            self.money2 = ""
        else:
            self.money2 = self.read_money(amount2, currency2)

    @staticmethod
    def read_money(amount, currency):
        if currency == "$":
            return currency + str(amount)
        else:
            return str(amount) + " " + currency


def print_transaction(transaction: printable_transaction):
    table.reset()
    table.set_cols_align(["l", "r"])
    table.set_deco(0)
    table.set_cols_width([50, 10])
    print(transaction.date + " " + transaction.concept)
    table.add_row(["\t" + transaction.account1, transaction.money1])
    table.add_row(["\t" + transaction.account2, transaction.money2])
    print(table.draw())
    print()


def print_entry(entry):
    date = entry[0]
    concept = entry[1]
    account1 = entry[2]
    amount1 = entry[3]
    currency1 = entry[4]
    account2 = entry[5]
    amount2 = entry[6]
    currency2 = entry[7]
    printable = printable_transaction(date, concept, account1, amount1, currency1, account2, amount2, currency2)
    print_transaction(printable)
