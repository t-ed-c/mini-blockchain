from block import Block
import time
import json

class Blockchain:
    def __init__(self, difficulty=2):
        """
        Initialize a new blockchain with genesis block
        :param difficulty: Number of leading zeros required for mining
        """
        self.difficulty = difficulty
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []  # Temporary storage before mining
        
    def create_genesis_block(self):
        """
        Create the first block in the blockchain (genesis block)
        """
        genesis = Block(
            index=0,
            transactions=["Genesis Block"],
            timestamp=time.time(),
            previous_hash="0"
        )
        # Manually set the genesis hash (no mining needed)
        genesis.hash = genesis.calculate_hash()
        return genesis
    
    def add_transaction(self, transaction):
        """
        Add a new transaction to be included in next block
        """
        self.pending_transactions.append(transaction)
        return self.last_block.index + 1  # Next block index
    
    def mine_pending_transactions(self):
        """
        Create a new block with pending transactions and mine it
        """
        if not self.pending_transactions:
            print("⚠️  No transactions to mine!")
            return None
            
        new_block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            timestamp=time.time(),
            previous_hash=self.last_block.hash
        )
        
        # Mine the block with the current difficulty
        new_block.mine_block(self.difficulty)
        
        self.chain.append(new_block)
        self.pending_transactions = []
        return new_block
    
    def add_block_from_peer(self, block_data):
        """
        Add a block received from a peer
        :param block_data: Dictionary with block properties
        """
        new_block = Block(
            index=block_data['index'],
            transactions=block_data['transactions'],
            timestamp=block_data['timestamp'],
            previous_hash=block_data['previous_hash']
        )
        new_block.hash = block_data['hash']
        new_block.nonce = block_data['nonce']
        
        # Validate and add to chain
        if self.is_chain_valid() and self.last_block.hash == new_block.previous_hash:
            self.chain.append(new_block)
            return True
        return False
    
    @property
    def last_block(self):
        """Get the most recent block in the chain"""
        return self.chain[-1]
    
    def to_dict(self):
        """Serialize blockchain to JSON-serializable format"""
        return {
            "difficulty": self.difficulty,
            "chain": [block.__dict__ for block in self.chain],
            "pending_transactions": self.pending_transactions
        }
    
    def save_to_file(self, filename="blockchain.json"):
        """Save blockchain to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load_from_file(cls, filename="blockchain.json"):
        """Load blockchain from JSON file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            # Create new blockchain instance
            bc = cls(difficulty=data.get('difficulty', 2))
            bc.pending_transactions = data.get('pending_transactions', [])
            
            # Reconstruct blocks
            bc.chain = []
            for block_data in data['chain']:
                block = Block(
                    index=block_data['index'],
                    transactions=block_data['transactions'],
                    timestamp=block_data['timestamp'],
                    previous_hash=block_data['previous_hash']
                )
                block.nonce = block_data['nonce']
                block.hash = block_data['hash']
                bc.chain.append(block)
            
            return bc
        except FileNotFoundError:
            # Return new blockchain if file doesn't exist
            return cls()
    
    def __repr__(self):
        return f"Blockchain<blocks={len(self.chain)}, pending_tx={len(self.pending_transactions)}, difficulty={self.difficulty}>"

    def is_chain_valid(self):
        """
        Verify the integrity of the entire blockchain
        Returns True if valid, False otherwise
        """
        # Check genesis block
        genesis = self.chain[0]
        if genesis.index != 0:
            print("❗ Invalid genesis block index")
            return False
        if genesis.previous_hash != "0":
            print("❗ Genesis block has invalid previous hash")
            return False
        if genesis.hash != genesis.calculate_hash():
            print("❗ Genesis block hash invalid")
            return False
        
        # Check subsequent blocks
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            # Validate block linkage
            if current.previous_hash != previous.hash:
                print(f"❌ Block {i}: Broken link to previous block")
                return False
                
            # Validate current block's hash
            if current.hash != current.calculate_hash():
                print(f"❌ Block {i}: Corrupted block data")
                return False
                
            # Validate index sequence
            if current.index != i:
                print(f"❌ Block {i}: Invalid index {current.index}")
                return False
                
        return True
    
    def tamper_test(self):
        """
        Demonstrate blockchain tamper detection
        """
        print("\n=== Running Tamper Test ===")
        
        # Add some transactions and mine a block
        self.add_transaction("Test transaction 1")
        self.add_transaction("Test transaction 2")
        self.mine_pending_transactions()
        
        print("Initial chain valid:", self.is_chain_valid())
        
        # Tamper with data in the new block
        tampered_block = self.chain[-1]
        print(f"\nTampering with block {tampered_block.index}...")
        original_transactions = tampered_block.transactions.copy()
        tampered_block.transactions = ["HACKED: Malicious transaction"]
        
        # Validation should fail
        print("After tampering, chain valid:", self.is_chain_valid())
        
        # Restore original data
        tampered_block.transactions = original_transactions
        print("\nRestored original data")
        print("Chain valid after restoration:", self.is_chain_valid())
    
    def adjust_difficulty(self, new_difficulty):
        """
        Adjust the mining difficulty
        :param new_difficulty: New number of leading zeros required
        """
        self.difficulty = new_difficulty
        print(f"🔧 Difficulty adjusted to {new_difficulty}")

# Test the blockchain with mining
if __name__ == "__main__":
    bc = Blockchain(difficulty=2)
    
    # Add and mine some transactions
    bc.add_transaction("Alice pays Bob 1 BTC")
    bc.mine_pending_transactions()
    
    bc.add_transaction("Bob pays Charlie 0.5 BTC")
    bc.add_transaction("Charlie pays Dave 0.2 BTC")
    bc.mine_pending_transactions()
    
    print("=== Initial Blockchain ===")
    print(f"Chain length: {len(bc.chain)} blocks")
    print("Chain valid:", bc.is_chain_valid())
    
    # Run the tamper demonstration
    bc.tamper_test()
    
    # Test difficulty adjustment
    bc.adjust_difficulty(3)
    bc.add_transaction("Dave pays Eve 0.1 BTC")
    bc.mine_pending_transactions()
    print(f"New block mined with difficulty {bc.difficulty}")