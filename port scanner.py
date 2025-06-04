import socket
import threading
import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext, ttk

results = []

def scan_ports(ip, start, end):
    total = end - start + 1
    scanned = 0

    for port in range(start, end + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.2)
                result = s.connect_ex((ip, port))
                if result == 0:
                    try:
                        service = socket.getservbyport(port)
                    except:
                        service = "unknown"
                    msg = f"Port {port} is open ({service})"
                    result_box.insert(tk.END, msg + "\n", "green")
                    results.append(msg)
        except:
            pass

        scanned += 1
        percent = int((scanned / total) * 100)
        progress_var.set(percent)
        progress_bar.update()

    result_box.insert(tk.END, f"\n✅ Scan Complete! {scanned} ports checked.\n", "blue")

def start_scan():
    results.clear()
    result_box.delete(1.0, tk.END)
    try:
        ip = ip_entry.get().strip()
        start = int(start_entry.get().strip())
        end = int(end_entry.get().strip())
    except:
        messagebox.showerror("Invalid Input", "Please enter valid values.")
        return

    progress_var.set(0)
    t = threading.Thread(target=scan_ports, args=(ip, start, end))
    t.start()

def save_results():
    if not results:
        messagebox.showwarning("No Result", "Nothing to save.")
        return
    path = filedialog.asksaveasfilename(defaultextension=".txt",
                                        filetypes=[("Text Files", "*.txt")],
                                        title="Save Result")
    if path:
        with open(path, "w") as f:
            f.write("\n".join(results))
        messagebox.showinfo("Saved", f"Results saved to:\n{path}")

# --- GUI ---
root = tk.Tk()
root.title("🚀 Port Scanner with Progress")
root.geometry("580x570")
root.resizable(False, False)
root.config(bg="#f2f2f2")

tk.Label(root, text="Target IP / Domain:", font=("Segoe UI", 10), bg="#f2f2f2").pack(pady=5)
ip_entry = tk.Entry(root, width=40, font=("Segoe UI", 10))
ip_entry.pack()

tk.Label(root, text="Start Port:", font=("Segoe UI", 10), bg="#f2f2f2").pack(pady=4)
start_entry = tk.Entry(root, width=20, font=("Segoe UI", 10))
start_entry.pack()

tk.Label(root, text="End Port:", font=("Segoe UI", 10), bg="#f2f2f2").pack(pady=4)
end_entry = tk.Entry(root, width=20, font=("Segoe UI", 10))
end_entry.pack()

tk.Button(root, text="Start Scan", command=start_scan, bg="green", fg="white", width=20).pack(pady=8)
tk.Button(root, text="Save Results", command=save_results, bg="blue", fg="white", width=20).pack(pady=2)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=500)
progress_bar.pack(pady=10)

result_box = scrolledtext.ScrolledText(root, height=20, width=70, font=("Consolas", 10))
result_box.pack(padx=10, pady=10)

result_box.tag_config("green", foreground="green")
result_box.tag_config("blue", foreground="blue")

root.mainloop()
