"""
The file for the ManualTitration class
"""
import time
from titration.devices.library import Keypad
from titration.ui_state import main_menu
from titration.ui_state.ui_state import UIState
from titration.ui_state.user_value.degas_time import DegasTime
from titration.ui_state.user_value.volume_to_move import VolumeToMove


class ManualTitration(UIState):
    """
    This is a class for the ManualTitration state of the titrator

    Attributes:
        titrator (Titrator object): the titrator is used to move through the state machine
        previous_state (UIState object): the previous_state is used to return the last visited state
        substate (int): the substate is used to keep track of substate of the UIState
        values (dict): values is a dictionary to hold the p_direction
    """

    def __init__(self, titrator):
        """
        The constructor for the ManualTitration class

        Parameters:
            titrator (Titrator object): the titrator is used to move through the state machine
        """
        super().__init__(titrator)
        self.values = {
            "p_direction": 0,
        }
        self._last_printed_substate = 0
        self._last_print_time = 0

    def handle_key(self, key):
        """
        The function to respond to a keypad input
        """
        if self.substate == 1:
            self._set_next_state(VolumeToMove(self.titrator, self), True)
            self.substate += 1

        elif self.substate == 2:
            if key == Keypad.KEY_0:
                self.values["p_direction"] = 0
                print(f"\n[Hardware] Pulling {self.titrator.volume_to_move} ml...")
                self.titrator.pump.pull_volume_in(self.titrator.volume_to_move)
                self.substate += 1
            elif key == Keypad.KEY_1:
                self.values["p_direction"] = 1
                print(f"\n[Hardware] Pushing {self.titrator.volume_to_move} ml...")
                self.titrator.pump.push_volume_out(self.titrator.volume_to_move)
                self.substate += 1

        elif self.substate == 3:
            if key == Keypad.KEY_1:
                print("\n")
                self.substate = 1
                self._last_printed_substate = 0
            elif key == Keypad.KEY_0:
                print("\n")
                self.substate += 1

        elif self.substate == 4:
            if key == Keypad.KEY_0:
                self.substate = 7
            elif key == Keypad.KEY_1:
                self.substate += 1

        elif self.substate == 5:
            self._set_next_state(DegasTime(self.titrator, self), True)
            self.substate += 1

        elif self.substate == 6:
            # Wait for degas to finish, handled in loop
            pass

        elif self.substate == 7:
            self._set_next_state(main_menu.MainMenu(self.titrator), True)

    def loop(self):
        """
        The function to loop through and display to the terminal
        """
        # Handle state-entry prints to prevent terminal spam
        if self.substate != self._last_printed_substate and self.substate != 3:
            if self.substate == 1:
                print("\n--- Manual Titration ---")
                print("Press any key to enter volume to move.")
            elif self.substate == 2:
                print("\nDirection:")
                print("0: Pull Volume In")
                print("1: Push Volume Out")
            elif self.substate == 4:
                print("\nDegas?")
                print("0 - No")
                print("1 - Yes")
            elif self.substate == 5:
                print("\nPress any key to enter degas time.")
            elif self.substate == 6:
                degas_time = self.titrator.degas_time
                print(f"\n[Hardware] Degassing for {degas_time} seconds...")
                self.titrator.stir_controller.set_fast()
                time.sleep(degas_time)
                self.titrator.stir_controller.set_stop()
                print("[Hardware] Degassing complete.")
                self.substate += 1
            elif self.substate == 7:
                print("\nReturn to main menu.")
                print("Press any key to continue.")

            self._last_printed_substate = self.substate

        # Handle continuous pH reading in substate 3
        if self.substate == 3:
            current_t = time.time()
            if current_t - self._last_print_time > 1.0:
                volts = self.titrator.ph_probe.get_voltage()
                print(f"[Hardware] Current pH Voltage: {volts:>4.5f} V | Add more HCl? (0: No, 1: Yes)")
                self._last_print_time = current_t

    def start(self):
        """
        The function to display MANUAL SELECTED upon entering the ManualTitration state
        """
        print("\nMANUAL SELECTED")
