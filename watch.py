#!/usr/bin/env python3

import os
import sys
import signal
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

WATCH_PATH = os.environ["WATCH_PATH"]

def on_created(event):
    print(f"[NEW FILE] {event.src_path}")

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
