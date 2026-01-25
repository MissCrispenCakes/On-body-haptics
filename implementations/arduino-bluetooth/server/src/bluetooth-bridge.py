#!/usr/bin/env python
"""
Bluetooth Bridge Script

Sends haptic commands to Arduino devices via Bluetooth RFCOMM.

Usage:
    python bluetooth-bridge.py <mac_address> <command>

Example:
    python bluetooth-bridge.py 98:D3:31:F0:5A:26 12345678
"""

import bluetooth
import sys

def send_bluetooth_command(mac_address, command):
    """
    Send command to Bluetooth device

    Args:
        mac_address (str): Bluetooth MAC address (e.g., "98:D3:31:F0:5A:26")
        command (str): Command string to send to Arduino
    """
    port = 1

    try:
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((mac_address, port))
        sock.send(command)
        sock.close()
    except bluetooth.BluetoothError as e:
        print(f"Bluetooth error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python bluetooth-bridge.py <mac_address> <command>", file=sys.stderr)
        sys.exit(1)

    mac_addr = sys.argv[1]
    data = sys.argv[2]

    send_bluetooth_command(mac_addr, data)
