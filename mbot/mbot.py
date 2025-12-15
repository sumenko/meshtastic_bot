# tcp_example.py
import time
import meshtastic
import meshtastic.tcp_interface
from pubsub import pub
from datetime import datetime
import os
from pprint import pprint
import logging
from google.protobuf.message import DecodeError

logging.basicConfig(
    filename='app.log',
    level=logging.INFO, # Set the minimum logging level to capture
    format='%(asctime)s - %(levelname)s - %(message)s' # Define the message format
)
# Configuration
HOST_IP = '192.168.10.185'  # Replace with your Meshtastic device's IP or hostname (e.g., 'meshtastic.local')

def clear_console():
    """Clears the console screen based on the operating system."""
    # For Windows, the command is 'cls'
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def onReceive(packet, interface):
    """
    Callback function called when a message is received.
    """
    # pprint(packet)
    # Check if the packet contains a text message
    if 'decoded' in packet and 'text' in packet['decoded']:
        message = packet['decoded']['text'].lower()
        # sender_id = packet.get('fromId', 'Unknown')
        sender_from = packet.get('from', 'Unknown')
        hop_start = packet.get('hopStart', 'hopStart')
        hop_limit = packet.get('hopLimit', 'hopLimit ')


        now = datetime.now()
        f_time = now.strftime("%H:%M:%S")
        sender = str(hex(sender_from))[-4:]
        log_msg = f"{f_time} {sender}: {message}"
        logging.info(log_msg)

        if message == 'hops?' or 'ping' in message or 'test' in message or message == 'ack':
            print('Got ', message)
            hops = ''
            try:
                hops_int = hop_limit - hop_start
                if hops_int > 0:
                    hops = ' hops ' + str(hops_int)
                else:
                    hops = ' Direct'
            except TypeError:
                print(hop_limit, "-",  hop_start)
                hops = ''

            answer = f"@{sender} ok!" + hops
            # print(answer)
            logging.info(f'{f_time} Send answer: {answer} {hops}')
            
            interface.sendText(answer)

        elif '/help' in message:
            prefix = f'{f_time} @{sender} '
            logging.info(f'answer /help: {prefix}')
            cmd_help(interface=interface, prefix=prefix)
        elif 'ping' in message or 'test' in message:
            with open('packets\\' + f'{sender}.proto', "a") as outp:
                outp.write(repr(packet))



def onConnection(interface, topic=pub.AUTO_TOPIC):
    """
    Callback function called when the bot successfully connects (or reconnects) to the radio.
    """
    print("Connected to radio. Sending initial message...")
    # Send a broadcast text message
    ###################
    # interface.sendText("Type /ping to bot")

def cmd_help(interface, prefix = ''):
    interface.sendText(prefix + "Bot commands: /help /ping")


def main():
    # Subscribe to the message reception and connection established topics
    pub.subscribe(onReceive, "meshtastic.receive")
    pub.subscribe(onConnection, "meshtastic.connection.established")

    print(f"Attempting to connect to {HOST_IP} over TCP...")
    try:
        # Initialize the TCP interface
        # The library automatically handles the connection process in a background thread
        interface = meshtastic.tcp_interface.TCPInterface(hostname=HOST_IP)
        clear_console()
        print("Bot is running and listening for messages. Press Ctrl+C to exit.")
        # Keep the script running indefinitely to listen for messages
        published = False
        while True:
            now = datetime.now()
            minute = now.minute
            second = now.second
            f_time = now.strftime("%H:%M:%S")
            # if not second % 5:
            #     print(f_time)
            # if not minute % 5 and not published:
                # print('Publish help')
                #cmd_help(interface=interface)
                # published = True

            if minute % 5:
                published = False

            time.sleep(1)

    except Exception as e:
        print(f"Error connecting or running the bot: {e}")
    finally:
        # Ensure the interface is closed cleanly if an error occurs or the loop breaks
        if 'interface' in locals() and interface:
            interface.close()
            print("Interface closed.")

if __name__ == "__main__":
    main()