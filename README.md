Windows Client: Reads joystick input using Pygame and sends it over the network.
Raspberry Pi Server: Listens for network data, interprets it, and controls motors/servos connected via a PCA9685 servo driver board.
Part 1: Setting up the Windows Client Machine

Install Python:

Go to the official Python website: https://www.python.org/downloads/
Download the latest stable version for Windows.
Run the installer. Crucially, check the box that says "Add Python X.Y to PATH" during installation. This makes it easier to run Python from the command line.
Follow the installer prompts.
Install a Text Editor (VS Code Recommended):

You need a program to write and edit the Python code. Visual Studio Code (VS Code) is a great free option.
Download VS Code: https://code.visualstudio.com/
Run the installer and follow the prompts.
Open VS Code. It might prompt you to install the Python extension; if so, do it. Otherwise, go to the Extensions view (icon looks like squares on the left sidebar), search for "Python", and install the one by Microsoft.
Get the Client Code:

Open VS Code.
Go to File > New Text File.
Copy the second block of code (the one starting with import socket and import pygame) from your request.
Paste it into the new file in VS Code.
Go to File > Save As.... Choose a location (e.g., create a folder like C:\Projects\JoystickClient) and save the file as client.py.
Install Pygame Module:

Open the Windows Command Prompt or PowerShell. You can search for cmd or powershell in the Windows Start menu.
Type the following command and press Enter:
Bash

pip install pygame
This will download and install the Pygame library, which is needed to interact with the joystick.
Connect Your Joystick:

Plug your joystick into a USB port on your Windows computer. Windows should automatically detect it. You can check in Control Panel > Hardware and Sound > Devices and Printers (or similar path depending on your Windows version) to see if it's listed.
Configure Network Address (Placeholder):

In the client.py file (open in VS Code), find this line:
Python

s.connect(("192.168.88.250", 5000)) # Change the IP address to the server's IP address
You will need to replace "192.168.88.250" with the actual IP address of your Raspberry Pi after you set up the Pi and find its address (we'll do that in the next part). Leave it as is for now, but remember to come back here.
Part 2: Setting up the Raspberry Pi Server

(Assuming you have Raspberry Pi OS installed and the Pi is connected to your network, keyboard, mouse, and monitor, or you can SSH into it).

Update Raspberry Pi OS:

Open the Terminal on your Raspberry Pi (the black icon in the top bar or find it in the Accessories menu).
Run the following commands, pressing Enter after each one:
Bash

sudo apt update
sudo apt full-upgrade -y
This ensures your system packages are up-to-date. It might take some time.
Enable I2C Interface:

The PCA9685 board communicates using the I2C protocol. You need to enable this on the Pi.
In the Terminal, run:
Bash

sudo raspi-config
Use the arrow keys to navigate to Interface Options. Press Enter.
Navigate to I2C. Press Enter.
Select <Yes> to enable the I2C interface. Press Enter.
Select <Ok>.
Navigate to Finish and press Enter. It might ask to reboot; select <Yes>.
Install I2C Tools (Optional but helpful):

After rebooting, open the Terminal again.
Install tools to help detect I2C devices:
Bash

sudo apt install -y i2c-tools
Connect Hardware (PCA9685 and Motors/Servos):

Power down the Raspberry Pi (sudo shutdown now).
Connect the Adafruit PCA9685 board to the Raspberry Pi's GPIO pins using the I2C pins:
Pi 3.3V to PCA9685 VCC
Pi SDA (GPIO 2) to PCA9685 SDA
Pi SCL (GPIO 3) to PCA9685 SCL
Pi GND to PCA9685 GND
Connect the separate power supply for your motors/servos to the PCA9685 board's power terminal block (V+ and GND). Do NOT try to power motors/servos directly from the Raspberry Pi's 5V pin.
Connect your motors (via ESCs if needed) and servos to the PWM output pins (0-15) on the PCA9685 board, matching the pin numbers defined in your server script (motor_1 = 4, claw_open = 15, etc.).
Power up the Raspberry Pi.
Verify I2C Connection (Optional):

Open the Terminal.
Run the command:
Bash

sudo i2cdetect -y 1
You should see a grid. If the PCA9685 is connected correctly, you'll likely see a number like 40 (the default address) appear in the grid. If you see nothing or get an error, double-check your wiring.
Install a Text Editor:

Raspberry Pi OS usually comes with Thonny IDE, which is great for beginners. You can find it in the Programming menu.
Alternatively, you can use the simple command-line editor nano.
Get the Server Code:

Open Thonny IDE (or use nano in the terminal: nano server.py).
Copy the first block of code (the one starting with # Activate Python environment and import socket) from your request.
Paste it into the editor.
Save the file in a location you can easily find (e.g., your home directory /home/pi/) as server.py.
Set Up a Python Virtual Environment (Recommended):

Using a virtual environment keeps dependencies for this project separate from system-wide Python packages.
Open the Terminal.
Navigate to the directory where you saved server.py (if you saved it in the home directory, you are likely already there. If not, use cd path/to/your/script).
Create the virtual environment:
Bash

python3 -m venv my_env
(This creates a folder named my_env).
Activate the virtual environment:
Bash

source my_env/bin/activate
You should see (my_env) appear at the beginning of your terminal prompt. You need to activate this environment every time you open a new terminal to work on this project.
Install Python Dependencies:

Make sure your virtual environment is active (you see (my_env) in the prompt).
Install the necessary Adafruit libraries:
Bash

pip install adafruit-circuitpython-pca9685 adafruit-circuitpython-servokit
(Note: adafruit-blinka, the library that provides CircuitPython compatibility (like board) on Raspberry Pi, is usually installed as a dependency of the above libraries. If you encounter errors related to board, you might need to install it explicitly: pip install adafruit-blinka)
Find the Raspberry Pi's IP Address:

In the Terminal, run:
Bash

hostname -I
This command will output the IP address(es) of your Raspberry Pi on the local network (e.g., 192.168.1.15 or similar). Write this IP address down. It might list multiple addresses; you usually want the one associated with your main network connection (WLAN or Ethernet).
Update the Client Script with the Pi's IP Address:

Go back to your Windows machine.
Open client.py in VS Code.
Find the line: s.connect(("192.168.88.250", 5000))
Replace "192.168.88.250" with the actual IP address of your Raspberry Pi that you just found.
Save the client.py file.
Install and Configure VNC Server (Remote Desktop):

This allows you to see and control the Raspberry Pi's graphical desktop from your Windows machine.
In the Pi's Terminal, install the VNC server:
Bash

sudo apt update
sudo apt install -y realvnc-vnc-server realvnc-vnc-viewer
Enable the VNC Server:
Bash

sudo raspi-config
Navigate to Interface Options. Press Enter.
Navigate to VNC. Press Enter.
Select <Yes> to enable the VNC Server. Press Enter.
Select <Ok>.
Navigate to Finish and press Enter. Reboot if prompted.
On your Windows machine: Download and install a VNC client like RealVNC Viewer: https://www.realvnc.com/en/connect/download/viewer/
Open RealVNC Viewer on Windows. Enter the Raspberry Pi's IP address in the connection bar and press Enter.
You'll likely be prompted for the Raspberry Pi's username (usually pi) and password.
You should now see the Raspberry Pi's desktop in a window on your Windows PC.
Part 3: Running the Code

Start the Server on the Raspberry Pi:

Open a Terminal on the Raspberry Pi (either directly or via VNC/SSH).
Navigate to the directory where you saved server.py (e.g., cd /home/pi/).
Activate the virtual environment:
Bash

source my_env/bin/activate
Run the server script:
Bash

python server.py
You should see the output Server is now running. The script is now waiting for a connection from the client.
Start the Client on the Windows Machine:

Make sure your joystick is plugged in.
Open Command Prompt or PowerShell on Windows.
Navigate to the directory where you saved client.py (e.g., cd C:\Projects\JoystickClient).
Run the client script:
Bash

python client.py
If the connection is successful, you should see Pygame initializing and potentially printing the detected joystick name.
As you move the joystick axes and press buttons, you should see the input list being printed in the Windows terminal, and this data will be sent to the Raspberry Pi.
On the Raspberry Pi's terminal, you should see the received inputs list being printed each time the client sends data. The motors/servos connected to the PCA9685 should react based on the joystick movements.
Troubleshooting Tips:

Connection Refused (Client):
Double-check the IP address in client.py matches the Pi's current IP address.
Ensure the server.py script is running on the Pi before you start client.py.
Check firewalls: Your Windows firewall might be blocking the outgoing connection, or (less likely) the Pi's firewall might block incoming connections on port 5000.
Server Not Starting (Pi):
ModuleNotFoundError: You forgot to install a required library (pip install ...) or you forgot to activate the virtual environment (source my_env/bin/activate) before running the script.
IOError or I2C errors: Double-check the I2C wiring between the Pi and PCA9685. Make sure I2C is enabled via raspi-config. Run sudo i2cdetect -y 1 to see if the board is detected.
Permission errors: Sometimes hardware access requires root privileges. Try running the server script with sudo python server.py, but be cautious when running scripts as root. Using Blinka usually avoids this.
Client Not Detecting Joystick:
Ensure the joystick is properly plugged in before running the script.
Verify Windows sees the joystick in the Control Panel.
Make sure pygame is installed correctly (pip install pygame).
Motors/Servos Not Moving:
Check the separate power supply for the PCA9685 board and motors/servos.
Verify the motor/servo connections to the correct pins on the PCA9685.
Check the PWM frequency setting (pca.frequency = 50) is appropriate for your servos/ESCs.
Ensure the server script is receiving data (check the print statements on the Pi's terminal).
You should now have a working system where your Windows joystick controls hardware connected to your Raspberry Pi!
