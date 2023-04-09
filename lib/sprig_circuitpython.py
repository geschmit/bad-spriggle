"""
CircuitPython library to interface with the Sprig portable console.
"""
# pylint:disable=unused-import
# pylint:disable=invalid-name
# pylint:disable=import-error

import terminalio # required for the terminal stuff
import audiobusio
import digitalio
import displayio
import adafruit_st7735r # we just need the init codes. will remove later.
import board
import busio
import microcontroller
import keypad

class Button:
    """
    Sprig input mapping.
    """

    # Left
    BUTTON_W = 0
    BUTTON_A = 1
    BUTTON_S = 2
    BUTTON_D = 3

    # Right
    BUTTON_I = 0
    BUTTON_J = 1
    BUTTON_K = 2
    BUTTON_L = 3

    # Pin references
    MC_BUTTON_W:microcontroller.Pin = board.GP5
    MC_BUTTON_A:microcontroller.Pin = board.GP6
    MC_BUTTON_S:microcontroller.Pin = board.GP7
    MC_BUTTON_D:microcontroller.Pin = board.GP8
    MC_BUTTON_I:microcontroller.Pin = board.GP12
    MC_BUTTON_J:microcontroller.Pin = board.GP13
    MC_BUTTON_K:microcontroller.Pin = board.GP14
    MC_BUTTON_L:microcontroller.Pin = board.GP15

class Sprig:
    """
    Sprig device class.
    """
    _fourwire: displayio.FourWire
    screen: str = "main_menu"
    cursor: int = 0
    display: adafruit_st7735r.ST7735R
    ledLeft: digitalio.DigitalInOut
    ledRight: digitalio.DigitalInOut
    buttons: keypad.Keys
    speaker: audiobusio.I2SOut

    def __init__(self) -> None:
        displayio.release_displays()
        self._fourwire = displayio.FourWire(
            spi_bus=busio.SPI(clock=board.GP18,MOSI=board.GP19,MISO=board.GP16),
            chip_select=board.GP20,
            command=board.GP22,
            reset=board.GP26
        )
        self.display = adafruit_st7735r.ST7735R(
            bus=self._fourwire,
            rotation=270,
            width=160,
            height=128,
            backlight_pin=board.GP17
        )
        self.ledLeft = digitalio.DigitalInOut(board.GP4)
        self.ledLeft.direction = digitalio.Direction.OUTPUT
        self.ledRight = digitalio.DigitalInOut(board.GP28)
        self.ledRight.direction = digitalio.Direction.OUTPUT
        self.buttons = keypad.Keys(pins=(
            Button.MC_BUTTON_W,
            Button.MC_BUTTON_A,
            Button.MC_BUTTON_S,
            Button.MC_BUTTON_D,
            Button.MC_BUTTON_I,
            Button.MC_BUTTON_J,
            Button.MC_BUTTON_K,
            Button.MC_BUTTON_L
        ),value_when_pressed=False,pull=True)
        speaker = audiobusio.I2SOut(
            bit_clock=board.GP11,
            word_select=board.GP10,
            data=board.GP9,
            left_justified=True
        )
        return None

    def poll_input(self,button:int|None=None) -> int|None:
        """
        Waits until an input is detected from one of the sprig's buttons. 
        If an argument is given, will pause until that button is pushed, otherwise will 
        return the button's name.
        """
        while True:
            ev = self.buttons.events.get()
            if ev and ev.pressed:
                if button:
                    if button == ev.key_number:
                        return
                else:
                    return ev.key_number