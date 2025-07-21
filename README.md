
---

````markdown
# ✅ MiniBlockchain - Python Blockchain Implementation
A lightweight, educational blockchain with Proof-of-Work, networking, and CLI interface**

📦 Features
- 🧱 Block structure with cryptographic hashing  
- ⛏️ Proof-of-Work mining with adjustable difficulty  
- 🔗 Blockchain validation and tamper detection  
- 🌐 Peer-to-peer networking  
- 💻 Interactive CLI interface  
- 📝 Transaction management

⚙️ Installation
Prerequisites
- Python 3.8+
- Git

Setup
bash
# Clone repository
git clone https://github.com/t-ed-c/mini-blockchain.git
cd mini-blockchain

# Create virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
---

## 🚀 Quick Start

### Start a Blockchain Node

```bash
python src/cli.py
```

### Interactive CLI Commands

```bash
> start --port 5000               # Start node on port 5000
> connect 127.0.0.1 5001          # Connect to another node
> add "Alice pays Bob 5 BTC"     # Add transaction
> mine                           # Mine pending transactions
> view                           # View blockchain
> difficulty 3                   # Set mining difficulty
> validate                       # Validate blockchain integrity
> tamper-test                    # Run tamper demonstration
> exit                           # Exit CLI
```

---

## 📋 Command Reference

| Command                             | Description                              |
| ----------------------------------- | ---------------------------------------- |
| `start [--host HOST] [--port PORT]` | Start node server                        |
| `connect HOST PORT`                 | Connect to peer node                     |
| `stop`                              | Stop node server                         |
| `add TRANSACTION`                   | Add transaction to pending pool          |
| `mine`                              | Mine pending transactions into new block |
| `view [--full]`                     | View blockchain (add --full for details) |
| `validate`                          | Validate blockchain integrity            |
| `difficulty LEVEL`                  | Set mining difficulty (1–5)              |
| `tamper-test`                       | Run blockchain tamper demonstration      |

---

## 🌐 Network Setup Guide

### Multi-Node Simulation

1. **Terminal 1 (Node 1):**

```bash
python src/cli.py
> start --port 5000
```

2. **Terminal 2 (Node 2):**

```bash
python src/cli.py
> start --port 5001
> connect 127.0.0.1 5000
```

3. **Add transactions and mine:**

```bash
> add "Node1 TX: Alice pays Bob 5 BTC"
> mine
```

4. **Verify propagation:**

```bash
> view
```

---

## 🧪 Testing the Blockchain

### Run Tamper Test

```bash
> tamper-test
```

This will demonstrate:

1. Original valid blockchain
2. Tampering with a block
3. Failed validation after tampering
4. Successful validation after restoration

### Manual Validation

```bash
> validate
```

Returns:

* ✅ VALID (if blockchain is intact)
* ❌ INVALID (if tampered)

---

## 🧩 Project Structure

```
mini-blockchain-python/
├── src/
│   ├── block.py             # Block implementation
│   ├── blockchain.py        # Blockchain core logic
│   ├── cli.py               # Command-line interface
│   └── p2p_network.py       # P2P networking
├── tests/                   # Unit tests
├── requirements.txt         # Dependencies
└── README.md                # This document
```

---

## 🛠️ Development

### Running Tests

```bash
pytest tests/
```

### Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## ✉️ Contact

Project Link: [mini-blockchain](https://github.com/t-ed-c/mini-blockchain.git)

---

## 🎓 Learning Resources

* [Bitcoin Whitepaper](https://bitcoin.org/bitcoin.pdf)
* [Proof-of-Work Explained](https://www.investopedia.com/terms/p/proof-work.asp)
* [Blockchain Basics](https://www.ibm.com/topics/blockchain)

```
