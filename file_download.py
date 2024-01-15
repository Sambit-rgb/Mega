# In this program we are using mega library and downloading each file
from mega import Mega
import os

mega = Mega()

# Login to your MEGA account
m = mega.login('email@email.com', 'password')

# Specify the folder
folder_name = 'linux-platform'

# Get the folder object using the folder's URL or ID
folder = m.find(folder_name)

if folder is not None:
    # Get all files in the folder
    files = m.get_files_in_node(folder[0])

    # Download each file
    for file in files:
        public_link = m.get_link(file)
        m.download_url(public_link)
