import time
import meshtastic
from meshtastic import serial_interface

# The gateway module is used for network connections, so we import from there
from meshtastic.tcp_interface import TCPInterface
# from tabulate import tabulate
from pprint import pprint
# Replace 'NODE_IP_ADDRESS' with your device's actual IP address
HOST_IP = '192.168.10.185' 

def onMessage(message):
    pprint(message)

def onReceive(packet, interface):
    """
    Callback function to handle received messages.
    """
    print(f"Received: {packet}")

def onConnection(interface, topics):
    """
    Callback function when a connection is established.
    """
    print("Connected to radio over TCP!")
    # Send a text message once connected
    interface.sendText("Hello from Python API over TCP!")

# Create a TCP interface
# The interface will automatically try to find a device at the specified host and default port
try:
    interface = TCPInterface(hostname=HOST_IP)
    # q = interface.getLongName()
    # q = interface.nodes
    # pprint(q)
    # interface.sendText
    r = interface.sendText(text="ping_bot", destinationId=0x6983CD10, wantAck=True, wantResponse=True, onResponse=onMessage) 
    #0x69851514 1770329364, destinationId=0x69851514
    # 0x6983CD10 1770245392
    # r = interface.sendAlert(text="ping", destinationId=0x69851514) #0x69851514 1770329364
    print(r)
    # print(interface.localNode)
    # interface.
    # Keep the script running to listen for messages
    # The 'run' method will block until disconnected
    print("Bot is running and listening for messages. Press Ctrl+C to exit.")
    x = 0
    interface._addResponseHandler(meshPacket.id, onResponse, ackPermitted=onResponseAckPermitted)
    while True:
        time.sleep(1)    
        

except Exception as e:
    print(f"Failed to connect: {e}")
    print("Please check the IP address and ensure the device is connected to WiFi.")

finally:
    # Ensure the interface is closed properly if the script stops
    if 'interface' in locals() and interface:
        interface.close()