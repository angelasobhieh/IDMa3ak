// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract IdentityVerification {
    struct User {
        string name;
        bool isRegistered;
    }

    struct AccessRequest {
        address requester;
        address approver;
        uint256 timestamp;
        bool isApproved;
    }

    mapping(address => User) public users;
    AccessRequest[] public accessRequests;

    function registerUser(string memory _name) public {
        require(!users[msg.sender].isRegistered, "User already registered");
        users[msg.sender] = User(_name, true);
    }

    function requestAccess(address approver) public {
        require(users[msg.sender].isRegistered, "User not registered");
        require(users[approver].isRegistered, "Approver not registered");
        accessRequests.push(AccessRequest(msg.sender, approver, block.timestamp, false));
    }

    function approveAccess(uint256 requestIndex) public {
        AccessRequest storage request = accessRequests[requestIndex];
        require(request.approver == msg.sender, "Not authorized");
        require(!request.isApproved, "Already approved");
        require(block.timestamp - request.timestamp < 1 hours, "Request expired");
        request.isApproved = true;
    }
}
