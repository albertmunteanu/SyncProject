

import os
import shutil
import time
import argparse

def sync_folders(source_path, replica_path, log_path, sync_interval):
    # Create the log file if it does not exist
    if not os.path.exists(log_path):
        with open(log_path, 'w'):
            pass

    # Synchronize the folders initially
    sync(source_path, replica_path, log_path)

    # Continuously synchronize the folders
    while True:
        time.sleep(sync_interval)
        sync(source_path, replica_path, log_path)

def sync(source_path, replica_path, log_path):
    # Log the start of synchronization
    log(f'Synchronizing {source_path} to {replica_path}', log_path)

    # Remove files from replica folder that don't exist in source folder
    for replica_file in os.listdir(replica_path):
        replica_file_path = os.path.join(replica_path, replica_file)
        source_file_path = os.path.join(source_path, replica_file)
        if not os.path.exists(source_file_path):
            os.remove(replica_file_path)
            log(f'Removed {replica_file_path}', log_path)

    # Copy files from source folder to replica folder
    for source_file in os.listdir(source_path):
        source_file_path = os.path.join(source_path, source_file)
        replica_file_path = os.path.join(replica_path, source_file)
        if os.path.isfile(source_file_path):
            if not os.path.exists(replica_file_path) or os.stat(source_file_path).st_mtime - os.stat(replica_file_path).st_mtime > 1:
                shutil.copy2(source_file_path, replica_file_path)
                log(f'Copied {source_file_path} to {replica_file_path}', log_path)

    # Log the end of synchronization
    log('Synchronization complete', log_path)

def log(message, log_path):
    # Log the message to the console output
    print(message)

    # Log the message to the log file
    with open(log_path, 'a') as log_file:
        log_file.write(f'{message}\n')

if __name__ == '__main__':
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='Synchronize two folders')
    parser.add_argument('source_path', type=str, help='path to the source folder')
    parser.add_argument('replica_path', type=str, help='path to the replica folder')
    parser.add_argument('log_path', type=str, help='path to the log file')
    parser.add_argument('sync_interval', type=int, help='interval between synchronizations in seconds')
    args = parser.parse_args()

    # Synchronize the folders
    sync_folders(args.source_path, args.replica_path, args.log_path, args.sync_interval)






