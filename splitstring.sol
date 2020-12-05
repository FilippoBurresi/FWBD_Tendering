pragma experimental ABIEncoderV2;

import "github.com/Arachnid/solidity-stringutils/strings.sol";

contract ContractString {                                                            
    using strings for *;                                                       

    function SMT(string _phrase,string _separator ) public returns(string[] memory) {                                               
        strings.slice memory s = _phrase.toSlice();                
        strings.slice memory delim = _separator.toSlice();                            
        string[] memory parts = new string[](s.count(delim));                  
        for (uint i = 0; i < parts.length; i++) {                              
           parts[i] = s.split(delim).toString();                               
        }
        
        return (parts);
    }                                                                          
  

}