import time
import tkinter as tk

VALVES = [
    {
        "display_name": "One",
        "default_on": 10,
        "default_off": 50,
    },
    {
        "display_name": "Two",
        "default_on": 10,
        "default_off": 50,
    },
    {
        "display_name": "Three",
        "default_on": 10,
        "default_off": 50,
    },
    {
        "display_name": "Four",
        "default_on": 10,
        "default_off": 50,
    },
    {
        "display_name": "Five",
        "default_on": 10,
        "default_off": 50,
    },
    {
        "display_name": "Six",
        "default_on": 10,
        "default_off": 50,
    },
    {
        "display_name": "Seven",
        "default_on": 10,
        "default_off": 50,
    },
    {
        "display_name": "Eight",
        "default_on": 10,
        "default_off": 50,
    },
    {
        "display_name": "Nine",
        "default_on": 10,
        "default_off": 50,
    },
    {
        "display_name": "Ten",
        "default_on": 10,
        "default_off": 50,
    },
]


class ValveController:
    def __init__(self):
        self.valves = []

    def add_valve(self, container, valve, idx):
        self.valves.append(Valve(container, valve, idx))
    
    def start_valves(self):
        # add logic here for valve control/management
        pass

class Valve:
    def __init__(self, container, valve, idx):
        self.container = container
        self.valve = valve
        self.display_name = valve["display_name"]
        self.current_time = 0.0
        self.start_time = 0.0
        self.end_time = 0.0

        self.label = tk.Label(container, text=self.display_name)
        self.label.grid(column=idx, row=1)

        self.time_elapsed = tk.Label(container, text="0:00")
        self.time_elapsed.grid(column=idx, row=2)

        self.time_remaining = tk.Label(container, text="0:00")
        self.time_remaining.grid(column=idx, row=3)

        self.user_value = tk.Entry(container, width=10)
        self.user_value.insert(0, "10:59")
        self.user_value.grid(column=idx, row=4)

    def start_valve(self):
        print(f"Start valve: ", self.display_name)
        self.running = True
        self.running_time = (int(self.user_value.get().split(
            ':')[0]) * 60) + int(self.user_value.get().split(':')[1])
        self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        if self.running:
            seconds_from_start = int(time.time() - self.start_time)
            seconds_from_end = self.running_time - seconds_from_start

            if seconds_from_end <= 0:
                self.stop_valve()
                return

            self.time_elapsed.configure(
                text=f"{seconds_from_start//60}:{str(seconds_from_start % 60).zfill(2)}")
            self.time_remaining.configure(
                text=f"{seconds_from_end//60}:{str(seconds_from_end % 60).zfill(2)}")
            self.container.after(1000, self.update_timer)

    def stop_valve(self):
        print(f"Stop valve: ", self.display_name)
        self.running = False
        self.time_elapsed.configure(text="0:00")
        self.time_remaining.configure(text="0:00")


class MainWindow:
    def __init__(self, master):
        self.master = master
        master.title("Hopperdashery Valve Controller")

        valve_frame = tk.Frame(master)
        valve_frame.pack()

        bottom_frame = tk.Frame(master)
        bottom_frame.pack(side=tk.BOTTOM)

        valve_controller = ValveController()

        for idx, valve in enumerate(VALVES):
            valve_controller.add_valve(valve_frame, valve, idx)

        self.start_button = tk.Button(
            bottom_frame, text="Start", command=valve_controller.start_valves())
        self.start_button.pack()

        self.close_button = tk.Button(
            bottom_frame, text="Exit", command=master.quit)
        self.close_button.pack()


root = tk.Tk()
my_gui = MainWindow(root)
root.mainloop()
