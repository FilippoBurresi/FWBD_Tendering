from tkinter import *
from tkinter import messagebox
import pandas as pd
from web3 import Web3
import string
import random
import json

filename = "/"


def initialize_contract(ganache_URL,address,abi):
    web3=Web3(Web3.HTTPProvider(ganache_URL))

    web3.eth.defaultAccount=web3.eth.accounts[0]
    abi=json.loads(abi)
    address=web3.toChecksumAddress(address)
    contract=web3.eth.contract(address=address,abi=abi)
    return web3,contract


def create_tender(web3,contract,input_dict_pa):
	try:
		###input_dict_pa={"tender_name":"ponte di messina","description":"blablabla","n_days1":"1";"n_days2":"2","weight_price":"0.3"
		#,"weight_time":"0.1","weight_environment":0.6}
		tender_name=input_dict_pa["tender name"].get()
		description=input_dict_pa["description"].get()
		n_days_1=int(input_dict_pa["n seconds to send hash"].get())
		n_days_2=int(input_dict_pa["n seconds to send file"].get())
		weight_1_price=int(input_dict_pa["weight price"].get())
		weight_2_time=int(input_dict_pa["weight time"].get())
		weight_3_envir=int(input_dict_pa["weight environment"].get())
		create_tender_solidity(web3,contract,tender_name,description,n_days_2,n_days_1,weight_1_price,weight_2_time,weight_3_envir)
		messagebox.showinfo("Create Tender", "the function has been called successfully")
	
	except Exception as e:
		messagebox.showerror("Create Tender", str(e) + " You might not have the permission to call this function")


    
def create_tender_solidity(web3,contract,tender_name,description,n_days_1,n_days_2,weight_1_price,weight_2_time,weight_3_envir):
    contract.functions.CreateTender(tender_name,description,n_days_1,n_days_2,weight_1_price,weight_2_time,weight_3_envir).transact()
 
def allowed_companies_ids(web3,contract,input_dict):
	try:
		list_allowed=input_dict["allowed companies"].get().split(",")
		for i in list_allowed:
			contract.functions.addFirm(web3.eth.accounts[int(i)]).transact()
			print(web3.eth.accounts[int(i)])
		messagebox.showinfo("Allowed Companies", "The companies have been added to the allowed list")
	except Exception as e:
		messagebox.showerror("Allowed Companies", str(e)+ " You might not have the permission to call this function")
		

def assign_winner(web3,contract,input_dict):
    try:
        tender_id=int(input_dict["tender id"].get())
        contract.functions.compute_scores(tender_id).transact()
        contract.functions.assign_winner(tender_id).transact()
        winning_address,score=contract.functions.displayWinner(tender_id).call()
        messagebox.showinfo("Assign Winner", "The winner of the tender has been appointed")
        return web3.eth.accounts.index(winning_address)
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
    df=pd.DataFrame(l,columns=["tender id","name","description","weights","bid list","winning contractor","pending?"])
    print(df["weights"][0])
    df["price weight"]=df["weights"].apply(lambda x: x[0])
    df["time weight"]=df["weights"].apply(lambda x: x[1])
    df["environment weight"]=df["weights"].apply(lambda x: x[2])
    dict_address={address:web3.eth.accounts.index(address) for address in web3.eth.accounts}
    df["bid list"]=df["bid list"].apply(lambda x: " ".join([str(dict_address[i]) for i in x]))
    df.drop('weights', inplace=True, axis=1)
    return df
  
def see_active_tenders(web3,contract, input_dict):
    try:
        input_dict['tv1'].delete(*input_dict['tv1'].get_children()) 
        df=get_tenders_status(web3,contract,input_dict)
        df = df[df["pending?"]==True]
        df.drop('pending?', inplace=True, axis=1)
        df.drop('winning contractor', inplace=True, axis=1)
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
        df.drop('pending?', inplace=True, axis=1)
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
        tender_id = int(input_dict['tender id'].get())
        num_bids=contract.functions.getResultsLenght(tender_id).call()
        bids_list=[]
        for i in range(0,num_bids):
            address,score,winner=contract.functions.getResultsValue(tender_id,i).call()
            bids_list.append(contract.functions.getBidDetails(tender_id,address).call())
            print(bids_list)
        df = pd.DataFrame(bids_list,columns=["address","description","separator used","score","winner?"])
        dict_address={address:web3.eth.accounts.index(address) for address in web3.eth.accounts}
        df["account"]=df["address"].apply(lambda x: dict_address[x])
        df["price"]=df["description"].apply(lambda x: x[0])
        df["time"]=df["description"].apply(lambda x: x[1])
        df["environment"]=df["description"].apply(lambda x: x[2])
        df=df[["account","separator used","price","time","environment","score","winner?"]]
        df.sort_values(by="score",ascending=True,inplace=True)
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
        tender_id=int(input_dict["tender id"].get())
        price=input_dict["price"].get()
        time=input_dict["time"].get()
        envir=input_dict["environment"].get()
        if int(envir) not in [1,2,3,4]:
            messagebox.showerror("Error", "the variable environment has to be 1,2,3,4")
        
        list_values_to_hash=[price,time,envir]
        unencrypted_message,separator=to_string_and_sep(list_values_to_hash)
        hash=encrypt(unencrypted_message)
        
        send_bid_solidity(web3,contract,tender_id,hash)
        save_txt(web3,str(web3.eth.defaultAccount),str(separator),unencrypted_message,str(tender_id))
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

def save_txt(web3,user_id,separator,unencrypted_message,tender_id):
    dict_address={address:web3.eth.accounts.index(address) for address in web3.eth.accounts}
    file=open("offer_{}.txt".format(dict_address[user_id]),"w")
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
    

