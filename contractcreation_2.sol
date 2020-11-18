pragma solidity >=0.5.0 <0.6.0;


/// @title A contract that bidding firms use to send their biddings
/// @notice For now, the contract allows firms to send their created biddings, and later we have to add the sending of the keys to the PA
contract ContractBidding is ContractFactory {
    
    event NewCompletedContract(uint contract_id, address _governement_Address, uint _tender_Id);
    
    /* idea: associate a status to the contract which stands for Pending or Complete: 
        - as soon as I create the contract, myContract will have status = Pending
        - I can only push myContract when its status is Complete
        
    The status should reflect that all info are correctly uploaded (to avoid to push incorrect biddings) 
    
    */
    
    Contract[] public completed_contracts;
    
    // to be written
    modifier onlyCompleted {
        // require bids with all the docs
        _;
    }
    
    // can be used only if the contract has already been created => should we check for this ?
    function biddingContract(uint contract_id) onlyCompleted, inTime {
        require(msg.sender == contractToOwner[contract_id]);
        
        contracts[contract_id].status = "complete"; //?? if we hash all the contents in Contract, how can we retrieve after the hash the status, tenderId, etc..
        
        completed_contracts.push(contracts[contract_id]);
        emit NewCompletedContract(uint contract_id, address contracts[contract_id]._governement_Address, uint contracts[contract_id]._tender_Id);
    }
    
    // function to be defined to send the keys at the deadline to the PA
    
}