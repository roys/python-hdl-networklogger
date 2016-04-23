## HDL network logger
**This is a Python script to log network traffic from the smart house system _HDL-BUS Pro_.**

### Running the script
To run the script just type `python networklogger.py`.

By default it will listen for UDP packages on *all available network interfaces on port 6000* and log the traffic to disk.

### Configuring the script
To configure the script you create a new file called `hdlconfig.py`. There's an example config file called `hdlconfig-example.py` you should use as basis for your config.

### Logging
The data from the HDL system is logged into a file (that will be created) called `network.log`. If the script is running continuously the files will be *rotated* at midnight. By default files will be kept for a week. Make sure you have enough disk space for this.

### Complete setup on a Raspberry PI running Raspbian GNU/Linux

#### 1. Directory setup and getting the script

First SSH into your Raspberry PI.

Then download the code:  
`cd ~`  
`git clone https://github.com/roys/python-hdl-networklogger.git`  

It can be smart to check that the script is working and getting data:  
`cd python-hdl-networklogger`  
`python networklogger.py`

Use `ctrl + c` to exit the script. Checkout if any data have been logged to a file called `network.log` in the same directory.

#### 2a. Running the script in the background

If you want to make the script run on startup then skip to **2b**. If you want to just run the script in the background (even afer you log out) you can enter the following
command:  
`nohup python networklogger.py &`

The number that is printed out is the process number. You can use this number to stop the script.

If you don't have the process number you can find it using `ps aux | grep networklogger`.

To kill/stop the script just enter the following command:
`kill [process number]`

#### 2b. Running the script on startup
TBC...

#### 3. Reading the logs

You can easily tap in to what's going by running `tail`:
`tail -f network.log`

This will let you follow the file and the contents that's written to it. To end the session just press `ctrl + c`.

#### Updating the script

If you chose to do a `git clone` in the first step you can just run `git pull` inside the directory at `~/python-hdl-networklogger`. If you run the script at boot
time it is easiest to just reboot your Raspberry PI using `sudo shutdown -r now`.
