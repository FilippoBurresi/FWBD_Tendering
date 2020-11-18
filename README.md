# FWBD_Tendering
Blockchain for public tendering  

The project deals with two parts: 

(1) **the bidding part**, namely the phase of the tendering procedure when the firm creates a bidding and send that bid to the public sector. In this phase, we structured the project as following: 

- a *contractFactory* contract that contains the code for what is a contract (i.e. it's a struct with several elements such as contractorAddress, governementAddress, tenderId, status ....) and the code for its creation. Whenever a contract is created, it is pushed in memory inside the array of contracts - which have status = "Pending" - and the event NewContract is triggered. Hence, every node on the blockchain is notified that a new contract for the tendering has been created, but they only see the contract_id, the governement_Address and the tenderId. Therefore, companies can get a sense of how competitive the tendering procedure is without knowing the firms that have created a contract. 

- *contractcreation* instead deals with sending the bidding to the PA. It inherits from the contractfactory, hence it can create the contract with the same function in contractfactory. Plus, it has the function biddingContract that allows the firm to send its bidding to the PA, conditional on the fact that its status = "Complete". We add the variable status in order to take into account sending incomplete biddings, with missing documents. Indeed, before launching the bidding, the modifier onlyCompleted is run. 

**OPEN ISSUES**
. understand the hash 
. how to retrieve contract's info, e.g. status, tenderId, etc, if we hash its content
. write the modifier
. security check

(2) the PA part: not considered here
