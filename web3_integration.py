from web3 import Web3
import json

import string
import random



ganache_URL="HTTP://127.0.0.1:7545"
web3=Web3(Web3.HTTPProvider(ganache_URL))
web3.eth.defaultAccount=web3.eth.accounts[0]

abi=json.loads("""[
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_descrizione1",
				"type": "string"
			},
			{
				"internalType": "bytes32",
				"name": "hash",
				"type": "bytes32"
			}
		],
		"name": "Check",
		"outputs": [
			{
				"internalType": "bytes32",
				"name": "hash4",
				"type": "bytes32"
			},
			{
				"internalType": "bytes32",
				"name": "hash3",
				"type": "bytes32"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_descrizione",
				"type": "string"
			}
		],
		"name": "CreateTender",
		"outputs": [
			{
				"internalType": "bytes32",
				"name": "hash2",
				"type": "bytes32"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]""")
    
address=web3.toChecksumAddress("0x72f54aF79D87535Ee31b00B9142e94b9A66F8882")
contract=web3.eth.contract(address=address,abi=abi)

#### PA INTERFACE

dictionary_input_pa={}

def create_tender(input_dict):
    pass

def allowed_companies_ids():
    pass

def allowed_citizens_ids():
    pass

def public_results():
    pass




##### CITIZEN INTERFACE


def see_results():
    pass


#### COMPANIES INTERFACE
dictionary_input_company={}

def send_bid(input_dict,web3,contract,allowed_companies):
    #inputdict={"user_id":"1","tender_id":"11","price":"38448","description":"blablabla"}
    user_id=input_dict["user_id"].text
    assert user_id in allowed_companies, "company is not allowed"
    tender_id=input_dict["tender_id"].text
    price=input_dict["price"].text
    description=input_dict["description"].text
    
    list_values_to_hash=[tender_id,price,description]
    unencrypted_message,separator=to_string_and_sep(list_values_to_hash)
    hash=encrypt(unencrypted_message)
    
    send_bid_solidity(web3,contract,user_id,tender_id,hash)
    save_txt(user_id,separator,unencrypted_message,tender_id)
    
def send_unencrypted(web3,contract,user_id):
    tender_id,user_id,unencrypted_message,separator=load_txt(user_id)
    send_unencrypted_solidity(web3,contract,tender_id,user_id,unencrypted_message,separator)
    
    
def see_results():
    pass



def to_string_and_sep(l):
    #"12" "12484" "è un bel progetto, si lo è"
    #s="1212484è un bel progetto"
    #unencripted_message="12#######"
    s="".join(l)
    while True:
        separator=get_random_separator()
        if separator not in s:
            unencrypted_message=separator.join(l)
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
    ##possiamo mettere qua condizione <datachiusura, devo trovare modo di chiamare la variabile
    web3.eth.defaultAccount=web3.eth.accounts[int(user_id)]
    contract.functions.placeBid(int(tender_id),hash)

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
    ##if now()>data chiusura:
    ##viene facile mettere bidkey==user_id (valori da 0 a 9)si può fare? devono andare in ordine da 0 a 9 per funzionare?
    web3.eth.defaultAccount=web3.eth.accounts[int(user_id)]
    contract.functions.concludeBid(tender_id,user_id,unencrypted_message,separator)


