from daemoniker import Daemonizer
import os, time, dropbox, _thread

access_token = 'your access token'	# dropbox access token, only app access needed
device_name = 'your device'			# name your device for convenience
device_location = 'your location'	# name location of device for convenience

# folder structure used for device/location combination
folder_path = '/' + device_location + '/' + device_name
work_path = os.getcwd() + folder_path

# using a daemonizer for efficient and independent cross platform background
# note that subprocess, ... is not enough to keep the script running after ssh logout.
with Daemonizer() as (is_setup, daemonizer):
	if is_setup:	# before daemonization
		pass

	is_parent = daemonizer(str(time.time()))

	if is_parent:	# after daemonization
		pass

# setup all dropbox folders needed for this device
"""
" Setup local aswell as dropbox cloud folder structure if not already setup
"""
def setup_folder():
	# setup cloud folder
	if folder_not_existent():
		dbx.files_create_folder(folder_path)
	# setup local folder
	if not os.path.exists(work_path):
		os.makedirs(work_path)

# checks whether folder structure existent in cloud
def folder_not_existent():
	try:
		dbx.files_get_metadata(folder_path)
	except:
		return True

"""
" Retrieves the script folder and saves it to local. Folder structure given through folder_path variable.
"""
def get_script_folder():
	for entry in dbx.files_list_folder(folder_path).entries:
		dbx.files_download_to_file(work_path + '/' + entry.name, folder_path + '/' + entry.name)

# executing specific command
def execute_command(cmd):
	os.system(cmd)

# executing list of commands
def execute_script(script):
	for cmd in script:
		execute_command(cmd)
	
"""
" Executing each .txt file in the folder_path as a script.
" Only sequency in a script is guaranteed, multiple scripts will be executed at the same time.
" Thread/Script
"""
def execute_scripts():
	for scriptfile in os.listdir(work_path):
		if scriptfile.endswith('.txt'):
			# read script, to directly delete the scriptfile afterwards
			script = open(work_path + '/' + scriptfile).read().splitlines()
			_thread.start_new_thread(execute_script, (script, ))
			
			# rm scriptfile from both local and cloud
			os.remove(work_path + '/' + scriptfile)
			try:
				dbx.files_delete(folder_path + '/' + scriptfile)
			except:
				# files not existent, that's fine
				pass

				
# DAEMONIZED :
dbx = dropbox.Dropbox(access_token)
setup_folder()

# <THIS IN A LOOP...>
while(True):
	time.sleep(5)
	get_script_folder()
	execute_scripts()
