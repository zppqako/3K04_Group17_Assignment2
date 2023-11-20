import customtkinter
import hashlib
from tkinter import messagebox
import time
import threading
import tkinter as tk
#import usb.core
import serial.tools.list_ports
import struct
from serial import Serial
from DCM_serial import test

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()

root.geometry("700x400")

users = {}

users_len = 0


def show_login_page():
    register_page.pack_forget()
    mode_page.pack_forget()
    AOO_page.pack_forget()
    VOO_page.pack_forget()
    AAI_page.pack_forget()
    VVI_page.pack_forget()
    login_page.pack()

def save_users():

    with open("users.txt", 'w') as file:
        for username, password in users.items():
            file.write(f"{username}:{password}\n")

    with open("users.txt", 'r') as file:
        lines = file.readlines()

    if len(lines) > 10:
        lines = lines[:10]
        messagebox.showerror('Error', 'Number of users has exceed 10')

        with open("users.txt", "w") as file:
            file.writelines(lines)
    else:
        messagebox.showinfo('Success', 'Account has been created successfully.')

    register_page.pack_forget()
    mode_page.pack_forget()
    login_page.pack()

def load_users():
    try:
        with open("users.txt", 'r') as file:
            lines = file.readlines()
            for line in lines:
                username, password = line.strip().split(":")
                users[username] = password
    except FileNotFoundError:
        pass
    register_page.pack_forget()
    mode_page.pack_forget()
    login_page.pack()

def confirm():
    username = new_username.get()
    password = new_password.get()
    if len(username) == 0 or len(password) == 0:
        messagebox.showerror('Error', 'Username or password cannot be empty.')
        register_page.pack()
        return
    if username in users:
        messagebox.showerror('Error', 'Username already exists.')
        register_page.pack()
        return

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    users[username] = hashed_password
    save_users()
    new_username.delete(0, 'end')
    new_password.delete(0, 'end')
    register_page.pack_forget()
    mode_page.pack_forget()
    login_page.pack()

def register():
    login_username.delete(0, 'end')
    login_password.delete(0, 'end')
    login_page.pack_forget()
    mode_page.pack_forget()
    AOO_page.pack_forget()
    register_page.pack()

def login():
    username = login_username.get()
    password = login_password.get()
    if len(username) == 0 or len(password) == 0:
        messagebox.showerror('Error', 'Username or password cannot be empty.')
        login_page.pack()
        return
    if username not in users:
        messagebox.showerror('Error', 'User does not exist.')
        login_username.delete(0, 'end')
        login_password.delete(0, 'end')
        login_page.pack()
        return
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if users[username] == hashed_password:
        messagebox.showinfo('Success', 'Login successfully')
        login_page.pack_forget()
        register_page.pack_forget()
        mode_page.pack()
    else:
        messagebox.showerror('Error', 'Password is not correct.')
        login_password.delete(0, 'end')
        login_page.pack()

def clear_entry():
    return 0
    # AOO_LRL.delete(0,'123')
    # AOO_URL.delete(0,'end')
    # AOO_AA.delete(0,'end')
    # AOO_APW.delete(0,'end')
    #
    # VOO_LRL.delete(0,'end')
    # VOO_URL.delete(0,'end')
    # VOO_VA.delete(0,'end')
    # VOO_VPW.delete(0,'end')
    #
    # AAI_LRL.delete(0,'end')
    # AAI_URL.delete(0,'end')
    # AAI_AA.delete(0,'end')
    # AAI_APW.delete(0,'end')
    # AAI_ARP.delete(0,'end')
    #
    # VVI_LRL.delete(0,'end')
    # VVI_URL.delete(0,'end')
    # VVI_VA.delete(0,'end')
    # VVI_VPW.delete(0,'end')
    # VVI_VRP.delete(0,'end')


def user_log_out():
    login_username.delete(0, 'end')
    login_password.delete(0, 'end')
    show_login_page()
    clear_entry()
def back_r():
    show_login_page()
    new_username.delete(0,'end')
    new_password.delete(0,'end')
def back_button():
    login_page.pack_forget()
    register_page.pack_forget()
    AOO_page.pack_forget()
    VOO_page.pack_forget()
    AAI_page.pack_forget()
    VVI_page.pack_forget()
    clear_entry()
    mode_page.pack()

def submit_aoo():
    valid = True
    invalid_input = False
    out_of_range = False

    # get user input
    aoo_lrl = AOO_LRL.get()
    aoo_url = AOO_URL.get()
    aoo_aa = AOO_AA.get()
    aoo_apw = AOO_APW.get()

    # Verify the lower rate limit parameter
    try:
        aoo_lrl = float(aoo_lrl)
        if not (30 <= aoo_lrl <= 175):
            # the input is out of range
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    # Verify the upper rate limit parameter
    try:
        aoo_url = float(aoo_url)
        if not (50 <= aoo_url <= 175):
            # the input is out of range
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True

    # Verify the atrial amplitude
    if aoo_aa == 'off':
        # the input can be "off"
        pass
    else:
        try:
            aoo_aa = float(aoo_aa)
            if not ((0.5 <= aoo_aa <= 3.2) or (3.5 <= aoo_aa <= 7)):
                # the input is out of range
                out_of_range = True
        except ValueError:
            # the input is neither a number nor "off"
            invalid_input = True
    # Verify the atrial pulse width
    try:
        aoo_apw = float(aoo_apw)
        if not (aoo_apw == 0.05 or (0.1 <= aoo_apw <= 1.9)):
            # the input is out of range
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    if invalid_input:
        messagebox.showerror("Erro", "Please entry a valid parameter")
    elif out_of_range:
        messagebox.showerror("Error", "Input parameter is out of range")
    else:
        with open('user_inputs.txt','w') as file:
            file.write(f"lower limit rate:{aoo_lrl} \n")
            file.write(f"upper limit rate:{aoo_url} \n")
            file.write(f"atrial amplitude:{aoo_aa} \n")
            file.write(f"atrial pulse width:{aoo_apw} \n")
        if refresh() == 1:
            messagebox.showinfo("Success", "Successfully submitted!")

def submit_voo():
    valid = True
    invalid_input = False
    out_of_range = False

    # get user input
    voo_lrl = VOO_LRL.get()
    voo_url = VOO_URL.get()
    voo_va = VOO_VA.get()
    voo_vpw = VOO_VPW.get()

    # Verify the lower rate limit parameter
    try:
        voo_lrl = float(voo_lrl)
        if not (30 <= voo_lrl <= 175):
            # the input is out of range
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    # Verify the upper rate limit parameter
    try:
        voo_url = float(voo_url)
        if not (50 <= voo_url <= 175):
            # the input is out of range
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    # Verify the ventricular amplitude
    if voo_va == 'off':
        # the input can be "off"
        pass
    else:
        try:
            voo_va = float(voo_va)
            if not ((0.5 <= voo_va <= 3.2) or (3.5 <= voo_va <= 7)):
                # the input is out of range
                out_of_range = True
        except ValueError:
            # the input is neither a number nor "off"
            invalid_input = True
    # Verify the ventricular pulse width
    try:
        voo_vpw = float(voo_vpw)
        if not (voo_vpw == 0.05 or (0.1 <= voo_vpw <= 1.9)):
            # the input is out of range
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    if invalid_input:
        messagebox.showerror("Erro", "Please entry a valid parameter")
    elif out_of_range:
        messagebox.showerror("Error", "Input parameter is out of range")
    else:
        with open('user_inputs.txt','w') as file:
            file.write(f"lower limit rate:{voo_lrl} \n")
            file.write(f"upper limit rate:{voo_lrl} \n")
            file.write(f"ventricular amplitude:{voo_va} \n")
            file.write(f"ventricular pulse width:{voo_vpw} \n")
        if refresh() == 1:
            messagebox.showinfo("Success", "Successfully submit!")

def submit_aai():
    valid = True
    invalid_input = False
    out_of_range = False

    # get user input
    aai_lrl = AAI_LRL.get()
    aai_url = AAI_URL.get()
    aai_aa = AAI_AA.get()
    aai_apw = AAI_APW.get()
    aai_arp = AAI_ARP.get()

    # Verify the lower rate limit parameter
    try:
        aai_lrl = float(aai_lrl)
        if not (30 <= aai_lrl <= 175):
            # the input is out of range
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    # Verify the upper rate limit parameter
    try:
        aai_url = float(aai_url)
        if not (50 <= aai_url <= 175):
            # the input is out of range
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True

    # Verify the atrial amplitude
    if aai_aa == 'off':
        # the input can be "off"
        pass
    else:
        try:
            aai_aa = float(aai_aa)
            if not ((0.5 <= aai_aa <= 3.2) or (3.5 <= aai_aa <= 7)):
                # the input is out of range
                out_of_range = True
        except ValueError:
            # the input is neither a number nor "off"
            invalid_input = True
    # Verify the atrial pulse width
    try:
        aai_apw = float(aai_apw)
        if not (aai_apw == 0.05 or (0.1 <= aai_apw <= 1.9)):
            # the input is out of range
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    try:
        aai_arp = float(aai_arp)
        if not(150 <= aai_arp <= 500):
            # the input is out of range
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True

    if invalid_input:
        messagebox.showerror("Erro", "Please entry a valid parameter")
    elif out_of_range:
        messagebox.showerror("Error", "Input parameter is out of range")
    elif refresh() == 1:
        with open('user_inputs.txt','w') as file:
            file.write(f"lower limit rate:{aai_lrl} \n")
            file.write(f"upper limit rate:{aai_url} \n")
            file.write(f"atrial amplitude:{aai_aa} \n")
            file.write(f"atrial pulse width:{aai_apw} \n")
            file.write(f"atrial refactory period:{aai_arp} \n")
            messagebox.showinfo("Success", "Successfully submit!")

def submit_vvi():
    valid = True
    invalid_input = False
    out_of_range = False

    # get user input
    vvi_lrl = VVI_LRL.get()
    vvi_url = VVI_URL.get()
    vvi_va = VVI_VA.get()
    vvi_vpw = VVI_VPW.get()
    vvi_vrp = VVI_VRP.get()

    # Verify the lower rate limit parameter
    try:
        vvi_lrl = float(vvi_lrl)
        if not (30 <= vvi_lrl <= 175):
            # the input is out of range
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    # Verify the upper rate limit parameter
    try:
        vvi_url = float(vvi_url)
        if not (50 <= vvi_url <= 175):
            # the input is out of range
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True

    # Verify the atrial amplitude
    if vvi_va == 'off':
        # the input can be "off"
        pass
    else:
        try:
            vvi_va = float(vvi_va)
            if not ((0.5 <= vvi_va <= 3.2) or (3.5 <= vvi_va <= 7)):
                # the input is out of range
                out_of_range = True
        except ValueError:
            # the input is neither a number nor "off"
            invalid_input = True
    # Verify the atrial pulse width
    try:
        vvi_vpw = float(vvi_vpw)
        if not (vvi_vpw == 0.05 or (0.1 <= vvi_vpw <= 1.9)):
            # the input is out of range
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    try:
        vvi_vrp = float(vvi_vrp)
        if not (150 <= vvi_vrp <= 500):
            # the input is out of range
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True

    if invalid_input:
        messagebox.showerror("Erro", "Please entry a valid parameter")
    elif out_of_range:
        messagebox.showerror("Error", "Input parameter is out of range")
    else:
        with open('user_inputs.txt','w') as file:
            file.write(f"lower limit rate:{vvi_lrl} \n")
            file.write(f"upper limit rate:{vvi_url} \n")
            file.write(f"ventricular amplitude:{vvi_va} \n")
            file.write(f"ventricular pulse width:{vvi_vpw} \n")
            file.write(f"ventricular refactory period:{vvi_vrp} \n")
        if refresh() == 1:
            messagebox.showinfo("Success", "Successfully submit!")

def AOO():
    login_page.pack_forget()
    mode_page.pack_forget()
    register_page.forget()
    AOO_page.pack()
def VOO():
    login_page.pack_forget()
    mode_page.pack_forget()
    register_page.forget()
    VOO_page.pack()
def AAI():
    login_page.pack_forget()
    mode_page.pack_forget()
    register_page.forget()
    AAI_page.pack()
def VVI():
    login_page.pack_forget()
    mode_page.pack_forget()
    register_page.forget()
    VVI_page.pack()

def refresh():
    try:
        ser = serial.Serial('COM3', 9600, timeout=0)
        if ser.is_open:
            messagebox.showinfo("Success", "Communicating")
            return 1
    except:
        messagebox.showerror("Error", "Serial port COM3 is not open")
        return 0
def check():
    messagebox.showinfo("Success", "The pacemaker has been the same")

# login page
login_page = customtkinter.CTkFrame(master=root)
login_page.pack(pady=20, padx=60, fill="both", expand=True)

login_label = customtkinter.CTkLabel(master=login_page, text="Pacemaker Login System", font=('Arial', 18))
login_label.pack(pady=12, padx=10)

login_username = customtkinter.CTkEntry(master=login_page, placeholder_text="Username")
login_username.pack(pady=12, padx=10)

login_password = customtkinter.CTkEntry(master=login_page, placeholder_text="Password", show="*")
login_password.pack(pady=12, padx=10)

login_button = customtkinter.CTkButton(master=login_page, command = login, text="Login", cursor ='hand2')
login_button.pack(pady=12, padx=10)

register_button = customtkinter.CTkButton(master=login_page, command = register, text="Register here", cursor ='hand2')
register_button.pack(pady=12, padx=10)


# register page
register_page = customtkinter.CTkFrame(master=root)
register_page.pack(pady=20, padx=60)#, fill="both", expand = True)
# register label
register_label = customtkinter.CTkLabel(master=register_page, text="Registration", font=('Arial', 18))
register_label.pack(pady=12, padx=10)
# new user name entry
new_username = customtkinter.CTkEntry(master=register_page, placeholder_text="New Username")
new_username.pack(pady=12, padx=10)
# new user name entry
new_password = customtkinter.CTkEntry(master=register_page, placeholder_text="New Password")
new_password.pack(pady=12,padx=10)
# click button to comfirm
confirm_button = customtkinter.CTkButton(master=register_page, text="Confirm", command=confirm)
confirm_button.pack(pady=12,padx=10)
# back button: back to login page from register page
back_r_button = customtkinter.CTkButton(master=register_page, text="Back", command = back_r)
back_r_button.pack(pady=12, padx=10)



# mode page
mode_page = customtkinter.CTkFrame(master=root)
mode_page.pack(pady=20, padx=60)#, fill="both", expand = True)
# output a label
label2 = customtkinter.CTkLabel(master=mode_page, text="Please select the mode of pacemaker")
label2.pack(pady=12, padx=10)
#AOO mode
AOO_button = customtkinter.CTkButton(master=mode_page, text="AOO", command=AOO)
AOO_button.pack(pady=12,padx=10)
#VOO mode
VOO_button = customtkinter.CTkButton(master=mode_page, text="VOO", command=VOO)
VOO_button.pack(pady=12,padx=10)
#AAI mode
AAI_button = customtkinter.CTkButton(master=mode_page, text="AAI", command=AAI)
AAI_button.pack(pady=12,padx=10)
#VVI mode
VVI_button = customtkinter.CTkButton(master=mode_page, text="VVI", command=VVI)
VVI_button.pack(pady=12,padx=10)
#back to login page from mode page
log_out = customtkinter.CTkButton(master=mode_page, text="Log out", command=user_log_out)
log_out.pack(pady=20, padx=10)
egram = customtkinter.CTkButton(master=mode_page, text="Egram")
egram.pack(pady=20, padx=10)
#check if the device is different than the previous one
check_device = customtkinter.CTkButton(master=mode_page, text="Check device", command=check)
check_device.pack(pady=20, padx=10)






#AOO page
AOO_page = customtkinter.CTkFrame(master=root)
AOO_page.pack(pady=1, padx=60)#, fill="both", expand = True)
# output a label
AOO_label = customtkinter.CTkLabel(master=AOO_page, text="Please Enter Parameters for AOO")
AOO_label.pack(pady=6, padx=10)
# Lower Rate Limit
AOO_label_LRL = customtkinter.CTkLabel(master=AOO_page, text="Lower Rate Limit (range: 30-175)")
AOO_label_LRL.pack(pady=6, padx=10)
AOO_LRL = customtkinter.CTkEntry(master=AOO_page, placeholder_text="Lower Rate Limit")
AOO_LRL.pack(pady=6, padx=10)
# Upper Rate Limit
AOO_label_URL = customtkinter.CTkLabel(master=AOO_page, text="Upper Rate Limit (range: 50-175)")
AOO_label_URL.pack(pady=6, padx=10)
AOO_URL = customtkinter.CTkEntry(master=AOO_page, placeholder_text="Upper Rate Limit")
AOO_URL.pack(pady=6, padx=10)
# Atrial Amplitude
AOO_label_AA = customtkinter.CTkLabel(master=AOO_page, text="Atrial Amplitude (range: off, 0.5-3.2, 3.5-7.0)")
AOO_label_AA.pack(pady=6, padx=10)
AOO_AA = customtkinter.CTkEntry(master=AOO_page, placeholder_text="Atrial Amplitude")
AOO_AA.pack(pady=6, padx=10)
# Atrial Amplitude
AOO_label_APW = customtkinter.CTkLabel(master=AOO_page, text="Arial Pulse Width (range: 0.05, 0.1-1.9)")
AOO_label_APW.pack(pady=6, padx=10)
AOO_APW = customtkinter.CTkEntry(master=AOO_page, placeholder_text="Arial Pulse Width")
AOO_APW.pack(pady=6, padx=10)
# submit
submit_aoo = customtkinter.CTkButton(master = AOO_page, text="Submit", command=submit_aoo)
submit_aoo.pack(pady=6, padx=10)
#back to mode page from AOO
back_aoo_button = customtkinter.CTkButton(master=AOO_page, text="Back", command = back_button)
back_aoo_button.pack(pady=6, padx=10)
#log out
log_out = customtkinter.CTkButton(master=AOO_page, text="Log out", command=user_log_out)
log_out.pack(pady=6, padx=10)








#VOO page
VOO_page = customtkinter.CTkFrame(master=root)
VOO_page.pack(pady=10, padx=60)#, fill="both", expand = True)
# output a label
VOO_label = customtkinter.CTkLabel(master=VOO_page, text="Please Enter Parameters for VOO")
VOO_label.pack(pady=6, padx=10)
# Lower Rate Limit
VOO_label_LRL = customtkinter.CTkLabel(master=VOO_page, text="Lower Rate Limit (range: 30-175)")
VOO_label_LRL.pack(pady=6, padx=10)
VOO_LRL = customtkinter.CTkEntry(master=VOO_page, placeholder_text="Lower Rate Limit")
VOO_LRL.pack(pady=6, padx=10)
# Upper Rate Limit
VOO_label_URL = customtkinter.CTkLabel(master=VOO_page, text="Upper Rate Limit (range: 50-175)")
VOO_label_URL.pack(pady=6, padx=10)
VOO_URL = customtkinter.CTkEntry(master=VOO_page, placeholder_text="Upper Rate Limit")
VOO_URL.pack(pady=6, padx=10)
# Ventricular Amplitude
VOO_label_VA = customtkinter.CTkLabel(master=VOO_page, text="Ventricular Amplitude (range: off, 0.5-3.2, 3.5-7.0)")
VOO_label_VA.pack(pady=6, padx=10)
VOO_VA = customtkinter.CTkEntry(master=VOO_page, placeholder_text="Ventricular Amplitude")
VOO_VA.pack(pady=6, padx=10)
# Ventricular Amplitude
VOO_label_VPW = customtkinter.CTkLabel(master=VOO_page, text="Ventricular Pulse Width (range: 0.05, 0.1-1.9)")
VOO_label_VPW.pack(pady=6, padx=10)
VOO_VPW = customtkinter.CTkEntry(master=VOO_page, placeholder_text="Ventricular Pulse Width")
VOO_VPW.pack(pady=6, padx=10)
#submit
submit_voo = customtkinter.CTkButton(master = VOO_page, text="Submit", command=submit_voo)
submit_voo.pack(pady=6, padx=10)
#back to mode page from AOO
back_voo_button = customtkinter.CTkButton(master=VOO_page, text="Back", command = back_button)
back_voo_button.pack(pady=6, padx=10)
#log out
log_out = customtkinter.CTkButton(master=VOO_page, text="Log out", command=user_log_out)
log_out.pack(pady=6, padx=10)






#AAI page
AAI_page = customtkinter.CTkFrame(master=root)
AAI_page.pack(pady=10, padx=60)#, fill="both", expand = True)
# output a label
AAI_label = customtkinter.CTkLabel(master=AAI_page, text="Please Enter Parameters for AAI")
AAI_label.pack(pady=6, padx=10)
# Lower Rate Limit
AAI_label_LRL = customtkinter.CTkLabel(master=AAI_page, text="Lower Rate Limit (range: 30-175)")
AAI_label_LRL.pack(pady=6, padx=10)
AAI_LRL = customtkinter.CTkEntry(master=AAI_page, placeholder_text="Lower Rate Limit")
AAI_LRL.pack(pady=6, padx=10)
# Upper Rate Limit
AAI_label_URL = customtkinter.CTkLabel(master=AAI_page, text="Upper Rate Limit (range: 50-175)")
AAI_label_URL.pack(pady=6, padx=10)
AAI_URL = customtkinter.CTkEntry(master=AAI_page, placeholder_text="Upper Rate Limit")
AAI_URL.pack(pady=6, padx=10)
# Atrial Amplitude
AAI_label_AA = customtkinter.CTkLabel(master=AAI_page, text="Atrial Amplitude (range: off, 0.5-3.2, 3.5-7.0)")
AAI_label_AA.pack(pady=6, padx=10)
AAI_AA = customtkinter.CTkEntry(master=AAI_page, placeholder_text="Atrial Amplitude")
AAI_AA.pack(pady=6, padx=10)
# Atrial Pulse Width
AAI_label_APW = customtkinter.CTkLabel(master=AAI_page, text="Atrial Pulse Width (range: 0.05, 0.1-1.9)")
AAI_label_APW.pack(pady=6, padx=10)
AAI_APW = customtkinter.CTkEntry(master=AAI_page, placeholder_text="Atrial Pulse Width")
AAI_APW.pack(pady=6, padx=10)
# ARP
AAI_label_ARP = customtkinter.CTkLabel(master=AAI_page, text="ARP (range: 150-500)")
AAI_label_ARP.pack(pady=6, padx=10)
AAI_ARP = customtkinter.CTkEntry(master=AAI_page, placeholder_text="ARP")
AAI_ARP.pack(pady=6, padx=10)
#submit
submit_aai = customtkinter.CTkButton(master = AAI_page, text="Submit", command=submit_aai)
submit_aai.pack(pady=6, padx=10)
#back to mode page from AOO
back_AAI_button = customtkinter.CTkButton(master=AAI_page, text="Back", command = back_button)
back_AAI_button.pack(pady=6, padx=10)
#log out
log_out = customtkinter.CTkButton(master=AAI_page, text="Log out", command=user_log_out)
log_out.pack(pady=6, padx=10)



#VVI page
VVI_page = customtkinter.CTkFrame(master=root)
VVI_page.pack(pady=10, padx=60)#, fill="both", expand = True)
# output a label
VVI_label = customtkinter.CTkLabel(master=VVI_page, text="Please Enter Parameters for VVI")
VVI_label.pack(pady=6, padx=10)
# Lower Rate Limit
VVI_label_LRL = customtkinter.CTkLabel(master=VVI_page, text="Lower Rate Limit (range: 30-175)")
VVI_label_LRL.pack(pady=6, padx=10)
VVI_LRL = customtkinter.CTkEntry(master=VVI_page, placeholder_text="Lower Rate Limit")
VVI_LRL.pack(pady=6, padx=10)
# Upper Rate Limit
VVI_label_URL = customtkinter.CTkLabel(master=VVI_page, text="Upper Rate Limit (range: 50-175)")
VVI_label_URL.pack(pady=6, padx=10)
VVI_URL = customtkinter.CTkEntry(master=VVI_page, placeholder_text="Upper Rate Limit")
VVI_URL.pack(pady=6, padx=10)
# Ventricular Amplitude
VVI_label_VA = customtkinter.CTkLabel(master=VVI_page, text="Ventricular Amplitude (range: off, 0.5-3.2, 3.5-7.0)")
VVI_label_VA.pack(pady=6, padx=10)
VVI_VA = customtkinter.CTkEntry(master=VVI_page, placeholder_text="Ventricular Amplitude")
VVI_VA.pack(pady=6, padx=10)
#   Ventricular Pulse Width
VVI_label_VPW = customtkinter.CTkLabel(master=VVI_page, text="Ventricular Pulse Width (range: 0.05, 0.1-1.9)")
VVI_label_VPW.pack(pady=6, padx=10)
VVI_VPW = customtkinter.CTkEntry(master=VVI_page, placeholder_text="Ventricular Pulse Width")
VVI_VPW.pack(pady=6, padx=10)
# VRP
VVI_label_VRP = customtkinter.CTkLabel(master=VVI_page, text="VRP (range: 150-500)")
VVI_label_VRP.pack(pady=6, padx=10)
VVI_VRP = customtkinter.CTkEntry(master=VVI_page, placeholder_text="VRP")
VVI_VRP.pack(pady=6, padx=10)
#submit
submit_vvi = customtkinter.CTkButton(master = VVI_page, text="Submit", command=submit_vvi)
submit_vvi.pack(pady=6,padx=10)
#back to mode page from AOO
back_VVI_button = customtkinter.CTkButton(master=VVI_page, text="Back", command = back_button)
back_VVI_button.pack(pady=6, padx=10)
#log out
log_out = customtkinter.CTkButton(master=VVI_page, text="Log out", command=user_log_out)
log_out.pack(pady=6, padx=10)


test()
show_login_page()
root.mainloop()
