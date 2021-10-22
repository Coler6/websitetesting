from __future__ import annotations
import asyncio
import logging
import rillrate
from rillrate import prime as rr_prime
import typing

HOME_GUILD_ID = 727195918180548728
STDOUT_CHANNEL_ID = 727196459518263437
PACKAGE = "HikariTesting"
DASHBOARD = "Dashboard"
GROUP_CONFIG = "Interactive"
GROUP_CONFIG1 = "Info"

class Data:
    def __init__(self) -> None:
        self.value = 0
        self.clicked = 0
        self.switch = True
        self.switch_1 = True

    def set_value(self, new_value):
        self.value = new_value
    def get_value(self):
        try:
            return int(self.value)
        except:
            return self.value
    def add_click(self):
        self.clicked += 1
    def get_click(self):
        return self.clicked
    def set_switch(self, value):
        self.switch = value
    def get_switch(self):
        return self.switch
    def set_switch_1(self, value):
        self.switch_1 = value
    def get_switch_1(self):
        if str(self.switch_1) == "True": return True
        else: return False

rillrate.install()
data = Data()
values = list(range(0, 100 + 1, 5))
value = []
for i in values:
    value.append(str(i))
selector = rr_prime.Selector(f"{PACKAGE}.{DASHBOARD}.{GROUP_CONFIG}.Selector", label="Choose!", options=value)
slider = rr_prime.Slider(
    f"{PACKAGE}.{DASHBOARD}.{GROUP_CONFIG}.Slider", label="More fine grain control", min=0, max=100, step=1
)
button = rr_prime.Click(f"{PACKAGE}.{DASHBOARD}.{GROUP_CONFIG}.Click", label="Click!")
button1 = rr_prime.Click(f"{PACKAGE}.{DASHBOARD}.{GROUP_CONFIG}.Click", label="Click2!")
switch = rr_prime.Switch(f"{PACKAGE}.{DASHBOARD}.{GROUP_CONFIG}.Switch", label="Switch!")
switch1 = rr_prime.Switch(f"{PACKAGE}.{DASHBOARD}.{GROUP_CONFIG}.Ping", label="Ping!")
pulse = rr_prime.LiveTail(f"{PACKAGE}.{DASHBOARD}.{GROUP_CONFIG1}.Logs")
table = (rr_prime.Table(f"{PACKAGE}.{DASHBOARD}.{GROUP_CONFIG1}.Values", columns=[(1, "Button"), (2, "Switch"), (3, "Slider/Selector"), (4, "Switch")]))
table.add_row(0)
table.set_cell(0, 1, "0")
table.set_cell(0, 2, "False")
table.set_cell(0, 3, "0")
table.set_cell(0, 4, "False")
gauge = rr_prime.Gauge(f"{PACKAGE}.{DASHBOARD}.{GROUP_CONFIG1}.Gauge", min=0, max=100)
gauge.set(0)
histogram = rr_prime.Histogram(f"{PACKAGE}.{DASHBOARD}.{GROUP_CONFIG1}.Histogram").add(42)

def selector_callback(activity: rillrate.Activity, action: rillrate.Action):
    logging.info("Selector activity: %s | action = %s", activity, action)
    if action is not None:
        logging.info("Selected: %s", action.value)
        pulse.log_now("Selector", "1", "Changed to " + action.value)
        table.set_cell(0, 3, str(int(action.value)))
        gauge.set(int(action.value))
        data.set_value(action.value)
        slider.apply(int(action.value))
        selector.apply(int(action.value))
        return

def slider_callback(activity: rillrate.Activity, action: rillrate.Action):
    logging.info("Slider activity: %s | action = %s", activity, action)
    if action is not None:
        logging.info(f"Slided: {action.value}")
        table.set_cell(0, 3, str(int(action.value)))
        gauge.set(int(action.value))
        data.set_value(action.value)
        slider.apply(str(int(action.value)))
        selector.apply(str(int(action.value)))
        return

def click_callback(activity: rillrate.Activity, action: rillrate.Action):
    logging.info("Button activity: %s | action = %s", activity, action)
    if action is not None:
        data.add_click()
        table.set_cell(0, 1, str(data.get_click()))
        pulse.log_now("Button", "1", "Button was clicked")
        return

def switch_callback(activity: rillrate.Activity, action: rillrate.Action):
    logging.info("Slider activity: %s | action = %s", activity, action.value)
    if action is not None:
        data.set_switch(action.value)
        table.set_cell(0, 2, str(action.value))
        pulse.log_now("Switch", "1", f"Switch is now {'On' if action.value == True else 'Off'}")
        switch.apply(action.value)
        print(action.value)
        return

def switch_1_callback(activity: rillrate.Activity, action: rillrate.Action):
    logging.info("Slider activity: %s | action = %s", activity, action.value)
    if action is not None:
        data.set_switch_1(action.value)
        table.set_cell(0, 4, str(action.value))
        pulse.log_now("Switch1", "1", f"Switch is now {'On' if action.value == True else 'Off'}")
        switch1.apply(action.value)
        return

selector.sync_callback(selector_callback)
slider.sync_callback(slider_callback)
button.sync_callback(click_callback)
button1.sync_callback(click_callback)
switch.sync_callback(switch_callback)
switch1.sync_callback(switch_1_callback)
