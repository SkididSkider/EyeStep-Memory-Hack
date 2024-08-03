import customtkinter
import pymem
import pymem.exception
import keyboard
from colorama import init, Fore
import threading
import time
import platform
import ctypes
import hwid
import os

# Initialize colorama for colored console output
init(autoreset=True)

# Set customtkinter appearance and theme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

# Set the hotkey to trigger memory writing
key = "end"
os_name = os.getlogin

# Set console output color
console_color = Fore.MAGENTA

# Print ASCII art and prompt for process name
print(console_color + r"    ______          _____ __")
print(console_color + r"   / ____/_  _____ / ___// /____  ____ ")
print(console_color + r"  / __/ / / / / _ \__ \/ __/ _ \/ __ \ ")
print(console_color + r" / /___/ /_/ /  __/__/ / /_/  __/ /_/ / ")
print(console_color + r"/_____/\__, /\___/____/\__/\___/ .___/  ")
print(console_color + r"      /____/                  /_/       ", '\n')

print(Fore.YELLOW + "Dev Edition, Admin:",Fore.MAGENTA + os_name,Fore.YELLOW + ", id =", Fore.MAGENTA + hwid.get_hwid(), '\n') # cool fucking id lol

process_name = input(Fore.MAGENTA + "Enter Process Name: ")

console_color = Fore.GREEN
print(console_color + "Press the 'end' button to write to memory after injecting!")

# Create the main application window
app = customtkinter.CTk()
app.title("EyeStep V1.2")
app.geometry("215x215")

# Create a frame within the main window
frame = customtkinter.CTkFrame(master=app)
frame.pack(expand=False)
frame.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")

# Initialize process memory object
pm = None

# Function to check if a process is 32-bit or 64-bit
def is_process_64bit(pid):
    process_handle = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid)
    if process_handle == 0:
        return False
    is64bit = ctypes.c_int()
    ctypes.windll.kernel32.IsWow64Process(process_handle, ctypes.byref(is64bit))
    ctypes.windll.kernel32.CloseHandle(process_handle)
    return is64bit.value == 0

# Function to inject into the specified process
def inject_function():
    global pm
    try:
        stat.configure(text="Injecting...", text_color="yellow")
        pm = pymem.Pymem(process_name)  # Use user-provided process name
        process_64bit = is_process_64bit(pm.process_id)
        app.after(400, lambda: stat.configure(text="Injected", text_color="green"))
        print(console_color + "Injected successfully")
        if process_64bit:
            print(console_color + "Target process is 64-bit.")
        else:
            print(console_color + "Target process is 32-bit.")
    except pymem.exception.PymemError as e:
        stat.configure(text=f"Process not found: {e}", text_color="red")
        print(Fore.RED + f"Error: {e}")
    except Exception as e:
        stat.configure(text=f"Error: {str(e)}", text_color="red")
        print(Fore.RED + f"Error: {str(e)}")

# Function to handle value locking based on switch state
def check_switch():
    while True:
        if switch_var.get() == "on" and pm:
            try:
                address = int(address_entry.get(), 16)
                value = int(value_entry.get())
                pm.write_int(address, value)
            except pymem.exception.PymemError as e:
                stat.configure(text=f"Error: {e}", text_color="red")
                print(Fore.RED + f"Error: {e}")
            except Exception as e:
                stat.configure(text=f"Error: {str(e)}", text_color="red")
                print(Fore.RED + f"Error: {str(e)}")
        time.sleep(0.5)  # Sleep to prevent busy-waiting

# Function to write to memory when the hotkey is pressed
def hotkey_action():
    try:
        if pm:
            address = int(address_entry.get(), 16)
            value = int(value_entry.get())
            pm.write_int(address, value)
            stat.configure(text="Memory Written", text_color="green")
            print(console_color + "Memory written successfully")
        else:
            stat.configure(text="Inject first", text_color="red")
            print(Fore.RED + "Please inject the process first")
    except pymem.exception.PymemError as e:
        stat.configure(text=f"Error: {e}", text_color="red")
        print(Fore.RED + f"Error: {e}")
    except Exception as e:
        stat.configure(text=f"Error: {str(e)}", text_color="red")
        print(Fore.RED + f"Error: {str(e)}")

# Set the hotkey action
try:
    keyboard.add_hotkey(key, hotkey_action)
except Exception as e:
    print(Fore.RED + f"Failed to set hotkey: {str(e)}")

# Create and place GUI elements
button = customtkinter.CTkButton(master=frame, text="Inject", command=inject_function, fg_color="#9b35db", hover_color="#7e21b9")
button.place(relx=0.5, rely=0.9, anchor=customtkinter.CENTER)

label = customtkinter.CTkLabel(master=frame, text="Status: ")
label.place(relx=0.2, rely=0.1, anchor=customtkinter.CENTER)

label2 = customtkinter.CTkLabel(master=frame, text="Address: ")
label2.place(relx=0.2, rely=0.3, anchor=customtkinter.CENTER)

label3 = customtkinter.CTkLabel(master=frame, text="Value: ")
label3.place(relx=0.2, rely=0.5, anchor=customtkinter.CENTER)

switch_var = customtkinter.StringVar(value="off")
switch = customtkinter.CTkSwitch(master=frame, text="Lock Value", variable=switch_var, onvalue="on", offvalue="off")
switch.place(relx=0.3, rely=0.7, anchor=customtkinter.CENTER)

stat = customtkinter.CTkLabel(master=frame, text="Not Injected", text_color="red")
stat.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)

address_entry = customtkinter.CTkEntry(master=frame, width=100)
address_entry.place(relx=0.6, rely=0.3, anchor=customtkinter.CENTER)
address_entry.insert(0, "0x07604F8")

value_entry = customtkinter.CTkEntry(master=frame, width=100)
value_entry.place(relx=0.6, rely=0.5, anchor=customtkinter.CENTER)
value_entry.insert(0, "1337")

# Start a thread for checking the switch state
switch_thread = threading.Thread(target=check_switch, daemon=True)
switch_thread.start()

# Start the main event loop
app.mainloop()
