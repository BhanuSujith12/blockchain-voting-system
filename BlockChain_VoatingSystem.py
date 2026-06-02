#BLOCKCHAIN VOTING SYSTEM 

import hashlib
import json
import os
# NEW
from datetime import datetime, timedelta, timezone


# BLOCK CLASS

class Block:

    #each block stores one vote and link to before one
    def __init__(self, index, vote_data, previous_hash,
                 timestamp=None, nonce=0):

        self.index = index
        self.timestamp = timestamp or str(datetime.now(timezone.utc))    #Time at which the block was created
        self.vote_data = vote_data                              #Stores vote information
        self.previous_hash = previous_hash                      #Stores previous hash 
        self.nonce = nonce                                      #Noncce
        self.hash = self.compute_hash()

    #Generates hash of a block 
    #-------------------------

    def compute_hash(self):

        block_string = json.dumps(
            {
                "index": self.index,
                "timestamp": self.timestamp,
                "vote_data": self.vote_data,
                "previous_hash": self.previous_hash,
                "nonce": self.nonce
            },
            sort_keys=True
        )

        return hashlib.sha256(
            block_string.encode()
        ).hexdigest()
    
    #Converts block object to dictionary format
    #------------------------------------------

    def to_dict(self):

        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "vote_data": self.vote_data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }

    @classmethod

    #Converts dictionary to block object format
    #------------------------------------------

    def from_dict(cls, data):

        block = cls(
            data["index"],
            data["vote_data"],
            data["previous_hash"],
            data["timestamp"],
            data["nonce"]
        )

        block.hash = data["hash"]

        return block
    


# BLOCKCHAIN CLASS

class Blockchain:

    #Determines how hard the proof of work is 
    #----------------------------------------

    def __init__(self, difficulty=2):

        self.difficulty = difficulty

        self.registered_voters = {
            "VOTER101",
            "VOTER102",
            "VOTER103",
            "VOTER104",
            "VOTER105"
        }

        self.candidates = {
            "Alice",
            "Bob",
            "Charlie"
        }

        # Voting deadline (24 hours from start)
        self.deadline = datetime.now(timezone.utc) + timedelta(days=1)

        self.chain = []

        self.create_genesis_block()

    # 2.Blockchain class
    #-------------------

    #Creates block of blockchain
    #---------------------------

    def create_genesis_block(self):

        genesis_block = Block(
            0,
            {
                "voter_id": "GENESIS",
                "candidate": "NONE"
            },
            "0"
        )

        self.proof_of_work(genesis_block)

        self.chain.append(genesis_block)

        print("Genesis Block Created")

    #Proof of work
    # ------------

    def proof_of_work(self, block):

        target = "0" * self.difficulty

        while not block.hash.startswith(target):
            block.nonce += 1
            block.hash = block.compute_hash()

    #Validating vote (According to Rules)
    # -----------------------------

    def validate_vote(self, voter_id, candidate):

        if datetime.now(timezone.utc) > self.deadline:
            return False, "Voting deadline has passed."

        if voter_id not in self.registered_voters:
            return False, "Voter is not registered."

        if candidate not in self.candidates:
            return False, "Invalid candidate."

        # Duplicate vote check
        for block in self.chain:

            if block.vote_data.get("voter_id") == voter_id:
                return False, "Voter has already voted."

        return True, "Vote accepted."

    #Adds new vote to blockchain
    #---------------------------

    def add_vote(self, voter_id, candidate):

        valid, message = self.validate_vote(
            voter_id,
            candidate
        )

        if not valid:
            print(message)
            return

        #Creates vote information in the block
        vote_data = {
            "voter_id": voter_id,
            "candidate": candidate
        }

        previous_hash = self.chain[-1].hash         #Assignment of new block 

        #Passing to new block
        new_block = Block(
            len(self.chain),
            vote_data,
            previous_hash
        )

        self.proof_of_work(new_block)

        self.chain.append(new_block)

        print("Vote recorded successfully.")

    #Checks whether blockchain is valid or not
    #-----------------------------------------

    def is_valid(self):

        seen_voters = set()

        for i in range(1, len(self.chain)):

            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.compute_hash():
                return False

            if current.previous_hash != previous.hash:
                return False

            voter = current.vote_data["voter_id"]

            if voter in seen_voters:
                return False

            seen_voters.add(voter)

        return True

    #Counts the number of votes received by each candidate
    # ----------------------------------------------------

    def count_votes(self):

        votes = {
            candidate: 0
            for candidate in self.candidates
        }

        for block in self.chain[1:]:

            candidate = block.vote_data["candidate"]

            votes[candidate] += 1

        return votes

    #Declaring the winner according to the votes 
    # ------------------------------------------

    def declare_winner(self):

        votes = self.count_votes()

        max_votes = max(votes.values())

        winners = [
            candidate
            for candidate, count in votes.items()
            if count == max_votes
        ]

        print("\nElection Result")

        if len(winners) == 1:
            print(
                f"Winner: {winners[0]} "
                f"({max_votes} votes)"
            )
        else:
            print(
                f"Tie between: "
                f"{', '.join(winners)}"
            )

    #Display all the blocks in the chain
    # ----------------------------------

    def display_chain(self):

        print("\n========== BLOCKCHAIN ==========\n")

        for block in self.chain:

            print(f"Block #{block.index}")
            print(f"Timestamp : {block.timestamp}")
            print(f"Vote Data : {block.vote_data}")
            print(f"Prev Hash : {block.previous_hash}")
            print(f"Hash      : {block.hash}")
            print(f"Nonce     : {block.nonce}")
            print("-" * 60)

    #Prints the given info
    # --------------------

    def blockchain_stats(self):

        print("\nBlockchain Statistics")

        print(
            f"Total Blocks : {len(self.chain)}"
        )

        print(
            f"Votes Cast   : {len(self.chain)-1}"
        )

        print(
            f"Difficulty   : {self.difficulty}"
        )

    #Stores the blockchain in JSON file
    # ---------------------------------

    def save_chain(
        self,
        filename="blockchain.json"
    ):

        data = {
            "difficulty": self.difficulty,
            "deadline": self.deadline.isoformat(),
            "chain": [
                block.to_dict()
                for block in self.chain
            ]
        }

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

        print("Blockchain saved.")

    @classmethod

    def load_chain(
        cls,
        filename="blockchain.json"
    ):

        if not os.path.exists(filename):
            print("File not found.")
            return None

        with open(filename, "r") as file:
            data = json.load(file)

        blockchain = cls(
            difficulty=data["difficulty"]
        )

        blockchain.deadline = datetime.fromisoformat(
            data["deadline"]
        )

        blockchain.chain = [
            Block.from_dict(block)
            for block in data["chain"]
        ]

        return blockchain

    #Tampering Detection 
    # ------------------

    def demonstrate_tampering(self):

        if len(self.chain) < 2:
            print("Not enough blocks.")
            return

        print("\nTampering Block #1...")

        self.chain[1].vote_data[
            "candidate"
        ] = "Bob"

        if self.is_valid():
            print("Chain Valid")
        else:
            print("Tampering Detected!")



# CLI

def menu():

    blockchain = Blockchain()

    while True:

        #Simple user interface

        print("\n========== MENU ==========")
        print("1. Register Vote")
        print("2. View Blockchain")
        print("3. Count Votes")
        print("4. Check Chain Validity")
        print("5. Declare Winner")
        print("6. Blockchain Statistics")
        print("7. Demonstrate Tampering")
        print("8. Save Blockchain")
        print("9. Load Blockchain")
        print("10. Exit")

        choice = input("\nEnter Choice: ")

        if choice == "1":

            voter_id = input(
                "Enter Voter ID: "
            ).strip().upper()

            candidate = input(
                "Enter Candidate: "
            ).strip().capitalize()

            blockchain.add_vote(
                voter_id,
                candidate
            )

        elif choice == "2":
            blockchain.display_chain()

        elif choice == "3":

            votes = blockchain.count_votes()

            print()

            for candidate, count in votes.items():
                print(
                    f"{candidate}: {count} votes"
                )

        elif choice == "4":

            if blockchain.is_valid():
                print("Blockchain is Valid")
            else:
                print("Blockchain is Corrupted")

        elif choice == "5":
            blockchain.declare_winner()

        elif choice == "6":
            blockchain.blockchain_stats()

        elif choice == "7":
            blockchain.demonstrate_tampering()

        elif choice == "8":
            blockchain.save_chain()

        elif choice == "9":

            loaded = Blockchain.load_chain()

            if loaded:
                blockchain = loaded
                print("Blockchain Loaded")

        elif choice == "10":
            print("Goodbye!")
            break

        else:
            print("Invalid Choice")


#Entry point of the program
#--------------------------

if __name__ == "__main__":
    menu()
