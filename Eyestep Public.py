import customtkinter
import pymem
import pymem.exception
import keyboard
from colorama import init, Fore
import threading
import time
import platform
import ctypes

init(autoreset=True)

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

key = "end"

console_color = Fore.MAGENTA

print(console_color + r"    ______          _____ __")
print(console_color + r"   / ____/_  _____ / ___// /____  ____ ")
print(console_color + r"  / __/ / / / / _ \__ \/ __/ _ \/ __ \ ")
print(console_color + r" / /___/ /_/ /  __/__/ / /_/  __/ /_/ / ")
print(console_color + r"/_____/\__, /\___/____/\__/\___/ .___/  ")
print(console_color + r"      /____/                  /_/       ", '\n')

print(Fore.YELLOW + "Public Edition(Omg Omg Private Exists!!!)", '\n')

process_name = input(Fore.MAGENTA + "Enter Process Name: ")

console_color = Fore.GREEN
print(console_color + "Press the 'end' button to write to memory after injecting!")

app = customtkinter.CTk()
app.title("EyeStep V1.1")
app.geometry("215x215")

frame = customtkinter.CTkFrame(master=app)
frame.pack(expand=False)
frame.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")

pm = None

def is_process_64bit(pid):
    process_handle = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid)
    if process_handle == 0:
        return False
    is64bit = ctypes.c_int()
    ctypes.windll.kernel32.IsWow64Process(process_handle, ctypes.byref(is64bit))
    ctypes.windll.kernel32.CloseHandle(process_handle)
    return is64bit.value == 0

def inject_function():
    global pm
    try:
        stat.configure(text="Injecting...", text_color="yellow")
        pm = pymem.Pymem(process_name)
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
        time.sleep(0.5)

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

try:
    keyboard.add_hotkey(key, hotkey_action)
except Exception as e:
    print(Fore.RED + f"Failed to set hotkey: {str(e)}")

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

switch_thread = threading.Thread(target=check_switch, daemon=True)
switch_thread.start()

app.mainloop()
