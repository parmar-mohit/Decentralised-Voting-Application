import tkinter as tk
from tkinter import messagebox
import pickle
from contracts.conduct_functions import startElection, endElection, addCandidate, isElectionRunning, getVotes
from web3 import Web3

def showElectionInterface(election_name,private_key,wallet_address):
    # Function to add a candidate to the list and update the candidate list
    def add_candidate():
        candidate_name = candidate_entry.get()
        if not candidate_name:
            messagebox.showerror("Candidate Name","Please enter a candidate name")
            return
        
        if isElectionRunning(my_contract):
            messagebox.showerror("Candidate Name","Election has started cannot add candidate now")
            return
        
        addCandidate(candidate_name,my_contract,private_key,wallet_address)
        messagebox.showinfo("Candidate Info","Candidate has been Added Sucessfully")
        refresh_candidates()

    def refresh_candidates():
        candidate_listbox.delete(0, tk.END)
        result = getVotes(my_contract, private_key,wallet_address)

        for i in range(len(result[0])):
            candidate_listbox.insert(tk.END, "Name : "+result[0][i]+", Votes : "+str(result[1][i]) )

    # Function to start the election
    def start_election():
        if election_status_label["text"] == "Election Status : Ended":
            messagebox.showerror("Election Status","Election has alredy been ended")
            return
        result = startElection(my_contract,private_key,wallet_address)
        if not result:
            messagebox.showerror("Election Error","Election could not be started")
            return
        election_status_label.config(text="Election Status : Live")

    # Function to end the election
    def end_election():
        endElection(my_contract,private_key,wallet_address)
        election_status_label.config(text="Election Status : Ended")

    # Reading Contract
    fin = open("./Deployed_Contracts/{}/contract.adr".format(election_name),"r")
    contract_address = fin.read()
    fin.close()

    fin = open("./Deployed_Contracts/{}/contract.abi".format(election_name),"rb")
    contract_abi = pickle.load(fin)
    fin.close()

    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
    my_contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi,
    )

    root = tk.Tk()
    root.title("Election : " + election_name)
    root.geometry("650x550")
    root.configure(bg='#f2f2f2')

    # Create and configure the candidate list
    candidates_list_label = election_status_label = tk.Label(root, text="Candidates List", fg="#00b33c",font=("Arial",16),justify="center")
    candidate_listbox = tk.Listbox(root)
    candidate_listbox.config(width=40, height=10,font=("Arial",16),fg="#00b33c")

    # Create and configure the candidate entry and add candidate button
    candidate_label = tk.Label(root, text="Enter Candidate Name", fg='#00b33c',font=("Arial",16))
    candidate_entry = tk.Entry(root,font=("Arial",16))
    add_candidate_button = tk.Button(root, text="Add Candidate", command=add_candidate,fg="#00b33c",font=("Arial",16))

    
    # Create and configure the start and end election buttons
    start_button = tk.Button(root, text="Start Election", command=start_election,fg="#00b33c",font=("Arial",16))
    refresh_button = tk.Button(root, text="Refresh", command=refresh_candidates,fg="#00b33c",font=("Arial",16))
    end_button = tk.Button(root, text="End Election", command=end_election,fg="#00b33c",font=("Arial",16))

    # Create and configure the election status label
    election_status_label = tk.Label(root, text="Election Status :  Not Started", fg="#00b33c",font=("Arial",16))

    # Pack the widgets
    candidates_list_label.grid(row=0,column=0,columnspan=3,padx=5,pady=5)
    candidate_listbox.grid(row=1,column=0,columnspan=3,padx=5,pady=5)
    candidate_label.grid(row=2,column=0,padx=5,pady=5)
    candidate_entry.grid(row=2,column=1,padx=5,pady=5)
    add_candidate_button.grid(row=2,column=2,padx=5,pady=5)
    election_status_label.grid(row=3,column=0,columnspan=3,padx=5,pady=5)
    start_button.grid(row=4,column=0,columnspan=3,padx=5,pady=5)
    refresh_button.grid(row=5,column=0,columnspan=3,padx=5,pady=5)
    end_button.grid(row=6,column=0,columnspan=3,padx=5,pady=5)
    
    root.mainloop()