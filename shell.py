import platform
import time
from logging import getLogger
from subprocess import Popen, PIPE
from threading import Thread
from typing import List


class Shell:
    def __init__(self):
        __shell_path = "sh"
        sys_type = platform.system()
        if sys_type == "windows":
            __shell_path = "C:\\Program Files\\Git\\bin\\sh.exe"
        self.__shell_process = Popen([__shell_path], stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=0)
        self.__cmd_history = []
        self.__history_size = 100
        self.__stdout = []
        self.__stdout_thread = Thread(target=self.__shellStdout, daemon=True)
        self.__stdout_thread.start()
        self.__logger = getLogger(self.__class__.__name__ + "_{}".format(self.__shell_process.pid))

    @property
    def history(self) -> List[str]:
        return self.__cmd_history

    def execute(self, cmd: str) -> str:
        self.__logger.debug("running execute: {}".format(cmd))
        self.__addHistory(cmd)
        self.__shell_process.stdin.write(cmd.encode('utf-8') + b' 2>&1\n')
        output = "[done]"
        time.sleep(1)
        if self.__stdout:
            output = ""
            while self.__stdout:
                output += self.__stdout.pop(0)
        self.__logger.debug("got output:\n{}".format(output))
        return output

    def __addHistory(self, cmd: str):
        self.__logger.debug("adding command \"{}\" to history".format(cmd))
        self.__cmd_history.append(cmd)
        if len(self.__cmd_history) > self.__history_size:
            self.__cmd_history.pop(0)

    def __shellStdout(self):
        while not self.__shell_process.stdout.closed:
            output = self.__shell_process.stdout.read(1 << 15).decode('utf-8', 'ignore')
            self.__stdout.append(output)

    def __del__(self):
        if self.__shell_process:
            self.close()

    def close(self):
        self.__logger.debug("closing shell")
        self.__shell_process.stdout.close()
        self.__stdout_thread.join()
        self.__shell_process.terminate()
        self.__shell_process = None
