# IFTTT Script Daemon

## What is it?
This script runs in the background on Windows / Linux systems, checking a Dropbox folder for scripts to be executed. Conveniently, scripts can be simply added through the IFTTT service, so with this daemon any IF trigger can execute any script on both Windows and Linux.
---
## How to use?
1. Create a Dropbox App through the [Dropbox development page](https://www.dropbox.com/developers/apps/create). Choose app folder and any "app name". Get the access token by generating it on the following page.
2. Add it to the script, also add any name for your device and any name for the location it is used in. (e.g. MainComputer, Home)
3. Install dependencies (`pip install dropbox daemoniker`).
4. Add the script to your systems autostart and reboot. (Windows: link it with the task scheduler, Linux: e.g. add `python3 <location_to_script>/script-daemon.py` to /etc/rc.local)
5. Now you can create an IFTTT applet, choose your IF, then as action use Dropbox and create textfile. Use your commands as content of the file, and choose the correct folder to safe it (if you used <app name>, the folder will be *Apps/"app name"/"location"/"device"*)
  
Commands will then be executed as soon a trigger is used. As with any script, this method is potentially dangerous and harmful for your system as any script that is in the folder structure will be executed (potentially with root permissions, if the rc.local method is used).
