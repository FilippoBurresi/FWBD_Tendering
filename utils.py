from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
from tkinter import filedialog
from web3 import Web3
import json
import string
import random


filename = "/"
abi = """[
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "id",
				"type": "address"
			}
		],
		"name": "addFirm",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "id",
				"type": "address"
			}
		],
		"name": "addPA",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_tenderKey",
				"type": "uint256"
			}
		],
		"name": "assign_winner",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_tenderKey",
				"type": "uint256"
			}
		],
		"name": "compute_scores",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_tenderKey",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "_description",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_separator",
				"type": "string"
			}
		],
		"name": "concludeBid",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_tenderName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_description",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_daysUntilClosingDateData",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_daysUntilClosingDateHash",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "w1",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "w2",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "w3",
				"type": "uint256"
			}
		],
		"name": "CreateTender",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_tenderKey",
				"type": "uint256"
			}
		],
		"name": "displayWinner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getTendersLength",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "role",
				"type": "bytes32"
			},
			{
				"internalType": "address",
				"name": "account",
				"type": "address"
			}
		],
		"name": "grantRole",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_tenderKey",
				"type": "uint256"
			}
		],
		"name": "isPending",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_value",
				"type": "string"
			}
		],
		"name": "parseInt",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "_ret",
				"type": "uint256"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_tenderKey",
				"type": "uint256"
			},
			{
				"internalType": "bytes32",
				"name": "_hashOffer",
				"type": "bytes32"
			}
		],
		"name": "placeBid",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "id",
				"type": "address"
			}
		],
		"name": "renounceFIRM",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "id",
				"type": "address"
			}
		],
		"name": "renouncePA",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "role",
				"type": "bytes32"
			},
			{
				"internalType": "address",
				"name": "account",
				"type": "address"
			}
		],
		"name": "renounceRole",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "id",
				"type": "address"
			}
		],
		"name": "revokeFirm",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "id",
				"type": "address"
			}
		],
		"name": "revokePA",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "role",
				"type": "bytes32"
			},
			{
				"internalType": "address",
				"name": "account",
				"type": "address"
			}
		],
		"name": "revokeRole",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "bytes32",
				"name": "role",
				"type": "bytes32"
			},
			{
				"indexed": true,
				"internalType": "bytes32",
				"name": "previousAdminRole",
				"type": "bytes32"
			},
			{
				"indexed": true,
				"internalType": "bytes32",
				"name": "newAdminRole",
				"type": "bytes32"
			}
		],
		"name": "RoleAdminChanged",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "bytes32",
				"name": "role",
				"type": "bytes32"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "account",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "sender",
				"type": "address"
			}
		],
		"name": "RoleGranted",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "bytes32",
				"name": "role",
				"type": "bytes32"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "account",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "sender",
				"type": "address"
			}
		],
		"name": "RoleRevoked",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_tenderKey",
				"type": "uint256"
			}
		],
		"name": "see_TenderDetails",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "tender_id",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "tenderName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "description",
				"type": "string"
			},
			{
				"internalType": "uint256[]",
				"name": "evaluation_weights",
				"type": "uint256[]"
			},
			{
				"internalType": "address[]",
				"name": "firms",
				"type": "address[]"
			},
			{
				"internalType": "address",
				"name": "winningContractor",
				"type": "address"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "allowedInstitution",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "DEFAULT_ADMIN_ROLE",
		"outputs": [
			{
				"internalType": "bytes32",
				"name": "",
				"type": "bytes32"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "FIRM_ROLE",
		"outputs": [
			{
				"internalType": "bytes32",
				"name": "",
				"type": "bytes32"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_tenderKey",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "_index",
				"type": "address"
			}
		],
		"name": "getBidDetails",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			},
			{
				"internalType": "string[]",
				"name": "",
				"type": "string[]"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_tenderKey",
				"type": "uint256"
			}
		],
		"name": "getResultsLenght",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_tenderKey",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_index",
				"type": "uint256"
			}
		],
		"name": "getResultsValue",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "role",
				"type": "bytes32"
			}
		],
		"name": "getRoleAdmin",
		"outputs": [
			{
				"internalType": "bytes32",
				"name": "",
				"type": "bytes32"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "role",
				"type": "bytes32"
			},
			{
				"internalType": "uint256",
				"name": "index",
				"type": "uint256"
			}
		],
		"name": "getRoleMember",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "role",
				"type": "bytes32"
			}
		],
		"name": "getRoleMemberCount",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "role",
				"type": "bytes32"
			},
			{
				"internalType": "address",
				"name": "account",
				"type": "address"
			}
		],
		"name": "hasRole",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "tenderKeys",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "tenderList",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "tenders",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "tender_id",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "bidOpeningDate",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "bidSubmissionClosingDateData",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "bidSubmissionClosingDateHash",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "tenderingInstitution",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "winningContractor",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "tenderName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "description",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]"""

function_info = {'CreateTender': "This function is used to create tenders and can only be called by the public administration. The first time variable indicates in how many days the tender will expire, while the second expiry indicates how soon the complete offers can be loaded and within which the hash must be loaded.The weights indicate the importance that we want the price, the speed of execution and the environmental impact to have, their sum must be equal to 100.",
			   'placeBid': 'This function is used to make an offer to the tender indicated by the tender id. It can only be used by PA approved contractors. The price in euros, the execution time in days and the environmental impact must be indicated (indicated on a scale of 1 to 4). Once the function is called, it will insert the hash of the offer in the blockchain and create a file with the information necessary to complete the offer that will be saved in the working directory',
			   'concludeBid': 'By clicking "File" upload the file created in the previous step to complete the offer. Once the file has been loaded, the path will be displayed to the right of the button. At this point it is possible to complete the offer by clicking "Call".',
			   'getTenderStatus': 'questa è la descrizione per get tender status vediamo come viene',
			   'seeActiveTenders': 'Through this function, citizens and contractor can see the details of currently active tenders. To better visualize the content, you can resize the width of the columns.',
			   'seeClosedTenders': 'Through this function, citizens and contractor can see the details of closed tenders. To better visualize the content, you can resize the width of the columns.',
			   'allowCompanies': 'This function allows companies to give permission to bid. The input is the account index for convenience and more than one can be entered at a time if separated by commas (in a normal scenario the input would be the address)',
			   "getBidsDetails": 'Through this function it is possible given the tender id of a completed tender to see the details of all the offers presented.',
			   'assignWinner': 'This function allows you to assign the winner to the tender specified by the id (only after the deadline), who will be awarded automatically by evaluating the offers made by the contractors according to the parameters entered in the tender.',}
# Web3 function

#### PA INTERFACE



def create_tender(web3,contract,input_dict_pa):
	try:

		## non capisco tender_keys // tender_id, come funzionano ?? ho messo come input anche ID TENDER
		###input_dict_pa={"tender_name":"ponte di messina","description":"blablabla","n_days1":"1";"n_days2":"2","weight_price":"0.3"
		#,"weight_time":"0.1","weight_environment":0.6}
		print(web3.eth.defaultAccount)
		tender_name=input_dict_pa["tender_name"].get()
		description=input_dict_pa["description"].get()
		n_days_1=int(input_dict_pa["n_days"].get())
		n_days_2=int(input_dict_pa["n_days_2"].get())
		n_days_2=int(input_dict_pa["n_days_2"].get())
		weight_1_price=int(input_dict_pa["weight_1_price"].get())
		weight_2_time=int(input_dict_pa["weight_2_time"].get())
		weight_3_envir=int(input_dict_pa["weight_3_envir"].get())
		create_tender_solidity(web3,contract,tender_name,description,n_days_1,n_days_2,weight_1_price,weight_2_time,weight_3_envir)
		messagebox.showinfo("Create Tender", "the function has been called successfully")
	
	except Exception as e:
		messagebox.showerror("Create Tender", str(e) + " You might not have the permission to call this function")


    
def create_tender_solidity(web3,contract,tender_name,description,n_days_1,n_days_2,weight_1_price,weight_2_time,weight_3_envir):
    contract.functions.CreateTender(tender_name,description,n_days_1,n_days_2,weight_1_price,weight_2_time,weight_3_envir).transact()
 
    
    
    

def allowed_companies_ids(web3,contract,input_dict):
	try:
		list_allowed=input_dict["allowed_companies"].get().split(",")
		for i in list_allowed:
			contract.functions.addFirm(web3.eth.accounts[int(i)]).transact()
			print(web3.eth.accounts[int(i)])
		messagebox.showinfo("Allowed Companies", "The companies have been added to the allowed list")
	except Exception as e:
		messagebox.showerror("Allowed Companies", str(e)+ " You might not have the permission to call this function")
		

def assign_winner(web3,contract,input_dict):
	try:
		tender_id=int(input_dict["tender_id"].get())
		contract.functions.compute_scores(tender_id).transact()
		contract.functions.assign_winner(tender_id).transact()
		winning_address,score=contract.functions.displayWinner(tender_id).call()
		return web3.eth.accounts.index(winning_address)
		messagebox.showinfo("Assign Winner", "The winner of the tender has been appointed")
	except Exception as e:
		messagebox.showerror("Allowed Companies", str(e)+ " You might not have the permission to call this function")





##### CITIZEN INTERFACE
def get_tenders_status(web3,contract, input_dict):
	num_tenders=contract.functions.getTendersLength().call()
	l=[]
	for i in range(num_tenders):
		key,status=contract.functions.isPending(i).call()
		list=contract.functions.see_TenderDetails(i).call()
		list.append(status)
		l.append(list)	
	df=pd.DataFrame(l,columns=["tender_id","name","description","weights","bid_list","winning contractor","pending?"])
	
	
	return df
  
def see_active_tenders(web3,contract, input_dict):
	try:
		input_dict['tv1'].delete(*input_dict['tv1'].get_children()) 
		df=get_tenders_status(web3,contract,input_dict)
		df = df[df["pending?"]==True]
		#from here the code "print" the dataframe
		input_dict['tv1']["column"] = list(df.columns)
		for column in input_dict['tv1']["column"]:
			input_dict['tv1'].column(column,minwidth=0, width=78, stretch=NO)
		input_dict['tv1']["show"] = "headings"
		for column in input_dict['tv1']["columns"]:
			input_dict['tv1'].heading(column, text=column) # let the column heading = column name

		df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
		for row in df_rows:
			input_dict['tv1'].insert("", "end", values=row)
	except Exception as e:
		messagebox.showerror("Allowed Companies", str(e))

    
def see_closed_tenders(web3,contract, input_dict):
	try:
		input_dict['tv1'].delete(*input_dict['tv1'].get_children()) 
		df=get_tenders_status(web3,contract,input_dict)
		df = df[df["pending?"]==False]
		#from here the code "print" the dataframe
		input_dict['tv1']["column"] = list(df.columns)
		for column in input_dict['tv1']["column"]:
			input_dict['tv1'].column(column,minwidth=0, width=78, stretch=NO)
		input_dict['tv1']["show"] = "headings"
		for column in input_dict['tv1']["columns"]:
			input_dict['tv1'].heading(column, text=column) # let the column heading = column name

		df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
		for row in df_rows:
			input_dict['tv1'].insert("", "end", values=row)
	except Exception as e:
		messagebox.showerror("Allowed Companies", str(e))


def get_bids_details(web3,contract,input_dict):
	#### io clicco sul df delle closed tenders su una riga 
	#e vado su questa nuova view: fattibile?come prendo input?
	try:
		input_dict['tv1'].delete(*input_dict['tv1'].get_children()) 
		tender_id = int(input_dict['tender_id'].get())
		num_bids=contract.functions.getResultsLenght(tender_id).call()
		bids_list=[]
		for i in range(0,num_bids):
			address,score,winner=contract.functions.getResultsValue(tender_id,i).call()
			bids_list.append(contract.functions.getBidDetails(tender_id,address).call())
			print(bids_list)
		df = pd.DataFrame(bids_list,columns=["name","description","separator","score","winner?"])

		input_dict['tv1']["column"] = list(df.columns)
		for column in input_dict['tv1']["column"]:
			input_dict['tv1'].column(column,minwidth=0, width=78, stretch=NO)
		input_dict['tv1']["show"] = "headings"
		for column in input_dict['tv1']["columns"]:
			input_dict['tv1'].heading(column, text=column) # let the column heading = column name

		df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
		for row in df_rows:
			input_dict['tv1'].insert("", "end", values=row)
	except Exception as e:
		messagebox.showerror("Allowed Companies", str(e))


    

    
    
#### COMPANIES INTERFACE

def send_bid(web3,contract, input_dict):
	try:
		#inputdict={"user_id":"1","tender_id":"11","price":"38448","time":"120","envir":"4"}
		tender_id=int(input_dict["tender_id"].get())
		price=input_dict["price"].get()
		time=input_dict["time"].get()
		envir=input_dict["envir"].get()

		list_values_to_hash=[price,time,envir]
		unencrypted_message,separator=to_string_and_sep(list_values_to_hash)
		hash=encrypt(unencrypted_message)

		send_bid_solidity(web3,contract,tender_id,hash)
		save_txt(str(web3.eth.defaultAccount),str(separator),unencrypted_message,str(tender_id))
		messagebox.showinfo("Send bid", "The bid has been sent successfully")
	except Exception as e:
		messagebox.showerror("Allowed Companies", str(e))
    
def send_unencrypted(web3,contract, input_dict):
	try:
		##come funziona qua per l'input con il txt?
		tender_id,unencrypted_message,separator=load_txt()
		send_unencrypted_solidity(web3,contract,tender_id,unencrypted_message,separator)
		messagebox.showinfo("Bid Completed", "The unencripted bid has been sent")
	except Exception as e:
		messagebox.showerror("Allowed Companies", str(e))



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

def send_bid_solidity(web3,contract,tender_id,hash):
    contract.functions.placeBid(int(tender_id),hash).transact()

def save_txt(user_id,separator,unencrypted_message,tender_id):
    file=open("offer_{}.txt".format(user_id),"w")
    file.writelines([separator+"\n",unencrypted_message+"\n",tender_id])
    file.close()
    
def load_txt():
	global filename
	print(filename)
	file=open(filename,"r")
	
	separator,unencrypted_message,tender_id=[i.replace("\n","") for i in file.readlines()]
	file.close()
	print(separator,unencrypted_message,tender_id)
	return tender_id,unencrypted_message,separator

def send_unencrypted_solidity(web3,contract,tender_id, unencrypted_message,separator):
    contract.functions.concludeBid(int(tender_id),unencrypted_message,separator).transact()
    


# User interface
def makeform(root, fields, title="Lorem Ipsum", description="Lorem Ipsum description",view = False, file = False):
	def fileDialog(v):
		global filename
		filename = filedialog.askopenfilename(initialdir ="/", title = "Select a file") #, filetype = (('text files', 'txt'),)
		v.set(filename)
	global filename
	entries = {}
	row = Frame(root)
	row.pack(fill = X, padx = 5, pady = 5)
	lab = Label(row, text = title,font=(None, 15) ,)
	lab.pack(side=LEFT)
	row = Frame(root)
	row.pack(fill = X, padx = 5, pady = 5)
	lab = Label(row, text = description,font=(None, 10), wraplength = 580, justify = LEFT )
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
		#row = LabelFrame(root, text="Data", height=250, width=600)
		sub_row1 = Frame(root)
		sub_row2 = Frame(root)
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
		v = StringVar()
		lab = Label(row, textvariable = v)
		btn = Button(row, text = "File", height=2, width=12, command = lambda arg1=v : fileDialog(arg1))
		row.pack(side=TOP, fill=X, expand = True)
		btn.pack(side= LEFT,padx = 5 , pady = 5)		
		lab.pack(side=LEFT)

        
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
