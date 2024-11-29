import requests
import string
import random
import time
import atexit

print("enter webhook")
DISCORD_WEBHOOK1 = input()

used_codes = set()

def save_used_codes():
    with open("used_codes.txt", "a") as file:
        for code in used_codes:
            file.write(f"{code}\n")

atexit.register(save_used_codes)

def send_to_discord_webhooks(message):
    payload = {
        "content": message
    }
    response1 = requests.post(DISCORD_WEBHOOK1, json=payload)

    if response1.status_code != 204:
        print(f"Error sending message to webhook: {response1.status_code}")

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def check_gift_code(code):
    url = f"https://discord.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"
    response = requests.get(url)
    if response.status_code == 200:
        send_to_discord_webhooks(f"Successfully redeemed {code}")
        return True
    else:
        print(f"Error redeeming gift code {code}: {response.status_code}")
        return False

def main():
    with open("used_codes.txt", "r") as file:
        for line in file:
            used_codes.add(line.strip())
        
    while len(used_codes) < 4.511e+48: # approximately all codes seem to be 4.511e+48 but I don't remember but I don't really know if you need to calculate it yourself there are from 1 to 16, If necessary, you can change the number symbols
        length = random.randint(1, 16)
        code = generate_random_string(length)
        if code not in used_codes:
            if check_gift_code(code):
                used_codes.add(code)
            else:
                used_codes.add(f"{code} (invalid)")
            time.sleep(0.01)

if __name__ == "__main__":
    main()
