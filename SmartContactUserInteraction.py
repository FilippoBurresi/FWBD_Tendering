from tkinter import *
from tkinter import ttk
import pandas as pd
from tkinter import filedialog
from web3 import Web3
import json
import string
import random
from utils import *

# COMUNICATE TO ETHEREUM

# ganache_URL="HTTP://127.0.0.1:7545"
# web3=Web3(Web3.HTTPProvider(ganache_URL))
# web3.eth.defaultAccount=web3.eth.accounts[0]
# abi=json.loads(abi) # we can change the name of the variable
# address=web3.toChecksumAddress("0x46D841b6900e2BF0925C248B7942D8B09a354E37")
# contract=web3.eth.contract(address=address,abi=abi)

# USER INTERFACE

# creating the main window
window = Tk()
window.title("Smart Contract Tendering")
window.geometry('500x750')

#creating tabS
tab_parent = ttk.Notebook(window)

tab_pa = ttk.Frame(tab_parent)
tab_contractor = ttk.Frame(tab_parent)
tab_citizen = ttk.Frame(tab_parent)

tab_parent.add(tab_pa, text="Public Administration")
tab_parent.add(tab_contractor, text="Contractor")
tab_parent.add(tab_citizen, text="Citizen")
tab_parent.pack(expand=1, fill='both')

# make each tab scrollable (PA)
main_frame_PA = Frame(tab_pa)
main_frame_PA.pack(fill=BOTH, expand = 1)

my_canvas_PA = Canvas(main_frame_PA)
my_canvas_PA.pack(side=LEFT, fill=BOTH, expand=1)

my_scrollbar_PA = ttk.Scrollbar(main_frame_PA, orient=VERTICAL, command=my_canvas_PA.yview)
my_scrollbar_PA.pack(side=RIGHT, fill=Y)

my_canvas_PA.configure(yscrollcommand=my_scrollbar_PA.set)
my_canvas_PA.bind('<Configure>', lambda e: my_canvas_PA.configure(scrollregion = my_canvas_PA.bbox("all")))

second_frame_PA = Frame(my_canvas_PA)

my_canvas_PA.create_window((0,0),window=second_frame_PA, anchor ="nw")

# (CONTRACTOR)

main_frame_contractor = Frame(tab_contractor)
main_frame_contractor.pack(fill=BOTH, expand = 1)

my_canvas_contractor = Canvas(main_frame_contractor)
my_canvas_contractor.pack(side=LEFT, fill=BOTH, expand=1)

my_scrollbar_contractor = ttk.Scrollbar(main_frame_contractor, orient=VERTICAL, command=my_canvas_contractor.yview)
my_scrollbar_contractor.pack(side=RIGHT, fill=Y)

my_canvas_contractor.configure(yscrollcommand=my_scrollbar_contractor.set)
my_canvas_contractor.bind('<Configure>', lambda e: my_canvas_contractor.configure(scrollregion = my_canvas_contractor.bbox("all")))

second_frame_contractor = Frame(my_canvas_contractor)

my_canvas_contractor.create_window((0,0),window=second_frame_contractor, anchor ="nw")

# (CITIZEN)

main_frame_citizen = Frame(tab_citizen)
main_frame_citizen.pack(fill=BOTH, expand = 1)

my_canvas_citizen = Canvas(main_frame_citizen)
my_canvas_citizen.pack(side=LEFT, fill=BOTH, expand=1)

my_scrollbar_citizen = ttk.Scrollbar(main_frame_citizen, orient=VERTICAL, command=my_canvas_citizen.yview)
my_scrollbar_citizen.pack(side=RIGHT, fill=Y)

my_canvas_citizen.configure(yscrollcommand=my_scrollbar_citizen.set)
my_canvas_citizen.bind('<Configure>', lambda e: my_canvas_citizen.configure(scrollregion = my_canvas_citizen.bbox("all")))

second_frame_citizen = Frame(my_canvas_citizen)

my_canvas_citizen.create_window((0,0),window=second_frame_citizen, anchor ="nw")

env1 = makeform(second_frame_contractor, ('Primo','Secondo','Terzo'))

# creating link the function to the user interface





window.mainloop()