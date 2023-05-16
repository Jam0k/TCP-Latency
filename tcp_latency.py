#!/usr/bin/python
import socket
from statistics import mean
from time import sleep, monotonic
from tkinter import *
from tkinter import scrolledtext
from typing import Optional
import threading

def measure_latency(
        host: str,
        port: int = 443,
        timeout: float = 5,
        runs: int = 1,
        wait: float = 1,
) -> list:
    '''
    :rtype: list
    Builds a list composed of latency_points
    '''
    latency_points = []

    for i in range(runs):
        sleep(wait)
        last_latency_point = latency_point(
            host=host, port=port, timeout=timeout,
        )
        if last_latency_point is not None:
            latency_points.append(last_latency_point)

    return latency_points


def latency_point(host: str, port: int = 443, timeout: float = 5) -> Optional[float]:
    '''
    :rtype: Returns float if possible
    Calculate a latency point using sockets. If something bad happens the point returned is None
    '''

    # Start a timer
    s_start = monotonic()

    # Try to Connect
    try:
        s = socket.create_connection((host,port), timeout = timeout)
        s.shutdown(socket.SHUT_RD)

    # If something bad happens, the latency_point is None
    except socket.timeout:
        return None
    except OSError:
        return None

    # Stop Timer
    s_runtime = (monotonic() - s_start) * 1000

    return float(s_runtime)


def start():
    host = host_entry.get()
    port = int(port_entry.get())
    timeout = float(timeout_entry.get())
    runs = int(runs_entry.get())
    wait = float(wait_entry.get())
    log.insert(END, 'tcp-latency {}\n'.format(host))
    for i in range(runs):
        latency = latency_point(host, port, timeout)
        if latency is not None:
            log.insert(END, f'{host}: tcp seq={i} port={port} timeout={timeout} time={latency} ms\n')
        else:
            log.insert(END, f'{host}: tcp seq={i} port={port} timeout={timeout} failed\n')


def clear_log():
    log.delete('1.0', END)


def start_thread():
    threading.Thread(target=start, daemon=True).start()


root = Tk()

host_label = Label(root, text="Host:")
host_label.pack()
host_entry = Entry(root)
host_entry.pack()

port_label = Label(root, text="Port:")
port_label.pack()
port_entry = Entry(root)
port_entry.pack()

timeout_label = Label(root, text="Timeout:")
timeout_label.pack()
timeout_entry = Entry(root)
timeout_entry.pack()

runs_label = Label(root, text="Runs:")
runs_label.pack()
runs_entry = Entry(root)
runs_entry.pack()

wait_label = Label(root, text="Wait:")
wait_label.pack()
wait_entry = Entry(root)
wait_entry.pack()

start_button = Button(root, text="Start", command=start_thread)
start_button.pack()

clear_button = Button(root, text="Clear Log", command=clear_log)
clear_button.pack()

log = scrolledtext.ScrolledText(root)
log.pack()

root.mainloop()
