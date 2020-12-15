# **Blockchain-based Public Tendering**
This project is part of the Finance with Big Data course at Bocconi University. In this repository, we develop a Solidity-based smart contract focused on tendering procedures. We believe Blockchain technology has the potential to disrupt the procurement field, that is the process of researching and exchanging goods and services often done by tendering procedures. Indeed, by transforming the tendering as a smart contract we would be able to improve the procurement by reducing the duration of a tendering – which is very costly – and the possibility of corruption that might happen. In turns, this would improve the welfare of the economy as well as our society. 
These are our motivations behind the project. Now, let’s deepen into our implementation.

## **Repository Overview**
```PA.sol``` : This contract is used by the user with an administrative role in the creation of the two main subjects that participate in our blockchain: the Public Administration and the firms. Through the functions in this contract their roles are assigned in order to allow them to carry out the appropriate interactions with the main contract.

```SafeMath.sol``` : The SafeMath library is created, which reverts transactions when an operation overflows and removes the risk of bugs when dealing with arithmetic operations.

```Tendering.sol``` : The main contract of our blockchain, this contains the functions for the whole tendering procedure. All four parts of the process are considered: request, bidding, evaluation, and publishing. 

```config.py``` : This python code sets up the application binary interface (ABI) to be used by the public administration, with the functions associated to this role. 

```gasPlot.jpeg``` : An image representing the decreases in transaction cost, based on gas, that occurred following the changes to the main smart contract.

```strings.sol``` : The strings and slice utility libraries are created, to be used for certain operations in the smart contract.

```userinterface.py``` : This python code produces the user interface that allows access to our smart contract and blockchain, with all the associated functions of the Tendering.sol file used for the tendering procedure.

```utils.py``` : This python code defines the functions to be implemented in the user interface.

## **Access Control with PA.sol**
Access control is crucial on the Blockchain, since we want to control who is allowed to do what in a tendering procedure. According to our approach, tendering procedures can be accessed by three different agents: the public administration that issues a request for tender, a firm that sends a bid, and finally a citizen that wants to access the process and check its fairness. Clearly, each of the agents involved has different powers in terms of accessibility. We implemented the aforementioned structure by following OpenZeppelin’s instructions (https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/access/AccessControl.sol), and we created a Role-based Access Control system for our smart contract that you can find in PA.sol. 

## **Outlining a public tendering with Tendering.sol**
The smart contract takes into account all the phases that define a tendering, that are: request for tenders, bidding, evaluation and publishing the results. The pursuit of the subsequent stage is controlled by ad hoc modifiers. 

1)	In the first phase, a public administration will create a tendering with the analogous function. The request for tenders is a struct that contains all relevant information, that are the name of the public institution, the description of the request, the deadlines – one for submitting the hash of the offer and another one for submitting the explicit offer – and the evaluation weights needed for the evaluation phase (see more later). To avoid fraudulent attacks, we control that only allowed institutions can actually create a tendering. 

Notice that the deadlines are theoretically considered in days but in the file they are expressed as seconds to make the implementation faster. Otherwise, you would wait days to proceed from a phase to another one. 

2)	In the second phase, every interested firm can look at the details of the tendering of interest and decide whether to apply or not. If yes, the firm must send a bid as a hash by the first deadline, i.e. ```bidSubmissionClosingDateHash```, with the function ```placeBid```. To reflect as closely as possible reality and to avoid excessive gas costs as well as fraudulent attacks, we decided to limit the number of times a firm can place a bid for a specific tender to only one time. In other words, a firm can participate in more than one tendering procedure but it can send no more than one bid for each tendering. After the first deadline, the firm must finalize its bid by submitting its offer explicitly through the function ```concludeBid```. To avoid bad behaviours, the system checks whether the hash previously sent and the explicit offer match through a require inside concludeBid. If valid, the bid is considered for the evaluation part. 

3)	In the third phase, the public administration that issued the request for tender runs the evaluation code after the deadline ```bidSubmissionClosingDateData``` is reached. Our approach evaluates offers by computing a weighted average of three different factors: price offered, timing to deliver the project and the 1-4 category representing the environmental safeguard level that the firm ensures for producing the request. All these factors are found inside the description of the offer sent by the firm. Although we tried to resemble how tendering works in reality – e.g. environmental safeguard levels are actually taken into account in tendering procedures – we are aware that our approach is an oversimplification of what happens in reality. Yet, we believe this work can still be taken into account as an easy and feasible alternative for a first taste of how tendering could work on a Blockchain-based application. In more details, during the evaluation phase, each firm that sent a valid bid is associated to a score, i.e. the weighted average. Such score is computed by firstly rescaling timing and environmental safeguard level so to make them comparable with the price thanks to the function ```adjust_measures```, which is called inside the function ```compute_scores```. Indeed, if those factors were not rescaled then the evaluation scores would be driven mainly by the price. To avoid possible bugs when working with numbers and formulas, we imported the SafeMath library in our smart contract. 
An important thing to note is that different approaches were possible to outline the evaluation phase. Indeed, we could have run the evaluation code outside Solidity, e.g. in Python, and simply have declared the algorithm for evaluation when creating the tendering at the beginning in Solidity. This would have surely increased the flexibility – since following our approach public administrations are forced to evaluate bids as a weighted average – and saved some gas. However, for the sake of transparency and the fact that the scope of the project was to implement a smart contract with Solidity, we preferred to integrate the evaluation part in Solidity. 

4)	Finally, the publishing of the results. In this phase, the allowed public administration that issued the tendering assigns the winner through the analogous function. The winner is the address that has the lowest score. Then, each person – both other firms or citizens – can look at the winner and its score by calling the function ```displayWinner```. We decided not to notify each node of the Blockchain about the conclusion of the tendering and its result because events are quite expensive. So, we opted for a user-friendly interface where people can easily access all the information related to a tendering, conditional on their own accessibility powers. Now, we will see more in details such user interface. 

## **User Interface**
The related files of this part to refer to are:
```
userinterface.py
utils.py
config.py
SmartContractUserInteraction.py
```
We wanted to create a intuitive way to interact with the Tendering Smart-Contract both for the PA in the tender creation process and for the firms willing to participate in a tender and all those citizens interested in investigating the correctness and fairness of the tendering procedure. In order to do so, we develop a web3-based python code capable of connecting each address to the range of functions specific to its own role. We also built a user-friendly interface based on the above-mentioned code thanks to the Tkinter library through which we created a prototype implementation of our model: in this way, you can get an idea of how the Smart Contract works.
To make this prototype more usable in the testing phase, the possibility to change at will the account with which to interact with the smart contract has been inserted in the login tab in order to see the difference in terms of permissions between the various types of accounts (PA, allowed contractor and citizen)
In the following sections, we are going to present some examples of how firms and citizens can make use of the Tendering Smart-Contract via python to better show how easily accessible our contract is.

### *PA-Role*

From the user interface, the public administration can easily create a tender by entering the details via text inputs. It can also give permission to some accounts to place bids and finally declare the winner once the tendering is closed.

### *Firm-Role* 

A company can view in tabular form from the Notice Board tab all the tenders currently active (this does not require any permission). Then, according to the one that better suits its offer, the firm will decide where to participate. In fact, once the company is authorized by the PA, to send its own proposal to the blockchain, the firm has just to call the SendBid function and to specify the characteristics of its bid. The three elements of the offer – price, estimated time of realization, environment-friendliness score – will be automatically saved in a txt file in the working directory and the hash of the offer will be then sent to the blockchain by calling the placeBid solidity function.  The company will use the txt file by uploading it and then, through the appropriate function, complete the offer. In fact, the smart contract will check whether the hash matches the extended offer before validating it and exposing it to evaluation.


All these steps can be performed and visualized by accessing the tkinter interface, choosing an address granted with firm role (1-8) in the first window and then playing within the notice board and the contractor windows.

### *Citizen (every account)*

Any citizen with an account can call all the functions present in the Notice Board tab and that show in tabular form all the active tenders, the tenders already concluded and all the offers related to a specific tender. The goal of this function is to make the operation of the smart contract transparent, giving citizens the opportunity to verify its work.

The previous step can be performed by choosing every account in the in the login tab.

## **Optimization**

The code in ```Tendering.sol``` has been optimized so to spend less gas as we can in transactions. This is crucial to make our project appealing to both public administrations and firms. Indeed, our goal is to show how easy, transparent and cheap are Blockchain-based tendering procedures to these two main actors. On the other hand, citizens do not spend any gas in checking the tendering since we took care of expressing those functions as pure/view. 

To optimize the smart contract we combined different adjustments: from eliminating redundant variables and events to small changes like avoiding the initialization of numeric variables and readjusting the order of the variables inside functions. Overall, we were able to save 292167 wei of transaction costs. Here, a more comprehensive plot of the results of the optimization steps that we followed: 

<p align="center">
  <img width="460" height="300" src="https://github.com/FilippoBurresi/FWBD_Tendering/blob/main/gasPlot.jpeg">
</p>

## **Security**

With smart contracts, the implementation of rules and procedures becomes easier and quicker.
However, there is always a drawback: the security might be at risk if not adequately handled.
We have discussed and thought a lot about what could possibly go wrong in our system.

Just in order to prevent any security breaches, we have built a Role-based Access Control system through OpenZeppelin.
In this way, we can control all the agents who interact and be sure that nobody does something he has not been authorized to do.
For example, without this role-based system, one main problem we could have incurred is that some malicious users could have started to send a very large amount of bids.
The cost of some functions in our smart contract, especially compute_scores and assign_winner which rely on a for loop whose length depends on the number of participants,  would have rocketed, causing consequently an unsustainable economical burden for the PA, creator of the tender.
Since in our contract the Public Administration has to authorize each firm prior to the bidding phase, the aforementioned risk has been avoided.

We have also assured that each rule is respected by inserting various require() that prevent, for example, any offer beyond the deadline from being considered and evaluated  or, yet, any bidder from modifying its own project once sent.
Moreover, we have also taken security measures on the numerical side: indeed we avoid overflows by making use of the SafeMath library.

Lastly, we have also evaluated the possibility to  insert an additional function in our SmartContract to let the PA withdraw a tender at any moment. However, we thought that if this function, on one hand, would have provided the PA with the possibility of overcoming any problem the tendering procedure might face, on the other it would have opened a not very realist scenario since if a Public Administration needs a certain service or product and launches a tender, then it will hardly step back.



