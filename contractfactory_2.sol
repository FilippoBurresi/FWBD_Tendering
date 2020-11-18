pragma solidity >=0.5.0 <0.6.0;

import "./tendering.sol"; // the smart contract of the PA


/// @title A contract to create a bidding contract
/// @notice For now, this code will simply tells us the basic feature of a bidding contract and its creation
contract ContractFactory {
    
    event NewContract(uint contract_id, address _governementAddress, uint _tenderId); // what will be published to all nodes when a contract is created
    
    uint constraint //?? to limit the times the firm can send a bid
    
    // defining state variables and structs that are going to be stored permanently on the blockchain
    // to reduce gas costs, we should keep all parameters of the same type near to each other
   struct  Contract {
        address _contractorAddress;
        address _governementAddress; //?? how to retrive its public key
        uint _tenderId; // number that uniquely identifies the tendering in question
        uint _bidAmount; // final price offered by the firm
        string _taskDescription // contain a more comprehensive description than the _bidAmount about timing, quantities etc offered by the firm 
        string _attacchments; // it can contain urls to external documents, e.g. accounting sheets
        string status; // it can be either 'pending' or 'complete'
    }
    
    Contract[] public contracts; //dynamic array of contracts => think how to hash the content of the contracts! 
    
    mapping (uint => address) public contractToOwner; // it is what will be published at the end 
    
    // to be written 
    modifier onlyApproved {
        // require the bidding firm to be registered inside the approved firm to deal with PA
        _;
    }
    
    // to be written 
    modifier inTime {
        // require the bidding to be pushed within the deadline 
        _;
    }
    
    // creating a pending contract and signaling it to all the nodes in the blockchain
    function createContract(address _contractorAddress, address _governementAddress, uint _tenderId, uint _bidAmount, string _taskDescription, string _attacchments) private onlyApproved, inTime {
        require(msg.sender == _contractorAddress); //?? maybe it's already checked with 'private'
        uint contract_id = contracts.push(Contract(_contractorAddress, _governementAddress, _tenderId, _bidAmount, _name, _taskDescription, "pending"));
        contractToOwner[contract_id] = msg.sender;
        emit NewContract(uint contract_id, address _governementAddress, uint _tenderId);
    }
    
    /*
    function addContract(address _contractorAddress, address _governementAddress, uint _tenderId, uint _bidAmount, string _name, string _taskDescription) inTime {
        myContract = createContract(_contractorAddress, _governementAddress, _tenderId, _bidAmount, _name, _taskDescription)
        contracts.push(keccak256(abi.encodePacked(myContract))); // now I am using keccak256 to hash but we should use the private keys of the firms 
    
    } 
    */
    
    // function to be defined to send the keys at the deadline to the PA
}
