import json
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo


states = {
        'AK': 1,
        'AL': 2,
        'AR': 3,
        'AZ': 4,
        'CA': 5,
        'CO': 6,
        'CT': 7,
        'DE': 8,
        'FL': 9,
        'GA': 10,
        'HI': 11,
        'IA': 12,
        'ID': 13,
        'IL': 14,
        'IN': 15,
        'KS': 16,
        'KY': 17,
        'LA': 18,
        'MA': 19,
        'MD': 20,
        'ME': 21,
        'MI': 22,
        'MN': 23,
        'MO': 24,
        'MS': 25,
        'MT': 26,
        'NC': 27,
        'ND': 28,
        'NE': 29,
        'NH': 30,
        'NJ': 31,
        'NM': 32,
        'NV': 33,
        'NY': 34,
        'OH': 35,
        'OK': 36,
        'OR': 37,
        'PA': 38,
        'RI': 39,
        'SC': 40,
        'SD': 41,
        'TN': 42,
        'TX': 43,
        'UT': 44,
        'VA': 45,
        'VT': 46,
        'WA': 47,
        'WI': 48,
        'WV': 49,
        'WY': 50
}

#json handling
f = open("profit.json", "r+")
data = json.load(f)

def findProfit(state, county, comm):
    #print(states[state])
    try:
        return data["states"][states[state]-1][state][0][county][0][comm+"_value"]
    except:
        return "null"

#tk window
root = tk.Tk()
root.geometry("1200x600")
root.title('John Deere Profit Utility')

state = tk.StringVar()
county = tk.StringVar()
comm = tk.StringVar()

def fetch_clicked():
    msg = f'Profitability of {state.get()}, {county.get()} in $ per acre: {findProfit(state.get(), county.get(), comm.get())}'
    showinfo(
        title='Profit',
        message=msg
    )


fetch = ttk.Frame(root)
fetch.pack(padx=10, pady=10, fill='x', expand=True)

state_label = ttk.Label(fetch, text="State(2-letter abbreviation, uppercase):")
state_label.pack(fill='x', expand=True)

state_entry = ttk.Entry(fetch, textvariable=state)
state_entry.pack(fill='x', expand=True)
state_entry.focus()

county_label = ttk.Label(fetch, text="County(full name, uppercase):")
county_label.pack(fill='x', expand=True)

county_entry = ttk.Entry(fetch, textvariable=county)
county_entry.pack(fill='x', expand=True)

comm_label = ttk.Label(fetch, text="Commodity(uppercase):")
comm_label.pack(fill='x', expand=True)

comm_entry = ttk.Entry(fetch, textvariable=comm)
comm_entry.pack(fill='x', expand=True)

fetch_button = ttk.Button(fetch, text="Enter", command=fetch_clicked)
fetch_button.pack(fill='x', expand=True, pady=10)


root.mainloop()