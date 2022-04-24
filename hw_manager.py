from typing import Callable
from RPi import GPIO
from time import sleep
import sys
import structlog
import time

logger = structlog.get_logger()
# rotary encoder
clk = 23
dt = 24
sw = 25
k1 = 4
k2 = 27
k3 = 22
k4 = 26

PIN_CLK = 23
PIN_DT = 24
SWITCHES = [
    {"name": "sw", "n": 25},
    {"name": "k1", "n": 4},
    {"name": "k2", "n": 27},
    {"name": "k3", "n": 22},
    {"name": "k4", "n": 26},
]


class HardwareManager:
    def __init__(
        self,
        clk_state: int,
        dt_state: int,
        sw_state: int,
        k1_state: int,
        k2_state: int,
        k3_state: int,
        k4_state: int,
        counter: int = 0,
    ):
        self.counter = counter
        self.last_clk_state = clk_state
        self.last_dt_state = dt_state
        self.last_switch = {
            "sw": sw_state,
            "k1": k1_state,
            "k2": k2_state,
            "k3": k3_state,
            "k4": k4_state,
        }
        self.n = 0
        self.time_s = int(time.time())
        self.last_print = self.time_s

    def read_scroll(self, clk_state: int, dt_state: int):
        action = "99"
        if clk_state != self.last_clk_state:
            if dt_state != clk_state:
                self.counter += 1
                action = 1
            else:
                self.counter -= 1
                action = -1
        self.last_clk_state = clk_state
        return action

    def read_switch(self, name: str, state: int):
        # 0 on press
        return_state = 1
        if state != self.last_switch[name]:
            return_state = state
        self.last_switch[name] = state
        return return_state

    def log_track_info(self, fn_info: Callable):
        if self.time_s % 10 == 0 and self.last_print != self.time_s:
            self.last_print = self.time_s
            fn_info()

    def bind_and_run(
        self,
        fn_scroll_right: Callable,
        fn_scroll_left: Callable,
        fn_select: Callable,
        fn_press_k1: Callable,
        fn_press_k2: Callable,
        fn_press_k3: Callable,
        fn_press_k4: Callable,
        fn_info: Callable,
    ):
        while True:
            s = self.read_scroll(GPIO.input(clk), GPIO.input(dt))
            if s == -1:
                fn_scroll_left()
            if s == 1:
                fn_scroll_right()
            if 0 == self.read_switch("sw", GPIO.input(sw)):
                fn_select()
            if 0 == self.read_switch("k1", GPIO.input(k1)):
                fn_press_k1()
            if 0 == self.read_switch("k2", GPIO.input(k2)):
                fn_press_k2()
            if 0 == self.read_switch("k3", GPIO.input(k3)):
                fn_press_k3()
            if 0 == self.read_switch("k4", GPIO.input(k4)):
                fn_press_k4()
            sleep(0.01)
            self.time_s = int(time.time())
            self.log_track_info(fn_info)

    def _dump_counter(self, clk_state: int, dt_state: int):
        if clk_state != self.last_clk_state:
            if dt_state != clk_state:
                self.counter += 1
            else:
                self.counter -= 1
            print(self.counter)
        self.last_clk_state = clk_state

    def _dump_switch(self, name: str, state: int):
        if state != self.last_switch[name]:
            print(f"{name} state {state}")
        self.last_switch[name] = state

    def monitor(self):
        while True:
            self._dump_counter(GPIO.input(clk), GPIO.input(dt))
            self._dump_switch("sw", GPIO.input(sw))
            self._dump_switch("k1", GPIO.input(k1))
            self._dump_switch("k2", GPIO.input(k2))
            self._dump_switch("k3", GPIO.input(k3))
            sleep(0.01)


def get_hardware_manager():

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(k1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(k2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(k3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(k4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    return HardwareManager(
        GPIO.input(clk),
        GPIO.input(dt),
        GPIO.input(sw),
        GPIO.input(k1),
        GPIO.input(k2),
        GPIO.input(k3),
        GPIO.input(k4),
    )


# x=get_hardware_manager()
# x.monitor()
