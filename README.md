# UniversalClock
Customizable Universal Clock using a Pico and RGB Matrix.

![alt text](https://raw.githubusercontent.com/waffl3ss/UniversalClock/main/Example.jpg)

# Parts List
Required:
- Raspberry Pi Pico WH
- Waveshare 64x32px RGB Matrix (https://www.amazon.com/gp/product/B0BRBGHFKQ/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&th=1)
- 5V 4A Power Adapter (https://www.amazon.com/gp/product/B087LY41PV/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&th=1)

Optional:
- Shrink Tube
- Cable Management Sleeve (or a really long heat shrink, but just something to cover cords all the way is the idea)
- 3d printed housing (STL uploaded in repo. modeled with the long legs on the matrix)
- Tint film (I applied a layer to the front since the LEDs are so bright)

# Guide
- Flash the pico with CircuitPython 9.x
- Modify secrets.py with your SSID information
- Upload code.py, secrets.py, and the whole lib folder to the root directory of the device
- Follow the guide for wiring at https://www.waveshare.com/wiki/RGB-Matrix-P2.5-64x32#Working_With_Raspberry_Pi_Pico
- Plug in and happy day

# Notes
By default it displays UTC, CET, and IST. You can modify the script to display timezones of your choice. The lines displaying the text and the amount to add to hours/mins are what you need. 
Its not written in the best way, but it works, and that took me long enough to figure out with CircuitPython being meant for Arduino and not the Pico.
