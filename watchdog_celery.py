import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess


# working watchdog 
EXCLUDED_FOLDERS = ['myenv']  # Add the names of folders you want to exclude

def restart_celery():
    print("Restarting Celery...")
    os.system("taskkill /F /IM celery.exe")
    subprocess.Popen(["cmd", "/start", "/K", "python watchdog_celery.py"])  
    # subprocess.Popen(["cmd", "/start", "/K", "celery -A base worker -l info -P eventlet"])  
class CodeChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"File {event.src_path} has been modified.")
            restart_celery()

if __name__ == "__main__":
    path = "."  # Adjust the path to the directory you want to monitor
    
    event_handler = CodeChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        print("Watchdog is running. Press Ctrl+C to stop.")
        while True:
            time.sleep(3)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
