# Import library
import hashlib
from collections import deque
from typing import List
from uuid import uuid4

class Transaction:
    def __init__(self, sender: str, receiver: str, amount: float):
    # start a transaction with sender,reciever and amount
        self.id = str(uuid4()) #unique identifier for transaction
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def calculate_hash(self) -> str:
    # Calculate the hash of transaction data
        transaction_data = f'{self.id}{self.sender}{self.receiver}{self.amount}'
        return hashlib.sha256(transaction_data.encode()).hexdigest()

    def is_valid(self) -> bool:
    # All transactions are valid for simplicity
        return True

class Block:
    def __init__(self, previous_hash: str, transactions: List[Transaction]):
    # Start a block with previous hash, current transactions, and timestamps
        self.previous_hash = previous_hash
        self.timestamp = datetime.datetime.now() # record the creation time
        self.transactions = transactions
        self.nonce = 0 # start noonce for proof of work
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
    #calculate the hash of the block data
        block_data = f'{self.previous_hash}{self.timestamp}{[tx.calculate_hash() for tx in self.transactions]}{self.nonce}'
        return hashlib.sha256(block_data.encode()).hexdigest()

    def mine_block(self, difficulty: int):
    # Preform proof of work to mine the block
        target = '0' * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
# start the block chain with genisis, diffeculty and mining reward
    def __init__(self, difficulty: int = 4, reward: float = 50.0):
        self.chain = deque([self.create_genesis_block()]) # Start with genesis block
        self.difficulty = difficulty
        self.reward = reward
        self.pending_transactions = deque() # Transactions waiting to be mined

    def create_genesis_block(self) -> Block:
    # create the first block in the blockchain
        return Block(previous_hash="0", transactions=[])

    def get_latest_block(self) -> Block:
    # Get the most recent block in the blockchain
        return self.chain[-1]

    def add_transaction(self, transaction: Transaction):
    # add a new transaction to the list of pending transactions
        if transaction.is_valid():
            self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, mining_reward_address: str):
    # Mine all pending transactions and reward the miner
        reward_tx = Transaction(sender="System", receiver=mining_reward_address, amount=self.reward)
        self.pending_transactions.append(reward_tx) # add reward transaction
        new_block = Block(previous_hash=self.get_latest_block().hash, transactions=list(self.pending_transactions))
        new_block.mine_block(self.difficulty) # Preform proof of work
        self.chain.append(new_block) # Add mined block to the block chain
        self.pending_transactions.clear() # Clear pending transactions
