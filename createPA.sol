pragma solidity >=0.5.0 <0.6.0;

import "./PA.sol";

contract createPA is PA {
    
    function create_remove_NewPA(address _uniqueID, string _name, string _competence, bool _remove) public OnlyOwner {
        if(_remove == True){
            delete PA[_uniqueID];
            allowedAddress[msg.sender] == false;
            return _; 
        }
        organisations[_uniqueID].name = _name;
        organisations[_uniqueID].competence = _competence;
        organisations[_uniqueID].addedBy = msg.sender;
        addAllowedAddress(_uniqueID);
    }
    // this function that can be called only by the owner of the contract, in this case the public administration 
    function _addAllowedAddress (address _newAddress) public OnlyOwner {
        allowedAddress[msg.sender] == True;
    }
    
}   
    