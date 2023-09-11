#!/usr/bin/env python3

import os
import requests
import sys
import signal

from requests.auth import HTTPBasicAuth
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

WATCH_PATH = os.environ["WATCH_PATH"]

NTFY_USER  = os.environ["NTFY_USER"]
NTFY_PASS  = os.environ["NTFY_PASS"]
NTFY_URL   = os.environ["NTFY_URL"]

def on_created(event):
    print(f"[NEW FILE] {event.src_path}")
    with open(event.src_path, "rb") as f:
        requests.put(NTFY_URL,
                     auth=HTTPBasicAuth(NTFY_USER, NTFY_PASS),
                     data=f,
                     headers={"Filename": os.path.basename(event.src_path)})

def handler(signum, frame):
    signame = signal.Signals(signum).name
    print(f"[SIGNAL] {signame} ({signum})")

def main(argc: int, argv: list[str]) -> None:
    event_handler = PatternMatchingEventHandler(patterns=["*"],
                                                ignore_patterns=None,
                                                ignore_directories=False,
                                                case_sensitive=True)
    event_handler.on_created = on_created

    observer = Observer()
    observer.schedule(event_handler=event_handler,
                      path=WATCH_PATH,
                      recursive=False)
    observer.start()

    print("Observer started.")

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)
    signal.pause()

    print("Stopping Observer...")

    observer.stop()
    observer.join()

    print("Observer stopped.")

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
