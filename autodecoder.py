import tkinter as tk
from tkinter import ttk, messagebox

class Ciphers:
    def __init__(self, ciphers):
        self.ciphers = ciphers
        self.num = len(ciphers)
        self.len = len(ciphers[0])
        
        self.init_ciphers()

    def init_ciphers(self):
        # Check if there are more than 2 ciphertexts
        assert self.num > 1, "Not enough ciphertexts"
        
        # Check if the ciphertexts have an even length
        assert self.len % 2 == 0, "Odd ciphertext length"

        # Check if all ciphertexts have the same length
        lengths = [len(c) for c in self.ciphers]
        assert max(lengths) == min(lengths), "Ciphertext length not match"

        for i in range(self.num):
            # Convert ASCII ciphers to hex
            try:
                int(self.ciphers[i], 16)
            except ValueError:
                self.ciphers[i] = self.ciphers[i].encode().hex()
                self.len *= 2

def is_range(char, search_range):
    """Return True if all the characters are in ASCII range"""
    for c in char:
        if c not in search_range:
            return False
    return True

def display_results(ciphers, key):
    # Display the possible messages
    for cipher in ciphers:
        print(f"Message: {cipher}")
        for i in range(len(key)):
            print("\t", end='')
            
            char = int(cipher[2*i:2*i+2], 16)
            for k in key[i]:
                print("%-2s" % chr(char ^ k), end=' ')
            print()
        print()

    # Display the possible key
    print("\nKey:")
    for k in key:
        print("\t", end='')
        for i in k:
            value = hex(i)[2:]
            if len(value) == 1:
                value = '0' + value
            
            print(f"{value}", end=' ')
        print()

def display_results(ciphers, key, text_widget):
    text_widget.delete('1.0', tk.END)
    for cipher in ciphers:
        text_widget.insert(tk.END, f"Message: {cipher}\n")
        for i in range(len(key)):
            text_widget.insert(tk.END, "\t")
            char = int(cipher[2*i:2*i+2], 16)
            for k in key[i]:
                text_widget.insert(tk.END, "%-2s " % chr(char ^ k))
            text_widget.insert(tk.END, "\n")
        text_widget.insert(tk.END, "\n")
    text_widget.insert(tk.END, "\nKey:\n")
    for k in key:
        text_widget.insert(tk.END, "\t")
        for i in k:
            value = hex(i)[2:]
            if len(value) == 1:
                value = '0' + value
            text_widget.insert(tk.END, f"{value} ")
        text_widget.insert(tk.END, "\n")

def get_range(labels):
    search_range = []
    for i in labels:
        if i == "Lower Alphabets":
            search_range += range(97, 123)  # a-z
        elif i == "Upper Alphabets":
            search_range += range(65, 91)   # A-Z
        elif i == "Numbers":
            search_range += range(48, 58)   # 0-9
        elif i == "Space":
            search_range.append(32)         # space
        elif i == "Punctuation":
            # Common ASCII punctuation
            search_range += list(range(33, 48)) + list(range(58, 65)) + list(range(91, 97)) + list(range(123, 127))
        else:
            try:
                search_range.append(ord(i))
            except TypeError:
                pass
    return search_range

def decode(selected_ciphers, selected_ranges, result_widget):
    if not selected_ciphers:
        messagebox.showerror("Error", "No ciphertexts selected.")
        return
    search_range = get_range(selected_ranges)
    try:
        C = Ciphers(selected_ciphers)
    except AssertionError as e:
        messagebox.showerror("Error", str(e))
        return
    key = []
    for i in range(C.len // 2):
        char = []
        for cipher in C.ciphers:
            char.append(int(cipher[2*i:2*i+2], 16))
        key.append([])
        for k in range(0xFF):
            msg = []
            for c in char:
                msg.append(c ^ k)
            if is_range(msg, search_range):
                key[i].append(k)
        if not key[i]:
            result_widget.insert(tk.END, f"Warning: Search range too small. Empty result at position {i}\n")
    display_results(C.ciphers, key, result_widget)

def main():
    root = tk.Tk()
    root.title("XOR Autodecoder")

    main_frame = ttk.Frame(root, padding="12 12 12 12")
    main_frame.grid(row=0, column=0, sticky="nsew")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    title_label = ttk.Label(main_frame, text="XOR Autodecoder", font=("Arial", 16, "bold"))
    title_label.grid(row=0, column=0, columnspan=4, pady=(0, 10))

    # Ciphertexts input bars
    cipher_frame = ttk.LabelFrame(main_frame, text="Ciphertexts", padding="8 8 8 8")
    cipher_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(0, 10))
    cipher_entries = []

    def add_ciphertext(value="", removable=True):
        idx = len(cipher_entries)
        entry = ttk.Entry(cipher_frame, width=40)
        entry.insert(0, value)
        entry.grid(row=idx, column=1, sticky='w', padx=(0, 5), pady=2)
        label = ttk.Label(cipher_frame, text=f"Ciphertext {idx+1}:")
        label.grid(row=idx, column=0, sticky='e', padx=(0, 5), pady=2)
        if removable:
            btn_remove = ttk.Button(cipher_frame, text="Remove", width=8,
                                    command=lambda e=entry, l=label, b=None: remove_ciphertext(e, l, btn_remove))
            btn_remove.grid(row=idx, column=2, padx=2)
        cipher_entries.append(entry)

    def remove_ciphertext(entry, label, button):
        idx = cipher_entries.index(entry)
        entry.destroy()
        label.destroy()
        if button:
            button.destroy()
        cipher_entries.pop(idx)
        # Re-label remaining entries
        for i, e in enumerate(cipher_entries):
            cipher_frame.grid_slaves(row=i, column=0)[0].config(text=f"Ciphertext {i+1}:")

    # Add example ciphertexts
    add_ciphertext("2c1549100043130b1000290a1b", removable=False)
    add_ciphertext("3f16421617175203114c020b1c", removable=False)

    btn_add = ttk.Button(cipher_frame, text="Add", width=8, command=lambda: add_ciphertext(removable=True))
    btn_add.grid(row=100, column=1, pady=4, sticky='w')

    # SearchRange selection
    range_frame = ttk.LabelFrame(main_frame, text="Search Range", padding="8 8 8 8")
    range_frame.grid(row=2, column=0, columnspan=4, sticky="ew", pady=(0, 10))
    range_vars = []
    search_range_labels = ["Lower Alphabets", "Upper Alphabets", "Numbers", "Space", "Punctuation"]
    for idx, r in enumerate(search_range_labels):
        var = tk.BooleanVar(value=False)
        cb = ttk.Checkbutton(range_frame, text=r, variable=var)
        cb.grid(row=0, column=idx, sticky='w', padx=5)
        range_vars.append(var)

    run_btn = ttk.Button(main_frame, text="Run Decoder")
    run_btn.grid(row=3, column=0, pady=(0, 10), sticky='w')

    result_frame = ttk.LabelFrame(main_frame, text="Results", padding="8 8 8 8")
    result_frame.grid(row=4, column=0, columnspan=4, sticky="nsew")

    # Add scrollbar to the result text box
    result_text = tk.Text(result_frame, width=80, height=20, wrap="word")
    scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=result_text.yview)
    result_text.configure(yscrollcommand=scrollbar.set)
    result_text.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def on_run():
        selected_ciphers = [e.get().strip() for e in cipher_entries if e.get().strip()]
        selected_ranges = [r for v, r in zip(range_vars, search_range_labels) if v.get()]
        result_text.delete('1.0', tk.END)
        decode(selected_ciphers, selected_ranges, result_text)

    run_btn.config(command=on_run)

    for i in range(4):
        main_frame.columnconfigure(i, weight=1)
    main_frame.rowconfigure(4, weight=1)
    result_frame.rowconfigure(0, weight=1)
    result_frame.columnconfigure(0, weight=1)

    root.minsize(700, 500)
    root.mainloop()

if __name__ == "__main__":
    main()
