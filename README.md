 ![ZS_logo_FINAL_small](https://github.com/user-attachments/assets/94b187b0-c548-46c7-892a-a9aa7afc60f2)
# ZSConnect Software              
Graphical user interface to connect to ZS data loggers.
# 1 - Installation 
## Option 1 - Compiled version
Dowload the folder named ZS_connect and all its contents to your computer. Then you can run the program by excecuting the file "ZS_connect.exe".
* This option is the easiest, but some security systems do not allow this method to run.

## Option 2 - Manual version
Download the files named "ZS_connect.py", "List_COM_Ports.py", and "locus.py" and run the ZS_connect script in Python, this will require installation of all the neccesary packages.

# 2 - Usage
## 2.1 Home screen
When you open the software you should see the following screen
![ZS_connect_HOME](https://github.com/user-attachments/assets/3afa39d5-41b6-4ed5-b384-88acf9231585)

## 2.2. Connect device
* Once the software is open, connect your device's PROGRAMMING CABLE to your computer (this cable will be marked with a "P" or be unmarked)
* Press the "Refresh" button and select the COM port number from the drop-down list
* Then press the "Connect COM" button
 ![ZS_connect_CONNECT](https://github.com/user-attachments/assets/4ae37c23-410b-4426-8264-58344b605d26)
* Then you should see the following screen
  
 ![ZS_connect_CONNECTED](https://github.com/user-attachments/assets/f9fafd1d-05ef-470b-97c7-454b2e58ea5b)

## 2.3 Configure device
* Click on the "Configure" button and you should see the following screen:
  ![ZS_connect_CONFIG](https://github.com/user-attachments/assets/8a1b4883-02c1-40c0-a8c8-4cf9335a384a)
* Initial delay - this is the amount of time the logger will go to sleep before filming starts. This is in seconds - the default is 72000 seconds which is 20 hours
* Filming duration - the total amount of time you want to film per FILM BOUT (next panel). 
* Film bouts - the number of times you want the FILM DURATION (above) to be repeated. This is important as the cameras may overwrite old files when the SD card is full. Thus, it might be needed to limit the total amount of time filming.
* Film delay - time that should pass between film bouts. This is only used if you don't want to film conitnuosly, otherwise set to 0.
* Water threshold - sensitivity of salt-water detection. Higher values are less sensitive, but this risks triggering with fresh water. This value will depend on the salinity of your operating waters, but 300 is a good default. When the saltwater switch is triggered the initial delay is bypassed and filming starts.
* Light threshold - The cameras have a light sensor to stop filming when it is too dark. A higher threshold will allow filming in darker conditions - set to 1024 to film in all conditions.
*Initial film duration - The cameras will film a video clip on startup - this is used for temporal synchronisation during data processing. During the initial video clip the user can point to camera to a watch to validate the timestamp and determine any temporal offsets.
*Water delay - some models have a second delay, where a second delay is activated with the saltwater switch. i.e. when the logger enters the water, wait for a certain amount of time before filming starts. If this field is empty set to 0.
* #### NB! none of these fields may be empty when clicking "Apply"
* Click "Apply" to save the changes.

## 2.4 Disconnect
* Once done, click the "Disconnect" button.
* Disconnect the USB cable.


