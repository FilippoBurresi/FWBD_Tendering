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
    }

    struct Tender {
        uint256 tender_id;
        string tenderName;
        string description;
        uint256 bidOpeningDate;
        uint256 bidSubmissionClosingDateData;
        uint256 bidSubmissionClosingDateHash;
        uint[] evaluation_weights; // array of lenght=3 that stores the weights used for evaluation, i.e. weighted average
        address[] bidList; // array where to store all the addresses that are bidding
        mapping(address => BiddingOffer) bids; // from bidding address to its bidding offer
        address tenderingInstitution;
        address winningContractor;
    }
    
    mapping (uint => Tender) public tenders;
    uint[] public tenderList; //list of tender keys so we can enumarate them
    uint public tenderKeys = 0;

    // needed for the evaluation part
    mapping(uint => address[]) private _participants; //from tenderKey => list of participants
    mapping(uint => uint[])  private _scores; //from tenderKey => list of scores
    
    
    // added this for the displayWinner function below. See there for more details
    mapping(uint => address) tenderIdToWinner; // from tenderId => address of the winner
    
    
    
    constructor()  public {
    owner = msg.sender;
    allowedInstitution[msg.sender] = true;
     }
     
    event message(string message, address sender);
    event Winner_display(string, uint, address, uint); //title, tender_key, winner address, its score
    
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
    
    function CreateTender(string memory _tenderName, string memory _description,uint256 _daysUntilClosingDateData, uint256 _daysUntilClosingDateHash, 
                            uint w1, uint w2, uint w3) public  isOwner{
        Tender storage c = tenders[tenderKeys];
        c.tender_id = tenderKeys;
        c.tenderName = _tenderName;
        c.description = _description;
        c.bidOpeningDate = now;
        c.bidSubmissionClosingDateHash= now + (_daysUntilClosingDateHash* 1 days);
        c.bidSubmissionClosingDateData = now + (_daysUntilClosingDateData * 1 days);
        c.tenderingInstitution = msg.sender;
        c.evaluation_weights.push(w1);
        c.evaluation_weights.push(w2);
        c.evaluation_weights.push(w3);
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
        
        //assert that the it is the bids of the contractor that it is trying to conclude the Bid
        assert(tenders[_tenderKey].bids[msg.sender].contractor == msg.sender);
        // check that the hash correspond
        assert (keccak256(abi.encodePacked(_description)) == tenders[_tenderKey].bids[msg.sender].hashOffer);
        // finally conclude the bid by submitting the description
        tenders[_tenderKey].bids[msg.sender].description = _description;
        //memorizing the separator used in each bid
        tenders[_tenderKey].bids[msg.sender].separator = _separator;
        tenders[_tenderKey].bids[msg.sender].valid = true;

    }
    
    
    modifier afterDeadline (uint256 _tenderKey) {
        assert(tenders[_tenderKey].bidSubmissionClosingDateData < now);
        _;
    } 
    
    //with this function each bid_id is assigned to a list of the elements presented in the original string-offer
    
    function SplitDescription(uint256 _tenderKey) public onlyAllowed afterDeadline(_tenderKey) {
        for (uint i=0; i<tenders[_tenderKey].bidList.length; i++){
             string memory separatorToUse  = tenders[_tenderKey].bids[tenders[_tenderKey].bidList[i]].separator;
            //UPDATE DESCRIPTION
            string memory descriptionAtTheMoment = tenders[_tenderKey].bids[tenders[_tenderKey].bidList[i]].description;
            tenders[_tenderKey].bids[tenders[_tenderKey].bidList[i]].NewDescription = SMT(descriptionAtTheMoment,separatorToUse);
        }
    }
    
    
    function stringToUint(string s) view returns (uint) { 
        bytes memory b = bytes(s);
        uint result = 0;
        for (uint i = 0; i < b.length; i++) { 
            if (b[i] >= 48 && b[i] <= 57) {
                result = result * 10 + (uint(b[i]) - 48); 
            }
        }
        return result;
    }
    
    function compute_scores(uint _tenderKey) onlyAllowed afterDeadline(_tenderKey) {
        uint w1 = tenders[_tenderKey].evaluation_weights[0]; // weight associated to price
        uint w2 = tenders[_tenderKey].evaluation_weights[1]; // weight associated to timing 
        uint w3 = tenders[_tenderKey].evaluation_weights[2]; // weight associated to environmental safeguard level, i.e. four categories: 1 [highest] to 4 [lowest]
        
        for (uint i = 0; i < tenders[_tenderKey].bidList.length; i++){
            address  target_address= tenders[_tenderKey].bidList[i];
            BiddingOffer  memory to_store= tenders[_tenderKey].bids[target_address];
            if (to_store.valid == true){
                
                uint price = stringToUint(to_store.NewDescription[0]);
                uint timing = stringToUint(to_store.NewDescription[1]);
                uint environment = stringToUint(to_store.NewDescription[2]);
                
                uint score = ((w1*price)+(w2*timing)+(w3*environment)); // the lowest score will win the tendering
                
               _participants[_tenderKey].push(to_store.contractor);
               _scores[_tenderKey].push(score);
            }
        }
    }
    
    function assign_winner(uint _tenderKey) onlyAllowed afterDeadline(_tenderKey) returns (address, uint) {
        uint winning_score = _scores[_tenderKey][0];
        uint winning_index = 0;
        
        for (uint i = 1; i < _participants[_tenderKey].length; i++){
            uint score = _scores[_tenderKey][i];
            
            if (score < winning_score){ //given the same score, the firm which sent the bidding first is preferred
                winning_score = score;
                winning_index = i;
            }
        }
        tenders[_tenderKey].winningContractor = _participants[_tenderKey][winning_index];
        tenderIdToWinner[_tenderKey] = _participants[_tenderKey][winning_index];
        emit Winner_display("We have a winner!", _tenderKey, _participants[_tenderKey][winning_index], winning_score);
        return (_participants[_tenderKey][winning_index], winning_score);
    }
    
    function displayWinner(uint _tenderKey) afterDeadline(_tenderKey) returns (address) {
        return tenderIdToWinner[_tenderKey];
        /*
        Alternatively, we can simply return tenders[_tenderKey].winningContractor
        
        Check which option consumes less gas. And, if tenders[_tenderKey].winningContractor consumes less, 
        we must eliminate the mapping tenderIdToWinner at the beginning of the smart contract
        */
    }
    
    function getResultsLenght(uint _tenderKey) public view afterDeadline(_tenderKey) returns(uint) {
        return _participants[_tenderKey].length;
    }
    
    function getResultsValue(uint _tenderKey, uint _index) public view afterDeadline(_tenderKey) returns (address,uint) {
        return (_participants[_tenderKey][_index], _scores[_tenderKey][_index]);
    }

    function getBidDetails(uint _tenderKey, address _index) public view afterDeadline(_tenderKey) returns (address, bytes32, bool, string[]) {
        address name_contractor = tenders[_tenderKey].bids[_index].contractor;
        bytes32 hash_offered = tenders[_tenderKey].bids[_index].hashOffer;
        bool is_valid = tenders[_tenderKey].bids[_index].valid;
        string[] text_description = tenders[_tenderKey].bids[_index].NewDescription;
        return (name_contractor, hash_offered, is_valid, text_description); 
    }
    
    function displayPendingTenders() public returns (string[], uint[], uint[], uint[], uint[], uint[], uint[]) {
        
        string[] names; 
        //string[] info; in see_TenderDetails
        uint[] ids;
        uint[] closingHash;
        uint[] closingData;
        uint[] eval_weight1;
        uint[] eval_weight2;
        uint[] eval_weight3;
        //uint[] num_bids; in see_TenderDetails
        
        for (uint i = 0; i < tenderKeys; i++){
            if (tenders[i].bidSubmissionClosingDateHash > now) {
                names[i] = tenders[i].tenderName;
                //info[i] = tenders[i].description;
                ids[i] = tenders[i].tender_id;
                closingHash[i] = tenders[i].bidSubmissionClosingDateHash;
                closingData[i] = tenders[i].bidSubmissionClosingDateData;
                eval_weight1[i] = tenders[i].evaluation_weights[0];
                eval_weight2[i] = tenders[i].evaluation_weights[1];
                eval_weight3[i] = tenders[i].evaluation_weights[2];
                //num_bids[i] = tenders[i].bidList.length;
            }
        }
        return (names, ids, closingHash, closingData, eval_weight1, eval_weight2, eval_weight3);
    }
    
    function see_TenderDetails(uint _tenderKey) public returns (uint  tender_id, string memory tenderName,string memory description, address[] memory bidList){
        return (tenders[_tenderKey].tender_id, tenders[_tenderKey].tenderName, tenders[_tenderKey].description, tenders[_tenderKey].bidList);
        
        /*
        Now, this function returns the list of all the contractors that sent a bid. 
        Check if it is better for gas costs returning only the length of bidList instead of all the addresses.
        */
    }

}


