import logging
import os
import datetime

#Handler that is needed to make the Debug Section work
class TkinterLogHandler(logging.Handler):
    log_history = []  # Central Class variable to store log history

    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def set_widget(self, text_widget):
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        # Only append to log history if it is not None and the last message is different - Prevent duplicates
        if self.log_history is not None and (not self.log_history or self.log_history[-1] != msg):
            self.log_history.append(msg)
        if self.text_widget is not None:
            def append():
                self.text_widget.config(state="normal")
                self.text_widget.insert("end", msg + "\n")
                self.text_widget.see("end")
                self.text_widget.config(state="disabled")
            self.text_widget.after(0, append)

    #Saves log history to a file - Will be called on close
    @classmethod
    def save_log_history(cls): 
        logging.info("Main.PY: Saving log history")
        logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
        os.makedirs(logs_dir, exist_ok=True)
        log_filename = datetime.datetime.now().strftime("log_%Y%m%d_%H%M%S.txt")
        log_path = os.path.join(logs_dir, log_filename)
        with open(log_path, "w") as f:
            for msg in TkinterLogHandler.log_history:
                f.write(msg + "\n")
        # Only Keep 2 newest log files
        logs = sorted([f for f in os.listdir(logs_dir) if f.startswith("log_") and f.endswith(".txt")])
        while len(logs) > 2:
            os.remove(os.path.join(logs_dir, logs[0]))
            logs.pop(0)