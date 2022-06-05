# grab log
import os
import time
import signal
import shlex
import subprocess
from threading import Timer


# strin = os.system("adb logcat -v time")
# print(str)
# strin = os.popen(strin)
# Parsing log
# todo

# Stop grabbing logs
# strin = os.system("ps aux | grep \"adb logcat\" | awk '{print $1}' | xargs kill -9")
def kill_proc(proc, timeout):
    timeout["value"] = True
    proc.kill()


def run(cmd, timeout_sec):
    proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    timeout = {"value": False}
    timer = Timer(timeout_sec, kill_proc, [proc, timeout])
    timer.start()
    stdout, stderr = proc.communicate()
    timer.cancel()
    return proc.returncode, stdout.decode("utf-8"), stderr.decode("utf-8"), timeout["value"]


def get_data(cmd="adb logcat -v time", timeout_time=2):
    run(cmd, timeout_time)

