import hashlib
import time
import json

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        """
        Initialize a new block
        
        :param index: Position in the blockchain (0 for genesis)
        :param transactions: List of transactions in this block
        :param timestamp: Creation time of block
        :param previous_hash: Hash of the previous block in chain
        """
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0  # Will be used for mining later
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """
        Calculate SHA-256 hash of the block's contents
        
        Includes: index, transactions, timestamp, previous_hash, and nonce
        """
        block_string = json.dumps({
            "index": self.index,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        
        return hashlib.sha256(block_string).hexdigest()
    
    def __repr__(self):
        """User-friendly block representation"""
        return (
            f"Block(index={self.index}, hash={self.hash[:8]}..., "
            f"prev_hash={self.previous_hash[:8]}..., "
            f"transactions={len(self.transactions)}, nonce={self.nonce})"
        )

# Test execution when run directly
if __name__ == "__main__":
    # Create genesis block
    genesis = Block(
        index=0,
        transactions=["Genesis transaction"],
        timestamp=time.time(),
        previous_hash="0"  # Hardcoded for genesis block
    )
    
    # Create second block
    block2 = Block(
        index=1,
        transactions=["Alice pays Bob 5 BTC", "Bob pays Charlie 3 BTC"],
        timestamp=time.time(),
        previous_hash=genesis.hash
    )
    
    print("=== Block Chain Demo ===")
    print(f"Genesis Block: {genesis}")
    print(f"Block 2: {block2}")
    print("\nBlock Details:")
    print(f"Genesis hash: {genesis.hash}")
    print(f"Block 2 previous hash: {block2.previous_hash}")
    print(f"Link valid: {block2.previous_hash == genesis.hash}")