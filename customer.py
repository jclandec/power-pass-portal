import random
import json
import os
from tkinter import *
from tkinter.ttk import Combobox
from PIL import Image, ImageTk

class Customer:
    def __init__(self, id=None, name="", dob="", pin="", pay_method="Unknown", days_purchased=0, reservation_list=None, buddy_pass_list=None):
        if reservation_list is None:
            reservation_list = []
        if buddy_pass_list is None:
            buddy_pass_list = []
        self._id = id if id is not None else random.randint(900000000, 999999999)
        self.name = name
        self.dob = dob
        self.pin = pin
        self.pay_method = pay_method
        self.days_purchased = days_purchased
        self.reservation_list = reservation_list
        self.buddy_pass_list = buddy_pass_list

    def save(self):
        data = self.to_dict()
        with open('passholders.json', 'r+') as file:
            try:
                passholders = json.load(file)
            except json.JSONDecodeError:
                passholders = {}
            passholders[str(self._id)] = data
            file.seek(0)
            json.dump(passholders, file, indent=4)
            file.truncate()

    def to_dict(self):
        return {
            "id": self._id,
            "name": self.name,
            "dob": self.dob,
            "pin": self.pin,
            "pay_method": self.pay_method,
            "days_purchased": self.days_purchased,
            "reservation_list": self.reservation_list,
            "buddy_pass_list": self.buddy_pass_list
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            name=data["name"],
            dob=data["dob"],
            pin=data["pin"],
            pay_method=data["pay_method"],
            days_purchased=data["days_purchased"],
            reservation_list=data["reservation_list"],
            buddy_pass_list=data["buddy_pass_list"]
        )

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value