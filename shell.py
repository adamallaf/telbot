import time
from subprocess import Popen, PIPE
from threading import Thread
from typing import List


class Shell:
    def __init__(self):
        self.__shell_process = Popen(["sh"], stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=0)
        self.__cmd_history = []
        self.__history_size = 100
        self.__stdout = []
        self.__stdout_thread = Thread(target=self.__shellStdout, daemon=True)
        self.__stdout_thread.start()

    @property
    def history(self) -> List[str]:
        return self.__cmd_history

    def execute(self, cmd: str) -> str:
        self.__addHistory(cmd)
        self.__shell_process.stdin.write(cmd.encode('utf-8') + b'\n')
        output = "[done]"
        st = time.time()
        while time.time() - st < 1:
            pass
        if self.__stdout:
            output = ""
            while self.__stdout:
                output += self.__stdout.pop(0)
        return output

    def __addHistory(self, cmd: str):
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
        self.__shell_process.stdout.close()
        self.__stdout_thread.join()
        self.__shell_process.terminate()
        self.__shell_process = None
