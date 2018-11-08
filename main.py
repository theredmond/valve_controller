import time
import tkinter as tk

VALVES = [
    {
        "name": "One"
    },
    {
        "name": "Two"
    },
    {
        "name": "Three"
    },
    {
        "name": "Four"
    },
    {
        "name": "Five"
    },
    {
        "name": "Six"
    },
    {
        "name": "Seven"
    },
    {
        "name": "Eight"
    },
    {
        "name": "Nine"
    },
    {
        "name": "Ten"
    },
]


class ValveController:
    def __init__(self, container, valve, idx):
        self.valve = Valve(container, valve, idx)

        self.label = tk.Label(container, text=valve["name"])
        self.label.grid(column=idx, row=1)

        self.start_button = tk.Button(
            container, text="Start Valve", command=self.valve.start_valve)
        self.start_button.grid(column=idx, row=5)

        self.stop_button = tk.Button(
            container, text="Stop Valve", command=self.valve.stop_valve)
        self.stop_button.grid(column=idx, row=6)


class Valve:
    def __init__(self, container, valve, idx):
        self.container = container
        self.name = valve["name"]
        self.current_time = 0.0
        self.start_time = 0.0
        self.end_time = 0.0

        self.time_elapsed = tk.Label(container, text="0:00")
        self.time_elapsed.grid(column=idx, row=2)

        self.time_remaining = tk.Label(container, text="0:00")
        self.time_remaining.grid(column=idx, row=3)

        self.user_value = tk.Entry(container, width=10)
        self.user_value.insert(0, "10:59")
        self.user_value.grid(column=idx, row=4)

    def start_valve(self):
        print(f"Start valve: ", self.name)
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
        print(f"Stop valve: ", self.name)
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

        for idx, valve in enumerate(VALVES):
            ValveController(valve_frame, valve, idx)

        self.close_button = tk.Button(
            bottom_frame, text="Exit", command=master.quit)
        self.close_button.pack()


root = tk.Tk()
my_gui = MainWindow(root)
root.mainloop()
