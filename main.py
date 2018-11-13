import time
import tkinter as tk

VALVES = [
    {
        "display_name": "One",
        "default_on": "00:3",
        "default_off": "50:00",
    },
    {
        "display_name": "Two",
        "default_on": "00:3",
        "default_off": "50:00",
    },
    {
        "display_name": "Three",
        "default_on": "00:3",
        "default_off": "50:00",
    },
    {
        "display_name": "Four",
        "default_on": "00:3",
        "default_off": "50:00",
    },
    {
        "display_name": "Five",
        "default_on": "00:3",
        "default_off": "50:00",
    },
    {
        "display_name": "Six",
        "default_on": "00:3",
        "default_off": "50:00",
    },
    {
        "display_name": "Seven",
        "default_on": "00:3",
        "default_off": "50:00",
    },
    {
        "display_name": "Eight",
        "default_on": "00:3",
        "default_off": "50:00",
    },
    {
        "display_name": "Nine",
        "default_on": "00:3",
        "default_off": "50:00",
    },
    {
        "display_name": "Ten",
        "default_on": "00:3",
        "default_off": "50:00",
    },
]

VALVE_LABELS = [
    "Name",
    "Running Time",
    "Time Remaining",
    "Run Time",
    "Wait Time",
]


class ValveController:
    def __init__(self):
        self.valves = []
        self.running = False
        self.currently_running_valve_index = None

    def add_valve(self, container, valve, valve_index):
        # valve index from MainWindow is 1-indexed because of the labels column
        # also helps with some reasoning
        self.valves.append(Valve(self.valve_complete, container, valve, valve_index))
    
    def start_valves(self, valve_index = 0):
        self.currently_running_valve_index = valve_index
        self.valves[valve_index].start_valve()
        self.running = True

    def stop_valves(self):
        self.running = False
        self.valves[self.currently_running_valve_index].stop_valve()

    def valve_complete(self, valve_index):
        print(f"Valve {self.valves[valve_index - 1].display_name} Complete")
        if self.running:
            # check to see if we need to rotate around
            if self.currently_running_valve_index < len(self.valves) - 1:
                self.currently_running_valve_index += 1
            else: 
                self.currently_running_valve_index = 0

            # start next valve
            self.valves[self.currently_running_valve_index].start_valve()


class Valve:
    def __init__(self, valve_completion_handler, container, valve, valve_index):
        self.valve_completion_handler = valve_completion_handler
        self.container = container
        self.valve = valve
        self.valve_index = valve_index

        self.display_name = valve["display_name"]
        self.current_time = 0.0
        self.start_time = 0.0
        self.running = False

        self.label = tk.Label(container, text=self.display_name)
        self.label.grid(column=self.valve_index, row=1)

        self.time_elapsed = tk.Label(container, text="0:00")
        self.time_elapsed.grid(column=self.valve_index, row=2)

        self.time_remaining = tk.Label(container, text="0:00")
        self.time_remaining.grid(column=self.valve_index, row=3)

        self.run_time = tk.Entry(container, width=10)
        self.run_time.insert(0, valve["default_on"])
        self.run_time.grid(column=self.valve_index, row=4)

        self.wait_time = tk.Entry(container, width=10)
        self.wait_time.insert(0, valve["default_off"])
        self.wait_time.grid(column=self.valve_index, row=5)

    def start_valve(self):
        print(f"Starting Valve {self.display_name}")
        self.running = True
        self.running_time = (int(self.run_time.get().split(
            ":")[0]) * 60) + int(self.run_time.get().split(":")[1])
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
            
            # this is calls back to the container to update the UI
            self.container.after(1000, self.update_timer)

    def stop_valve(self):
        self.running = False
        self.time_elapsed.configure(text="0:00")
        self.time_remaining.configure(text="0:00")
        self.valve_completion_handler(self.valve_index)


class MainWindow:
    def __init__(self, master):
        self.master = master
        master.title("Hopperdashery Valve Controller")

        valve_frame = tk.Frame(master)
        valve_frame.pack()

        bottom_frame = tk.Frame(master)
        bottom_frame.pack(side=tk.BOTTOM)

        for idx, name in enumerate(VALVE_LABELS):
            self.label = tk.Label(valve_frame, text=name)
            self.label.grid(column=0, row=idx + 1)

        valve_controller = ValveController()

        for idx, valve in enumerate(VALVES):
            valve_controller.add_valve(valve_frame, valve, idx + 1)

        self.start_button = tk.Button(
            bottom_frame, text="Start", command=valve_controller.start_valves)
        self.start_button.pack()

        self.start_button = tk.Button(
            bottom_frame, text="Stop", command=valve_controller.stop_valves)
        self.start_button.pack()

        self.close_button = tk.Button(
            bottom_frame, text="Exit", command=master.quit)
        self.close_button.pack()


root = tk.Tk()
my_gui = MainWindow(root)
root.mainloop()
