import tkinter as tk
from tkinter import messagebox
from web3 import Web3, HTTPProvider
from conduct_interfaces.conduct_election import showConductElectionInterface
from eth_keys import keys

def import_wallet():
    def getWalletAddress(private_key_hex):
        private_key = keys.PrivateKey(bytes.fromhex(private_key_hex))

        # Get the Ethereum address from the public key
        ethereum_address = private_key.public_key.to_checksum_address()

        return ethereum_address

    private_key = private_key_entry.get()

    w3 = Web3(HTTPProvider("http://127.0.0.1:7545"))
    
    if not private_key:
        messagebox.showerror("Private key","Enter Private Key")
        return

    if not private_key.startswith('0x') or len(private_key[2:]) != 64 or not all(c in '0123456789abcdefABCDEF' for c in private_key[2:]):
        messagebox.showerror("Private key","Enter a Valid Private Key")
        return False
    
    account = w3.eth.account.from_key(private_key)
    balance = w3.eth.get_balance(account.address)
    if balance <= 0:
        messagebox.showerror("Private key","Wallet with Entered private key does not exist")
        return
    
    root.destroy()
    showConductElectionInterface(private_key, getWalletAddress(private_key[2:]))
    

# Create the main window
root = tk.Tk()
root.geometry('1000x200')
root.title("Wallet Import")

# Set a red and black color theme
root.configure(bg='#f2f2f2')

# Create a label with a red foreground color
label = tk.Label(root, text="Enter Private Key", fg='#00b33c',font=("Arial",16))
label.pack(pady=10)

# Create an Entry widget for the private key with a red foreground color
private_key_entry = tk.Entry(root, fg='#00b33c',width=75,font=("Arial",14))
private_key_entry.pack(pady=10)

# Create a button to import the wallet with a red foreground color
import_button = tk.Button(root, text="Import Wallet", command=import_wallet, fg='#00b33c',font=("Arial",14))
import_button.pack(pady=10)

# Start the Tkinter main loop
root.mainloop()
