# Blockchain Voting System

A decentralized, tamper-evident electronic voting system implemented in Python using core blockchain principles. This application features block hashing, proof-of-work consensus, registration constraints, dual-voting prevention, and automated fraud detection.

## 🚀 Features Implemented
*   **Immutable Ledger**: Every vote is sealed inside a block using SHA-256 cryptographic hashing linked to the preceding block.
*   **Proof of Work**: Implements a puzzle-based mining mechanism using variable difficulty settings.
*   **Voter & Candidate Verification**: Restricts voting to a closed set of registered IDs (`VOTER101`–`VOTER105`) and valid candidates (`Alice`, `Bob`, `Charlie`).
*   **Double-Voting Prevention**: Scans the entire ledger sequentially to catch and block duplicate voter IDs instantly.
*   **Tamper Detection**: Includes an intentional database manipulation simulation to demonstrate how the blockchain breaks validation when a single record is modified.
*   **Persistent Storage**: Saves and loads the live blockchain history directly to and from a formatted JSON file.

---

## 📸 Screenshots & Feature Walkthrough

### 1. Interactive CLI Menu & Statistics
The interface allows users to step through every blockchain operation cleanly.

### 2. Registering a Vote (Mining a Block)
Validates voter authorization, calculates the hash target using Proof of Work, and securely appends the vote.

### 3. Viewing the Ledger Chain
Displays the individual block index tracking, precise UTC timestamps, stored transaction data, and cryptographic linkage.

### 4. Tampering & Fraud Detection
Modifying data out-of-sequence causes subsequent hashes to mismatch. The system instantly flags the chain as corrupted.

---

## 🛠️ How to Run the Project

### Prerequisites
*   Python 3.12 or higher installed on your system.

### Steps to Run
1.  **Clone the repository:**
    ```bash
    git clone https://github.com
    cd blockchain-voting-system
    ```
2.  **Execute the application:**
    ```bash
    python main.py
    ```
3.  Use the on-screen numbers (**1-10**) to navigate through the program features.
