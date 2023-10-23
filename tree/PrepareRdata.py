#!/usr/bin/python3

import os
import subprocess
import shutil

# Define the directory path
data_dir = '/var/www/html/data/'

# Create the directory if it doesn't exist
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Remove any files in the directory
for filename in os.listdir(data_dir):
    file_path = os.path.join(data_dir, filename)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(f"Error deleting {file_path}: {e}")

# Execute the R script
try:
    subprocess.run(['Rscript', 'ConvertAndCompress.R'])
except Exception as e:
    print(f"Error executing R script: {e}")
    exit(1)

# Move the lmdata.Rdata file to the new location
source_file = 'lmdata.Rdata'
dest_file = os.path.join(data_dir, 'lmdata.Rdata')

try:
    shutil.move(source_file, dest_file)
    print(f"File {source_file} moved to {dest_file}")
except Exception as e:
    print(f"Error moving {source_file} to {dest_file}: {e}")
    exit(1)

