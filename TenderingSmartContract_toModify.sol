pragma solidity >0.4.0 <0.7.0;
pragma experimental ABIEncoderV2;

import "splitstring.sol";

contract TenderingSmartContract is ContractString {
    
    
    address owner;
    mapping (address => bool) public allowedInstitution;


    struct BiddingOffer {
        address contractor;
        bytes32 hashOffer;
        uint256 bidId;
        string description;
        bool valid;
        string separator;
        //mapping each bid id to its final description (the original splitted description)
        //if we had description = '12####1283####è bello####'
        //now we will have [12,1283,è bello] 
        mapping(uint => string[]) NewDescription;
    }

    struct Tender {

        string tenderName;
        string description;
        uint256 tenderId;
        uint256 bidOpeningDate;
        uint256 bidSubmissionClosingDateHash;
        uint256 bidSubmissionClosingDateData;
        uint[] bidList; // array where to store the index of all the bid
        mapping(uint => BiddingOffer) bids;
        mapping(address => uint) bidIdFromAddress;
        address tenderingInstitution;
        address winningContractor;
        
    }
    
    mapping (uint => Tender) public tenders;
    uint[] public tenderList; // list of tender keys so we can enumarate them
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

    
    function CreateTender(string memory _tenderName, string memory _description, uint256 _daysUntilClosingDateHash,
    uint256 _daysUntilClosingDateData) public  onlyAllowed{
        tenders[tenderKeys].tenderName = _tenderName;
        tenders[tenderKeys].description = _description;
        tenders[tenderKeys].bidOpeningDate = now;
        tenders[tenderKeys].bidSubmissionClosingDateHash = now + (_daysUntilClosingDateHash * 1 days);
        tenders[tenderKeys].bidSubmissionClosingDateData = now + (_daysUntilClosingDateData * 1 days);
        emit message("Tender Depoyed", msg.sender);

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

        uint bidKey = tenders[_tenderKey].bidList.length;
        tenders[_tenderKey].bidList.push(bidKey);
        tenders[_tenderKey].bids[bidKey].contractor = msg.sender;
        tenders[_tenderKey].bids[bidKey].hashOffer = _hashOffer;
        
        //assigning to the address of the contractor its bidkey
        tenders[_tenderKey].bidIdFromAddress[msg.sender] = bidKey;

    }
    
    //The following function returns the bid_id of a certain address.
    //this bid_id has to be put in the concludeBid function when called from Python
    //in Python send_unencrypted_solidity(web3,contract,tender_id,user_id,unencrypted_message,separator) will become:
    //web3.eth.defaultAccount=web3.eth.accounts[int(user_id)]
    //bid_id = contract.functions.returningBidIdAddress(tender_id).call()
    //contract.functions.concludeBid(tender_id,bid_id,unencrypted_message,separator)
    
   
    function returningBidIdAddress (uint256 _tenderKey) public view returns(uint) {
        
        uint bid_id = tenders[_tenderKey].bidIdFromAddress[msg.sender];
        return(bid_id);
    }
    
    
    modifier inTimeData (uint256 _tenderKey) {
        require(
        (now > tenders[_tenderKey].bidSubmissionClosingDateHash) && (now < tenders[_tenderKey].bidSubmissionClosingDateData),
        "The data has to be sent after the hash closing date and before the data closing date."
        );
        _;
    } 

    // after the deadline contractors can send the actual offer
    function concludeBid(uint256 _tenderKey, uint32 _bidkey, string memory _description) public inTimeData(_tenderKey) {
    
        
        //assert(tenders[_tenderKey].bidSubmissionClosingDateData > now); // I have commented this line because the modifier inTimeData checks for this
        
        //assert that the it is the bids of the contractor that it is trying to conclude the Bid
        assert(tenders[_tenderKey].bids[_bidkey].contractor == msg.sender);
        // check that the hash correspond
        assert (keccak256(abi.encodePacked(_description)) == tenders[_tenderKey].bids[_bidkey].hashOffer);
        // finally conclude the bid by submitting the restriction
        tenders[_tenderKey].bids[_bidkey].description = _description;
        //memorizing the separator used in each bid
        tenders[_tenderKey].bids[_bidkey].separator = _separator;
        tenders[_tenderKey].bids[_bidkey].valid = true;

    }
    
    //with this function each bid_id is assigned to a list of the elements presented in the original string-offer
    
    function SplitDescription(uint256 _tenderKey) public onlyAllowed {
        for (uint i = 0; i < tenders[_tenderKey].bidList.length; i++){
             string memory separatorToUse  = tenders[_tenderKey].bids[i].separator;
            //UPDATE DESCRIPTION
            string memory descriptionAtTheMoment = tenders[_tenderKey].bids[i].description;
            tenders[_tenderKey].bids[i].NewDescription[i] = SMT(descriptionAtTheMoment,separatorToUse);
        }
    }
    

    // after the deadline for submitting the actual offer the tendering organization can see all offer and assigned the
    // ! I didn't managed to declare this as a view function... 
    // the function cannot be declared as view if push is used
    function getBidsByKey(uint256 _tenderId) public returns (address[] memory, string[] memory) {


        for (uint i = 0; i < tenders[_tenderId].bidList.length; i++){

            if (tenders[_tenderId].bids[i].valid == true){
               _contractors.push(tenders[_tenderId].bids[i].contractor);
               _descriptions.push(tenders[_tenderId].bids[i].description);
            }

        }

        return (_contractors, _descriptions);

    }

    function assignWinningContractor(uint256 _tenderId, uint256 _bidId) public {

        // assert that only the "owner" of the bid can assign the winner
        assert(tenders[_tenderId].tenderingInstitution == msg.sender);

        BiddingOffer memory winningBid = tenders[_tenderId].bids[_bidId];

        // only the contractor that had a valid bid can win
        if (winningBid.valid == true){

            tenders[_tenderId].winningContractor = winningBid.contractor;
        }

    }


}
