// SPDX-License-Identifier: Rafi

pragma solidity ^0.7.0;

contract Overflow {

    function overflow() public view returns(uint8){
        uint8 big = 255 + uint8(1);
        return big;
    }
}