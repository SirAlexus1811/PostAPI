import logging

#Handler that is needed to make the Debug Section work
class TkinterTextHandler(logging.Handler):
    def __init__(self, text_widget, log_history):
        super().__init__()
        self.text_widget = text_widget
        self.log_history = log_history  # Used for saving log history

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