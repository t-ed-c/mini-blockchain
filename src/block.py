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
        self.nonce = 0  # Mining counter
        self.hash = None  # Will be set during mining
    
    def calculate_hash(self):
        """
        Calculate SHA-256 hash of the block's contents
        """
        block_string = json.dumps({
            "index": self.index,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        
        return hashlib.sha256(block_string).hexdigest()
    
    def mine_block(self, difficulty):
        """
        Perform proof-of-work mining
        """
        print(f"⛏️  Mining block {self.index} with difficulty {difficulty}...")
        prefix = "0" * difficulty
        start_time = time.time()
        
        while True:
            self.hash = self.calculate_hash()
            if self.hash.startswith(prefix):
                break
            self.nonce += 1
        
        mining_time = time.time() - start_time
        print(f"✅ Block mined! Hash: {self.hash}")
        print(f"🔢 Nonce: {self.nonce} | ⏱️  Time: {mining_time:.2f}s")
        return self
    
    def __repr__(self):
        """User-friendly block representation"""
        short_hash = self.hash[:8] + "..." if self.hash else "None"
        return (
            f"Block(index={self.index}, hash={short_hash}, "
            f"prev_hash={self.previous_hash[:8]}..., "
            f"transactions={len(self.transactions)}, nonce={self.nonce})"
        )

# Test execution when run directly
if __name__ == "__main__":
    # Create a block with difficulty 2
    test_block = Block(
        index=1,
        transactions=["Test TX1", "Test TX2"],
        timestamp=time.time(),
        previous_hash="00000000abc"
    )
    
    print("Mining test block with difficulty 2...")
    test_block.mine_block(2)
    print(f"Mined block: {test_block}")