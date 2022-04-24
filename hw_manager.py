from RPi import GPIO
from time import sleep
import sys
import structlog
logger = structlog.get_logger()
# rotary encoder
clk=23
dt=24
sw=25
k1=4
k2=27

PIN_CLK=23
PIN_DT=24
SWITCHES = [
    {
    "name":"sw",
    "n": 25
},
    {
    "name":"k1",
    "n": 4
},
    {
    "name":"k2",
    "n": 27
}
]

class HardwareManager:
    def __init__(self, clk_state, dt_state, sw_state, k1_state, k2_state, counter=0):
        self.counter=counter
        self.last_clk_state = clk_state
        self.last_dt_state = dt_state
        self.last_switch = {
            "sw": sw_state,
            "k1": k1_state,
            "k2": k2_state
        }

    def read_scroll(self,clk_state, dt_state):
        action="99"
        if clk_state != self.last_clk_state:
            if dt_state != clk_state:
                self.counter += 1
                action=1
            else:
                self.counter -= 1
                action=-1
        self.last_clk_state = clk_state
        return action

    def read_switch(self, name, state):
        # 0 on press
        return_state=1
        if state != self.last_switch[name]:
            return_state = state
        self.last_switch[name] = state
        return return_state

    def bind_and_run(self, fn_scroll_right, fn_scroll_left, fn_select, fn_press_k1, fn_press_k2):
        while True:
            s=self.read_scroll(GPIO.input(clk), GPIO.input(dt))
            if s == -1:
                fn_scroll_left()
            if s == 1:
                fn_scroll_right()
            if 0==self.read_switch("sw", GPIO.input(sw)):
                fn_select()
            if 0==self.read_switch("k1", GPIO.input(k1)):
                fn_press_k1()
            if 0==self.read_switch("k2", GPIO.input(k2)):
                fn_press_k2()
            sleep(0.01)


    def _dump_counter(self, clk_state, dt_state):
        if clk_state != self.last_clk_state:
            if dt_state != clk_state:
                    self.counter += 1
            else:
                    self.counter -= 1
            print(self.counter)
        self.last_clk_state = clk_state

    def _dump_switch(self, name, state):
        if state != self.last_switch[name]:
            print(f"{name} state {state}")
        self.last_switch[name] = state

    def monitor(self):
        while True:
            self._dump_counter(GPIO.input(clk), GPIO.input(dt))
            self._dump_switch("sw", GPIO.input(sw))
            self._dump_switch("k1", GPIO.input(k1))
            self._dump_switch("k2", GPIO.input(k2))
            sleep(0.01)

def get_hardware_manager():

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(k1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(k2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    return HardwareManager(GPIO.input(clk), GPIO.input(dt),GPIO.input(sw), GPIO.input(k1), GPIO.input(k2))    

#x=get_hardware_manager()
#x.monitor()
