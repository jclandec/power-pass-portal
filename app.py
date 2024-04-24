import random
import json
import os
from tkinter import *
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
import datetime
import re
from customer import Customer

win = Tk()
win.title('Power Pass Portal')
win.geometry('600x800')

win.columnconfigure(0, weight=1)
win.columnconfigure(1, weight=1)
win.columnconfigure(2, weight=1)

id_var = StringVar()
pin_var = StringVar()
name_var = StringVar()
dob_var = StringVar()
payment_method_var = StringVar()
days_purchased = IntVar()
reservation_date_var = StringVar()
buddy_email_var = StringVar()

def valid_date_format(date):
    try:
        datetime.datetime.strptime(date, '%m-%d-%Y')
        return True
    except ValueError:
        return False

def date_in_future(date):
    reservation_date = datetime.datetime.strptime(date, '%m-%d-%Y')
    current_date = datetime.datetime.now()
    return reservation_date > current_date

def valid_email_format(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    # re.match() checks for a match only at the beginning of the string,
    # while re.search() checks for a match anywhere in the string.
    if re.match(pattern, email):
        return True
    else:
        return False

def load_login_frame():
    global login_frame
    login_frame = Frame(win)
    login_frame.grid(row=2, column=1, padx=None, pady=5)

    login_title_label = Label(login_frame, text='Power Pass Login', font=('Arial', 24), fg='black')
    login_title_label.grid(row=0, column=0, padx=None, pady=5, columnspan=2)

    id_label = Label(login_frame, text='Power Pass ID (ex: 999912345678)', font=('Arial', 16), fg='black')
    id_label.grid(row=2, column=0, padx=10, pady=5, sticky='E')

    id_box = Entry(login_frame, justify='left', font=('Arial', 14), textvariable=id_var)
    id_box.grid(row=2, column=1, padx=10, pady=5, sticky='W')

    pin_label = Label(login_frame, text='Power Pass PIN (ex: 1234)', font=('Arial', 16), fg='black')
    pin_label.grid(row=3, column=0, padx=10, pady=5, sticky='E')

    pin_box = Entry(login_frame, justify='left', font=('Arial', 14), textvariable=pin_var)
    pin_box.grid(row=3, column=1, padx=10, pady=5, sticky='W')

    login_button = Button(login_frame, command=login, font=('Arial', 16), text='Login', width=15)
    login_button.grid(row=4, column=0, padx=None, pady=5, columnspan=2)

    purchase_button = Button(login_frame, command=load_purchase_frame, font=('Arial', 16), text='Purchase a new pass', width=15)
    purchase_button.grid(row=5, column=0, padx=None, pady=5, columnspan=2)

    exit_button = Button(login_frame, command=close, font=('Arial', 16), text='Exit Application', width=15)
    exit_button.grid(row=6, column=0, padx=None, pady=5, columnspan=2)

def login():
    if not os.path.exists('passholders.json') or os.stat('passholders.json').st_size == 0:
        with open('passholders.json', 'w') as fp:
            json.dump({}, fp)

    with open('passholders.json', 'r') as fp:
        try:
            customer_data = json.load(fp)
        except json.JSONDecodeError:
            customer_data = {}

    user_id = id_var.get()
    user_pin = pin_var.get()

    try:
        if customer_data[user_id]['pin'] == user_pin:
            login_frame.grid_remove()
            load_dashboard_frame(user_id)
        else:
            login_failed_label = Label(login_frame, text='Login failed - please ensure your pin is correct',
                                       font=('Arial', 16), fg='red')
            login_failed_label.grid(row=1, column=0, padx=None, pady=10, columnspan=2)
    except KeyError:
        login_failed_label = Label(login_frame, text='Login failed - please ensure your ID and pin are correct.',
                                   font=('Arial', 16), fg='red')
        login_failed_label.grid(row=1, column=0, padx=None, pady=10, columnspan=2)

def load_purchase_frame():
    global purchase_frame
    purchase_frame = Frame(win)
    purchase_frame.grid(row=2, column=1, padx=None, pady=10)

    name_label = Label(purchase_frame, text='Full Name', font=('Arial', 16), fg='black')
    name_label.grid(row=1, column=0, padx=10, pady=5, sticky='E')

    name_box = Entry(purchase_frame, justify='left', font=('Arial', 14), textvariable=name_var)
    name_box.grid(row=1, column=1, padx=10, pady=5, sticky='W')

    dob_label = Label(purchase_frame, text='Date Of Birth (ex: 01-10-1975)', font=('Arial', 16), fg='black')
    dob_label.grid(row=2, column=0, padx=10, pady=5, sticky='E')

    dob_box = Entry(purchase_frame, justify='left', font=('Arial', 14), textvariable=dob_var)
    dob_box.grid(row=2, column=1, padx=10, pady=5, sticky='W')

    payment_method_label = Label(purchase_frame, text='Payment Method', font=('Arial', 16), fg='black')
    payment_method_label.grid(row=3, column=0, padx=10, pady=5, sticky='E')

    payment_method_dropdown = Combobox(purchase_frame, justify='center', font=('Arial', 14), textvariable=payment_method_var)
    payment_method_dropdown['values'] = ('Select a card...', 'Visa x9998', 'Amex x1112', 'MasterCard x5678')
    payment_method_dropdown.grid(row=3, column=1, padx=10, pady=5)
    payment_method_dropdown.current(0)

    days_selection_frame = Frame(purchase_frame)
    days_selection_frame.grid(row=4, column=0, padx=None, pady=5, columnspan=2)

    days_selection_label = Label(days_selection_frame, text='Select your pass', font=('Arial',16), fg='black')
    days_selection_label.grid(row=0, column=0, sticky='EW')

    twelve_day_radiobutton = Radiobutton(days_selection_frame, text='12 Day Pass - $249', variable=days_purchased, value=12)
    twelve_day_radiobutton.grid(row=1, column=0)

    four_day_radiobutton = Radiobutton(days_selection_frame, text='4 Day Pass - $99', variable=days_purchased, value=4)
    four_day_radiobutton.grid(row=2, column=0)

    pin_label = Label(purchase_frame, text='Enter a 4 digit pin:', font=('Arial', 16), fg='black')
    pin_label.grid(row=5, column=0, padx=10, pady=5, sticky='E')

    pin_box = Entry(purchase_frame, justify='left', font=('Arial', 14), textvariable=pin_var)
    pin_box.grid(row=5, column=1, padx=10, pady=5, sticky='W')

    purchase_button = Button(purchase_frame, text="Purchase", font=('Arial',16), width=15, command=lambda: purchase_pass())
    purchase_button.grid(row=6, column=0, pady=5, columnspan=2)

    exit_button = Button(purchase_frame, command=close, font=('Arial', 16), text='Exit Application', width=15)
    exit_button.grid(row=7, column=0, padx=None, pady=5, columnspan=2)

    win.update_idletasks()
    login_frame.grid_remove()

def purchase_pass():
    if not valid_date_format(dob_var.get()):
        date_error_label = Label(purchase_frame, font=('Arial', 16), fg='red',
                                 text='Error: Date must be format mm-dd-yyyy')
        date_error_label.grid(row=8, column=0, padx=None, pady=5, sticky='EW', columnspan=3)
    else:
        customer = Customer(id=None, name=name_var.get(), dob=dob_var.get(), pin=pin_var.get(), pay_method=payment_method_var.get(), days_purchased=days_purchased.get(), reservation_list=[])
        customer.save()
        purchase_frame.grid_remove()
        load_dashboard_frame(customer.id)

def load_dashboard_frame(id):
    global dashboard_frame
    dashboard_frame = Frame(win)
    dashboard_frame.grid(row=2, column=1, padx=None, pady=10)

    with open('passholders.json', 'r') as fp:
        customer_data = json.load(fp)

    customer = Customer.from_dict(customer_data[str(id)])

    dashboard_title_label = Label(dashboard_frame, text=f'Welcome back, {customer.name}', font=('Arial', 24), fg='black')
    dashboard_title_label.grid(row=0, column=0, padx=None, pady=5, columnspan=3)

    id_label = Label(dashboard_frame, text=f'ID Number: {customer.id}',font=('Arial', 16))
    id_label.grid(row=1,column=0,padx=None,pady=5, columnspan=3)

    def load_reservation_listbox():

        days_remaining_label = Label(dashboard_frame)
        if days_remaining_label.winfo_manager() == 'grid':
            if days_remaining_label.grid_info():
                days_remaining_label.grid_remove()

        days_remaining_label = Label(dashboard_frame,
                                     text=f'You have {customer.days_purchased - len(customer.reservation_list)} days remaining on your Power Pass!',
                                     font=('Arial', 20))
        days_remaining_label.grid(row=2, column=0, padx=None, pady=5, columnspan=3)

        reservation_listbox = Listbox(dashboard_frame, height=20,width=10,bg='white',fg='black')
        for date in customer.reservation_list:
            reservation_listbox.insert(END, date)
        reservation_listbox.grid(row=4, column=0, padx=None, pady=5, columnspan=3)
    load_reservation_listbox()

    add_reservation_label = Label(dashboard_frame, text='Add a new reservation (ex: 03-26-2024)',font=('Arial', 16),fg='black')
    add_reservation_label.grid(row=5, column=0, padx=None, pady=5,sticky='E')

    add_reservation_box = Entry(dashboard_frame, font=('Arial', 14), textvariable=reservation_date_var, width=15)
    add_reservation_box.grid(row=5,column=1,padx=None,pady=5)

    add_reservation_button = Button(dashboard_frame, font=('Arial', 16), text='Add',width=10,command=lambda: add_reservation(customer, reservation_date_var.get()))
    add_reservation_button.grid(row=5,column=2,padx=None,pady=5,sticky='W')

    def add_reservation(customer, date):

        date_error_label = Label(dashboard_frame)
        if date_error_label.winfo_manager() == 'grid':
            if date_error_label.grid_info():
                date_error_label.grid_remove()

        if not valid_date_format(date):
            date_error_label = Label(dashboard_frame, font=('Arial', 16),fg='red', text='Error: Date must be format mm-dd-yyyy')
            date_error_label.grid(row=6,column=0,padx=None,pady=5,sticky='EW',columnspan=3)
        elif not date_in_future(date):
            date_error_label = Label(dashboard_frame, font=('Arial', 16), fg='red',
                                     text='Error: Reservation date must be after current date')
            date_error_label.grid(row=6, column=0, padx=None, pady=5, sticky='EW',columnspan=3)
        elif date in customer.reservation_list:
            date_error_label = Label(dashboard_frame, font=('Arial', 16), fg='red',
                                     text='Error: Date has already been reserved')
            date_error_label.grid(row=6, column=0, padx=None, pady=5, sticky='EW',columnspan=3)
        elif (customer.days_purchased - len(customer.reservation_list)) == 0:
            date_error_label = Label(dashboard_frame, font=('Arial', 16), fg='red',
                                     text='Error: You are out of dates to reserve this season.')
            date_error_label.grid(row=6, column=0, padx=None, pady=5, sticky='EW', columnspan=3)
        else:

            date_error_label = Label(dashboard_frame)
            if date_error_label.winfo_manager() == 'grid':
                if date_error_label.grid_info():
                    date_error_label.grid_remove()

            customer.reservation_list.append(date)
            customer.save()
            load_reservation_listbox()

    buddy_pass_button = Button(dashboard_frame, font=('Arial', 16), text='Manage buddy passes',width=30,command=lambda: load_buddy_pass_dashboard_frame(customer.id))
    buddy_pass_button.grid(row=7,column=0,padx=None,pady=5,columnspan=3)

    exit_button = Button(dashboard_frame, command=close, font=('Arial', 16), text='Exit Application', width=30)
    exit_button.grid(row=8, column=0, padx=None, pady=5, columnspan=3)

    win.update_idletasks()

def load_buddy_pass_dashboard_frame(id):
    global buddy_pass_dashboard_frame
    buddy_pass_dashboard_frame = Frame(win)
    dashboard_frame.grid_remove()
    buddy_pass_dashboard_frame.grid(row=2, column=1, padx=None, pady=10)

    with open('passholders.json', 'r') as fp:
        customer_data = json.load(fp)

    customer = Customer.from_dict(customer_data[str(id)])

    dashboard_title_label = Label(buddy_pass_dashboard_frame, text=f'Welcome back, {customer.name}', font=('Arial', 24),
                                  fg='black')
    dashboard_title_label.grid(row=0, column=0, padx=None, pady=5, columnspan=3)

    id_label = Label(buddy_pass_dashboard_frame, text=f'ID Number: {customer.id}', font=('Arial', 16))
    id_label.grid(row=1, column=0, padx=None, pady=5, columnspan=3)

    def load_buddy_pass_listbox():
        days_remaining_label = Label(buddy_pass_dashboard_frame,
                                     text=f'You have {5 - len(customer.buddy_pass_list)} buddy pass discounts remaining!',
                                     font=('Arial', 20))
        days_remaining_label.grid(row=2, column=0, padx=None, pady=5, columnspan=3)

        buddy_pass_listbox = Listbox(buddy_pass_dashboard_frame, height=5,width=20,bg='white',fg='black')
        for buddy in customer.buddy_pass_list:
            buddy_pass_listbox.insert(END, buddy)
        buddy_pass_listbox.grid(row=4, column=0, padx=None, pady=5, columnspan=3)
    load_buddy_pass_listbox()

    add_buddy_pass_label = Label(buddy_pass_dashboard_frame, text="Add a buddy's email (ex: jclandec@asu.edu)",font=('Arial', 16),fg='black')
    add_buddy_pass_label.grid(row=5, column=0, padx=None, pady=5,sticky='E')

    add_buddy_pass_box = Entry(buddy_pass_dashboard_frame, font=('Arial', 14), textvariable=buddy_email_var, width=30)
    add_buddy_pass_box.grid(row=5,column=1,padx=None,pady=5)

    add_buddy_pass_button = Button(buddy_pass_dashboard_frame, font=('Arial', 16), text='Add',width=10,command=lambda: add_buddy_pass(customer, buddy_email_var.get()))
    add_buddy_pass_button.grid(row=5,column=2,padx=None,pady=5,sticky='W')

    def add_buddy_pass(customer, buddy_email):

        email_error_label = Label(dashboard_frame)
        if email_error_label.winfo_manager() == 'grid':
            if email_error_label.grid_info():
                email_error_label.grid_remove()

        if not valid_email_format(buddy_email):
            email_error_label = Label(buddy_pass_dashboard_frame, font=('Arial', 16), fg='red', text='Error: Email must be a valid email.')
            email_error_label.grid(row=6, column=0, padx=None, pady=5, sticky='EW',columnspan=3)
        elif (5 - len(customer.buddy_pass_list)) == 0:
            email_error_label = Label(buddy_pass_dashboard_frame, font=('Arial', 16), fg='red', text='Error: You have no buddy pass discounts remaining.')
            email_error_label.grid(row=6, column=0, padx=None, pady=5, sticky='EW', columnspan=3)
        else:
            email_error_label = Label(dashboard_frame)
            if email_error_label.winfo_manager() == 'grid':
                if email_error_label.grid_info():
                    email_error_label.grid_remove()

            customer.buddy_pass_list.append(buddy_email)
            customer.save()
            load_buddy_pass_listbox()

    def return_to_dashboard(id):
        buddy_pass_dashboard_frame.grid_remove()
        load_dashboard_frame(id)

    reservations_button = Button(buddy_pass_dashboard_frame, font=('Arial', 16), text='Manage reservations', width=30,
                               command=lambda: return_to_dashboard(customer.id))
    reservations_button.grid(row=7, column=0, padx=None, pady=5, columnspan=3)

    exit_button = Button(buddy_pass_dashboard_frame, command=close, font=('Arial', 16), text='Exit Application', width=30)
    exit_button.grid(row=8, column=0, padx=None, pady=5, columnspan=3)

    win.update_idletasks()

    # TODO: add buddy pass handling

def close():
    win.destroy()

top_banner = Frame(win, height=100, bg='#0066CC')
top_banner.grid(row=0, column=0, padx=None, pady=None, sticky='EW', columnspan=3)

top_banner.columnconfigure(0, weight=1)
top_banner.columnconfigure(1, weight=1)
top_banner.columnconfigure(2, weight=1)


snowbowl_logo = Image.open('snowbowl_logo.png')
snowbowl_logo_resized = ImageTk.PhotoImage(snowbowl_logo.resize((100, 100), Image.LANCZOS))
logo_label = Label(top_banner, image=snowbowl_logo_resized, bg='#0066CC')
logo_label.grid(row=0, column=1, padx=None, pady=10, sticky='NSEW')

load_login_frame()

win.mainloop()
