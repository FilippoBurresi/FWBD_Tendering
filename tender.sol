pragma solidity >=0.5.0 <0.6.0;
import "./PA.sol";

contract Tender is PA {
        // here we define the strucure of the tender 
    struct Tender {
        address owner_contract;
        string tenderName; 
        string tenderId;
        uint256 bidSubmissionClosingDate;
        uint256 bidOpeningDate;
        string description;
        uint[] requirements; 
        // F: why tendering data ? better manage it in another contract 
    }
    
    // we then create an array that will contain all the tender
    Tender[] public activeTender;
    uint256 public numActiveTender = 0;
    
    mapping (string => uint) quant_requirements;
    mapping (string => string) descr_requirements;
        
    //run the function every time you need a new requirements (GAS implications)
    function addQuantRequirements(string _name, uint _data) public onlyAllowedAddress {
        quant_requirements[_name] = _data;
    }
    function addDescrRequirements(string _name, string _req) public onlyAlloweeAddress {
        descr_requirements[_name] = _req;
        
    }
    
    // this function create a Tender and add it to activeTender
    function createTender(
    address _owner, string _tenderName,  uint256 _bidSubmissionClosingDate,
    uint256 _bidOpeningDate, string _description
    ) public onlyAllowedAddress {
        activeTender.push(_ownerofcontracts, _tenderName, _bidSubmissionClosingDate, _bidOpeningDate, _description, quant_requirements);
    }
    
    
    // return: send the contract on the blockchain and communcates it ---- why already done before 
    
    function view_tenders(address _ownerofcontracts, string _tenderName, uint numActiveTender, string _bidSubmissionClosingDate, string _bidOpeningDate, string description) public onlyAllowedAddress {
        numActiveTender ++;
        newTender = Tender(_ownerofcontracts, _tenderName, numActiveTender, _bidSubmissionClosingDate, _bidOpeningDate, description);
        activeTender.push(newTender);
    }
}