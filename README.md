# **Blockchain-based Public Tendering**
This project is part of the Finance with Big Data course at Bocconi University. In this repository, we develop a Solidity-based smart contract focused on tendering procedures. We believe Blockchain technology has the potential to disrupt the procurement field, that is the process of researching and exchanging goods and services often done by tendering procedures. Indeed, by transforming the tendering as a smart contract we would be able to improve the procurement by reducing the duration of a tendering – which is very costly – and the possibility of corruption that might happen. In turns, this would improve the welfare of the economy as well as our society. 
These are our motivations behind the project. Now, let’s deepen into our implementation. 

## **Access Control with PA.sol**
Access control is crucial on the Blockchain, since we want to control who is allowed to do what in a tendering procedure. According to our approach, tendering procedures can be accessed by three different agents: the public administration that issues a request for tender, a firm that sends a bid, and finally a citizen that wants to access the process and check its fairness. Clearly, each of the agents involved has different powers in terms of accessibility. We implemented the aforementioned structure by following OpenZeppelin’s instructions (https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/access/AccessControl.sol), and we created a Role-based Access Control system for our smart contract that you can find in PA.sol. 

## **Tendering.sol**
The smart contract takes into account all the phases that define a tendering, that are: request for tenders, bidding, evaluation and publishing the results. 
1)	In the first phase, a public administration will create a tendering with the analogous function. The request for tenders is a struct that contains all relevant information, that are the deadlines – one for submitting the hash of the offer and another one for submitting the explicit offer – the description of the request and the evaluation weights needed for the evaluation phase (see more later). To avoid fraudulent attacks, we control that only allowed institutions can actually create a tendering. 
2)	In the second phase, every interested firm can look at the details of the tendering of interest and decide whether to apply or not. If yes, the firm must send a bid as a hash by the first deadline, i.e. bidSubmissionClosingDateHash. To reflect as closely as possible reality and to avoid excessive gas costs as well as fraudulent attacks, we decided to limit the number of times a firm can place a bid for a specific tender to only one time. In other words, a firm can participate in more than one tendering procedure but it can send no more than one bid for each tendering. After the first deadline, the firm must finalize its bid by submitting its offer explicitly through the function concludeBid. To avoid bad behaviours, the system checks whether the hash previously sent and the explicit offer match through a require inside concludeBid. If valid, the bid is considered for the evaluation part. 

## **User Interface**
The related files of this part to refer to are:
```
userinterface.py
utils.py
config.py
SmartContractUserInteraction.py
```
We wanted to create a simple way to interact with the Tendering Smart-Contract especially for the firms willing to participate into a tender and all those citizens interested in investigating the correctness and fairness of the tendering procedure.
In order to do so, we develop a web3-based python code capable of connecting each address to the range of functions specific to its own role.
We also built a user-friendly interface based on the above-mentioned code thanks to the tkinter library through which we created a prototype implementation of our model: in this way, you can get an idea of how the Smart Contract works.

In the following sections, we are going to present some examples of how firms and citizens can make use of the Tendering Smart-Contract via python to better show how easily accessible our contract is.


### *Firm-Role* 

A firm might visualize all the tenders with the `get_tender_status` python function that calls three different functions defined in `Tendering.sol`: ```getTendersLenght, isPending, TenderDetails```.
At this point, the firm will have an idea of how many tenders have been generated so far and what tenders are still active. Then, according to the one that better suits its offer, the firm will decide where to participate. To send its own proposal to the blockchain, the firm has just to call the `send_bid` python function and to specify the characteristics of its bid.  The three elements of the offer – price, estimated time of realization, environment-friendliness score – will be automatically saved in a txt file and an hashed copy of this file will be then sent to the blockchain by accessing the `placeBid` solidity function.
Whereas, to conclude a bid, a firm has to call the `send_unencrypted_solidity` python function, directly connected to `concludeBid` solidity Function: the hash of the unencrypted offer will be checked to match the hash sent in the initial phase. 

All these steps can be performed and visualized by accessing the tkinter interface, choosing an address granted with firm role (1-8) in the first window and then playing within the notice board and the contractor windows.

