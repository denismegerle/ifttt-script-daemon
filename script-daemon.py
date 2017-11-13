from daemoniker import Daemonizer
import os, time, dropbox, _thread

access_token = 'your acces token'
device_name = 'your device'
device_location = 'your location'
folder_path = '/' + device_location + '/' + device_name
work_path = os.getcwd() + folder_path

with Daemonizer() as (is_setup, daemonizer):
	if is_setup:
		# This code is run before daemonization.
		pass

	# We need to explicitly pass resources to the daemon; other variables
	# may not be correct
	is_parent = daemonizer(
		str(time.time())
	)

	if is_parent:
	# Run code in the parent after daemonization
		pass

# setup all dropbox folders needed for this device
def setup_folder():
	# setup cloud folder
	if folder_not_existent():
		dbx.files_create_folder(folder_path)
	# setup local folder
	if not os.path.exists(work_path):
		os.makedirs(work_path)
		
def folder_not_existent():
	try:
		dbx.files_get_metadata(folder_path)
	except:
		return True

# This method retrieves a special folder of dropbox containing all scripts
def get_script_folder():
	for entry in dbx.files_list_folder(folder_path).entries:
		dbx.files_download_to_file(work_path + '/' + entry.name, folder_path + '/' + entry.name)

def execute_command(cmd):
	os.system(cmd)

def execute_script(script):
	for cmd in script:
		execute_command(cmd)
	
def execute_scripts():
	for scriptfile in os.listdir(work_path):
		if scriptfile.endswith('.txt'):
			# read script...
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
