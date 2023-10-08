import tkinter as tk
from web3 import Web3
from tkinter import messagebox
from contracts.conduct_functions import deploy_contract
from conduct_interfaces.election_interface import showElectionInterface

def showConductElectionInterface(private_key, wallet_address):
    web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

    def get_balance():
        try:
            balance_wei = web3.eth.get_balance(wallet_address)
            balance_eth = web3.from_wei(balance_wei, 'ether')
            balance_label.config(text=f'Balance: {round(balance_eth,2)} ETH')
        except Exception as e:
            print(e)
            balance_label.config(text='Error fetching balance')

    def conduct_election():
        election_name = election_name_entry.get()
        if not election_name:
            messagebox.showerror("Election Name","Enter Election Name")
            return 
        
        contract_address = deploy_contract(election_name, private_key,wallet_address)
        messagebox.showinfo("Contract","Contract Deployed Successfully with address: {}".format(contract_address))

        root.destroy()
        showElectionInterface(election_name,private_key,wallet_address)

    # Create the main window
    root = tk.Tk()
    root.title('Election')
    root.geometry("400x250")
    root.configure(bg='#f2f2f2')

    balance_label = tk.Label(root, text='Balance: N/A', fg='#00b33c',font=("Arial",16))
    balance_label.pack(pady=30) 
    get_balance()

    label = tk.Label(root, text="Enter Election Name", fg='#00b33c',font=("Arial",16))
    label.pack(pady=10)

    # Create an Entry widget for the private key with a red foreground color
    election_name_entry = tk.Entry(root, fg='#00b33c',width=20,font=("Arial",14))
    election_name_entry.pack(pady=10)

    conduct_election_button = tk.Button(root, text='Conduct Election', command=conduct_election, fg='#00b33c',font=("Arial",16))
    conduct_election_button.pack(pady=10)

    root.mainloop()