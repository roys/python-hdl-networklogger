## HDL network logger
This is a Python script to log network traffic from the smart house system HDL-BUS Pro.

### Running the script
To run the script just type `python networklogger.py`.

By default it will listen for UDP packages on *all available network interfaces on port 6000*.

### Configuring the script
To configure the script you create a new file called `hdlconfig.py`. There's an example config file called `hdlconfig-example.py` you should use as basis for your config.

### Complete setup on a Raspberry PI running Raspbian GNU/Linux

#### 1. Directory setup and getting the script

First SSH into your Raspberry PI.

Then download the code:  
`cd ~`  
`git clone https://github.com/roys/python-hdl-networklogger.git`  

It can be smart to check that the script is working and getting data:  
`cd python-hdl-networklogger`  
`python networklogger.py`  
Use ctrl + c to exit the script.

#### 2a. Running the script in the background

If you want to make the script run on startup then skip to **2b**. If you want to just run the script in the background you can enter the following command:  
`nohup python networklogger.py &`

The number that is printed out is the process number. You can use this number to stop the script.

If you don't have the process number you can find it using `ps aux | grep networklogger`.

To kill/stop the script just enter the following command:
`kill [process number]`

#### 2b. Running the script on startup
TBC...

#### Updating the script

If you chose to do a `git clone` in the first step you can just run `git pull` inside the directory at `~/python-hdl-networklogger`. If you run the script at boot
time it is easiest to just reboot your Raspberry PI using `sudo shutdown -r now`.
