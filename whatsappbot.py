import time
import webbrowser as web
from datetime import datetime
from typing import Optional
from urllib.parse import quote

import pyautogui as pg

from pywhatkit.core import core, exceptions, log

pg.FAILSAFE = False

core.check_connection()


phonenum = ["+919540240000"]


def sendwhatmsg_instantly(
    phone_no: str,
    message: str,
    wait_time: int = 15,
    tab_close: bool = False,
    close_time: int = 3,
) -> None:
    """Send WhatsApp Message Instantly"""

    if not core.check_number(number=phone_no):
        raise exceptions.CountryCodeException("Country Code Missing in Phone Number!")

    web.open(f"https://web.whatsapp.com/send?phone={phone_no}&text={quote(message)}")
    time.sleep(4)
    pg.click(core.WIDTH / 2, core.HEIGHT / 2)
    time.sleep(wait_time - 4)
    pg.press("enter")
    log.log_message(_time=time.localtime(), receiver=phone_no, message=message)
    if tab_close:
        core.close_tab(wait_time=close_time)

# for i in phonenum:
#     sendwhatmsg_instantly(i,"hi")

# def open_web() -> bool:
#     """Opens WhatsApp Web"""

#     try:
#         web.open("https://web.whatsapp.com",new=2)
#     except web.Error:
#         return False
#     else:
#         return True


def read_last_message(contact_name: str) -> Optional[str]:
    """Read the last message received from a specific contact"""
    time.sleep(5)  # Wait for WhatsApp Web to load
    
    web.open(f"https://web.whatsapp.com/send?phone={phonenum[0]}")
    pg.click(core.WIDTH / 2, core.HEIGHT / 2)  # Click on the chat
    time.sleep(1)
    
    # Grab the last message
    messages = list(pg.locateAllOnScreen('path/to/message_element.png'))  # Convert generator to list
    if messages:
        last_message = messages[-1]  # Get the last message
        return last_message
    return None

last_message = read_last_message("Ritvishh")  # Replace with the desired number
print("Last message received:", last_message)