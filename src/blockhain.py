from block import Block
import time
import json

class Blockchain:
    def __init__(self):
        """
        Initialize a new blockchain with genesis block
        """
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []  # Temporary storage before mining
        
    def create_genesis_block(self):
        """
        Create the first block in the blockchain (genesis block)
        """
        return Block(
            index=0,
            transactions=["Genesis Block"],
            timestamp=time.time(),
            previous_hash="0"
        )
    
    def add_transaction(self, transaction):
        """
        Add a new transaction to be included in next block
        """
        self.pending_transactions.append(transaction)
        return self.last_block.index + 1  # Next block index
    
    def mine_pending_transactions(self):
        """
        Create a new block with pending transactions
        """
        if not self.pending_transactions:
            print("No transactions to mine!")
            return None
            
        new_block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            timestamp=time.time(),
            previous_hash=self.last_block.hash
        )
        
        self.chain.append(new_block)
        self.pending_transactions = []
        return new_block
    
    @property
    def last_block(self):
        """Get the most recent block in the chain"""
        return self.chain[-1]
    
    def to_dict(self):
        """Serialize blockchain to JSON-serializable format"""
        return {
            "chain": [block.__dict__ for block in self.chain],
            "pending_transactions": self.pending_transactions
        }
    
    def __repr__(self):
        return f"Blockchain<blocks={len(self.chain)}, pending_tx={len(self.pending_transactions)}>"

# Test the blockchain
if __name__ == "__main__":
    # Initialize blockchain
    bc = Blockchain()
    print(f"Created: {bc}")
    print(f"Genesis block: {bc.chain[0]}\n")
    
    # Add some transactions
    bc.add_transaction("Alice pays Bob 5 BTC")
    bc.add_transaction("Bob pays Charlie 3 BTC")
    print(f"Added transactions: {bc.pending_transactions}")
    print(f"Status: {bc}\n")
    
    # Mine a new block
    print("Mining block...")
    new_block = bc.mine_pending_transactions()
    print(f"Mined block: {new_block}")
    print(f"Status: {bc}\n")
    
    # Add more transactions
    bc.add_transaction("Charlie pays Dave 1 BTC")
    bc.add_transaction("Dave pays Alice 0.5 BTC")
    print(f"Added transactions: {bc.pending_transactions}")
    
    # Mine second block
    print("\nMining second block...")
    bc.mine_pending_transactions()
    print(f"Status: {bc}")
    
    # Print full chain
    print("\n=== Full Blockchain ===")
    for i, block in enumerate(bc.chain):
        print(f"Block {i}: {block}")
    
    # Export to JSON
    print("\n=== Blockchain JSON ===")
    print(json.dumps(bc.to_dict(), indent=2))