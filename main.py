import customtkinter
import hashlib
import serial
#import serial.tools.list_ports
from tkinter import messagebox, Canvas, Scrollbar
import time
import threading
import tkinter as tk
#import usb.core
from DCM_serial import serial

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
    AOOR_page.pack_forget()
    VOOR_page.pack_forget()
    AAIR_page.pack_forget()
    VVIR_page.pack_forget()
    login_page.pack()

def save_users():
    with open("users.txt", 'a+') as file:
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
       # return
    if username in users:
        messagebox.showerror('Error', 'Username already exists.')
        register_page.pack()
      #  return

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
    load_users()
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

def user_log_out():
    login_username.delete(0, 'end')
    login_password.delete(0, 'end')
    show_login_page()

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
    AOOR_page.pack_forget()
    VOOR_page.pack_forget()
    AAIR_page.pack_forget()
    VVIR_page.pack_forget()
#    clear_entry()
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

        if (30 <= aoo_lrl <= 50) and (aoo_lrl%5 !=0):
            out_of_range = True
        elif (50 < aoo_lrl <= 90) and (aoo_lrl %1 != 0):
            out_of_range = True
        elif (90 < aoo_lrl <= 175) and (aoo_lrl % 5 != 0):
            out_of_range = True
        elif not(30 <= aoo_lrl <= 175):
            out_of_range =True
    except ValueError:
        # the input is not a number
        invalid_input = True
    # Verify the upper rate limit parameter
    try:
        aoo_url = float(aoo_url)
        if not (50 <= aoo_url <= 175):
            out_of_range = True
        elif (50 <= aoo_url <= 175) and (aoo_url % 5 != 0):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    # Verify the atrial amplitude
    try:
        aoo_aa = float(aoo_aa)
        if not (0 <= aoo_aa <= 100):
            out_of_range = True
        elif (0 <= aoo_aa <= 100) and (aoo_aa % 2 !=0):
            out_of_range =True
    except ValueError:
        # the input is neither a number nor "off"
        invalid_input = True
    # Verify the atrial pulse width
    try:
        aoo_apw = float(aoo_apw)
        if not (1 <= aoo_apw <= 30):
            out_of_range = True
        elif (1<= aoo_apw <= 30) and (aoo_apw %1 !=0):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    if invalid_input:
        messagebox.showerror("Error", "Please entry a valid parameter")
    elif out_of_range:
        messagebox.showerror("Error", "Input parameter is out of range")
    else:
        with open('user_inputs.txt','w') as file:
            file.write(f"lower limit rate:{aoo_lrl} \n")
            file.write(f"upper limit rate:{aoo_url} \n")
            file.write(f"atrial amplitude:{aoo_aa} \n")
            file.write(f"atrial pulse width:{aoo_apw} \n")
            serial(aoo_lrl, aoo_url, aoo_aa, aoo_apw, 0, 0, 0, 0)
        if refresh() == 1:
            messagebox.showinfo("Success", "Successfully submit!")

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
        if (30 <= voo_lrl <= 50) and (voo_lrl % 5 !=0):
            out_of_range = True
        elif (50 < voo_lrl <= 90) and (voo_lrl % 1 != 0):
            out_of_range = True
        elif (90 < voo_lrl <=175) and (voo_lrl % 5 !=0):
            out_of_range = True
        elif not(30 <= voo_lrl <= 175):
            out_of_range =True
    except ValueError:
        # the input is not a number
        invalid_input = True
    # Verify the upper rate limit parameter
    try:
        voo_url = float(voo_url)
        if (50 <= voo_url <= 175) and (voo_url % 5 !=0):
            out_of_range = True
        elif not (50 <= voo_url <= 175):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    # Verify the ventricular amplitude
    try:
        voo_va = float(voo_va)
        if (0 <= voo_va <= 100) and (voo_va % 2 != 0):
            out_of_range = True
        elif not (0 <= voo_va <= 100):
            out_of_range = True
    except ValueError:
            # the input is neither a number nor "off"
        invalid_input = True
    # Verify the ventricular pulse width
    try:
        voo_vpw = float(voo_vpw)
        if(1 <= voo_vpw <= 30) and (voo_vpw % 1 != 0):
            out_of_range = True
        elif not (1 <= voo_vpw <= 30):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    if invalid_input:
        messagebox.showerror("Error", "Please entry a valid parameter")
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
    aai_as = AAI_AS.get()
    aai_pvarp = AAI_PVARP.get()
    aai_h = AAI_H.get()
    aai_rs = AAI_RS.get()
    # Verify the lower rate limit parameter
    try:
        aai_lrl = float(aai_lrl)
        if (30 <= aai_lrl <= 50) and (aai_lrl % 5 !=0):
            out_of_range = True
        elif (50 < aai_lrl <= 90) and (aai_lrl % 1 != 0):
            out_of_range = True
        elif (90 < aai_lrl <=175) and (aai_lrl % 5 !=0):
            out_of_range = True
        elif not(30 <= aai_lrl <= 175):
            out_of_range =True
    except ValueError:
        # the input is not a number
        invalid_input = True
    # Verify the upper rate limit parameter
    try:
        aai_url = float(aai_url)
        if (50 <= aai_url <= 175) and (aai_url % 5 !=0):
            out_of_range = True
        elif not (50 <= aai_url <= 175):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True

    # Verify the atrial amplitude
    try:
        aai_aa = float(aai_aa)
        if (0 <= aai_aa <= 100) and (aai_aa % 2 != 0):
            out_of_range = True
        elif not (0 <= aai_aa <= 100):
            out_of_range = True
    except ValueError:
            # the input is neither a number nor "off"
        invalid_input = True
    # Verify the atrial pulse width
    try:
        aai_apw = float(aai_apw)
        if (1 <= aai_apw <= 30) and (aai_apw % 1 != 0):
            out_of_range = True
        elif not (1 <= aai_apw <= 30):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    try:
        aai_arp = float(aai_arp)
        if (150 <= aai_arp <= 500) and (aai_arp % 10 != 0):
            out_of_range = True
        elif not (150 <= aai_arp <= 500):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    #Verify the atrial sensitivity
    try:
        aai_as = float(aai_as)
        if (0 <=aai_as<= 100) and (aai_as % 2 != 0):
            out_of_range = True
        elif not (0 <=aai_as<= 100):
            out_of_range =True
    except ValueError:
        invalid_input = True
    #Verify the PVARP
    try:
        aai_pvarp = float(aai_pvarp)
        if (150<= aai_pvarp <=500 ) and (aai_pvarp % 10 != 0):
            out_of_range = True
        elif not (150<= aai_pvarp <=500 ):
            out_of_range = True
    except ValueError:
        invalid_input = True
    # Verify the Hysteresis
    if aai_h == 'off':
        # the input can be "off"
        pass
    else:
        try:
            aai_h = float(aai_h)
            if not (((30<=aai_lrl<=50)and(30<=aai_h<=50)) or ((50<=aai_lrl<=90)and(50<=aai_h<=90)) or ((90<=aai_lrl<=175)and(90<=aai_h<=175))):
                # the input is out of range
                out_of_range = True
        except ValueError:
            # the input is neither a number nor "off"
            invalid_input = True
    #Verify the Rate Smoothing
    if aai_rs == 'off':
        pass
    else:
        try:
            aai_rs = float(aai_rs)
            if not(aai_rs == 3.0 or aai_rs == 6.0 or aai_rs == 9.0 or aai_rs == 12.0 or aai_rs == 15.0 or aai_rs == 18.0 or aai_rs == 21.0 or aai_rs == 25.0):
                out_of_range = True
        except ValueError:
            invalid_input = True

    if invalid_input:
        messagebox.showerror("Error", "Please entry a valid parameter")
    elif out_of_range:
        messagebox.showerror("Error", "Input parameter is out of range")
    else:
        with open('user_inputs.txt','w') as file:
            file.write(f"lower limit rate:{aai_lrl} \n")
            file.write(f"upper limit rate:{aai_url} \n")
            file.write(f"atrial amplitude:{aai_aa} \n")
            file.write(f"atrial pulse width:{aai_apw} \n")
            file.write(f"atrial refactory period:{aai_arp} \n")
            file.write(f"atrial sensitivity:{aai_as} \n")
            file.write(f"PVARP:{aai_pvarp} \n")
            file.write(f"Hysteresis:{aai_h} \n")
            file.write(f"Rate smoothing:{aai_rs} \n")
        if refresh() == 1:
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
    vvi_vs = VVI_VS.get()
    vvi_h = VVI_H.get()
    vvi_rs = VVI_RS.get()
    # Verify the lower rate limit parameter
    try:
        vvi_lrl = float(vvi_lrl)
        if (30 <= vvi_lrl <= 50) and (vvi_lrl %5 !=0):
            # the input is out of range
            out_of_range = True
        elif (50 < vvi_lrl <= 90) and (vvi_lrl %1 !=0):
            out_of_range = True
        elif (90 < vvi_lrl <= 150) and (vvi_lrl %5 != 0):
            out_of_range = True
        elif not (30 <= vvi_lrl <= 50):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    # Verify the upper rate limit parameter
    try:
        vvi_url = float(vvi_url)
        if(50 <= vvi_url <= 175) and (vvi_lrl %5 !=0):
            # the input is out of range
            out_of_range = True
        elif not(50 <= vvi_url <= 175):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True

    # Verify the atrial amplitude
    try:
        vvi_va = float(vvi_va)
        if (0 <= vvi_va <= 100) and  (vvi_va %2 !=0):
                # the input is out of range
            out_of_range = True
        elif not (0 <= vvi_va <= 100):
            out_of_range = True
    except ValueError:
            # the input is neither a number nor "off"
        invalid_input = True
    # Verify the atrial pulse width
    try:
        vvi_vpw = float(vvi_vpw)
        if (1 <= vvi_vpw <= 30) and (vvi_vpw %1 != 0):
            # the input is out of range
            out_of_range = True
        elif not (1 <= vvi_vpw <= 30):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    try:
        vvi_vrp = float(vvi_vrp)
        if (150 <= vvi_vrp <= 500) and (vvi_vrp%10 !=0):
            # the input is out of range
            out_of_range = True
        elif not (150 <= vvi_vrp <= 500):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    #Verify the ventricular sensitivity
    try:
        vvi_vs = float(vvi_vs)
        if(0<=vvi_vs<=100) and (vvi_vs %2 !=0):
            out_of_range = True
        elif not (0<=vvi_vs<=100) :
            out_of_range = True
    except ValueError:
        invalid_input = True
    # Verify the Hysteresis
    if vvi_h == 'off':
        # the input can be "off"
        pass
    else:
        try:
            vvi_h = float(vvi_h)
            if not (((30<=vvi_lrl<=50)and(30<=vvi_h<=50)) or ((50<=vvi_lrl<=90)and(50<=vvi_h<=90)) or ((90<=vvi_lrl<=175)and(90<=vvi_h<=175))):
                # the input is out of range
                out_of_range = True
        except ValueError:
            # the input is neither a number nor "off"
            invalid_input = True
    #Verify the Rate Smoothing
    if vvi_rs == 'off':
        pass
    else:
        try:
            vvi_rs = float(vvi_rs)
            if not(vvi_rs == 3.0 or vvi_rs == 6.0 or vvi_rs == 9.0 or vvi_rs == 12.0 or vvi_rs == 15.0 or vvi_rs == 18.0 or vvi_rs == 21.0 or vvi_rs == 25.0):
                out_of_range = True
        except ValueError:
            invalid_input = True

    if invalid_input:
        messagebox.showerror("Error", "Please entry a valid parameter")
    elif out_of_range:
        messagebox.showerror("Error", "Input parameter is out of range")
    else:
        with open('user_inputs.txt','w') as file:
            file.write(f"lower limit rate:{vvi_lrl} \n")
            file.write(f"upper limit rate:{vvi_url} \n")
            file.write(f"ventricular amplitude:{vvi_va} \n")
            file.write(f"ventricular pulse width:{vvi_vpw} \n")
            file.write(f"ventricular refactory period:{vvi_vrp} \n")
            file.write(f"ventricular sensitivity:{vvi_vs} \n")
            file.write(f"hysteresis:{vvi_h} \n")
            file.write(f"rate smoothing:{vvi_rs} \n")
        if refresh() == 1:
            messagebox.showinfo("Success", "Successfully submit!")

def submit_aoor():
    valid = True
    invalid_input = False
    out_of_range = False

    # get user input
    aoor_lrl = AOOR_LRL.get()
    aoor_url = AOOR_URL.get()
    aoor_aa = AOOR_AA.get()
    aoor_apw = AOOR_APW.get()
    aoor_msr = AOOR_MSR.get()
    aoor_at = AOOR_AT.get()
    aoor_reactionT = AOOR_ReactionT.get()
    aoor_rf = AOOR_RF.get()
    aoor_recoveryT = AOOR_RecoveryT.get()

    # Verify the lower rate limit parameter
    try:
        aoor_lrl = float(aoor_lrl)
        if (30 <= aoor_lrl <= 50) and (aoor_lrl % 5 != 0):
            # the input is out of range
            out_of_range = True
        elif (50 < aoor_lrl <= 90) and (aoor_lrl %1 != 0):
            out_of_range = True
        elif(90 < aoor_lrl <= 175) and (aoor_lrl %5 !=0):
            out_of_range = True
        elif not(30 <= aoor_lrl <= 175):
            out_of_range =True
    except ValueError:
        # the input is not a number
        invalid_input = True
    # Verify the upper rate limit parameter
    try:
        aoor_url = float(aoor_url)
        if (50 <= aoor_url <= 175) and (aoor_url %5 != 0):
            # the input is out of range
            out_of_range = True
        elif not (50 <= aoor_url <= 175):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True

    # Verify the atrial amplitude
    try:
        aoor_aa = float(aoor_aa)
        if (0 <= aoor_aa <= 100) and (aoor_aa %2 != 0):
            # the input is out of range
            out_of_range = True
        elif not (0 <=aoor_aa <= 100):
            out_of_range = True
    except ValueError:
            # the input is neither a number nor "off"
        invalid_input = True
    # Verify the atrial pulse width
    try:
        aoor_apw = float(aoor_apw)
        if (1 <= aoor_apw <= 30) and (aoor_apw % 1 != 0):
            # the input is out of range
            out_of_range = True
        elif not(1 <= aoor_apw <= 30):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True

    # Verify the Maximum Sensor Rate
    try:
        aoor_msr = float(aoor_msr)
        if (50 <= aoor_msr <= 175) and (aoor_msr %5 !=0):
            # the input is out of range
            out_of_range = True
        elif not (50 <= aoor_msr <= 175):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True

    # Verify the Reaction Time
    try:
        aoor_reactionT = float(aoor_reactionT)
        if (10 <= aoor_reactionT <= 50) and (aoor_reactionT % 10 !=0):
            # the input is out of range
            out_of_range = True
        elif not(10 <= aoor_reactionT <= 50):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    # Verify the Response Factor
    try:
        aoor_rf= float(aoor_rf)
        if (1 <= aoor_rf <= 16) and (aoor_rf % 1 != 0):
            # the input is out of range
            out_of_range = True
        elif not(1<= aoor_rf <= 16):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    # Verify the Recovery Time
    try:
        aoor_recoveryT= float(aoor_recoveryT)
        if (2 <= aoor_recoveryT <= 16) and (aoor_recoveryT % 1 !=0):
            # the input is out of range
            out_of_range = True
        elif not (2 <= aoor_recoveryT <= 16):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    # Verify the Recovery Time
    if aoor_at not in ["V-Low","Low","Med-Low","Med","Med-High","High","V-high"]:
        invalid_input = True
    if invalid_input:
        messagebox.showerror("Error", "Please entry a valid parameter")
    elif out_of_range:
        messagebox.showerror("Error", "Input parameter is out of range")
    else:
        with open('user_inputs.txt','w') as file:
            file.write(f"lower limit rate:{aoor_lrl} \n")
            file.write(f"upper limit rate:{aoor_url} \n")
            file.write(f"atrial amplitude:{aoor_aa} \n")
            file.write(f"atrial pulse width:{aoor_apw} \n")

            file.write(f"maximum sensor rate:{aoor_msr} \n")
            file.write(f"activity threshold:{aoor_at} \n")
            file.write(f"reaction time:{aoor_reactionT} \n")
            file.write(f"response factor:{aoor_rf} \n")
            file.write(f"recovery time:{aoor_recoveryT} \n")

        if refresh() == 1:
            messagebox.showinfo("Success", "Successfully submit!")

def submit_voor():
    valid = True
    invalid_input = False
    out_of_range = False

    # get user input
    voor_lrl = VOOR_LRL.get()
    voor_url = VOOR_URL.get()
    voor_va = VOOR_VA.get()
    voor_vpw = VOOR_VPW.get()
    voor_msr = VOOR_MSR.get()
    voor_at = VOOR_AT.get()
    voor_reactionT = VOOR_ReactionT.get()
    voor_rf = VOOR_RF.get()
    voor_recoveryT = VOOR_RecoveryT.get()

    # Verify the lower rate limit parameter
    try:
        voor_lrl = float(voor_lrl)
        if (30 <= voor_lrl <= 50) and (voor_lrl % 5 != 0):
            # the input is out of range
            out_of_range = True
        elif(50 < voor_lrl <= 90) and (voor_lrl %1 != 0):
            out_of_range = True
        elif(90 < voor_lrl <= 175) and (voor_lrl %5 != 0):
            out_of_range = True
        elif not (30 <= voor_lrl <= 175):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    # Verify the upper rate limit parameter
    try:
        voor_url = float(voor_url)
        if (50 <= voor_url <= 175) and (voor_url %5 !=0):
            # the input is out of range
            out_of_range = True
        elif not (50 <= voor_url <= 175):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    # Verify the ventricular amplitude

    try:
        voor_va = float(voor_va)
        if  (0 <= voor_va <= 100) and (voor_va % 2 != 0):
                # the input is out of range
            out_of_range = True
        elif not (0 <= voor_va <= 100):
            out_of_range = True
    except ValueError:
            # the input is neither a number nor "off"
        nvalid_input = True
    # Verify the ventricular pulse width
    try:
        voor_vpw = float(voor_vpw)
        if (1 <= voor_vpw <= 30) and  (voor_vpw % 1 != 0):
            # the input is out of range
            out_of_range = True
        elif not (1<=voor_vpw<=30):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    # Verify the Maximum Sensor Rate
    try:
        voor_msr = float(voor_msr)
        if (50 <= voor_msr <= 175) and (voor_msr % 5 !=0):
            # the input is out of range
            out_of_range = True
        elif not (50 <= voor_msr <= 175):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True

    # Verify the Reaction Time
    try:
        voor_reactionT = float(voor_reactionT)
        if (10 <= voor_reactionT <= 50) and (voor_reactionT % 10 != 0):
            # the input is out of range
            out_of_range = True
        elif not (10<=voor_reactionT<=50):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    # Verify the Response Factor
    try:
        voor_rf= float(voor_rf)
        if (1 <= voor_rf <= 16) and (voor_rf % 1 != 0):
            # the input is out of range
            out_of_range = True
        elif not (1 <= voor_rf <= 16):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    # Verify the Recovery Time
    try:
        voor_recoveryT= float(voor_recoveryT)
        if (2 <= voor_recoveryT <= 16) and (voor_recoveryT %1 !=0):
            # the input is out of range
            out_of_range = True
        elif not (2<= voor_recoveryT <=16):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    # Verify the Recovery Time
    if voor_at not in ["V-Low","Low","Med-Low","Med","Med-High","High","V-high"]:
        invalid_input = True
    if invalid_input:
        messagebox.showerror("Error", "Please entry a valid parameter")
    elif out_of_range:
        messagebox.showerror("Error", "Input parameter is out of range")
    else:
        with open('user_inputs.txt','w') as file:
            file.write(f"lower limit rate:{voor_lrl} \n")
            file.write(f"upper limit rate:{voor_lrl} \n")
            file.write(f"ventricular amplitude:{voor_va} \n")
            file.write(f"ventricular pulse width:{voor_vpw} \n")

            file.write(f"maximum sensor rate:{voor_msr} \n")
            file.write(f"activity threshold:{voor_at} \n")
            file.write(f"reaction time:{voor_reactionT} \n")
            file.write(f"response factor:{voor_rf} \n")
            file.write(f"recovery time:{voor_recoveryT} \n")
        if refresh() == 1:
            messagebox.showinfo("Success", "Successfully submit!")

def submit_aair():
    valid = True
    invalid_input = False
    out_of_range = False

    # get user input
    aair_lrl = AAIR_LRL.get()
    aair_url = AAIR_URL.get()
    aair_aa = AAIR_AA.get()
    aair_apw = AAIR_APW.get()
    aair_arp = AAIR_ARP.get()
    aair_as = AAIR_AS.get()
    aair_pvarp = AAIR_PVARP.get()
    aair_h = AAIR_H.get()
    aair_rs = AAIR_RS.get()
    aair_msr = AAIR_MSR.get()
    aair_at = AAIR_AT.get()
    aair_reactionT = AAIR_ReactionT.get()
    aair_rf = AAIR_RF.get()
    aair_recoveryT = AAIR_RecoveryT.get()
    # Verify the lower rate limit parameter
    try:
        aair_lrl = float(aair_lrl)
        if (30 <= aair_lrl <= 50) and (aair_lrl %5 !=0):
            # the input is out of range
            out_of_range = True
        elif (50 < aair_lrl <= 90) and (aair_lrl % 1 !=0):
            out_of_range = True
        elif(90 < aair_lrl <= 175) and(aair_lrl % 5 !=0):
            out_of_range = True
        elif not (30<= aair_lrl <=175):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    # Verify the upper rate limit parameter
    try:
        aair_url = float(aair_url)
        if (50 <= aair_url <= 175) and (aair_url %5 !=0):
            # the input is out of range
            out_of_range = True
        elif not (50 <= aair_url <= 175):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True

    # Verify the atrial amplitude
    try:
        aair_aa = float(aair_aa)
        if (0 <= aair_aa <= 100) and (aair_aa % 2 != 0):
                # the input is out of range
            out_of_range = True
        elif not (0 <= aair_aa <= 100):
            out_of_range = True
    except ValueError:
            # the input is neither a number nor "off"
        invalid_input = True
    # Verify the atrial pulse width
    try:
        aair_apw = float(aair_apw)
        if (1 <= aair_apw <= 30) and (aair_apw %1 != 0):
            # the input is out of range
            out_of_range = True
        elif not (1 <= aair_apw <= 30):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    try:
        aair_arp = float(aair_arp)
        if (150 <= aair_arp <= 500) and (aair_arp %10 != 0):
            # the input is out of range
            out_of_range = True
        elif not (150 <= aair_arp <= 500):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    #Verify the atrial sensitivity
    try:
        aair_as = float(aair_as)
        if (0 <=aair_as<= 100) and (aair_as %2 !=0):
            out_of_range = True
        elif (0 <=aair_as<= 100):
            out_of_range = True
    except ValueError:
        invalid_input = True
    #Verify the PVARP
    try:
        aair_pvarp = float(aair_pvarp)
        if (150<= aair_pvarp <=500 ) and (aair_pvarp %10 !=0):
            out_of_range = True
        elif not (150<= aair_pvarp <=500):
            out_of_range = True
    except ValueError:
        invalid_input = True
    # Verify the Hysteresis
    if aair_h == 'off':
        # the input can be "off"
        pass
    else:
        try:
            aair_h = float(aair_h)
            if not (((30<=aair_lrl<=50)and(30<=aair_h<=50)) or ((50<=aair_lrl<=90)and(50<=aair_h<=90)) or ((90<=aair_lrl<=175)and(90<=aair_h<=175))):
                # the input is out of range
                out_of_range = True
        except ValueError:
            # the input is neither a number nor "off"
            invalid_input = True
    #Verify the Rate Smoothing
    if aair_rs == 'off':
        pass
    else:
        try:
            aair_rs = float(aair_rs)
            if not(aair_rs == 3.0 or aair_rs == 6.0 or aair_rs == 9.0 or aair_rs == 12.0 or aair_rs == 15.0 or aair_rs == 18.0 or aair_rs == 21.0 or aair_rs == 25.0):
                out_of_range = True
        except ValueError:
            invalid_input = True
    # Verify the Maximum Sensor Rate
    try:
        aair_msr = float(aair_msr)
        if (50 <= aair_msr <= 175) and (aair_msr %5 !=0):
            # the input is out of range
            out_of_range = True
        elif not (50 <= aair_msr <= 175):
            out_of_range =True
    except ValueError:
        # the input is not a number
        invalid_input = True

    # Verify the Reaction Time
    try:
        aair_reactionT = float(aair_reactionT)
        if  (10 <= aair_reactionT <= 50) and (aair_reactionT %10 !=0):
            # the input is out of range
            out_of_range = True
        elif not (10 <= aair_reactionT <= 50):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    # Verify the Response Factor
    try:
        aair_rf= float(aair_rf)
        if (1 <= aair_rf <= 16) and (aair_rf %1 != 0):
            # the input is out of range
            out_of_range = True
        elif not (1<=aair_rf<=16):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    # Verify the Recovery Time
    try:
        aair_recoveryT= float(aair_recoveryT)
        if  (2 <= aair_recoveryT <= 16) and (aair_recoveryT %1 !=0):
            # the input is out of range
            out_of_range = True
        elif not (2 <= aair_recoveryT <= 16):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    # Verify the Recovery Time
    if aair_at not in ["V-Low","Low","Med-Low","Med","Med-High","High","V-high"]:
        invalid_input = True
    if invalid_input:
        messagebox.showerror("Error", "Please entry a valid parameter")
    elif out_of_range:
        messagebox.showerror("Error", "Input parameter is out of range")
    else:
        with open('user_inputs.txt','w') as file:
            file.write(f"lower limit rate:{aair_lrl} \n")
            file.write(f"upper limit rate:{aair_url} \n")
            file.write(f"atrial amplitude:{aair_aa} \n")
            file.write(f"atrial pulse width:{aair_apw} \n")
            file.write(f"atrial refactory period:{aair_arp} \n")
            file.write(f"atrial sensitivity:{aair_as} \n")
            file.write(f"PVARP:{aair_pvarp} \n")
            file.write(f"Hysteresis:{aair_h} \n")
            file.write(f"Rate smoothing:{aair_rs} \n")

            file.write(f"maximum sensor rate:{aair_msr} \n")
            file.write(f"activity threshold:{aair_at} \n")
            file.write(f"reaction time:{aair_reactionT} \n")
            file.write(f"response factor:{aair_rf} \n")
            file.write(f"recovery time:{aair_recoveryT} \n")
        if refresh() == 1:
            messagebox.showinfo("Success", "Successfully submit!")

def submit_vvir():
    valid = True
    invalid_input = False
    out_of_range = False

    # get user input
    vvir_lrl = VVIR_LRL.get()
    vvir_url = VVIR_URL.get()
    vvir_va = VVIR_VA.get()
    vvir_vpw = VVIR_VPW.get()
    vvir_vrp = VVIR_VRP.get()
    vvir_vs = VVIR_VS.get()
    vvir_h = VVIR_H.get()
    vvir_rs = VVIR_RS.get()
    vvir_msr = VVIR_MSR.get()
    vvir_at = VVIR_AT.get()
    vvir_reactionT = VVIR_ReactionT.get()
    vvir_rf = VVIR_RF.get()
    vvir_recoveryT = VVIR_RecoveryT.get()
    # Verify the lower rate limit parameter
    try:
        vvir_lrl = float(vvir_lrl)
        if (30 <= vvir_lrl <= 50) and (vvir_lrl %5 != 0):
            # the input is out of range
            out_of_range = True
        elif (50< vvir_lrl <= 90) and (vvir_lrl %1!=0):
            out_of_range = True
        elif (90<vvir_lrl<= 175) and (vvir_lrl %5 !=0):
            out_of_range = True
        elif not (30 <= vvir_lrl <= 175):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    # Verify the upper rate limit parameter
    try:
        vvir_url = float(vvir_url)
        if (50 <= vvir_url <= 175) and (vvir_url %5 !=0):
            # the input is out of range
            out_of_range = True
        elif not (50 <= vvir_url <= 175):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True

    # Verify the atrial amplitude
    try:
        vvir_va = float(vvir_va)
        if (0 <= vvir_va <= 100) and (vvir_va %2 !=0):
                # the input is out of range
            out_of_range = True
        elif not (0 <= vvir_va <= 100):
            out_of_range = True
    except ValueError:
            # the input is neither a number nor "off"
        invalid_input = True
    # Verify the atrial pulse width
    try:
        vvir_vpw = float(vvir_vpw)
        if (1 <= vvir_vpw <= 30) and (vvir_vpw %1 != 0):
            # the input is out of range
            out_of_range = True
        elif not (1<= vvir_vpw <= 30):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    try:
        vvir_vrp = float(vvir_vrp)
        if (150 <= vvir_vrp <= 500) and (vvir_vrp%10 != 0):
            # the input is out of range
            out_of_range = True
        elif not (150 <= vvir_vrp <= 500):
            out_of_range =True
    except ValueError:
        # the input is not a number
        invalid_input = True
    #Verify the ventricular sensitivity
    try:
        vvir_vs = float(vvir_vs)
        if (0<=vvir_vs<=100) and (vvir_vs %2 !=0):
            out_of_range = True
        elif not (0<= vvir_vs <= 100):
            out_of_range = True
    except ValueError:
        invalid_input = True
    # Verify the Hysteresis
    if vvir_h == 'off':
        # the input can be "off"
        pass
    else:
        try:
            vvi_h = float(vvir_h)
            if not (((30<=vvir_lrl<=50)and(30<=vvir_h<=50)) or ((50<=vvir_lrl<=90)and(50<=vvir_h<=90)) or ((90<=vvir_lrl<=175)and(90<=vvir_h<=175))):
                # the input is out of range
                out_of_range = True
        except ValueError:
            # the input is neither a number nor "off"
            invalid_input = True
    # Verify the Maximum Sensor Rate
    try:
        vvir_msr = float(vvir_msr)
        if (50 <= vvir_msr <= 175) and (vvir_msr %5 !=0):
            # the input is out of range
            out_of_range = True
        elif not (50 <= vvir_msr<=175):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True

    # Verify the Reaction Time
    try:
        vvir_reactionT = float(vvir_reactionT)
        if (10 <= vvir_reactionT <= 50) and (vvir_recoveryT %10 != 0):
            # the input is out of range
            out_of_range = True
        elif not (10 <= vvir_reactionT <= 50):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    # Verify the Response Factor
    try:
        vvir_rf= float(vvir_rf)
        if (1 <= vvir_rf <= 16) and (vvir_rf %1 != 0):
            # the input is out of range
            out_of_range = True
        elif not (1 <= vvir_rf <= 16) :
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    # Verify the Recovery Time
    try:
        vvir_recoveryT= float(vvir_recoveryT)
        if (2 <= vvir_recoveryT <= 16) and (vvir_recoveryT %1 !=0):
            # the input is out of range
            out_of_range = True
        elif not (2 <= vvir_recoveryT <= 16):
            out_of_range = True
    except ValueError:
        # the input is not a number
        invalid_input = True
    # Verify the Recovery Time
    if vvir_at not in ["V-Low","Low","Med-Low","Med","Med-High","High","V-high"]:
        invalid_input = True
    #Verify the Rate Smoothing
    if vvir_rs == 'off':
        pass
    else:
        try:
            vvir_rs = float(vvir_rs)
            if not(vvir_rs == 3.0 or vvir_rs == 6.0 or vvir_rs == 9.0 or vvir_rs == 12.0 or vvir_rs == 15.0 or vvir_rs == 18.0 or vvir_rs == 21.0 or vvir_rs == 25.0):
                out_of_range = True
        except ValueError:
            invalid_input = True

    if invalid_input:
        messagebox.showerror("Error", "Please entry a valid parameter")
    elif out_of_range:
        messagebox.showerror("Error", "Input parameter is out of range")
    else:
        with open('user_inputs.txt','w') as file:
            file.write(f"lower limit rate:{vvir_lrl} \n")
            file.write(f"upper limit rate:{vvir_url} \n")
            file.write(f"ventricular amplitude:{vvir_va} \n")
            file.write(f"ventricular pulse width:{vvir_vpw} \n")
            file.write(f"ventricular refactory period:{vvir_vrp} \n")
            file.write(f"ventricular sensitivity:{vvir_vs} \n")
            file.write(f"hysteresis:{vvir_h} \n")
            file.write(f"rate smoothing:{vvir_rs} \n")

            file.write(f"maximum sensor rate:{vvir_msr} \n")
            file.write(f"activity threshold:{vvir_at} \n")
            file.write(f"reaction time:{vvir_reactionT} \n")
            file.write(f"response factor:{vvir_rf} \n")
            file.write(f"recovery time:{vvir_recoveryT} \n")
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
def AOOR():
    login_page.pack_forget()
    mode_page.pack_forget()
    register_page.forget()
    AOOR_page.pack()
def VOOR():
    login_page.pack_forget()
    mode_page.pack_forget()
    register_page.forget()
    VOOR_page.pack()
def AAIR():
    login_page.pack_forget()
    mode_page.pack_forget()
    register_page.forget()
    AAIR_page.pack()
def VVIR():
    login_page.pack_forget()
    mode_page.pack_forget()
    register_page.forget()
    VVIR_page.pack()
def refresh():
    try:
        ser = serial.Serial('COM12', 115200, timeout=0)
        if ser.is_open:
            messagebox.showinfo("Success", "Communicating")
            return 1
    except:
        messagebox.showerror("Error", "Serial port COM3 is not open")
        return 0
def check():
    messagebox.showinfo("Success", "The pacemaker has been the same")


###################################login page##########################################
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


###################################register page##########################################
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



################################### mode page##########################################
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

#AOOR mode
AOOR_button = customtkinter.CTkButton(master=mode_page, text="AOOR", command=AOOR)
AOOR_button.pack(pady=12,padx=10)
#VOOR mode
VOOR_button = customtkinter.CTkButton(master=mode_page, text="VOOR", command=VOOR)
VOOR_button.pack(pady=12,padx=10)
#AAIR mode
AAIR_button = customtkinter.CTkButton(master=mode_page, text="AAIR", command=AAIR)
AAIR_button.pack(pady=12,padx=10)
#VVIR mode
VVIR_button = customtkinter.CTkButton(master=mode_page, text="VVIR", command=VVIR)
VVIR_button.pack(pady=12,padx=10)
#back to login page from mode page
log_out = customtkinter.CTkButton(master=mode_page, text="Log out", command=user_log_out)
log_out.pack(pady=12, padx=10)
#check if the device is different than the previous one
check_device = customtkinter.CTkButton(master=mode_page, text="Check device", command=check)
check_device.pack(pady=12, padx=10)
A_button = customtkinter.CTkButton(master=mode_page, text="Atrial Button")
A_button.pack(pady=12,padx=10)
V_button = customtkinter.CTkButton(master=mode_page, text="Ventricular Button")
V_button.pack(pady=12,padx=10)





################################### AOO page##########################################
AOO_page = customtkinter.CTkFrame(master=root)
AOO_page.pack(pady=10, padx=60)#, fill="both", expand = True)
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
AOO_label_AA = customtkinter.CTkLabel(master=AOO_page, text="Atrial Amplitude (range: 0-100)")
AOO_label_AA.pack(pady=6, padx=10)
AOO_AA = customtkinter.CTkEntry(master=AOO_page, placeholder_text="Atrial Amplitude")
AOO_AA.pack(pady=6, padx=10)
# Atrial Amplitude
AOO_label_APW = customtkinter.CTkLabel(master=AOO_page, text="Arial Pulse Width (range: 1-30)")
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








################################### VVO page##########################################
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
VOO_label_VA = customtkinter.CTkLabel(master=VOO_page, text="Ventricular Amplitude (range: 0-100)")
VOO_label_VA.pack(pady=6, padx=10)
VOO_VA = customtkinter.CTkEntry(master=VOO_page, placeholder_text="Ventricular Amplitude")
VOO_VA.pack(pady=6, padx=10)
# Ventricular Amplitude
VOO_label_VPW = customtkinter.CTkLabel(master=VOO_page, text="Ventricular Pulse Width (range: 1-30)")
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





################################### AAI page##########################################
AAI_page = customtkinter.CTkFrame(master=root)
AAI_page.pack(pady=6, padx=60)#, fill="both", expand = True)
# output a label
AAI_label = customtkinter.CTkLabel(master=AAI_page, text="Please Enter Parameters for AAI")
AAI_label.pack(pady=2, padx=10)
# Lower Rate Limit
AAI_label_LRL = customtkinter.CTkLabel(master=AAI_page, text="Lower Rate Limit (range: 30-175)")
AAI_label_LRL.pack(pady=2, padx=10)
AAI_LRL = customtkinter.CTkEntry(master=AAI_page, placeholder_text="Lower Rate Limit")
AAI_LRL.pack(pady=2, padx=10)
# Upper Rate Limit
AAI_label_URL = customtkinter.CTkLabel(master=AAI_page, text="Upper Rate Limit (range: 50-175)")
AAI_label_URL.pack(pady=2, padx=10)
AAI_URL = customtkinter.CTkEntry(master=AAI_page, placeholder_text="Upper Rate Limit")
AAI_URL.pack(pady=2, padx=10)
# Atrial Amplitude
AAI_label_AA = customtkinter.CTkLabel(master=AAI_page, text="Atrial Amplitude (range: 0-100)")
AAI_label_AA.pack(pady=2, padx=10)
AAI_AA = customtkinter.CTkEntry(master=AAI_page, placeholder_text="Atrial Amplitude")
AAI_AA.pack(pady=2, padx=10)
# Atrial Pulse Width
AAI_label_APW = customtkinter.CTkLabel(master=AAI_page, text="Atrial Pulse Width (range: 1-30)")
AAI_label_APW.pack(pady=2, padx=10)
AAI_APW = customtkinter.CTkEntry(master=AAI_page, placeholder_text="Atrial Pulse Width")
AAI_APW.pack(pady=2, padx=10)
# ARP
AAI_label_ARP = customtkinter.CTkLabel(master=AAI_page, text="ARP (range: 150-500)")
AAI_label_ARP.pack(pady=2, padx=10)
AAI_ARP = customtkinter.CTkEntry(master=AAI_page, placeholder_text="ARP")
AAI_ARP.pack(pady=2, padx=10)
# Atrial sensitivity
AAI_label_AS = customtkinter.CTkLabel(master=AAI_page, text="Atrial Sensitivity (range: 0-5)")
AAI_label_AS.pack(pady=2, padx=10)
AAI_AS = customtkinter.CTkEntry(master=AAI_page, placeholder_text="Atrial Sensitivity")
AAI_AS.pack(pady=2, padx=10)
# PVARP
AAI_label_PVARP = customtkinter.CTkLabel(master=AAI_page, text="PVARP (range: 150-500)")
AAI_label_PVARP.pack(pady=2, padx=10)
AAI_PVARP = customtkinter.CTkEntry(master=AAI_page, placeholder_text="PVARP")
AAI_PVARP.pack(pady=2, padx=10)
# Hysteresis
AAI_label_H = customtkinter.CTkLabel(master=AAI_page, text="Hysteresis Rate Limit (range: Off or same as LRL)")
AAI_label_H.pack(pady=2, padx=10)
AAI_H = customtkinter.CTkEntry(master=AAI_page, placeholder_text="Hysteresis Rate Limit")
AAI_H.pack(pady=2, padx=10)
# Rate Smoothing
AAI_label_RS = customtkinter.CTkLabel(master=AAI_page, text="Rate Smoothing (range: Off, 3, 6, 9, 12, 15,18,21, 25)")
AAI_label_RS.pack(pady=2, padx=10)
AAI_RS = customtkinter.CTkEntry(master=AAI_page, placeholder_text="Rate Smoothing")
AAI_RS.pack(pady=2, padx=10)
#submit
submit_aai = customtkinter.CTkButton(master = AAI_page, text="Submit", command=submit_aai)
submit_aai.pack(pady=2, padx=10)
#back to mode page from AOO
back_AAI_button = customtkinter.CTkButton(master=AAI_page, text="Back", command = back_button)
back_AAI_button.pack(pady=2, padx=10)
#log out
log_out = customtkinter.CTkButton(master=AAI_page, text="Log out", command=user_log_out)
log_out.pack(pady=2, padx=10)



################################### VVI page##########################################
VVI_page = customtkinter.CTkFrame(master=root)
VVI_page.pack(pady=10, padx=60)#, fill="both", expand = True)
# output a label
VVI_label = customtkinter.CTkLabel(master=VVI_page, text="Please Enter Parameters for VVI")
VVI_label.pack(pady=2, padx=10)
# Lower Rate Limit
VVI_label_LRL = customtkinter.CTkLabel(master=VVI_page, text="Lower Rate Limit (range: 30-175)")
VVI_label_LRL.pack(pady=2, padx=10)
VVI_LRL = customtkinter.CTkEntry(master=VVI_page, placeholder_text="Lower Rate Limit")
VVI_LRL.pack(pady=2, padx=10)
# Upper Rate Limit
VVI_label_URL = customtkinter.CTkLabel(master=VVI_page, text="Upper Rate Limit (range: 50-175)")
VVI_label_URL.pack(pady=2, padx=10)
VVI_URL = customtkinter.CTkEntry(master=VVI_page, placeholder_text="Upper Rate Limit")
VVI_URL.pack(pady=2, padx=10)
# Ventricular Amplitude
VVI_label_VA = customtkinter.CTkLabel(master=VVI_page, text="Ventricular Amplitude (range: 0-100)")
VVI_label_VA.pack(pady=2, padx=10)
VVI_VA = customtkinter.CTkEntry(master=VVI_page, placeholder_text="Ventricular Amplitude")
VVI_VA.pack(pady=2, padx=10)
#   Ventricular Pulse Width
VVI_label_VPW = customtkinter.CTkLabel(master=VVI_page, text="Ventricular Pulse Width (range: 1-30)")
VVI_label_VPW.pack(pady=2, padx=10)
VVI_VPW = customtkinter.CTkEntry(master=VVI_page, placeholder_text="Ventricular Pulse Width")
VVI_VPW.pack(pady=2, padx=10)
# VRP
VVI_label_VRP = customtkinter.CTkLabel(master=VVI_page, text="VRP (range: 150-500)")
VVI_label_VRP.pack(pady=2, padx=10)
VVI_VRP = customtkinter.CTkEntry(master=VVI_page, placeholder_text="VRP")
VVI_VRP.pack(pady=2, padx=10)
#Ventricular Sensitivity
VVI_label_VS = customtkinter.CTkLabel(master=VVI_page, text="Ventricular Sensitivity (range: 0-5)")
VVI_label_VS.pack(pady=2, padx=10)
VVI_VS = customtkinter.CTkEntry(master=VVI_page, placeholder_text="Ventricular Sensitivity")
VVI_VS.pack(pady=2, padx=10)
# Hysteresis
VVI_label_H = customtkinter.CTkLabel(master=VVI_page, text="Hysteresis Rate Limit (range: 0 or same as LRL)")
VVI_label_H.pack(pady=2, padx=10)
VVI_H = customtkinter.CTkEntry(master=VVI_page, placeholder_text="Hysteresis Rate Limit")
VVI_H.pack(pady=2, padx=10)
#Rate Smoothing
VVI_label_RS = customtkinter.CTkLabel(master=VVI_page, text="Rate Smoothing (range: Off, 3, 6, 9, 12, 15,18,21, 25)")
VVI_label_RS.pack(pady=2, padx=10)
VVI_RS = customtkinter.CTkEntry(master=VVI_page, placeholder_text="Rate Smoothing")
VVI_RS.pack(pady=2, padx=10)
#submit
submit_vvi = customtkinter.CTkButton(master = VVI_page, text="Submit", command=submit_vvi)
submit_vvi.pack(pady=2,padx=10)
#back to mode page from AOO
back_VVI_button = customtkinter.CTkButton(master=VVI_page, text="Back", command = back_button)
back_VVI_button.pack(pady=2, padx=10)
#log out
log_out = customtkinter.CTkButton(master=VVI_page, text="Log out", command=user_log_out)
log_out.pack(pady=2, padx=10)

################################### AOOR page##########################################
AOOR_page = customtkinter.CTkFrame(master=root)
AOOR_page.pack(pady=2, padx=60)#, fill="both", expand = True)
# output a label
AOOR_label = customtkinter.CTkLabel(master=AOOR_page, text="Please Enter Parameters for AOOR")
AOOR_label.pack(pady=1, padx=10)
# Lower Rate Limit
AOOR_label_LRL = customtkinter.CTkLabel(master=AOOR_page, text="LRL (range: 30-175)")
AOOR_label_LRL.pack(pady=1, padx=10)
AOOR_LRL = customtkinter.CTkEntry(master=AOOR_page, placeholder_text="Lower Rate Limit")
AOOR_LRL.pack(pady=1, padx=10)
# Upper Rate Limit
AOOR_label_URL = customtkinter.CTkLabel(master=AOOR_page, text="URL (range: 50-175)")
AOOR_label_URL.pack(pady=1, padx=10)
AOOR_URL = customtkinter.CTkEntry(master=AOOR_page, placeholder_text="Upper Rate Limit")
AOOR_URL.pack(pady=1, padx=10)
# Maximum Sensor Rate
AOOR_label_MSR = customtkinter.CTkLabel(master=AOOR_page, text="MSR (range: 50-175)")
AOOR_label_MSR.pack(pady=1, padx=10)
AOOR_MSR = customtkinter.CTkEntry(master=AOOR_page, placeholder_text="Maximum Sensor Rate")
AOOR_MSR.pack(pady=1, padx=10)
# Atrial Amplitude
AOOR_label_AA = customtkinter.CTkLabel(master=AOOR_page, text="Atrial Amplitude (range: 0-100)")
AOOR_label_AA.pack(pady=1, padx=10)
AOOR_AA = customtkinter.CTkEntry(master=AOOR_page, placeholder_text="Atrial Amplitude")
AOOR_AA.pack(pady=1, padx=10)
# Atrial Pulse Width
AOOR_label_APW = customtkinter.CTkLabel(master=AOOR_page, text="Atrial Pulse Width (range: 1-30)")
AOOR_label_APW.pack(pady=1, padx=10)
AOOR_APW = customtkinter.CTkEntry(master=AOOR_page, placeholder_text="Atrial Pulse Width")
AOOR_APW.pack(pady=1, padx=10)
# Activity Threshold
AOOR_label_AT = customtkinter.CTkLabel(master=AOOR_page, text="Activity Threshold (input: V-Low,Low,Med-Low,Med,Med-High,High,V-High)")
AOOR_label_AT.pack(pady=1, padx=10)
AOOR_AT = customtkinter.CTkEntry(master=AOOR_page, placeholder_text="Atrial Activity Threshold")
AOOR_AT.pack(pady=1, padx=10)
# Reaction Time
AOOR_label_ReactionT = customtkinter.CTkLabel(master=AOOR_page, text="Reaction Time (range: 10-50)")
AOOR_label_ReactionT.pack(pady=1, padx=10)
AOOR_ReactionT = customtkinter.CTkEntry(master=AOOR_page, placeholder_text="Reaction Time")
AOOR_ReactionT.pack(pady=1, padx=10)
# Response Factor
AOOR_label_RF = customtkinter.CTkLabel(master=AOOR_page, text="Response Factor (range: 1-16)")
AOOR_label_RF.pack(pady=1, padx=10)
AOOR_RF = customtkinter.CTkEntry(master=AOOR_page, placeholder_text="Response Factor")
AOOR_RF.pack(pady=1, padx=10)
#Recovery Time
AOOR_label_RecoveryT = customtkinter.CTkLabel(master=AOOR_page, text="Recovery Time (range: 2-16)")
AOOR_label_RecoveryT.pack(pady=1, padx=10)
AOOR_RecoveryT = customtkinter.CTkEntry(master=AOOR_page, placeholder_text="Recovery Time")
AOOR_RecoveryT.pack(pady=1, padx=10)
#submit
submit_aoor = customtkinter.CTkButton(master = AOOR_page, text="Submit", command=submit_aoor)
submit_aoor.pack(pady=1,padx=10)
#back to mode page from AOO
back_AOOR_button = customtkinter.CTkButton(master=AOOR_page, text="Back", command = back_button)
back_AOOR_button.pack(pady=6, padx=10)
#log out
log_out = customtkinter.CTkButton(master=AOOR_page, text="Log out", command=user_log_out)
log_out.pack(pady=6, padx=10)


################################### VOOR page##########################################
VOOR_page = customtkinter.CTkFrame(master=root)
VOOR_page.pack(pady=11, padx=60)#, fill="both", expand = True)
# output a label
VOOR_label = customtkinter.CTkLabel(master=VOOR_page, text="Please Enter Parameters for VOOR")
VOOR_label.pack(pady=1, padx=10)
# Lower Rate Limit
VOOR_label_LRL = customtkinter.CTkLabel(master=VOOR_page, text="Lower Rate Limit (range: 30-175)")
VOOR_label_LRL.pack(pady=1, padx=10)
VOOR_LRL = customtkinter.CTkEntry(master=VOOR_page, placeholder_text="Lower Rate Limit")
VOOR_LRL.pack(pady=1, padx=10)
# Upper Rate Limit
VOOR_label_URL = customtkinter.CTkLabel(master=VOOR_page, text="Upper Rate Limit (range: 50-175)")
VOOR_label_URL.pack(pady=1, padx=10)
VOOR_URL = customtkinter.CTkEntry(master=VOOR_page, placeholder_text="Upper Rate Limit")
VOOR_URL.pack(pady=1, padx=10)
# Ventricular Amplitude
VOOR_label_VA = customtkinter.CTkLabel(master=VOOR_page, text="Ventricular Amplitude (range: 0-100)")
VOOR_label_VA.pack(pady=1, padx=10)
VOOR_VA = customtkinter.CTkEntry(master=VOOR_page, placeholder_text="Ventricular Amplitude")
VOOR_VA.pack(pady=1, padx=10)
# Ventricular Pulse Width
VOOR_label_VPW = customtkinter.CTkLabel(master=VOOR_page, text="Ventricular Pulse Width (range: 1-30)")
VOOR_label_VPW.pack(pady=1, padx=10)
VOOR_VPW = customtkinter.CTkEntry(master=VOOR_page, placeholder_text="Ventricular Pulse Width")
VOOR_VPW.pack(pady=1, padx=10)
# Maximum Sensor Rate
VOOR_label_MSR = customtkinter.CTkLabel(master=VOOR_page, text="MSR (range: 50-175)")
VOOR_label_MSR.pack(pady=1, padx=10)
VOOR_MSR = customtkinter.CTkEntry(master=VOOR_page, placeholder_text="Maximum Sensor Rate")
VOOR_MSR.pack(pady=1, padx=10)
# Activity Threshold
VOOR_label_AT = customtkinter.CTkLabel(master=VOOR_page, text="Activity Threshold (input: V-Low,Low,Med-Low,Med,Med-High,High,V-High)")
VOOR_label_AT.pack(pady=1, padx=10)
VOOR_AT = customtkinter.CTkEntry(master=VOOR_page, placeholder_text="Atrial Activity Threshold")
VOOR_AT.pack(pady=1, padx=10)
# Reaction Time
VOOR_label_ReactionT = customtkinter.CTkLabel(master=VOOR_page, text="Reaction Time (range: 10-50)")
VOOR_label_ReactionT.pack(pady=1, padx=10)
VOOR_ReactionT = customtkinter.CTkEntry(master=VOOR_page, placeholder_text="Reaction Time")
VOOR_ReactionT.pack(pady=1, padx=10)
# Response Factor
VOOR_label_RF = customtkinter.CTkLabel(master=VOOR_page, text="Response Factor (range: 1-16)")
VOOR_label_RF.pack(pady=1, padx=10)
VOOR_RF = customtkinter.CTkEntry(master=VOOR_page, placeholder_text="Response Factor")
VOOR_RF.pack(pady=1, padx=10)
#Recovery Time
VOOR_label_RecoveryT = customtkinter.CTkLabel(master=VOOR_page, text="Recovery Time (range: 2-16)")
VOOR_label_RecoveryT.pack(pady=1, padx=10)
VOOR_RecoveryT = customtkinter.CTkEntry(master=VOOR_page, placeholder_text="Recovery Time")
VOOR_RecoveryT.pack(pady=1, padx=10)
#submit
submit_voor = customtkinter.CTkButton(master = VOOR_page, text="Submit", command=submit_voo)
submit_voor.pack(pady=6, padx=10)
#back to mode page from AOO
back_voor_button = customtkinter.CTkButton(master=VOOR_page, text="Back", command = back_button)
back_voor_button.pack(pady=6, padx=10)
#log out
log_out = customtkinter.CTkButton(master=VOOR_page, text="Log out", command=user_log_out)
log_out.pack(pady=6, padx=10)


################################### AAIR page##########################################
AAIR_page = customtkinter.CTkFrame(master=root)
AAIR_page.pack(pady=0, padx=60)#, fill="both", expand = True)
# output a label
AAIR_label = customtkinter.CTkLabel(master=AAIR_page, text="Please Enter Parameters for AAIR")
AAIR_label.grid(row=0, column=0, ipadx=5, ipady=5)
# Lower Rate Limit
AAIR_label_LRL = customtkinter.CTkLabel(master=AAIR_page, text="Lower Rate Limit (range: 30-175)")
AAIR_label_LRL.grid(row=1, column=0, ipadx=5, ipady=5)
AAIR_LRL = customtkinter.CTkEntry(master=AAIR_page, placeholder_text="Lower Rate Limit")
AAIR_LRL.grid(row=1, column=1, ipadx=5, ipady=5)
# Upper Rate Limit
AAIR_label_URL = customtkinter.CTkLabel(master=AAIR_page, text="Upper Rate Limit (range: 50-175)")
AAIR_label_URL.grid(row=2, column=0, ipadx=5, ipady=5)
AAIR_URL = customtkinter.CTkEntry(master=AAIR_page, placeholder_text="Upper Rate Limit")
AAIR_URL.grid(row=2, column=1, ipadx=5, ipady=5)
# Atrial Amplitude
AAIR_label_AA = customtkinter.CTkLabel(master=AAIR_page, text="Atrial Amplitude (range: off, 0.1-5.0)")
AAIR_label_AA.grid(row=3, column=0, ipadx=5, ipady=5)
AAIR_AA = customtkinter.CTkEntry(master=AAIR_page, placeholder_text="Atrial Amplitude")
AAIR_AA.grid(row=3, column=1, ipadx=5, ipady=5)
# Atrial Pulse Width
AAIR_label_APW = customtkinter.CTkLabel(master=AAIR_page, text="Atrial Pulse Width (range: 1-30)")
AAIR_label_APW.grid(row=4, column=0, ipadx=5, ipady=5)
AAIR_APW = customtkinter.CTkEntry(master=AAIR_page, placeholder_text="Atrial Pulse Width")
AAIR_APW.grid(row=4, column=1, ipadx=5, ipady=5)
# ARP
AAIR_label_ARP = customtkinter.CTkLabel(master=AAIR_page, text="ARP (range: 150-500)")
AAIR_label_ARP.grid(row=5, column=0, ipadx=5, ipady=5)
AAIR_ARP = customtkinter.CTkEntry(master=AAIR_page, placeholder_text="ARP")
AAIR_ARP.grid(row=5, column=1, ipadx=5, ipady=5)
# Atrial sensitivity
AAIR_label_AS = customtkinter.CTkLabel(master=AAIR_page, text="Atrial Sensitivity (range: 0-5)")
AAIR_label_AS.grid(row=6, column=0, ipadx=5, ipady=5)
AAIR_AS = customtkinter.CTkEntry(master=AAIR_page, placeholder_text="Atrial Sensitivity")
AAIR_AS.grid(row=6, column=1, ipadx=5, ipady=5)
# PVARP
AAIR_label_PVARP = customtkinter.CTkLabel(master=AAIR_page, text="PVARP (range: 150-500)")
AAIR_label_PVARP.grid(row=7, column=0, ipadx=5, ipady=5)
AAIR_PVARP = customtkinter.CTkEntry(master=AAIR_page, placeholder_text="PVARP")
AAIR_PVARP.grid(row=7, column=1, ipadx=5, ipady=5)
# Hysteresis
AAIR_label_H = customtkinter.CTkLabel(master=AAIR_page, text="Hysteresis Rate Limit (range: Off or same as LRL)")
AAIR_label_H.grid(row=8, column=0, ipadx=5, ipady=5)
AAIR_H = customtkinter.CTkEntry(master=AAIR_page, placeholder_text="Hysteresis Rate Limit")
AAIR_H.grid(row=8, column=1, ipadx=5, ipady=5)
# Rate Smoothing
AAIR_label_RS = customtkinter.CTkLabel(master=AAIR_page, text="Rate Smoothing (range: Off, 3, 6, 9, 12, 15,18,21, 25)")
AAIR_label_RS.grid(row=9, column=0, ipadx=5, ipady=5)
AAIR_RS = customtkinter.CTkEntry(master=AAIR_page, placeholder_text="Rate Smoothing")
AAIR_RS.grid(row=9, column=1, ipadx=5, ipady=5)
# Maximum Sensor Rate
AAIR_label_MSR = customtkinter.CTkLabel(master=AAIR_page, text="MSR (range: 50-175)")
AAIR_label_MSR.grid(row=10, column=0, ipadx=5, ipady=5)
AAIR_MSR = customtkinter.CTkEntry(master=AAIR_page, placeholder_text="Maximum Sensor Rate")
AAIR_MSR.grid(row=10, column=1, ipadx=5, ipady=5)
# Activity Threshold
AAIR_label_AT = customtkinter.CTkLabel(master=AAIR_page, text="Activity Threshold (input: V-Low,Low,Med-Low,Med,Med-High,High,V-High)")
AAIR_label_AT.grid(row=11, column=0, ipadx=5, ipady=5)
AAIR_AT = customtkinter.CTkEntry(master=AAIR_page, placeholder_text="Atrial Activity Threshold")
AAIR_AT.grid(row=11, column=1, ipadx=5, ipady=5)
# Reaction Time
AAIR_label_ReactionT = customtkinter.CTkLabel(master=AAIR_page, text="Reaction Time (range: 10-50)")
AAIR_label_ReactionT.grid(row=12, column=0, ipadx=5, ipady=5)
AAIR_ReactionT = customtkinter.CTkEntry(master=AAIR_page, placeholder_text="Reaction Time")
AAIR_ReactionT.grid(row=12, column=1, ipadx=5, ipady=5)
# Response Factor
AAIR_label_RF = customtkinter.CTkLabel(master=AAIR_page, text="Response Factor (range: 1-16)")
AAIR_label_RF.grid(row=13, column=0, ipadx=5, ipady=5)
AAIR_RF = customtkinter.CTkEntry(master=AAIR_page, placeholder_text="Response Factor")
AAIR_RF.grid(row=13, column=1, ipadx=5, ipady=5)
#Recovery Time
AAIR_label_RecoveryT = customtkinter.CTkLabel(master=AAIR_page, text="Recovery Time (range: 2-16)")
AAIR_label_RecoveryT.grid(row=14, column=0, ipadx=5, ipady=5)
AAIR_RecoveryT = customtkinter.CTkEntry(master=AAIR_page, placeholder_text="Recovery Time")
AAIR_RecoveryT.grid(row=14, column=1, ipadx=5, ipady=5)

#submit
submit_aair = customtkinter.CTkButton(master = AAIR_page, text="Submit", command=submit_aair)
submit_aair.grid(row=15, column=0, ipadx=5, ipady=10)
#back to mode page from AOO
back_AAIR_button = customtkinter.CTkButton(master=AAIR_page, text="Back", command = back_button)
back_AAIR_button.grid(row=16, column=0, ipadx=5, ipady=10)
#log out
log_out = customtkinter.CTkButton(master=AAIR_page, text="Log out", command=user_log_out)
log_out.grid(row=17, column=0, ipadx=5, ipady=10)

################################### VVIR page##########################################

VVIR_page = customtkinter.CTkFrame(master=root)
VVIR_page.pack(pady=0, padx=60)#, fill="both", expand = True)
# output a label
VVIR_label = customtkinter.CTkLabel(master=VVIR_page, text="Please Enter Parameters for VVIR")
VVIR_label.grid(row=0, column=0, ipadx=5, ipady=5)
# Lower Rate Limit
VVIR_label_LRL = customtkinter.CTkLabel(master=VVIR_page, text="Lower Rate Limit (range: 30-175)")
VVIR_label_LRL.grid(row=1, column=0, ipadx=5, ipady=5)
VVIR_LRL = customtkinter.CTkEntry(master=VVIR_page, placeholder_text="Lower Rate Limit")
VVIR_LRL.grid(row=1, column=1, ipadx=5, ipady=5)
# Upper Rate Limit
VVIR_label_URL = customtkinter.CTkLabel(master=VVIR_page, text="Upper Rate Limit (range: 50-175)")
VVIR_label_URL.grid(row=2, column=0, ipadx=5, ipady=5)
VVIR_URL = customtkinter.CTkEntry(master=VVIR_page, placeholder_text="Upper Rate Limit")
VVIR_URL.grid(row=2, column=1, ipadx=5, ipady=5)
# Ventricular Amplitude
VVIR_label_VA = customtkinter.CTkLabel(master=VVIR_page, text="Ventricular Amplitude (range: off, 0.1-5.0)")
VVIR_label_VA.grid(row=3, column=0, ipadx=5, ipady=5)
VVIR_VA = customtkinter.CTkEntry(master=VVIR_page, placeholder_text="Ventricular Amplitude")
VVIR_VA.grid(row=3, column=1, ipadx=5, ipady=5)
#   Ventricular Pulse Width
VVIR_label_VPW = customtkinter.CTkLabel(master=VVIR_page, text="Ventricular Pulse Width (range: 1-30)")
VVIR_label_VPW.grid(row=4, column=0, ipadx=5, ipady=5)
VVIR_VPW = customtkinter.CTkEntry(master=VVIR_page, placeholder_text="Ventricular Pulse Width")
VVIR_VPW.grid(row=4, column=1, ipadx=5, ipady=5)
# VRP
VVIR_label_VRP = customtkinter.CTkLabel(master=VVIR_page, text="VRP (range: 150-500)")
VVIR_label_VRP.grid(row=5, column=0, ipadx=5, ipady=5)
VVIR_VRP = customtkinter.CTkEntry(master=VVIR_page, placeholder_text="VRP")
VVIR_VRP.grid(row=5, column=1, ipadx=5, ipady=5)
#Ventricular Sensitivity
VVIR_label_VS = customtkinter.CTkLabel(master=VVIR_page, text="Ventricular Sensitivity (range: 0-5)")
VVIR_label_VS.grid(row=6, column=0, ipadx=5, ipady=5)
VVIR_VS = customtkinter.CTkEntry(master=VVIR_page, placeholder_text="Ventricular Sensitivity")
VVIR_VS.grid(row=6, column=1, ipadx=5, ipady=5)
# Hysteresis
VVIR_label_H = customtkinter.CTkLabel(master=VVIR_page, text="Hysteresis Rate Limit (range: OFF, 30-175)")
VVIR_label_H.grid(row=7, column=0, ipadx=5, ipady=5)
VVIR_H = customtkinter.CTkEntry(master=VVIR_page, placeholder_text="Hysteresis Rate Limit")
VVIR_H.grid(row=7, column=1, ipadx=5, ipady=5)
#Rate Smoothing
VVIR_label_RS = customtkinter.CTkLabel(master=VVIR_page, text="Rate Smoothing (range: Off, 3, 6, 9, 12, 15,18,21, 25)")
VVIR_label_RS.grid(row=8, column=0, ipadx=5, ipady=5)
VVIR_RS = customtkinter.CTkEntry(master=VVIR_page, placeholder_text="Rate Smoothing")
VVIR_RS.grid(row=8, column=1, ipadx=5, ipady=5)
# Maximum Sensor Rate
VVIR_label_MSR = customtkinter.CTkLabel(master=VVIR_page, text="MSR (range: 50-175)")
VVIR_label_MSR.grid(row=9, column=0, ipadx=5, ipady=5)
VVIR_MSR = customtkinter.CTkEntry(master=VVIR_page, placeholder_text="Maximum Sensor Rate")
VVIR_MSR.grid(row=9, column=1, ipadx=5, ipady=5)
# Activity Threshold
VVIR_label_AT = customtkinter.CTkLabel(master=VVIR_page, text="Activity Threshold (input: V-Low,Low,Med-Low,Med,Med-High,High,V-High)")
VVIR_label_AT.grid(row=10, column=0, ipadx=5, ipady=5)
VVIR_AT = customtkinter.CTkEntry(master=VVIR_page, placeholder_text="Activity Threshold")
VVIR_AT.grid(row=10, column=1, ipadx=5, ipady=5)
# Reaction Time
VVIR_label_ReactionT = customtkinter.CTkLabel(master=VVIR_page, text="Reaction Time (range: 10-50)")
VVIR_label_ReactionT.grid(row=11, column=0, ipadx=5, ipady=5)
VVIR_ReactionT = customtkinter.CTkEntry(master=VVIR_page, placeholder_text="Reaction Time")
VVIR_ReactionT.grid(row=11, column=1, ipadx=5, ipady=5)
# Response Factor
VVIR_label_RF = customtkinter.CTkLabel(master=VVIR_page, text="Response Factor (range: 1-16)")
VVIR_label_RF.grid(row=12, column=0, ipadx=5, ipady=5)
VVIR_RF = customtkinter.CTkEntry(master=VVIR_page, placeholder_text="Response Factor")
VVIR_RF.grid(row=12, column=1, ipadx=5, ipady=5)
#Recovery Time
VVIR_label_RecoveryT = customtkinter.CTkLabel(master=VVIR_page, text="Recovery Time (range: 2-16)")
VVIR_label_RecoveryT.grid(row=13, column=0, ipadx=5, ipady=5)
VVIR_RecoveryT = customtkinter.CTkEntry(master=VVIR_page, placeholder_text="Recovery Time")
VVIR_RecoveryT.grid(row=13, column=1, ipadx=5, ipady=5)
#submit
submit_vvir = customtkinter.CTkButton(master = VVIR_page, text="Submit", command=submit_vvir)
submit_vvir.grid(row=14, column=0, ipadx=10, ipady=10)
#back to mode page from AOO
back_VVIR_button = customtkinter.CTkButton(master=VVIR_page, text="Back", command = back_button)
back_VVIR_button.grid(row=15, column=0, ipadx=10, ipady=10)
#log out
log_out = customtkinter.CTkButton(master=VVIR_page, text="Log out", command=user_log_out)
log_out.grid(row=16, column=0, ipadx=10, ipady=10)




show_login_page()
root.mainloop()
