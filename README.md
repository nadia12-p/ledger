# ledger
Simple implementation of the ledger-cli

Prerequisites:  
Python 3.8.9 

Libraries needed to install that aren’t originally from python: 
  texttable 
  termcolor 
  
Expected files: 
  Journal entries.
  Price history.

Execution of the program: 
To run my ledger implementation, you should type in the command line interface: python3 main.py (flags or commands you wish to implement). Take into account that the flag –f or --file is always needed, so my ledger will know from where it’ll read the values. At least you should have a line like this: python3 main.py --file index.ledger. The file flag is a required flag, my ledger won’t work if you don’t assign this flag.  

However, this last line won’t show you anything, it’s only part of the logic for my ledger to work.  

Important: The –file or –f flag is expecting a path towards your file. If your file is an index that calls another file. Be sure that you’re including the path towards the file from where you saved my ledger implementation. To avoid confusion, I suggest working with all the files at the same level, so you’ll only need to input the name of the file because this will be the same as the relative path. 
 
 
To actually get outputs you need to add commands. The flags should always be written before a command, and only one command can be used at a time.  


Flags 

--help, or –h 
    This flag shows you a help message. 

--file, or –f {PATH} 
    This flag lets you load a journal entry. 

--sort {d,a} 
    This flag lets you sort the data. Only relevant to print and register commands because the balance doesn’t output dates. For now, it only sorts by date {d}, sorting by amount {a} is still in progress. 

--prices-db {FILE} 
    This flag will load your price history file that should have the conversion rates. It will do the conversion to the currency specified in the price history file. For example: 
 
 
 
Commands 

Print. 
This command will give you a formatted version of your journal entries, excluding any comments. This command supports the –sort flag. For example, the Expenses entries will look like this: 
 
Register. 
This command will show all transactions and a running total. The formatted version is still in process. 
This command supports the –sort and –price-db flags: 
 
Balance. 
This command lets you find the balances of all of your accounts. It will give you the total amount of every sub account and the sum of the parent account of every sub account. The formatted version is still in progress. It adds to the parents’ value and shows you the total balance.  
This command also supports the price-db flag: 
 
