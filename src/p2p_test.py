#!/usr/bin/env python3
"""
Simple P2P network test script
Run this in two terminals to test networking
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from blockchain import Blockchain
from p2p_network import Node
import time
import threading

def run_node(port, peer_port=None):
    """Run a node and optionally connect to a peer"""
    print(f"🚀 Starting node on port {port}")
    
    # Create blockchain and node
    bc = Blockchain.load_from_file()
    node = Node('127.0.0.1', port, bc)
    
    # Start the node
    node.start()
    
    # Connect to peer if specified
    if peer_port:
        print(f"⏳ Waiting 2 seconds before connecting to peer...")
        time.sleep(2)
        if node.connect_to_peer('127.0.0.1', peer_port):
            print(f"✅ Successfully connected to peer on port {peer_port}")
        else:
            print(f"❌ Failed to connect to peer on port {peer_port}")
    
    print(f"✅ Node running on port {port}")
    print("Commands:")
    print("  'status' - Show node status")
    print("  'peers'  - Show connected peers") 
    print("  'mine'   - Mine a test transaction")
    print("  'quit'   - Stop node")
    print()
    
    # Interactive commands
    try:
        while True:
            cmd = input(f"Node-{port}> ").strip().lower()
            
            if cmd == 'quit':
                break
            elif cmd == 'status':
                print(f"Node: 127.0.0.1:{port}")
                print(f"Peers: {len(node.peers)}")
                print(f"Blockchain length: {len(bc.chain)}")
            elif cmd == 'peers':
                print(f"Connected peers: {list(node.peers)}")
            elif cmd == 'mine':
                bc.add_transaction(f"Test tx from node {port} at {time.time()}")
                block = bc.mine_pending_transactions()
                if block:
                    print(f"⛏️  Mined block {block.index}")
                    # Broadcast to peers
                    node.broadcast_block(block)
            else:
                print("Unknown command")
                
    except KeyboardInterrupt:
        pass
    finally:
        node.stop()
        print("👋 Node stopped")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python p2p_test.py <port>           # Start node")
        print("  python p2p_test.py <port> <peer>    # Start node and connect to peer")
        print()
        print("Example:")
        print("  Terminal 1: python p2p_test.py 5000")
        print("  Terminal 2: python p2p_test.py 5001 5000")
        sys.exit(1)
    
    port = int(sys.argv[1])
    peer_port = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    run_node(port, peer_port)
