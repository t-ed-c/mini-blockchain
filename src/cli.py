import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__))) 
import argparse
from blockchain import Blockchain
import json
import time

def main():
    # Load existing blockchain or create new one
    bc = Blockchain.load_from_file()
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
            
    else:
        parser.print_help()

if __name__ == '__main__':
    main()