import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__))) 
import argparse
from blockchain import Blockchain
from p2p_network import Node
import json
import time
import pickle

def save_node_state(node):
    """Save node state to file"""
    if node:
        with open('node_state.pkl', 'wb') as f:
            pickle.dump({
                'host': node.host,
                'port': node.port,
                'is_running': True
            }, f)

def load_node_state(bc):
    """Load node state from file"""
    try:
        with open('node_state.pkl', 'rb') as f:
            state = pickle.load(f)
            if state.get('is_running'):
                node = Node(state['host'], state['port'], bc)
                return node
    except FileNotFoundError:
        pass
    return None

def clear_node_state():
    """Clear node state file"""
    try:
        os.remove('node_state.pkl')
    except FileNotFoundError:
        pass

def main():
    # Load existing blockchain or create new one
    bc = Blockchain.load_from_file()
    node = load_node_state(bc)
    parser = argparse.ArgumentParser(description='Mini Blockchain CLI')
    
    subparsers = parser.add_subparsers(dest='command')
    
    # Add transaction command
    add_parser = subparsers.add_parser('add', help='Add a transaction')
    add_parser.add_argument('transaction', help='Transaction content')
    
    # Mine command
    subparsers.add_parser('mine', help='Mine pending transactions')
    
    # View chain command
    view_parser = subparsers.add_parser('view', help='View blockchain')
    view_parser.add_argument('--full', action='store_true', help='Show full block details')
    
    # Validate command
    subparsers.add_parser('validate', help='Validate blockchain integrity')
    
    # Tamper test command
    subparsers.add_parser('tamper-test', help='Run tamper detection demo')
    
    # Difficulty adjustment
    diff_parser = subparsers.add_parser('difficulty', help='Adjust mining difficulty')
    diff_parser.add_argument('level', type=int, help='New difficulty level (1-5)')
    
    # Network operations
    net_parser = subparsers.add_parser('network', help='Network operations')
    net_sub = net_parser.add_subparsers(dest='net_command')

    # Start node
    start_parser = net_sub.add_parser('start', help='Start node server')
    start_parser.add_argument('--host', default='127.0.0.1', help='Host to bind to')
    start_parser.add_argument('--port', type=int, default=5000, help='Port to listen on')
    start_parser.add_argument('--interactive', action='store_true', help='Keep node running interactively')

    # Connect to peer
    connect_parser = net_sub.add_parser('connect', help='Connect to peer')
    connect_parser.add_argument('peer_host', help='Peer host address')
    connect_parser.add_argument('peer_port', type=int, help='Peer port number')

    # Stop node
    net_sub.add_parser('stop', help='Stop node server')
    
    # Node status
    net_sub.add_parser('status', help='Check node status')
    
    args = parser.parse_args()
    
    if args.command == 'add':
        bc.add_transaction(args.transaction)
        bc.save_to_file()  # Save after adding transaction
        print(f"✅ Transaction added to pending pool (will be in block {len(bc.chain)})")
        
    elif args.command == 'mine':
        start_time = time.time()
        block = bc.mine_pending_transactions()
        if block:
            bc.save_to_file()  # Save after mining
            print(f"⛏️  Mined block {block.index} in {time.time()-start_time:.4f}s")
            print(f"   Hash: {block.hash}")
            
    elif args.command == 'view':
        print(f"\n🔗 Blockchain (length: {len(bc.chain)}, difficulty: {bc.difficulty})")
        print(f"⏳ Pending transactions: {len(bc.pending_transactions)}")
        
        for i, block in enumerate(bc.chain):
            print(f"\nBlock {i}:")
            print(f"  Hash: {block.hash}")
            print(f"  Prev: {block.previous_hash[:16]}...")
            print(f"  Nonce: {block.nonce}")
            print(f"  Timestamp: {time.ctime(block.timestamp)}")
            print(f"  Transactions: {len(block.transactions)}")
            
            if args.full:
                for j, tx in enumerate(block.transactions):
                    print(f"    TX{j}: {tx}")
    
    elif args.command == 'validate':
        valid = bc.is_chain_valid()
        status = "✅ VALID" if valid else "❌ INVALID"
        print(f"\nBlockchain validation: {status}")
        
    elif args.command == 'tamper-test':
        print("\n=== Starting Tamper Test ===")
        bc.tamper_test()
        
    elif args.command == 'difficulty':
        if 1 <= args.level <= 5:
            bc.adjust_difficulty(args.level)
            bc.save_to_file()  # Save after difficulty change
        else:
            print("⚠️  Difficulty must be between 1-5")
    
    elif args.command == 'network':
        if args.net_command == 'start':
            if node:
                print(f"⚠️  Node already running at {node.host}:{node.port}")
            else:
                node = Node(args.host, args.port, bc)
                node.start()
                save_node_state(node)
                print(f"🖥️  Node started at {args.host}:{args.port}")
                
                # Interactive mode to keep node running
                if args.interactive:
                    print("\n=== Interactive Node Mode ===")
                    print("Commands:")
                    print("  add <transaction>   - Add transaction")
                    print("  mine               - Mine pending transactions")
                    print("  view               - View blockchain")
                    print("  connect <host> <port> - Connect to peer")
                    print("  peers              - Show connected peers")
                    print("  quit               - Stop node")
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
                                print(f"✅ Transaction added: {transaction}")
                            elif cmd[0] == 'mine':
                                start_time = time.time()
                                block = bc.mine_pending_transactions()
                                if block:
                                    bc.save_to_file()
                                    print(f"⛏️  Mined block {block.index} in {time.time()-start_time:.4f}s")
                                    # Broadcast to peers
                                    node.broadcast_block(block)
                            elif cmd[0] == 'view':
                                print(f"🔗 Blockchain length: {len(bc.chain)}")
                                print(f"⏳ Pending transactions: {len(bc.pending_transactions)}")
                            elif cmd[0] == 'connect' and len(cmd) == 3:
                                peer_host, peer_port = cmd[1], int(cmd[2])
                                if node.connect_to_peer(peer_host, peer_port):
                                    print(f"🔗 Connected to {peer_host}:{peer_port}")
                                else:
                                    print(f"❌ Failed to connect to {peer_host}:{peer_port}")
                            elif cmd[0] == 'peers':
                                print(f"Connected peers: {list(node.peers)}")
                            else:
                                print("Unknown command or wrong arguments")
                                
                    except KeyboardInterrupt:
                        pass
                    finally:
                        node.stop()
                        clear_node_state()
                        print("\n🛑 Node stopped")
            
        elif args.net_command == 'connect':
            if node:
                if node.connect_to_peer(args.peer_host, args.peer_port):
                    print(f"🔗 Connected to {args.peer_host}:{args.peer_port}")
                else:
                    print(f"❌ Failed to connect to {args.peer_host}:{args.peer_port}")
            else:
                print("⚠️  Start node first with 'network start'")
                
        elif args.net_command == 'stop':
            if node:
                node.stop()
                clear_node_state()
                node = None
                print("🛑 Node stopped")
            else:
                print("⚠️  No node is currently running")
                
        elif args.net_command == 'status':
            if node:
                print(f"✅ Node running at {node.host}:{node.port}")
                print(f"📡 Connected peers: {len(node.peers) if hasattr(node, 'peers') else 0}")
            else:
                print("❌ No node is currently running")
            
    else:
        parser.print_help()

if __name__ == '__main__':
    main()