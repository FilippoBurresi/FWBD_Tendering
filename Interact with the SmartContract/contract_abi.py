# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 17:01:52 2020

@author: Flavia
"""

abi = """[
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_tenderId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_bidId",
				"type": "uint256"
			}
		],
		"name": "assignWinningContractor",
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
				"internalType": "uint32",
				"name": "_bidkey",
				"type": "uint32"
			},
			{
				"internalType": "string",
				"name": "_description",
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
				"name": "_bidOpeningDate",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_bidSubmissionClosingDateHash",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_bidSubmissionClosingDateData",
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
				"name": "_tenderId",
				"type": "uint256"
			}
		],
		"name": "getBidsByKey",
		"outputs": [
			{
				"internalType": "string[]",
				"name": "",
				"type": "string[]"
			},
			{
				"internalType": "address[]",
				"name": "",
				"type": "address[]"
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
				"internalType": "uint256",
				"name": "tenderId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "bidOpeningDate",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "bidSubmissionClosingDateHash",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "bidSubmissionClosingDateData",
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
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]"""