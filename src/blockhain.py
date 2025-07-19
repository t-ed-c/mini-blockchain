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

# Test the validation
if __name__ == "__main__":
    bc = Blockchain()
    
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