import socket
import threading
import tkinter as tk
from tkinter import messagebox, filedialog

results = []  # Scan ke results yahan store honge

window = tk.Tk()
window.title("Port Scanner")
window.geometry("520x480")
window.resizable(False, False)

# IP ya domain lene ke liye input box
tk.Label(window, text="Enter IP or Domain to Scan:").pack(pady=5)
target_input = tk.Entry(window, width=42)
target_input.pack()

# Start port input
tk.Label(window, text="Start Port:").pack(pady=5)
start_input = tk.Entry(window, width=20)
start_input.pack()

# End port input
tk.Label(window, text="End Port:").pack(pady=5)
end_input = tk.Entry(window, width=20)
end_input.pack()

# Output dikhane wala box
output_box = tk.Text(window, height=15, width=65)
output_box.pack(pady=8)

# Yeh function ek port check karta hai open hai ya nahi
def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "unknown"
            line = f"Port {port} is open ({service})"
            output_box.insert(tk.END, line + "\n")
            results.append(line)
        sock.close()
    except:
        pass

# Jab user scan button dabaye, yeh function call hota hai
def start_scan():
    ip = target_input.get().strip()
    try:
        start_port = int(start_input.get().strip())
        end_port = int(end_input.get().strip())
    except:
        messagebox.showerror("Error", "Ports must be valid numbers.")
        return

    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, f"Scanning {ip} from port {start_port} to {end_port}...\n\n")
    results.clear()

    # Har port ke liye ek thread banake scan karte hain
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(ip, port))
        t.start()

# Agar user results ko file me save karna chahe
def save_results():
    if not results:
        messagebox.showwarning("No Results", "Nothing to save yet.")
        return

    path = filedialog.asksaveasfilename(defaultextension=".txt",
                                        filetypes=[("Text files", "*.txt")],
                                        title="Save results as...")
    if path:
        with open(path, "w") as f:
            f.write("\n".join(results))
        messagebox.showinfo("Saved", f"Results saved to:\n{path}")

# Button: Start Scan
tk.Button(window, text="Start Scan", command=start_scan, bg="green", fg="white").pack(pady=6)

# Button: Save Result
tk.Button(window, text="Save Results", command=save_results, bg="blue", fg="white").pack(pady=4)

window.mainloop()