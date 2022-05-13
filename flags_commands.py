import argparse

parser = argparse.ArgumentParser(description="This is a simple implementation of the ledger-cli")

parser.add_argument('-f', '--file',
                    action='append',
                    dest="path",
                    help='read journal data from FILE.',
                    required=True)

subparsers = parser.add_subparsers(title="COMMANDS", dest="command", description="The following commands are accepted:")
print_subparser = subparsers.add_parser("print", help="prints the transactions.")
balance_subparser = subparsers.add_parser("bal", help="gives you a balance of the data called.")
register_subparser = subparsers.add_parser("reg", help="makes a register of the data called.")
parser.add_argument("--sort", dest="sortingType", help="lets you sort data by date (use 'd' argument)")
parser.add_argument("--price-db", help="loads price history file, with this you'll be able to do conversion rates.")

args = parser.parse_args()