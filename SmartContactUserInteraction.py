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

ganache_URL="HTTP://127.0.0.1:7545"
web3=Web3(Web3.HTTPProvider(ganache_URL))
web3.eth.defaultAccount=web3.eth.accounts[0]
abi=json.loads(abi) # we can change the name of the variable
address=web3.toChecksumAddress("0x2b9bD2953d70743A6F3b8e3f3Ecaa28eacAc50E5")
contract=web3.eth.contract(address=address,abi=abi)

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

# creating link the function to the user interface
#CreateTender
title = "CreateTender"
create_tender_fields = ('tender_name','description','n_days','n_days_2','weight_1_price', 'weight_2_time', 'weight_3_envir')
elem_1= makeform(second_frame_PA, create_tender_fields, title=title, description=function_info[title])
btn_1 = elem_1["btn"]
btn_1['command'] = lambda arg1=web3, arg2=contract, arg3=elem_1: create_tender(arg1,arg2,arg3)

#placeBid
title = 'placeBid'
place_bid_fields = ('user_id','tender_id','price','time','envir')
elem_2 = makeform(second_frame_contractor, place_bid_fields,title=title, description=function_info[title])
btn_2 = elem_2['btn']
btn_2['command'] = lambda arg1=web3, arg2=contract, arg3=elem_2: send_bid(arg1,arg2,arg3)

#concludeBid
title = 'concludeBid'
conclude_bid_fields = ('user_id',)
elem_3 = makeform(second_frame_contractor, conclude_bid_fields, title=title, description=function_info[title],file= True)
btn_3 = elem_3['btn']
btn_3['command'] = lambda arg1=web3, arg2= contract, arg3 = elem_3: send_unencrypted(arg1, arg2, arg3)

#getTenderStatus
title = 'getTenderStatus'
elem_4 = makeform(second_frame_citizen, (),title=title,description=function_info[title],view=True)
btn_4 = elem_4['btn']
btn_4['command'] = lambda arg1=web3, arg2=contract, arg3=elem_4: get_tenders_status(arg1, arg2, arg3)

#see_active_tenders
title = "seeActiveTenders"
see_active_tenders_fields = ()
elem_5 = makeform(second_frame_citizen,see_active_tenders_fields,title=title, description=function_info[title], view=True)
btn_5 = elem_5['btn']
btn_5['command'] = lambda arg1=web3, arg2=contract, arg3=elem_5:see_active_tenders(arg1,arg2,arg3)

#see_closed_tenders
title = 'seeClosedTenders'
see_closed_tenders_fields = ()
elem_6 = makeform(second_frame_citizen,see_closed_tenders_fields, title = title, description=function_info[title], view = True)
btn_6 = elem_6['btn']
btn_6['command'] = lambda arg1=web3, arg2=contract, arg3=elem_6:see_closed_tenders(arg1,arg2,arg3)


window.mainloop()
