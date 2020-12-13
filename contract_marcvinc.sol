pragma solidity >0.4.13 <0.7.0;
pragma experimental ABIEncoderV2;

import "./strings.sol";
import "./SafeMath.sol";
import "./PA.sol";

contract TenderingSmartContract is PA {

    using SafeMath for uint;
    using strings for *;

    address owner;
    // a Public Administration can publish a tender only if authorized
    mapping (address => bool) public allowedInstitution; 

    struct BiddingOffer {
        address contractor; // bidder address
        bytes32 hashOffer; // hash of the offer sent
        bool valid; // a bid becomes valid what the actual offer is verified to coincide with the hash sent 
        string description; //each bid has to indicate the price, time of realization and environment friendliness (expressed with a score that goes from 1 to 4)
        string separator; //each offer is a string where the 3 aforementioned elements are separated by a random separator
        string[] NewDescription; //the offer written without separator: a list of the 3 elements(prince,time,environment)
    }

    struct Tender {
        uint256 tender_id;
        uint256 bidOpeningDate; // date from which hashes can be sent
        uint256 bidSubmissionClosingDateData; // date by which to sent the unencrypted bid
        uint256 bidSubmissionClosingDateHash; // date by which to sent the hash
        uint[] evaluation_weights; // array of lenght=3 that stores the weights used for evaluation, i.e. weighted average
        mapping(address => BiddingOffer) bids; // from bidding address to its bidding offer
        mapping(address => uint) addressToScore; // from bidding address to its score
        mapping(address => bool) AlreadyBid; // checking each bidder = 1 bid per tender
        address tenderingInstitution;
        address winningContractor; //the winning bidder
        string tenderName; 
        string description; // tender description
    }

    uint[] public tenderList; //list of tender keys so we can enumarate them
    uint public tenderKeys; //lenght of tenderList
    mapping (uint => Tender) public tenders; //from tender_id to the tender characteristics

    // needed for the evaluation part
    mapping(uint => address[]) private _participants; // from tender id => list of participants
    mapping(uint => uint[])  private _scores; // from tender id => list of scores

    mapping(uint => address) tenderIdToWinner; // from tenderId => address of the winner

    /**
     * a modifier to check that an encrypted bid is sent between the bid opening date and the first 
     * deadline, i.e. the date by which to sent the hash of an offer.
     */
    modifier inTimeHash (uint256 _tenderKey) {
        require(
        (now >= tenders[_tenderKey].bidOpeningDate) && (now <= tenders[_tenderKey].bidSubmissionClosingDateHash),
        "hash sent before the opening date or after the hash closing date!"
        );
        _;
    }
    
    /**
     * a modifier to ensure that each bidder can partecipate into a speficic tender 
     * only once.
     */
    modifier AlreadyPlacedBid(uint256 _tenderKey) {
        require(
            (tenders[_tenderKey].AlreadyBid[msg.sender] != true),
        "Bid already placed for this tender!"
        );
        _;
    }

    /**
     * a modifier to check that each unencrypted bid is sent after the first 
     * deadline and before the second one.
     */
    modifier inTimeData (uint256 _tenderKey) {
        require(
        (now >= tenders[_tenderKey].bidSubmissionClosingDateHash) && (now < tenders[_tenderKey].bidSubmissionClosingDateData),
        "data sent before the hash closing date or after the data closing date."
        );
        _;
    }
    
    /**
    * a modifier to check that the date by which to send the unencrypted offer
    * has alredy passed.
    */ 
    modifier afterDeadline (uint256 _tenderKey) {
        require(tenders[_tenderKey].bidSubmissionClosingDateData < now);
        _;
    }

    /**
     * @notice CreateTender function can only be called by an authorized PA to create a new tender
     * @param _daysUntilClosingDateHash _daysUntilClosingDateData indicate the days between 
     * the bid opening date and the first and second deadlines. 
     * For simplicity, we are going to express them as seconds.
     * @param w1, w2, w3 are the weights - to be assigned to price, time, environment -
     * that will be used to evaluate the scores.
     * Requirements:
     * - the sum of the weights has to = 100
     * - _daysUntilClosingDateData has to be greater than _daysUntilClosingDateHash
     */ 
    function CreateTender(string memory _tenderName, string memory _description,uint256 _daysUntilClosingDateData, uint256 _daysUntilClosingDateHash,
                            uint w1, uint w2, uint w3) public onlyPA{
        uint sum = w1.add(w2.add(w3));
        require(sum == 100, 'sum must be 100');
        require(_daysUntilClosingDateData > _daysUntilClosingDateHash);
        // the value of tenderKeys specifies the id the created tender
        Tender storage c = tenders[tenderKeys];
        c.tender_id = tenderKeys;
        c.tenderName = _tenderName;
        c.description = _description;
        // the parameters of the function are used to set the characteristics of the tender
        c.bidOpeningDate = now;
        c.bidSubmissionClosingDateHash= now + (_daysUntilClosingDateHash* 1 seconds);
        c.bidSubmissionClosingDateData = now + (_daysUntilClosingDateData* 1 seconds);
        c.tenderingInstitution = msg.sender;
        // the chosen weights are memorized 
        c.evaluation_weights.push(w1);
        c.evaluation_weights.push(w2);
        c.evaluation_weights.push(w3);
        // tenderKeys keeps memory of how many tenders have been created so far
        tenderKeys ++;

            }

    /**
     * @notice placeBid can only be called by an authorized firm to place a bid.
     * This function has to be called before the first hash deadline.
     * @param _tenderKey is the id of the tender for which placing a bid
     * @param _hashOffer is the encrypted offer
     */ 
    function placeBid (uint256 _tenderKey, bytes32 _hashOffer) public onlyFirm inTimeHash(_tenderKey) AlreadyPlacedBid(_tenderKey) {
        Tender storage c = tenders[_tenderKey];
        
        /* once a firm has placed a bid for a specific tender, 
        it cannot partecipate into that tender anymore */
        c.AlreadyBid[msg.sender] = true; 
        // a new offer is created. All the elements a BiddingOffer type is made of are inserted 
        c.bids[msg.sender] = BiddingOffer(msg.sender,_hashOffer,false,"","", new string[](0));
        _participants[_tenderKey].push(msg.sender);
    }


    /**
     * @notice concludeBid can only be called by an authorized firm to conclude a bid,
     * by sending the unencrypted offer before the second (data) deadline.
     * @param _tenderKey is the id of the tender the bid refers to.
     * @param _description is a string containing the price, the realization time and the environment score.
     * @param _separator indicates the separator that arises between these three elements.
     * 
     * Requirements:
     * - the firm concluding the Bid has to match the firm that has placed that Bid 
     * - The hash sent at the beginning has to match the hash of the unencrypted bid.
     */ 
    function concludeBid(uint256 _tenderKey, string memory _description, string memory _separator) public onlyFirm inTimeData(_tenderKey) {

        /* assert that the contractor who is trying to conclude the Bid
        is the one who has placed the bid in the first palce */
        require(tenders[_tenderKey].bids[msg.sender].contractor == msg.sender);
        // check that the hash corresponds
        require(keccak256(abi.encodePacked(_description)) == tenders[_tenderKey].bids[msg.sender].hashOffer);
        // finally conclude the bid by submitting the description
        tenders[_tenderKey].bids[msg.sender].description = _description;
        //memorizing the separator used in each bid
        tenders[_tenderKey].bids[msg.sender].separator = _separator;
        tenders[_tenderKey].bids[msg.sender].valid = true;

    }
    
    
    /**
     * @notice this function is based on the String & slice utility library.
     * It performs the splitting of a string according to a specified separator
     * @return the list of strings obtained after the splitting
     */
    function SMT(string memory _phrase,string memory _separator ) private returns(string[] memory) {
        strings.slice memory s = _phrase.toSlice();
        strings.slice memory delim = _separator.toSlice();
        string[] memory parts = new string[](s.count(delim));
        for (uint i = 0; i < parts.length; i++) {
           parts[i] = s.split(delim).toString();
        }

        return (parts);
    }
    
    /**
     * @notice this function converts a string to an integer type
     * @return _ret : the initial parameter parsed as uint
     */
    function parseInt(string memory _value) public returns (uint _ret) {
        bytes memory _bytesValue = bytes(_value);
        uint j = 1;
        for(uint i = _bytesValue.length-1; i >= 0 && i < _bytesValue.length; i--) {
            assert(uint8(_bytesValue[i]) >= 48 && uint8(_bytesValue[i]) <= 57);
            _ret += (uint8(_bytesValue[i]) - 48)*j;
            j*=10;
        }
    }
    
    /**
     * @notice this function is called by the PA after the tender is closed to 
     * split each bidding offer.
     * The starting point is an offer presented as a string of type price////time////environment_score////.
     * Each string offer is then splitted and 
     * converted into a list made of the three separated elements: [price,time,environment_score]
     * This step is necessary to then evaluate all the offers and compute the scores.
     */
    function splitDescription(uint256 _tenderKey) private onlyPA afterDeadline(_tenderKey) {
        for (uint i=0; i < _participants[_tenderKey].length; i++){
            // looking at the sepator used in each string offer
             string memory separatorToUse  = tenders[_tenderKey].bids[_participants[_tenderKey][i]].separator;
            // update the description
            string memory descriptionAtTheMoment = tenders[_tenderKey].bids[_participants[_tenderKey][i]].description;
            tenders[_tenderKey].bids[_participants[_tenderKey][i]].NewDescription = SMT(descriptionAtTheMoment,separatorToUse);
        }
    }
    
    /** @notice this function makes some changes on the measures the three elements characterizing
     * each offer are expressed with.
     * This is necessary for the computations of the weighted averages (i.e. the scores).
     * The reason lies on the fact that the price is probably expressed on the scale of thousands,
     * while the time on that of tens/hundreds and the environment score is just a number between 
     * 1 and 4 (where 1 = highest attention to the environment).
     * Without any arrangment, a small change in the price will always predominate even in the case 
     * of a very small weight assigned to this variable.
     * Therefore, adjusting the measures is fundamental to make things fair and to 
     * make each variable as important as the related weight requires.
     * @param _thingToLook is the variable of reference 
     * @param _thingToAdjust is the variable whose scale of size needs to be changed
     * according to which rescaling the other variable (in our case the price)
     * 
     */
    function adjust_measures(uint _thingToLook, uint _thingToAdjust) private returns(uint) {

        uint n_times;
        uint _thingNew = _thingToLook;
        while (_thingNew / (10) != 0) {
            _thingNew = _thingNew / 10;
            n_times ++;
        }
        return ( _thingToAdjust.mul(10 ** n_times));
    }

    /**
     * @notice compute_scores function is called by the PA after the tender is closed to evaluate 
     * all the offers.
     * In the evaluation phase the weights chosen at the beginning are used 
     * and before computing the weighted averages, the adjust_measures function is called
     * in order to make the time and the environment_score comparable with the price
     */
    function compute_scores(uint _tenderKey) public onlyPA afterDeadline(_tenderKey) {
        // weight associated to price
        uint w1 = tenders[_tenderKey].evaluation_weights[0]; 
        // weight associated to timing
        uint w2 = tenders[_tenderKey].evaluation_weights[1]; 
        /* weight associated to environmental safeguard level, 
        i.e. four categories: 1 [highest] to 4 [lowest] */
        uint w3 = tenders[_tenderKey].evaluation_weights[2]; 
        
        splitDescription(_tenderKey);

        for (uint i = 0; i < _participants[_tenderKey].length; i++){
            address  target_address = _participants[_tenderKey][i];
            BiddingOffer  memory to_store= tenders[_tenderKey].bids[target_address];
            if (to_store.valid == true){

                //to make timing and envir comparable with price
                uint price = parseInt(to_store.NewDescription[0]);
                uint timing = adjust_measures(price, parseInt(to_store.NewDescription[1]));
                // e.g. if price=10000 and env=2 then envir_adj = 20000
                uint environment = adjust_measures(price, parseInt(to_store.NewDescription[2])); 
                uint score = w1.mul(price);
                score = score.add(w2.mul(timing));
                score = score.add(w3.mul(environment));
    
               //_participants[_tenderKey].push(to_store.contractor);
               // all the scores are saved in the _scores mapping
               _scores[_tenderKey].push(score);
               // each bidder address is assigned to its own score
               tenders[_tenderKey].addressToScore[to_store.contractor] = score;
            }
        }
    }

    /**
     * @notice assign_winner function is called by the PA after the tender is closed to compare
     * the scores previously computed and to decree the winner,
     * i.e. the bidder with the lowest score .
     * In case of the same score between two bidders, 
     * the firm which sent the bidding first is preferred.
     */
    function assign_winner(uint _tenderKey) public onlyPA afterDeadline(_tenderKey) {
        uint winning_score = _scores[_tenderKey][0];
        uint winning_index;

        for (uint i = 1; i < _participants[_tenderKey].length; i++){
            uint score = _scores[_tenderKey][i];

            if (score < winning_score){ 
                winning_score = score;
                winning_index = i;
            }
        }
        tenders[_tenderKey].winningContractor = _participants[_tenderKey][winning_index];
        tenderIdToWinner[_tenderKey] = _participants[_tenderKey][winning_index];
        //emit Winner_display("We have a winner!", _tenderKey, _participants[_tenderKey][winning_index], winning_score);
        //return (_participants[_tenderKey][winning_index], winning_score);
    }
    
    /**
     * @notice displayWinner function can be called by any citizen after the tender is closed.
     * @return the address of the winner and its score.
     */
    function displayWinner(uint _tenderKey) public afterDeadline(_tenderKey) returns (address, uint) {
        return (tenderIdToWinner[_tenderKey], tenders[_tenderKey].addressToScore[tenderIdToWinner[_tenderKey]]);
        /*
        Alternatively, we can simply return tenders[_tenderKey].winningContractor
        Check which option consumes less gas. And, if tenders[_tenderKey].winningContractor consumes less,
        we must eliminate the mapping tenderIdToWinner at the beginning of the smart contract
        */
    }

    /**
     * @notice getResultsLenght function can be called after the tender is closed.
     * @return the number of participants to a specific tender.
     */
    function getResultsLenght(uint _tenderKey) public view afterDeadline(_tenderKey) returns(uint) {
        return _participants[_tenderKey].length;
    }
    
    /**
     * @notice getResultsValue function can be called after the tender is closed.
     * @param _index speficies the bidder id we are interested in.
     * @return the address of the contractor, its score and wheter it has won the tender or not.
     */
    function getResultsValue(uint _tenderKey, uint _index) public view afterDeadline(_tenderKey) returns (address,uint, bool) {

        bool is_winner;
        if (tenders[_tenderKey].winningContractor == _participants[_tenderKey][_index]) {
            is_winner = true;
        } else {
            is_winner = false;
        }

        return (_participants[_tenderKey][_index], _scores[_tenderKey][_index], is_winner);
    }

    /**
     * @notice getBidDetails function can be called by any citizen after the tender is closed.
     * @param _index speficies the bidder id we are interested in.
     * @return the name of the firm contractor, its offer ([price, time, envir]),
     * the sepator used in presenting the string offer initially, the reached score and 
     * whether it has won the tender or not.
     */
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

    /**
     * @notice this function returns the total number of created tenders
     * @return tenderKeys
     */
    function getTendersLength() public returns(uint) {
        return (tenderKeys);
    }
    
    /**
     * @notice this function allows to visualize the status of a speficix tender.
     * A tender is pending if the first deadline has already passed
     * (meaning that new hashed offers cannot be accepted anymore)
     * @return the tender_id we are interested in and its pending status.
     */
    function isPending(uint _tenderKey) public returns(uint, bool) {

        bool pending_status;

        if (tenders[_tenderKey].bidSubmissionClosingDateHash > now) {
            pending_status = true;
        } else {
            pending_status = false;
        }
        return (_tenderKey, pending_status);
    }
    
    /**
     * @notice this function allows to visualize some information related to a specific tender.
     * It returns the id of the tender we are interested in, its name, its description, 
     * the weights chosen to evaluate the offers with, the participants addresses
     * and the final winner.
     */
    function see_TenderDetails(uint _tenderKey) public returns (uint  tender_id, string memory tenderName,string memory description,
                                uint[] memory evaluation_weights, address[] memory firms, address winningContractor){

        return (tenders[_tenderKey].tender_id, tenders[_tenderKey].tenderName, tenders[_tenderKey].description, tenders[_tenderKey].evaluation_weights, _participants[_tenderKey], tenders[_tenderKey].winningContractor);

        /*
        Now, this function returns the list of all the contractors that sent a bid.
        Check if it is better for gas costs returning only the length of bidList instead of all the addresses.
        */
    }

}
