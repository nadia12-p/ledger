import flags_commands
import read_files
import command_print
import flag_pricesdb
from command_balance import get_accounts_and_amounts_for_balance
from command_register import Register

args = flags_commands.args
read_files.read(args.path)
data = read_files.get_all_transactions()
prices = None

if args.price_db is not None:
    flag_pricesdb.read_price_history(args.price_db)
    prices = flag_pricesdb.get_all_conversion_rates()

if args.sortingType == "d":
    data = read_files.get_all_transactions_sorted_by_date()

if args.command == "print":
    for entry in data:
        command_print.print_entry(entry)

if args.command == "reg":
    register = Register()
    for entry in data:
        register.print_register(entry, prices)

if args.command == "bal":
    get_accounts_and_amounts_for_balance(prices)