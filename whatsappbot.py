import time
import webbrowser as web
from datetime import datetime
from typing import Optional
from urllib.parse import quote

import pyautogui as pg

from pywhatkit.core import core, exceptions, log

pg.FAILSAFE = False

core.check_connection()




def sendwhatmsg_instantly(
    phone_no: str,
    message: str,
    wait_time: int = 15,
    tab_close: bool = True,
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
    time.sleep(4)
    # log.log_message(_time=time.localtime(), receiver=phone_no, message=message)
    if tab_close:
        core.close_tab(wait_time=close_time)



message = """
Hi [User's Name],

We hope you’re doing well! To ensure that those in need of blood can find suitable donors quickly, we kindly ask you to update your profile with your current location and availability.

Having accurate and up-to-date information makes a significant difference in connecting donors with recipients efficiently.

Thank you for your support and for being a part of our community!

Best regards,
Friends2Support
"""



file_path = 'numbers.csv'  # Change this to your actual file path

# Open the file and read it
phonenum = []
name = []
with open(file_path, 'r') as file:

    # Read the rest of the lines (rows)
    for line in file:
        row = line.strip().split(',')
        phonenum.append("+91" + row[0])
        name.append(row[1])


print(phonenum)
print(name)

for i in range(len(phonenum)):
    personalized_message = message.replace("[User's Name]", name[i])
    sendwhatmsg_instantly(phonenum[i] , personalized_message)