#!/usr/bin/env python3
"""
IP Display Utility

Displays network information (IP and MAC address) on SSD1306 OLED display.
Shows info when button is pressed, clears after 10 seconds.

Usage:
    python ip-display.py

Can also be run as a systemd service for persistent display functionality.

Press Ctrl+C to stop.
"""

import board
import digitalio
import busio
import netifaces
import time
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


def get_network_info():
    """
    Get wireless network IP and MAC address.

    Returns:
        tuple: (ip_address, mac_address)
    """
    wl_ip = "Not connected"
    wl_mac = ""

    for ifacename in netifaces.interfaces():
        # Check wireless interfaces
        if not (ifacename.startswith('wl') or ifacename.startswith('wlan')):
            continue

        addrs = netifaces.ifaddresses(ifacename)

        if netifaces.AF_INET in addrs and netifaces.AF_LINK in addrs:
            ips = [addr['addr'] for addr in addrs[netifaces.AF_INET]]

            for ip in ips:
                if not ip.startswith('127.'):
                    wl_ip = ip
                    wl_mac = addrs[netifaces.AF_LINK][0]['addr']
                    break

    return wl_ip, wl_mac


def display_info(display, ip, mac):
    """
    Display network information on OLED.

    Args:
        display: SSD1306 display object
        ip: IP address string
        mac: MAC address string
    """
    # Create image
    image = Image.new("1", (display.width, display.height))
    draw = ImageDraw.Draw(image)

    # Load fonts
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
        font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
    except:
        # Fallback to default font if truetype not available
        font = ImageFont.load_default()
        font2 = font

    # Draw text
    draw.text((0, 0), "OctoPulse", font=font, fill=255)
    draw.text((0, 11), f"IP: {ip}", font=font, fill=255)
    draw.text((0, 22), f"MAC: {mac}", font=font2, fill=255)

    # Show on display
    display.image(image)
    display.show()


def main():
    """Main display loop."""
    # Initialize I2C and display
    i2c = busio.I2C(board.SCL, board.SDA)
    display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

    # Initialize button on GPIO26 (D26)
    button = digitalio.DigitalInOut(board.D26)
    button.direction = digitalio.Direction.INPUT

    print("IP Display Service")
    print("Press button to show network info")
    print("Press Ctrl+C to exit\n")

    try:
        while True:
            if not button.value:  # Button pressed (active low)
                # Get network info
                ip, mac = get_network_info()
                print(f"Displaying - IP: {ip}, MAC: {mac}")

                # Display info
                display_info(display, ip, mac)

                # Wait 10 seconds
                time.sleep(10)

                # Clear display
                display.fill(0)
                display.show()
                print("Display cleared")

            time.sleep(0.1)  # Poll button at 10Hz

    except KeyboardInterrupt:
        print("\nExiting...")
        display.fill(0)
        display.show()


if __name__ == "__main__":
    main()
