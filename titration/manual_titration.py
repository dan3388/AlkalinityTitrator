"""
Open Acidification: Alkalinity Titrator 2025-2026
Manual Titration Test Script
"""

import time

from titration.titrator import Titrator
from titration.ui_state.titration.manual_titration import ManualTitration


def run():
    """
    Runs the manual titration state directly for testing the hardware APIs.
    """
    print("Initializing Titrator for Manual Test...")
    titrator = Titrator()

    # Set the initial state directly to ManualTitration for testing
    titrator.state = ManualTitration(titrator)
    titrator.state.start()

    print("Starting hardware test loop. Press Ctrl+C to exit.")
    try:
        while True:
            titrator.loop()
            time.sleep(0.05)  # Yield slightly to prevent 100% CPU utilization
    except KeyboardInterrupt:
        print("\nTest terminated by user.")


if __name__ == "__main__":
    run()
