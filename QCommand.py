import sys
import os
import subprocess
from enum import Enum
from threading import Thread

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPlainTextEdit,
)
from PySide6.QtCore import QRunnable, Signal, QObject, QThreadPool, Qt
from PySide6.QtGui import QTextCursor, QColor, QPalette, QTextCharFormat


class ShellType(Enum):
    CMD = "cmd"
    POWERSHELL = "powershell"
    BASH = "bash"


class WorkerSignals(QObject):
    output = Signal(str)
    finished = Signal()


class CommandRunnable(QRunnable):
    def __init__(self, shell, cmd, cwd, signals):
        super().__init__()
        self.shell = shell
        self.cmd = cmd
        self.cwd = cwd
        self.signals = signals
        self.process = None

    def run(self):
        command, encoding = self.prepare_command()

        try:
            self.process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.cwd,
                encoding=encoding,
            )
            self.read_output(self.process.stdout)
            self.read_output(self.process.stderr)
            self.process.wait()
            self.signals.finished.emit()
        except Exception as e:
            self.signals.output.emit(f"Error: {str(e)}")
            self.signals.finished.emit()

    def prepare_command(self):
        cmd = self.convert_command(self.cmd)
        if self.shell == ShellType.CMD:
            return f"cmd.exe /c {cmd}", "cp850"
        elif self.shell == ShellType.POWERSHELL:
            return f'powershell.exe -Command "{cmd}"', "utf-8"
        elif self.shell == ShellType.BASH:
            return f'bash -c "{cmd}"', "utf-8"
        return cmd, "utf-8"

    def convert_command(self, cmd):
        if self.shell == ShellType.CMD:
            if cmd.startswith("ls"):
                cmd = self.convert_ls_to_dir(cmd)
            elif cmd == "python -v":
                cmd = "python --version"
        elif self.shell == ShellType.POWERSHELL:
            if cmd.startswith("ls"):
                cmd = cmd.replace("ls", "Get-ChildItem", 1)
            elif cmd == "python -v":
                cmd = "python --version"
        return cmd

    def convert_ls_to_dir(self, cmd):
        args = cmd.split()
        options = {
            "-l": "/-C",
            "-a": "/A",
            "-h": "",
            "-R": "/S",
        }
        new_cmd = ["dir"] + [options.get(arg, arg) for arg in args[1:]]
        return " ".join(new_cmd)

    def read_output(self, stream):
        def read_stream():
            for line in iter(stream.readline, ""):
                self.signals.output.emit(line.strip())
            stream.close()

        Thread(target=read_stream).start()

    def stop(self):
        if self.process:
            self.process.terminate()
            self.signals.output.emit("Process terminated")


class ConsoleWidget(QPlainTextEdit):
    def __init__(self, shell, cwd, thread_pool):
        super().__init__()
        self.shell = shell
        self.cwd = cwd
        self.thread_pool = thread_pool
        self.signals = WorkerSignals()
        self.signals.output.connect(self.append_output)
        self.signals.finished.connect(self.command_finished)
        self.setStyleSheet("""
            background-color: black;
            color: white;
            font-family: Courier;
            """)

        self.setReadOnly(False)
        self.history = []
        self.history_index = -1
        self.cursor_color = QColor("#00FF00")

        palette = self.palette()
        palette.setColor(QPalette.Text, QColor("white"))
        palette.setColor(QPalette.Base, QColor("black"))
        self.setPalette(palette)
        self.setCursorWidth(2)

        self.append_prompt(initial=True)
        self.current_runnable = None

    def append_prompt(self, initial=False):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        prompt_format = QTextCharFormat()
        prompt_format.setForeground(self.cursor_color)
        if not initial:
            cursor.insertText("\n")
        cursor.insertText(f"{self.cwd}> ", prompt_format)
        self.setTextCursor(cursor)

    def execute_command(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.select(QTextCursor.LineUnderCursor)
        cmd = cursor.selectedText().strip()
        if cmd.startswith(f"{self.cwd}> "):
            cmd = cmd[len(f"{self.cwd}> ") :]
        if cmd:
            self.history.append(cmd)
            self.history_index = len(self.history)
            if cmd.lower() == "cls":
                self.clear_screen()
            elif cmd.lower() == "pwd":
                self.append_output(self.cwd)
                self.command_finished()
            elif cmd.startswith("cd "):
                new_dir = cmd[3:].strip()
                self.change_directory(new_dir)
            else:
                self.setReadOnly(True)
                self.clear_command()
                runnable = CommandRunnable(self.shell, cmd, self.cwd, self.signals)
                self.current_runnable = runnable
                self.thread_pool.start(runnable)

    def change_directory(self, new_dir):
        try:
            os.chdir(new_dir)
            self.cwd = os.getcwd()
            self.append_output(f"Changed directory to {self.cwd}")
        except Exception as e:
            self.append_output(f"Error: {str(e)}")
        finally:
            self.command_finished()

    def clear_screen(self):
        self.clear()
        self.append_prompt(initial=True)

    def append_output(self, output):
        self.appendPlainText(output)
        self.moveCursor(QTextCursor.End)
        self.update_cursor()

    def command_finished(self):
        self.setReadOnly(False)
        self.moveCursor(QTextCursor.End)
        self.ensureCursorVisible()
        self.append_prompt()
        self.update_cursor()

    def clear_command(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.select(QTextCursor.LineUnderCursor)
        cursor.removeSelectedText()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.execute_command()
        elif event.key() == Qt.Key_Up:
            self.show_previous_command()
        elif event.key() == Qt.Key_Down:
            self.show_next_command()
        elif event.key() == Qt.Key_C and event.modifiers() == Qt.ControlModifier:
            self.interrupt_command()
        else:
            super().keyPressEvent(event)
        self.update_cursor()

    def show_previous_command(self):
        if self.history and self.history_index > 0:
            self.history_index -= 1
            self.update_command_with_history()

    def show_next_command(self):
        if self.history and self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.update_command_with_history()
        else:
            self.history_index = len(self.history)
            self.append_prompt()

    def update_command_with_history(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.select(QTextCursor.LineUnderCursor)
        cursor.removeSelectedText()
        self.insert_text_with_prompt(self.history[self.history_index])
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)

    def insert_text_with_prompt(self, text):
        cursor = self.textCursor()
        prompt_format = QTextCharFormat()
        prompt_format.setForeground(self.cursor_color)
        cursor.insertText(f"{self.cwd}> ", prompt_format)
        cursor.insertText(text)
        self.setTextCursor(cursor)

    def update_cursor(self):
        cursor = self.textCursor()
        fmt = QTextCharFormat()
        fmt.setForeground(QColor("white"))
        cursor.setCharFormat(fmt)
        self.setTextCursor(cursor)

    def interrupt_command(self):
        if self.current_runnable and self.current_runnable.process:
            self.current_runnable.stop()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Console")
        self.shell = ShellType.CMD
        self.cwd = os.getcwd()
        self.console = ConsoleWidget(self.shell, self.cwd, QThreadPool.globalInstance())

        layout = QVBoxLayout()
        layout.addWidget(self.console)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.console.clear_screen()
        self.resize(800, 600)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec())
