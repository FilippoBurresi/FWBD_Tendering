pragma solidity ^0.4.14;
pragma experimental ABIEncoderV2;

import "splitstring.sol";

contract TenderingSmartContract is ContractString {
    
    
    address owner;
    mapping (address => bool) public allowedInstitution;


    struct BiddingOffer {
        address contractor;
        bytes32 hashOffer;
        string description;
        bool valid;
        string separator;
        string[] NewDescription;
        //mapping each bid id to its final description (the original splitted description)
        //if we had description = '12####1283####è bello####'
        //now we will have [12,1283,è bello] 
    }

    struct Tender {
        uint256 tender_id;
        string tenderName;
        string description;
        uint256 bidOpeningDate;
        uint256 bidSubmissionClosingDateData;
        uint256 bidSubmissionClosingDateHash;
        address[] bidList; // array where to store the index of all the bid
        mapping(address => BiddingOffer) bids;
        address tenderingInstitution;
        address winningContractor;
        
    }
    
    mapping (uint => Tender) public tenders;
    uint[] public tenderList; //list of tender keys so we can enumarate them
    uint public tenderKeys = 0;


    // this is a turnaround to use push on a memory variable
    address[] private _contractors;
    string[] private _descriptions;
    
    constructor()  public {
    owner = msg.sender;
    allowedInstitution[msg.sender] = true;
     }
     
    event message(string message, address sender);
    
    
    // parte Filo
     
     modifier isOwner{
        require(msg.sender == owner);
        _;
     }
    
    modifier onlyAllowed{
        require(allowedInstitution[msg.sender] == true);
        _;
    }
    
    function CreatePA(address _addressPA) public isOwner{
        allowedInstitution[_addressPA] = true;
    }
    
    // fine 

    
    function CreateTender(string memory _tenderName, string memory _description,uint256 _daysUntilClosingDateData, uint256 _daysUntilClosingDateHash) public  isOwner{
        Tender storage c = tenders[tenderKeys];
        c.tender_id = tenderKeys;
        c.tenderName = _tenderName;
        c.description = _description;
        c.bidOpeningDate = now;
        c.bidSubmissionClosingDateHash= now + (_daysUntilClosingDateHash* 1 days);
        c.bidSubmissionClosingDateData = now + (_daysUntilClosingDateData * 1 days);
        c.tenderingInstitution= msg.sender;
        c.bidList= new address[](0);
        emit message("Tender Deployed", msg.sender);

        tenderKeys ++;

            }
      
    modifier inTimeHash (uint256 _tenderKey) {
        require(
        (now >= tenders[_tenderKey].bidOpeningDate) && (now <= tenders[_tenderKey].bidSubmissionClosingDateHash),
        "The hashed bid has to be placed after the bid opening date and before the hash closing date."
        );
        _;
    }        

    // this function allowed contractors to participate the tender by sumbitting the hash
    function placeBid (uint256 _tenderKey, bytes32 _hashOffer) public inTimeHash(_tenderKey) {
        Tender storage c = tenders[_tenderKey];
        c.bids[msg.sender] = BiddingOffer(msg.sender,_hashOffer,"",false,"", new string[](0));
        c.bidList.push(msg.sender);
    }
    
    //The following function returns the bid_id of a certain address.
    //this bid_id has to be put in the concludeBid function when called from Python
    //in Python send_unencrypted_solidity(web3,contract,tender_id,user_id,unencrypted_message,separator) will become:
    //web3.eth.defaultAccount=web3.eth.accounts[int(user_id)]
    //bid_id = contract.functions.returningBidIdAddress(tender_id).call()
    //contract.functions.concludeBid(tender_id,bid_id,unencrypted_message,separator)
    
   

    
    modifier inTimeData (uint256 _tenderKey) {
        require(
        (now >= tenders[_tenderKey].bidSubmissionClosingDateHash) && (now < tenders[_tenderKey].bidSubmissionClosingDateData),
        "The data has to be sent after the hash closing date and before the data closing date."
        );
        _;
    } 

    // after the deadline contractors can send the actual offer
    function concludeBid(uint256 _tenderKey, string memory _description, string memory _separator) public inTimeData(_tenderKey) {
    
        
        //assert(tenders[_tenderKey].bidSubmissionClosingDateData > now); // I have commented this line because the modifier inTimeData checks for this
        
        //assert that the it is the bids of the contractor that it is trying to conclude the Bid
        assert(tenders[_tenderKey].bids[msg.sender].contractor == msg.sender);
        // check that the hash correspond
        assert (keccak256(abi.encodePacked(_description)) == tenders[_tenderKey].bids[msg.sender].hashOffer);
        // finally conclude the bid by submitting the restriction
        tenders[_tenderKey].bids[msg.sender].description = _description;
        //memorizing the separator used in each bid
        tenders[_tenderKey].bids[msg.sender].separator = _separator;
        tenders[_tenderKey].bids[msg.sender].valid = true;

    }
    
    //with this function each bid_id is assigned to a list of the elements presented in the original string-offer
    
    function SplitDescription(uint256 _tenderKey) public onlyAllowed {
        for (uint i=0; i<tenders[_tenderKey].bidList.length; i++){
             string memory separatorToUse  = tenders[_tenderKey].bids[tenders[_tenderKey].bidList[i]].separator;
            //UPDATE DESCRIPTION
            string memory descriptionAtTheMoment = tenders[_tenderKey].bids[tenders[_tenderKey].bidList[i]].description;
            tenders[_tenderKey].bids[tenders[_tenderKey].bidList[i]].NewDescription = SMT(descriptionAtTheMoment,separatorToUse);
        }
    }
    

    // after the deadline for submitting the actual offer the tendering organization can see all offer and assigned the
    // ! I didn't managed to declare this as a view function... 
    // the function cannot be declared as view if push is used
    function getBidsByKey(uint256 _tenderId) public returns (address[] memory, string[] memory) {


        for (uint i=0; i<tenders[_tenderId].bidList.length; i++){

            if (tenders[_tenderId].bids[tenders[_tenderId].bidList[i]].valid == true){
               _contractors.push(tenders[_tenderId].bids[tenders[_tenderId].bidList[i]].contractor);
               _descriptions.push(tenders[_tenderId].bids[tenders[_tenderId].bidList[i]].description);
            }

        }

        return (_contractors, _descriptions);

    }

    function assignWinningContractor(uint256 _tenderId, address _bidId) public {

        // assert that only the "owner" of the bid can assign the winner
        assert(tenders[_tenderId].tenderingInstitution == msg.sender);

        BiddingOffer memory winningBid = tenders[_tenderId].bids[_bidId];

        // only the contractor that had a valid bid can win
        if (winningBid.valid == true){

            tenders[_tenderId].winningContractor = winningBid.contractor;
        }

    }
    
    function see_tender(uint _tenderId) public returns (uint  tender_id, string memory tenderName,string memory description,
    uint256 bidOpeningDate,uint256 bidSubmissionClosingDateData,address[] memory bidList, BiddingOffer memory){
        BiddingOffer memory to_store= tenders[_tenderId].bids[tenders[_tenderId].bidList[0]];
        return (tenders[_tenderId].tender_id,tenders[_tenderId].tenderName,tenders[_tenderId].description,
        tenders[_tenderId].bidOpeningDate,tenders[_tenderId].bidSubmissionClosingDateData,tenders[_tenderId].bidList,to_store);
    }


}

