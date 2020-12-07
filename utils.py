from tkinter import *
from tkinter import ttk
import pandas as pd
from tkinter import filedialog
from web3 import Web3
import json
import string
import random

abi = """[
	{
		"constant": false,
		"inputs": [
			{
				"name": "_tenderKey",
				"type": "uint256"
			}
		],
		"name": "assign_winner",
		"outputs": [
			{
				"name": "",
				"type": "address"
			},
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_tenderKey",
				"type": "uint256"
			}
		],
		"name": "compute_scores",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_tenderKey",
				"type": "uint256"
			},
			{
				"name": "_description",
				"type": "string"
			},
			{
				"name": "_separator",
				"type": "string"
			}
		],
		"name": "concludeBid",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_addressPA",
				"type": "address"
			}
		],
		"name": "CreatePA",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_tenderName",
				"type": "string"
			},
			{
				"name": "_description",
				"type": "string"
			},
			{
				"name": "_daysUntilClosingDateData",
				"type": "uint256"
			},
			{
				"name": "_daysUntilClosingDateHash",
				"type": "uint256"
			},
			{
				"name": "w1",
				"type": "uint256"
			},
			{
				"name": "w2",
				"type": "uint256"
			},
			{
				"name": "w3",
				"type": "uint256"
			}
		],
		"name": "CreateTender",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [],
		"name": "displayPendingTenders",
		"outputs": [
			{
				"name": "",
				"type": "string[]"
			},
			{
				"name": "",
				"type": "uint256[]"
			},
			{
				"name": "",
				"type": "uint256[]"
			},
			{
				"name": "",
				"type": "uint256[]"
			},
			{
				"name": "",
				"type": "uint256[]"
			},
			{
				"name": "",
				"type": "uint256[]"
			},
			{
				"name": "",
				"type": "uint256[]"
			}
		],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_tenderKey",
				"type": "uint256"
			}
		],
		"name": "displayWinner",
		"outputs": [
			{
				"name": "",
				"type": "address"
			}
		],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_tenderKey",
				"type": "uint256"
			},
			{
				"name": "_hashOffer",
				"type": "bytes32"
			}
		],
		"name": "placeBid",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_tenderKey",
				"type": "uint256"
			}
		],
		"name": "see_TenderDetails",
		"outputs": [
			{
				"name": "tender_id",
				"type": "uint256"
			},
			{
				"name": "tenderName",
				"type": "string"
			},
			{
				"name": "description",
				"type": "string"
			},
			{
				"name": "bidList",
				"type": "address[]"
			}
		],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_phrase",
				"type": "string"
			},
			{
				"name": "_separator",
				"type": "string"
			}
		],
		"name": "SMT",
		"outputs": [
			{
				"name": "",
				"type": "string[]"
			}
		],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_tenderKey",
				"type": "uint256"
			}
		],
		"name": "SplitDescription",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"name": "message",
				"type": "string"
			},
			{
				"indexed": false,
				"name": "sender",
				"type": "address"
			}
		],
		"name": "message",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"name": "",
				"type": "string"
			},
			{
				"indexed": false,
				"name": "",
				"type": "uint256"
			},
			{
				"indexed": false,
				"name": "",
				"type": "address"
			},
			{
				"indexed": false,
				"name": "",
				"type": "uint256"
			}
		],
		"name": "Winner_display",
		"type": "event"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "",
				"type": "address"
			}
		],
		"name": "allowedInstitution",
		"outputs": [
			{
				"name": "",
				"type": "bool"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "_tenderKey",
				"type": "uint256"
			},
			{
				"name": "_index",
				"type": "address"
			}
		],
		"name": "getBidDetails",
		"outputs": [
			{
				"name": "",
				"type": "address"
			},
			{
				"name": "",
				"type": "bytes32"
			},
			{
				"name": "",
				"type": "bool"
			},
			{
				"name": "",
				"type": "string[]"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "_tenderKey",
				"type": "uint256"
			}
		],
		"name": "getResultsLenght",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "_tenderKey",
				"type": "uint256"
			},
			{
				"name": "_index",
				"type": "uint256"
			}
		],
		"name": "getResultsValue",
		"outputs": [
			{
				"name": "",
				"type": "address"
			},
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "s",
				"type": "string"
			}
		],
		"name": "stringToUint",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "tenderKeys",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"name": "tenderList",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"name": "tenders",
		"outputs": [
			{
				"name": "tender_id",
				"type": "uint256"
			},
			{
				"name": "tenderName",
				"type": "string"
			},
			{
				"name": "description",
				"type": "string"
			},
			{
				"name": "bidOpeningDate",
				"type": "uint256"
			},
			{
				"name": "bidSubmissionClosingDateData",
				"type": "uint256"
			},
			{
				"name": "bidSubmissionClosingDateHash",
				"type": "uint256"
			},
			{
				"name": "tenderingInstitution",
				"type": "address"
			},
			{
				"name": "winningContractor",
				"type": "address"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	}
]"""

# Web3 function

#### PA INTERFACE



def create_tender(web3,contract,input_dict_pa):
    ## non capisco tender_keys // tender_id, come funzionano ?? ho messo come input anche ID TENDER
    ###input_dict_pa={"tender_name":"ponte di messina","description":"blablabla","n_days1":"1";"n_days2":"2","weight_price":"0.3"
    #,"weight_time":"0.1","weight_environment":0.6}
    tender_name=input_dict_pa["tender_name"].get()
    description=input_dict_pa["description"].get()
    n_days_1=int(input_dict_pa["n_days"].get())
    n_days_2=int(input_dict_pa["n_days_2"].get())
    n_days_2=int(input_dict_pa["n_days_2"].get())
    weight_1_price=int(input_dict_pa["weight_1_price"].get())
    weight_2_time=int(input_dict_pa["weight_2_time"].get())
    weight_3_envir=int(input_dict_pa["weight_3_envir"].get())
    create_tender_solidity(web3,contract,tender_name,description,n_days_1,n_days_2,weight_1_price,weight_2_time,weight_3_envir)
    
def create_tender_solidity(web3,contract,tender_name,description,n_days_1,n_days_2,weight_1_price,weight_2_time,weight_3_envir):
    web3.eth.defaultAccount=web3.eth.accounts[0]
    contract.functions.CreateTender(tender_name,description,n_days_1,n_days_2,weight_1_price,weight_2_time,weight_3_envir).transact()
    
    
    
    

def allowed_companies_ids(web3,contract,input_dict):
    list_allowed=input_dict["allowed_companies"].get().split(",")
    for i in list_allowed:
        contract.functions.CreatePA(web3.eth.accounts[int(i)]).transact()
        

def assign_winner(web3,contract,input_dict):
    tender_id=int(input_dict["tender_id"].get())
    web3.eth.defaultAccount=web3.eth.accounts[0]
    contract.functions.compute_scores(tender_id).transact()
    contract.functions.assign_winner(tender_id).transact()
    winning_address,score=contract.functions.displayWinner(tender_id).call()
    return web3.eth.accounts.index(winning_address)





##### CITIZEN INTERFACE
def get_tenders_status(web3,contract):
    num_tenders=contract.functions.getTendersLenght().call()
    l=[]
    for i in range(num_tenders):
        key,status=contract.functions.isPending(i).call()
        list=see_TenderDetails(i).call()
        list.append(status)
        l.append(list)
    df=pd.Dataframe(l,columns=["tender_id","name","description","weights","bid_list","pending?"])
    return df
  
def see_active_tenders(web3,contract):
    df=get_tenders_status(web3,contract)
    return df[df["pending?"]==True]

    
def see_closed_tenders(web3,contract):
    df=get_tenders_status(web3,contract)
    return df[df["pending?"]==False]
    
def get_bids_details(web3,contract,tender_id):
    #### io clicco sul df delle closed tenders su una riga 
    #e vado su questa nuova view: fattibile?come prendo input?
    num_bids=contract.functions.getResultsLenght(tender_id).call()
    bids_list=[]
    for i in range(0,num_bids):
        bids_list.append(contract.functions.getBidDetails(tender_id,address).call())
    df = pd.DataFrame(bids_list,columns=["name","description","separator","score","winner?"])
    return df

    

    
    
#### COMPANIES INTERFACE

def send_bid(input_dict,web3,contract):
    #inputdict={"user_id":"1","tender_id":"11","price":"38448","time":"120","envir":"4"}
    user_id=int(input_dict["user_id"].get())
    tender_id=int(input_dict["tender_id"].get())
    price=input_dict["price"].get()
    time=input_dict["time"].get()
    envir=input_dict["envir"].get()
    
    list_values_to_hash=[price,time,envir]
    unencrypted_message,separator=to_string_and_sep(list_values_to_hash)
    hash=encrypt(unencrypted_message)
    
    send_bid_solidity(web3,contract,user_id,tender_id,hash)
    save_txt(user_id,separator,unencrypted_message,tender_id)
    
def send_unencrypted(web3,contract,user_id):
    ##come funziona qua per l'input con il txt?
    tender_id,user_id,unencrypted_message,separator=load_txt(user_id)
    send_unencrypted_solidity(web3,contract,tender_id,user_id,unencrypted_message,separator)



def to_string_and_sep(l):
    #"12" "12484" "è un bel progetto, si lo è"
    #s="1212484è un bel progetto"
    #unencripted_message="12#######12848######è UN BEL PROGETTO SI LO è"
    s="".join(l)
    while True:
        separator=get_random_separator()
        if separator not in s:
            unencrypted_message=separator.join(l)+separator
            print(unencrypted_message,separator)
            return unencrypted_message,separator

def get_random_separator(length=10):
    allowed_characters = string.ascii_letters + string.digits + string.punctuation
    separator = ''.join(random.choice(allowed_characters) for i in range(length))
    return separator

def encrypt(unencrypted_message):
    hash=bytes(Web3.soliditySha3(['string[]'], [unencrypted_message]))
    print(hash)
    return hash

def send_bid_solidity(web3,contract,user_id,tender_id,hash):
    web3.eth.defaultAccount=web3.eth.accounts[int(user_id)]
    contract.functions.placeBid(int(tender_id),hash).transact()

def save_txt(user_id,separator,unencrypted_message,tender_id):
    file=open("offer_{}.txt".format(user_id),"w")
    file.writelines([separator+"\n",unencrypted_message+"\n",tender_id])
    file.close()
    
def load_txt(user_id):
    file=open("offer_{}.txt".format(user_id),"r")
    separator,unencrypted_message,tender_id=[i.replace("\n","") for i in file.readlines()]
    file.close()
    print(separator,unencrypted_message,tender_id)
    return tender_id,user_id,unencrypted_message,separator

def send_unencrypted_solidity(web3,contract,tender_id,user_id,unencrypted_message,separator):
    
    web3.eth.defaultAccount=web3.eth.accounts[int(user_id)]
    bid_id = contract.functions.returningBidIdAddress(tender_id).call()
    contract.functions.concludeBid(tender_id,unencrypted_message,separator).transact()
    


# User interface
def makeform(root, fields, title="Lorem Ipsum", description="Lorem Ipsum description",view = False, file = False):
    def fileDialog():
        global filename
        filename = filedialog.askopenfilename(initialdir ="/", title = "Select a file") #, filetype = (('text files', 'txt'),)

    entries = {}
    row = Frame(root)
    row.pack(fill = X, padx = 5, pady = 5)
    lab = Label(row, text = title,font=(None, 15) )
    lab.pack(side=LEFT)
    row = Frame(root)
    row.pack(fill = X, padx = 5, pady = 5)
    lab = Label(row, text = description,font=(None, 10) )
    lab.pack(side=LEFT)
    for field in fields:
        row = Frame(root)
        lab = Label(row, width=22, text=field+": ", anchor='w')
        ent = Entry(row, width=40)
        ent.insert(0,"0")
        row.pack(side = TOP, fill = X, padx = 5 , pady = 5)
        lab.pack(side = LEFT,fill = X, padx = 10 , pady = 0)
        ent.pack(side = RIGHT, expand = YES, fill = X)
        entries[field] = ent
    if view:
        row = LabelFrame(root, text="Excel Data", height=250, width=600)
        sub_row1 = Frame(row)
        sub_row2 = Frame(row)
        tv1 = ttk.Treeview(sub_row1)   
        treescrolly = Scrollbar(sub_row1, orient="vertical", command=tv1.yview) 
        treescrollx = Scrollbar(sub_row2, orient="horizontal", command=tv1.xview) 
        tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)

        row.pack(side = TOP, fill = X, expand = True,  padx = 5 , pady = 5) #,  padx = 5 , pady = 5
        sub_row1.pack(side = TOP, fill = X, expand = True,  padx = 5 , pady = 5)
        tv1.pack(side = LEFT, fill = X, expand = True,  padx = 5 , pady = 5) #, padx = 5 , pady = 5     
        treescrolly.pack(side="left", fill="y")
        #row.pack(side = BOTTOM, fill = X, padx = 5 , pady = 5) 
        sub_row2.pack(side = TOP, fill = X, expand = True,  padx = 5 , pady = 5)
        treescrollx.pack(side="bottom", fill="x")   

        entries['tv1'] = tv1
    # button to search a file
    if file:
        row = Frame(root)
        btn = Button(row, text = "File", height=2, width=12, command = fileDialog)
        row.pack(side=TOP, fill=X, expand = True)
        btn.pack(side= LEFT,padx = 5 , pady = 5)
        
    # button to call the
    row = Frame(root)
    btn = Button(row, text = "Call", height=2, width=12)
    row.pack(side=TOP, fill=X, expand = True)
    btn.pack(side= LEFT,padx = 5 , pady = 5)
    entries["btn"]=btn
    
    # button to call the function
    row = Frame(root)
    s = ttk.Separator(row, orient=HORIZONTAL )
    row.pack(fill=X,padx = 5 , pady = 5)
    s.pack(fill = X)
    
    

    return entries
