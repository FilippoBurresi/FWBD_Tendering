pragma solidity >0.4.13 <0.8.6;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/access/AccessControl.sol";
// import "../.deps/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/access/AccessControl.sol"
 
 /// @title A smart contract for controlling the accessibility 
 /// @notice With the following contract we create two different 'characters':
 /// - the Public Administration: the address which deploys the TenderingSmart Contract will be authomatically granted with the PA role,
 ///   hence it will be able to call all those functions with the onlyPA modifier. It will also be in charge of deciding which firms 
 ///   can partecipate in the tender with the addFirm function, and additionally it could allow any other user to play the PA role.
 ///   Furthermore, it can revoke any permission previously granted either to a firm or another public administration. 
 ///   Note that all those users added as PA or firm can - at any time - renounce the assigned role.
 /// - the firm : an address granted with the firm-role is able to take part in a tender as bidder and, thus, it can call all those 
 ///   functions in the TenderingSmart Contract with the OnlyFirm modifier.
 
contract PA is AccessControl {

    bytes32 public constant FIRM_ROLE = keccak256("FIRM_ROLE");


    // grant ownership to the deployer of the contract

    constructor () public {
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _setRoleAdmin(FIRM_ROLE, DEFAULT_ADMIN_ROLE);
    }

    modifier onlyPA {
        require(hasRole(DEFAULT_ADMIN_ROLE, msg.sender) == true, 'The address has not permission');
        _;
    }

    modifier onlyFirm {
        require(hasRole(FIRM_ROLE, msg.sender) == true, 'The address has not permission');
        _;
    }

    function addPA (address id) public  {
        grantRole(DEFAULT_ADMIN_ROLE, id);
    }

    function revokePA(address id) public {
        revokeRole(DEFAULT_ADMIN_ROLE, id);
    }

    function addFirm (address id) public  {
        grantRole(FIRM_ROLE, id);
    }

    function revokeFirm(address id) public {
        revokeRole(FIRM_ROLE, id);
    }

    function renouncePA(address id) public {
        renounceRole(DEFAULT_ADMIN_ROLE, id);
    }

    function renounceFIRM(address id) public {
        renounceRole(FIRM_ROLE, id);
    }
}
