import tkinter as tk
from tkinter import ttk, messagebox
from autodecoder import Ciphers

def decode_messages(ciphers, key, result_widget):
    result_widget.delete('1.0', tk.END)
    if not ciphers or not key:
        result_widget.insert(tk.END, "Please enter ciphertexts and key.\n")
        return
    try:
        C = Ciphers(ciphers)
    except AssertionError as e:
        result_widget.insert(tk.END, f"Error: {str(e)}\n")
        return

    # Key length check and conversion
    if len(key) != C.len:
        if len(key) * 2 == C.len:
            key = key.encode().hex()
        else:
            result_widget.insert(tk.END, "Invalid key length.\n")
            return

    result_widget.insert(tk.END, f"Key:\n\t{key}\n")
    for cipher in C.ciphers:
        result_widget.insert(tk.END, f"\nMessage: {cipher}\n\t")
        msg = ""
        for i in range(len(key) // 2):
            char = int(cipher[2*i:2*i+2], 16) ^ int(key[2*i:2*i+2], 16)
            msg += chr(char)
        result_widget.insert(tk.END, msg + "\n")

def main():
    root = tk.Tk()
    root.title("XOR Decoder")

    main_frame = ttk.Frame(root, padding="12 12 12 12")
    main_frame.grid(row=0, column=0, sticky="nsew")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    title_label = ttk.Label(main_frame, text="XOR Decoder", font=("Arial", 16, "bold"))
    title_label.grid(row=0, column=0, columnspan=4, pady=(0, 10))

    # Ciphertexts input bars (dynamic)
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

    # Add default ciphertexts (not removable)
    add_ciphertext("2c1549100043130b1000290a1b", removable=False)
    add_ciphertext("3f16421617175203114c020b1c", removable=False)

    btn_add = ttk.Button(cipher_frame, text="Add", width=8, command=lambda: add_ciphertext(removable=True))
    btn_add.grid(row=100, column=1, pady=4, sticky='w')

    # Key input
    key_frame = ttk.LabelFrame(main_frame, text="Key", padding="8 8 8 8")
    key_frame.grid(row=2, column=0, columnspan=4, sticky="ew", pady=(0, 10))
    ttk.Label(key_frame, text="Key:").grid(row=0, column=0, sticky='e', padx=(0, 5))
    key_entry = ttk.Entry(key_frame, width=40)
    key_entry.grid(row=0, column=1, sticky='w', padx=(0, 5))

    run_btn = ttk.Button(main_frame, text="Decode")
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
        key = key_entry.get().strip()
        decode_messages(selected_ciphers, key, result_text)

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