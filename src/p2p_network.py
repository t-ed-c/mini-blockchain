import socket
import threading
import json
from blockchain import Blockchain
import time

class Node:
    def __init__(self, host, port, blockchain):
        """
        Initialize a blockchain node
        
        :param host: IP address to bind to
        :param port: Port to listen on
        :param blockchain: Blockchain instance
        """
        self.host = host
        self.port = port
        self.blockchain = blockchain
        self.peers = set()  # Stores (host, port) of connected peers
        self.server_socket = None
        self.running = False
        
    def start(self):
        """Start the node server"""
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"🖥️  Node started at {self.host}:{self.port}")
        
        # Start accepting connections
        threading.Thread(target=self.accept_connections, daemon=True).start()
        
    def accept_connections(self):
        """Accept incoming connections"""
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                print(f"🔌 Connection from {addr[0]}:{addr[1]}")
                threading.Thread(
                    target=self.handle_connection, 
                    args=(client_socket,),
                    daemon=True
                ).start()
            except:
                if self.running:
                    print("⚠️  Error accepting connection")
                    
    def handle_connection(self, client_socket):
        """Handle incoming messages"""
        with client_socket:
            try:
                data = client_socket.recv(4096).decode('utf-8')
                if not data:
                    return
                    
                message = json.loads(data)
                print(f"📨 Received: {message['type']}")
                
                if message['type'] == 'connect':
                    # Add new peer
                    self.peers.add((message['host'], message['port']))
                    client_socket.sendall(json.dumps({
                        'type': 'acknowledge',
                        'message': f"Connected to {self.host}:{self.port}"
                    }).encode('utf-8'))
                    
                elif message['type'] == 'get_chain':
                    # Send blockchain data
                    chain_data = self.blockchain.to_dict()
                    client_socket.sendall(json.dumps({
                        'type': 'chain',
                        'data': chain_data
                    }).encode('utf-8'))
                    
                elif message['type'] == 'new_block':
                    # Handle new block from peer
                    block_data = message['data']
                    new_block = Block(
                        index=block_data['index'],
                        transactions=block_data['transactions'],
                        timestamp=block_data['timestamp'],
                        previous_hash=block_data['previous_hash']
                    )
                    new_block.hash = block_data['hash']
                    new_block.nonce = block_data['nonce']
                    
                    # Add to chain if valid
                    if self.blockchain.is_chain_valid() and self.blockchain.last_block.hash == new_block.previous_hash:
                        self.blockchain.chain.append(new_block)
                        print(f"🔗 Added block {new_block.index} from peer")
                    
            except Exception as e:
                print(f"⚠️  Connection error: {e}")
                
    def connect_to_peer(self, peer_host, peer_port):
        """Connect to another node"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((peer_host, peer_port))
                s.sendall(json.dumps({
                    'type': 'connect',
                    'host': self.host,
                    'port': self.port
                }).encode('utf-8'))
                
                response = json.loads(s.recv(4096).decode('utf-8'))
                if response['type'] == 'acknowledge':
                    self.peers.add((peer_host, peer_port))
                    print(f"🔗 Connected to peer {peer_host}:{peer_port}")
                    return True
        except Exception as e:
            print(f"⚠️  Failed to connect to {peer_host}:{peer_port}: {e}")
        return False
        
    def broadcast_block(self, block):
        """Broadcast a new block to all peers"""
        block_data = {
            'index': block.index,
            'transactions': block.transactions,
            'timestamp': block.timestamp,
            'previous_hash': block.previous_hash,
            'hash': block.hash,
            'nonce': block.nonce
        }
        
        message = json.dumps({
            'type': 'new_block',
            'data': block_data
        })
        
        for peer_host, peer_port in self.peers:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((peer_host, peer_port))
                    s.sendall(message.encode('utf-8'))
                    print(f"📤 Sent block {block.index} to {peer_host}:{peer_port}")
            except:
                print(f"⚠️  Failed to send to {peer_host}:{peer_port}")
                
    def stop(self):
        """Stop the node"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("🛑 Node stopped")

# Test the networking
if __name__ == "__main__":
    # Create blockchain
    bc = Blockchain(difficulty=2)
    
    # Create two nodes
    node1 = Node('127.0.0.1', 5000, bc)
    node2 = Node('127.0.0.1', 5001, bc)
    
    # Start nodes
    node1.start()
    node2.start()
    
    # Connect node1 to node2
    print("\nConnecting nodes...")
    node1.connect_to_peer('127.0.0.1', 5001)
    
    # Add transactions and mine on node1
    print("\nMining on node1...")
    bc.add_transaction("Node1 TX: Alice pays Bob 5 BTC")
    block = bc.mine_pending_transactions()
    
    # Broadcast the new block
    print("\nBroadcasting block...")
    node1.broadcast_block(block)
    
    # Give time for propagation
    time.sleep(1)
    
    # Check node2's chain
    print("\nNode2 blockchain:")
    for block in node2.blockchain.chain:
        print(f"Block {block.index}: {block.hash[:12]}...")
    
    # Stop nodes
    node1.stop()
    node2.stop()