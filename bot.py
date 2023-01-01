from http.client import HTTPSConnection
import sys
from json import dumps
from time import sleep
from random import random, choice

file = open("info.txt")
text = file.read().splitlines()

print()
print("------------- WELCOME TO JAGCWEB AUTO-MESSAGE DISCORD BOT -------------")
print()

if len(sys.argv) > 1:
    if sys.argv[1] == "--setall" and input("Configure bot? (y/n)") == "y":
        file.close()
        file = open("info.txt", "w")
        text = []
        text.append(input("Discord ID (Example#1234): "))
        text.append(input("Discord token: "))
        text.append(input("Discord channel URL: "))
        text.append(input("Discord channel ID (enable developer options): "))

        for parameter in text:
            file.write(parameter + "\n")

        file.close()
        exit()
    elif sys.argv[1] == "--setchannel" and input("Set channel? (y/n)") == "y":
        user_agent = text[0]
        token = text[1]
        text = text[0:2]
        file.close()
        file = open("info.txt", "w")
        text.append(input("Discord channel URL: "))
        text.append(input("Discord channel ID: "))
        for parameter in text:
            file.write(parameter + "\n")

        file.close()
        exit()
    elif sys.argv[1] == "--setauth" and input("Set authentication? (y/n)") == "y":
        channelurl = text[2]
        channelid = text[3]
        text = text[2:4]
        file.close()
        file = open("info.txt", "w")
        text.insert(0, input("Discord token: "))
        text.insert(0, input("User agent: "))
        for parameter in text:
            file.write(parameter + "\n")

        file.close()
        exit()
    elif sys.argv[1] == "--help":
        print("Showing help for discord-auto-message")
        print("Usage:")
        print("  'py bot.py'               :  Runs the autotyper. Fill in the messages and wait times.")
        print("  'py bot.py --setall'      :  Configure all settings.")
        print("  'py bot.py --setchannel'  :  Set channel to send message to. Includes Channel ID and Channel URL")
        print("  'py bot.py --setauth'     :  Set authentication. Includes User Token and User Agent")
        print("  'py bot.py --help'        :  Show help")
        exit()

    if len(text) != 4:
        print("An error was found inside the user information file. Run the script with the 'Set All' flag ('py bot.py --setall') to reconfigure.")
        exit()
        
if len(sys.argv) == 0:
    exit()
    
header_data = {
    "content-type": "application/json",
    "user-agent": text[0],
    "authorization": text[1],
    "host": "discordapp.com",
    "referrer": text[2]
}

def get_connection():
    return HTTPSConnection("discordapp.com", 443)


def send_message(conn, channel_id, message_data):
    try:
        conn.request("POST", f"/api/v6/channels/{channel_id}/messages", message_data, header_data)
        resp = conn.getresponse()

        if 199 < resp.status < 300:
            print("Message sent!")
            pass

        else:
            sys.stderr.write(f"Received HTTP {resp.status}: {resp.reason}\n")
            pass

    except:
        sys.stderr.write("Failed to send_message\n")
        for key in header_data:
            print(key + ": " + header_data[key])


def main(msg):
    message_data = {
        "content": msg,
        "tts": "false",
    }

    send_message(get_connection(), text[3], dumps(message_data))


if __name__ == '__main__':
    print("Messages will send automatically after config next info:")
    #thislist = ["Hi", "Hope lvl10 soon :)", "GM guys", "hahaha", "yes it is :)", "xD", "desire to airdrop", "Want my shilling role :(", "shilling role i come", "wow lvl50 too much", "lvl10 soon guys :D", "how are you guys?", "want my airdrop soon :(", "Good afternon", "When will we know the OG3 Gold requirements?", "Want my OG3 Bronze role :(", "impatient for claim my OATs", "My nfts will claimed soon haha", "Yo guys", "Merry christmas", "Have a happy night with your families", "yes xD", ":)", ":(", "Happy holidays", "Regards from Spain", "Titi the best", ":D", "OG3 comming!!!", "hahahahaha", "lol", "thx"]
    message = input("Message Text: ")
    messages = int(input("Message Quantity: "))
    main_wait = int(input("Waiting time between messages (in seconds): "))
    human_margin = int(input("Margin of human error (recommended: 5): "))
    print()
    print(messages)
    for i in range(0, messages):
        #main(choice(thislist))
        main(message)
        print("Estimated time to complete: " + str((messages-i) * (human_margin // 2 + main_wait) // 60) + " minutes.")
        print("Iteration " + str(i) + " complete.\n")
        sleep(main_wait)
        sleep(random()*human_margin)

    print("Session complete! " + str(messages) + " messages sent.")
