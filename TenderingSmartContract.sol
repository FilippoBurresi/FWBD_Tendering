pragma solidity ^0.6.6;
pragma experimental ABIEncoderV2;

contract TenderingSmartContract {

    struct BiddingOffer {
        address contractor;
        bytes32 hashOffer;
        uint256 bidId;
        string description;
        bool valid;
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
        address tenderingInstitution;
        address winningContractor;
    }

    mapping (uint => Tender) public tenders;
    uint[] public tenderList; // list of tender keys so we can enumarate them
    uint public tenderKeys = 0;

    mapping (address => bool) public allowedInstitution;

    // this is a turnaround to use push on a memory variable
    address[] private _contractors;
    string[] private _descriptions;



    modifier onlyAllowed{
        allowedInstitution[msg.sender] == true;
        _;
    }

    function CreateTender(string memory _tenderName, string memory _description, uint256 _bidOpeningDate,uint256 _bidSubmissionClosingDateHash,
    uint256 _bidSubmissionClosingDateData) public onlyAllowed {

        tenders[tenderKeys].tenderName = _tenderName;
        tenders[tenderKeys].description = _description;
        tenders[tenderKeys].bidOpeningDate = _bidOpeningDate;
        tenders[tenderKeys].bidSubmissionClosingDateHash = _bidSubmissionClosingDateHash;
        tenders[tenderKeys].bidSubmissionClosingDateData = _bidSubmissionClosingDateData;

        tenderKeys ++;

            }

    // this function allowed contractors to participate the tender by sumbitting the hash
    function placeBid (uint256 _tenderKey, bytes32 _hashOffer) public {

        uint bidKey = tenders[_tenderKey].bidList.length;
        tenders[_tenderKey].bidList.push(bidKey);
        tenders[_tenderKey].bids[bidKey].contractor = msg.sender;
        tenders[_tenderKey].bids[bidKey].hashOffer = _hashOffer;

    }

    // after the deadline contractors can send the actual offer
    function concludeBid(uint256 _tenderKey, uint32 _bidkey, string memory _description) public {
        //assert that the deadline is respected
        assert(tenders[_tenderKey].bidSubmissionClosingDateData > now);
        //assert that the it is the bids of the contractor that it is trying to conclude the Bid
        assert(tenders[_tenderKey].bids[_bidkey].contractor == msg.sender);
        // check that the hash correspond
        assert (keccak256(abi.encodePacked(_description)) == tenders[_tenderKey].bids[_bidkey].hashOffer);
        // finally conclude the bid by submitting the restriction
        tenders[_tenderKey].bids[_bidkey].description = _description;
        tenders[_tenderKey].bids[_bidkey].valid = true;

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
