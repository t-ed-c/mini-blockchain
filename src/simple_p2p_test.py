"""
Simple P2P Network Test
Run this script to test peer-to-peer networking

Usage:
    Terminal 1: python simple_p2p_test.py 5000
    Terminal 2: python simple_p2p_test.py 5001 --connect 5000
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from blockchain import Blockchain
from p2p_network import Node
import time
import argparse

def main():
    parser = argparse.ArgumentParser(description='Simple P2P Test')
    parser.add_argument('port', type=int, help='Port to run node on')
    parser.add_argument('--connect', type=int, help='Port of peer to connect to')
    
    args = parser.parse_args()
    
    print(f"🚀 Starting blockchain node on port {args.port}")
    
    # Create blockchain and node
    bc = Blockchain.load_from_file()
    node = Node('127.0.0.1', args.port, bc)
    
    # Start the node
    node.start()
    print(f"✅ Node running at 127.0.0.1:{args.port}")
    
    # Connect to peer if specified
    if args.connect:
        print(f"⏳ Attempting to connect to peer on port {args.connect}...")
        time.sleep(1)  # Give the node a moment to start
        
        if node.connect_to_peer('127.0.0.1', args.connect):
            print(f"🔗 Successfully connected to peer on port {args.connect}")
        else:
            print(f"❌ Failed to connect to peer on port {args.connect}")
    
    print("\n=== Commands ===")
    print("add <msg>     - Add transaction")
    print("mine          - Mine pending transactions")
    print("view          - View blockchain")
    print("peers         - Show connected peers")
    print("status        - Show node status")
    print("quit          - Exit")
    print()
    
    try:
        while True:
            cmd = input(f"Node-{args.port}> ").strip().split()
            if not cmd:
                continue
                
            if cmd[0] == 'quit':
                break
            elif cmd[0] == 'add' and len(cmd) > 1:
                transaction = ' '.join(cmd[1:])
                bc.add_transaction(transaction)
                bc.save_to_file()
                print(f"✅ Added transaction: {transaction}")
                
            elif cmd[0] == 'mine':
                if not bc.pending_transactions:
                    print("⚠️  No pending transactions to mine")
                    continue
                    
                start_time = time.time()
                block = bc.mine_pending_transactions()
                if block:
                    bc.save_to_file()
                    mining_time = time.time() - start_time
                    print(f"⛏️  Mined block {block.index} in {mining_time:.2f}s")
                    print(f"   Hash: {block.hash}")
                    
                    # Broadcast to all connected peers
                    if node.peers:
                        print(f"📡 Broadcasting block to {len(node.peers)} peers...")
                        node.broadcast_block(block)
                    else:
                        print("📡 No peers to broadcast to")
                        
            elif cmd[0] == 'view':
                print(f"\n🔗 Blockchain (length: {len(bc.chain)})")
                print(f"⏳ Pending transactions: {len(bc.pending_transactions)}")
                
                for i, block in enumerate(bc.chain):
                    print(f"\nBlock {i}:")
                    print(f"  Hash: {block.hash[:16]}...")
                    print(f"  Transactions: {len(block.transactions)}")
                    if i > 0:  # Skip genesis block details
                        for j, tx in enumerate(block.transactions):
                            print(f"    TX{j}: {tx}")
                            
            elif cmd[0] == 'peers':
                if node.peers:
                    print(f"Connected peers: {list(node.peers)}")
                else:
                    print("No connected peers")
                    
            elif cmd[0] == 'status':
                print(f"Node: 127.0.0.1:{args.port}")
                print(f"Peers: {len(node.peers)}")
                print(f"Blockchain length: {len(bc.chain)}")
                print(f"Pending transactions: {len(bc.pending_transactions)}")
                
            else:
                print("Unknown command")
                
    except KeyboardInterrupt:
        pass
    except EOFError:
        pass
    finally:
        print("\n🛑 Stopping node...")
        node.stop()
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()
