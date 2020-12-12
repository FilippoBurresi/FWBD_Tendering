pragma solidity >0.4.13 <0.7.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/access/AccessControl.sol";

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
