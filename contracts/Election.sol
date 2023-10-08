pragma solidity ^0.8.0;

contract Election{
    mapping ( string => uint) private candidatesVotes;
    string[] candidatesList;
    string electionName;
    bool electionStart;
    bool electionEnd;
    address owner;
    address[] voters;

    constructor(string memory election){
        electionStart = false;
        electionEnd = false;
        electionName = election;
        owner = msg.sender;
    }

    function startElection() external returns(bool){
        if( msg.sender == owner ){
            electionStart = true;
            return true;
        }

        return false;
    }

    function endElection() external returns(bool){
        if( msg.sender == owner ){
            electionEnd = true;
            return true;
        }

        return false;
    }

    function isElectionRunning() view external returns(bool){
        if( electionStart == true && electionEnd == false ){
            return true;
        }

        return false;
    }

    function addCandidate(string memory candidateName) external returns(bool){
        if( electionStart == false && msg.sender == owner ){
            candidatesVotes[candidateName] = 0;
            candidatesList.push(candidateName);

            return true;
        }

        return false;
    }

    function voteCandidate(string memory candidateName) external{
        if( electionStart == true && electionEnd == false ){
            for( uint i = 0; i < voters.length; i++ ){
                if( voters[i] == msg.sender ){
                    return;
                }
            }

            candidatesVotes[candidateName] += 1;
            voters.push(msg.sender);
        }
    }

    function getCandidates() external view returns(string[] memory){
        return candidatesList;
    }

    function getVotes() external view returns(string[] memory, uint[] memory) {
        uint256[] memory votes= new uint256[](candidatesList.length);
        for( uint i = 0; i < candidatesList.length; i++ ){
            votes[i] = candidatesVotes[candidatesList[i]];
        }

        return(candidatesList,votes);
    }

    function getWinner() external view returns(string memory){
        string memory winner = candidatesList[0];
        uint votes = candidatesVotes[winner];

        for( uint i = 1; i < candidatesList.length; i++ ){
            if( votes < candidatesVotes[candidatesList[i]] ){
                votes = candidatesVotes[candidatesList[i]];
                winner = candidatesList[i];
            }
        }

        return winner;
    }

    function getElectionName() external returns(string memory){
        return electionName;
    }

    function hasVoted() external returns(bool){
        for( uint i = 0; i < voters.length; i++ ){
            if( voters[i] == msg.sender ){
                return true;
            }
        }
        
        return false;
    }
}