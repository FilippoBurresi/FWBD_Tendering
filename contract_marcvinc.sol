pragma solidity >0.4.13 <0.7.0;
pragma experimental ABIEncoderV2;

import "./strings.sol";
import "./SafeMath.sol";
import "./PA.sol";

contract TenderingSmartContract is PA {

    using SafeMath for uint;
    using strings for *;

    address owner;
    mapping (address => bool) public allowedInstitution;

    struct BiddingOffer {
        address contractor;
        bytes32 hashOffer;
        bool valid;
        string description;
        string separator;
        string[] NewDescription;
    }

    struct Tender {
        uint256 tender_id;
        uint256 bidOpeningDate;
        uint256 bidSubmissionClosingDateData;
        uint256 bidSubmissionClosingDateHash;
        uint[] evaluation_weights; // array of lenght=3 that stores the weights used for evaluation, i.e. weighted average
        //address[] bidList; // array where to store all the addresses that are bidding
        mapping(address => BiddingOffer) bids; // from bidding address to its bidding offer
        mapping(address => uint) addressToScore; // NEW! from bidding address to its score
        //checking each bidder = 1 bid per tender
        mapping(address => bool) AlreadyBid;
        address tenderingInstitution;
        address winningContractor;
        string tenderName;
        string description;
    }

    uint[] public tenderList; //list of tender keys so we can enumarate them
    uint public tenderKeys;
    mapping (uint => Tender) public tenders;

    // needed for the evaluation part
    mapping(uint => address[]) private _participants; //from tenderKey => list of participants
    mapping(uint => uint[])  private _scores; //from tenderKey => list of scores

    // added this for the displayWinner function below. See there for more details
    mapping(uint => address) tenderIdToWinner; // from tenderId => address of the winner

    modifier inTimeHash (uint256 _tenderKey) {
        require(
        (now >= tenders[_tenderKey].bidOpeningDate) && (now <= tenders[_tenderKey].bidSubmissionClosingDateHash),
        "hash sent before the opening date or after the hash closing date!"
        );
        _;
    }

    modifier AlreadyPlacedBid(uint256 _tenderKey) {
        require(
            (tenders[_tenderKey].AlreadyBid[msg.sender] != true),
        "Bid already placed for this tender!"
        );
        _;
    }

    modifier inTimeData (uint256 _tenderKey) {
        require(
        (now >= tenders[_tenderKey].bidSubmissionClosingDateHash) && (now < tenders[_tenderKey].bidSubmissionClosingDateData),
        "data sent before the hash closing date or after the data closing date."
        );
        _;
    }

    modifier afterDeadline (uint256 _tenderKey) {
        require(tenders[_tenderKey].bidSubmissionClosingDateData < now);
        _;
    }

    function CreateTender(string memory _tenderName, string memory _description,uint256 _daysUntilClosingDateData, uint256 _daysUntilClosingDateHash,
                            uint w1, uint w2, uint w3) public onlyPA{
        uint sum = w1.add(w2.add(w3));
        require(sum == 100, 'sum must be 100');
        require(_daysUntilClosingDateData > _daysUntilClosingDateHash);

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
        tenderKeys ++;

            }

    // this function allowed contractors to participate the tender by sumbitting the hash
    function placeBid (uint256 _tenderKey, bytes32 _hashOffer) public onlyFirm inTimeHash(_tenderKey) AlreadyPlacedBid(_tenderKey) {
        Tender storage c = tenders[_tenderKey];
        c.AlreadyBid[msg.sender] = true;
        c.bids[msg.sender] = BiddingOffer(msg.sender,_hashOffer,false,"","", new string[](0));
        //c.bidList.push(msg.sender);
        _participants[_tenderKey].push(msg.sender);
    }

    // after the deadline contractors can send the actual offer
    function concludeBid(uint256 _tenderKey, string memory _description, string memory _separator) public onlyFirm inTimeData(_tenderKey) {

        //assert that the it is the bids of the contractor that it is trying to conclude the Bid
        require(tenders[_tenderKey].bids[msg.sender].contractor == msg.sender);
        // check that the hash correspond
        require(keccak256(abi.encodePacked(_description)) == tenders[_tenderKey].bids[msg.sender].hashOffer);
        // finally conclude the bid by submitting the description
        tenders[_tenderKey].bids[msg.sender].description = _description;
        //memorizing the separator used in each bid
        tenders[_tenderKey].bids[msg.sender].separator = _separator;
        tenders[_tenderKey].bids[msg.sender].valid = true;

    }

    function SMT(string memory _phrase,string memory _separator ) private returns(string[] memory) {
        strings.slice memory s = _phrase.toSlice();
        strings.slice memory delim = _separator.toSlice();
        string[] memory parts = new string[](s.count(delim));
        for (uint i = 0; i < parts.length; i++) {
           parts[i] = s.split(delim).toString();
        }

        return (parts);
    }

    function parseInt(string memory _value)
        public
        returns (uint _ret) {
        bytes memory _bytesValue = bytes(_value);
        uint j = 1;
        for(uint i = _bytesValue.length-1; i >= 0 && i < _bytesValue.length; i--) {
            assert(uint8(_bytesValue[i]) >= 48 && uint8(_bytesValue[i]) <= 57);
            _ret += (uint8(_bytesValue[i]) - 48)*j;
            j*=10;
        }
    }

    //with this function each bid_id is assigned to a list of the elements presented in the original string-offer
    function splitDescription(uint256 _tenderKey) private onlyPA afterDeadline(_tenderKey) {
        for (uint i=0; i < _participants[_tenderKey].length; i++){
             string memory separatorToUse  = tenders[_tenderKey].bids[_participants[_tenderKey][i]].separator;
            //UPDATE DESCRIPTION
            string memory descriptionAtTheMoment = tenders[_tenderKey].bids[_participants[_tenderKey][i]].description;
            tenders[_tenderKey].bids[_participants[_tenderKey][i]].NewDescription = SMT(descriptionAtTheMoment,separatorToUse);
        }
    }

    function adjust_measures(uint _thingToLook, uint _thingToAdjust) private returns(uint) {

        uint n_times;
        uint _thingNew = _thingToLook;
        while (_thingNew / (10) != 0) {
            _thingNew = _thingNew / 10;
            n_times ++;
        }
        return ( _thingToAdjust.mul(10 ** n_times));
    }

    function compute_scores(uint _tenderKey) public onlyPA afterDeadline(_tenderKey) {
        uint w1 = tenders[_tenderKey].evaluation_weights[0]; // weight associated to price
        uint w2 = tenders[_tenderKey].evaluation_weights[1]; // weight associated to timing
        uint w3 = tenders[_tenderKey].evaluation_weights[2]; // weight associated to environmental safeguard level, i.e. four categories: 1 [highest] to 4 [lowest]

        splitDescription(_tenderKey);

        for (uint i = 0; i < _participants[_tenderKey].length; i++){
            address  target_address = _participants[_tenderKey][i];
            BiddingOffer  memory to_store= tenders[_tenderKey].bids[target_address];
            if (to_store.valid == true){

                //to make timing and envir comparable with price
                uint price = parseInt(to_store.NewDescription[0]);
                uint timing = adjust_measures(price, parseInt(to_store.NewDescription[1]));
                uint environment = adjust_measures(price, parseInt(to_store.NewDescription[2])); // e.g. if price=10000 and env=2 then envir_adj = 20000

                uint score = w1.mul(price);
                score = score.add(w2.mul(timing));
                score = score.add(w3.mul(environment));

               //_participants[_tenderKey].push(to_store.contractor);
               _scores[_tenderKey].push(score);
               tenders[_tenderKey].addressToScore[to_store.contractor] = score;
            }
        }
    }

    function assign_winner(uint _tenderKey) public onlyPA afterDeadline(_tenderKey) {
        uint winning_score = _scores[_tenderKey][0];
        uint winning_index;

        for (uint i = 1; i < _participants[_tenderKey].length; i++){
            uint score = _scores[_tenderKey][i];

            if (score < winning_score){ //given the same score, the firm which sent the bidding first is preferred
                winning_score = score;
                winning_index = i;
            }
        }
        tenders[_tenderKey].winningContractor = _participants[_tenderKey][winning_index];
        tenderIdToWinner[_tenderKey] = _participants[_tenderKey][winning_index];
        //emit Winner_display("We have a winner!", _tenderKey, _participants[_tenderKey][winning_index], winning_score);
        //return (_participants[_tenderKey][winning_index], winning_score);
    }

    function displayWinner(uint _tenderKey) public afterDeadline(_tenderKey) returns (address, uint) {
        return (tenderIdToWinner[_tenderKey], tenders[_tenderKey].addressToScore[tenderIdToWinner[_tenderKey]]);
        /*
        Alternatively, we can simply return tenders[_tenderKey].winningContractor
        Check which option consumes less gas. And, if tenders[_tenderKey].winningContractor consumes less,
        we must eliminate the mapping tenderIdToWinner at the beginning of the smart contract
        */
    }

    function getResultsLenght(uint _tenderKey) public view afterDeadline(_tenderKey) returns(uint) {
        return _participants[_tenderKey].length;
    }

    function getResultsValue(uint _tenderKey, uint _index) public view afterDeadline(_tenderKey) returns (address,uint, bool) {

        bool is_winner;
        if (tenders[_tenderKey].winningContractor == _participants[_tenderKey][_index]) {
            is_winner = true;
        } else {
            is_winner = false;
        }

        return (_participants[_tenderKey][_index], _scores[_tenderKey][_index], is_winner);
    }

    function getBidDetails(uint _tenderKey, address _index) public view afterDeadline(_tenderKey) returns (address, string[] memory, string memory, uint, bool) {
        address name_contractor = tenders[_tenderKey].bids[_index].contractor;
        string[] memory text_description = tenders[_tenderKey].bids[_index].NewDescription;
        string memory sep = tenders[_tenderKey].bids[_index].separator; // thus, one can check if the score was correct by using the separator and the description

        bool is_winner;
        if (tenders[_tenderKey].winningContractor == _index) {
            is_winner = true;
        } else {
            is_winner = false;
        }

        // the index is an address so I needed to create this mapping inside Tender to retrieve the score by the given address
        uint score = tenders[_tenderKey].addressToScore[_index];

        return (name_contractor, text_description, sep, score, is_winner);
    }

    function getTendersLength() public returns(uint) {
        return (tenderKeys);
    }

    function isPending(uint _tenderKey) public returns(uint, bool) {

        bool pending_status;

        if (tenders[_tenderKey].bidSubmissionClosingDateHash > now) {
            pending_status = true;
        } else {
            pending_status = false;
        }
        return (_tenderKey, pending_status);
    }

    function see_TenderDetails(uint _tenderKey) public returns (uint  tender_id, string memory tenderName,string memory description,
                                uint[] memory evaluation_weights, address[] memory firms, address winningContractor){

        return (tenders[_tenderKey].tender_id, tenders[_tenderKey].tenderName, tenders[_tenderKey].description, tenders[_tenderKey].evaluation_weights, _participants[_tenderKey], tenders[_tenderKey].winningContractor);

        /*
        Now, this function returns the list of all the contractors that sent a bid.
        Check if it is better for gas costs returning only the length of bidList instead of all the addresses.
        */
    }

}
