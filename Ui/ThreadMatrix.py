import tkinter as tk

#This will be the class for the toplayer Matrix window which shows the statuses of the threads
class ThreadMatrix(tk.Toplevel):
    def __init__(self, master, controller, rows=10, cols=10, interval=500):
        super().__init__(master)
        self.controller = controller
        self.rows = rows
        self.cols = cols
        self.interval = interval
        self.labels = [] # List for all labels inside the matrix
        self.title("Thread Matrix")
        self.build_matrix()
        self.build_legend()
        self.after(interval, self.update_matrix) # Update matrix every 500ms (standart setting)
    
    #Builds the Matrix
    def build_matrix(self):
        for r in range(self.rows):
            row_labels = [] # Labels in each row
            for c in range(self.cols):
                idx = r * self.cols + c
                lbl = tk.Label(self, text=".", width=4, height=2, relief="ridge", bg="gray")
                lbl.grid(row=r, column=c, padx=1, pady=1)
                row_labels.append(lbl)
            self.labels.append(row_labels)
            
    def build_legend(self):
        legend_frame = tk.Frame(self)
        legend_frame.grid(row=self.rows, column=0, columnspan=self.cols, pady=10)
        legend = [
            (".", "gray", "Wartet"),
            ("~", "yellow", "Läuft"),
            ("✔", "green", "Fertig"),
            ("✖", "red", "Fehler"),
        ]
        for symbol, color, text in legend:
            tk.Label(legend_frame, text=symbol, bg=color, width=2).pack(side="left", padx=5)
            tk.Label(legend_frame, text=text).pack(side="left", padx=10)
            
    def update_matrix(self):
        status_dict = self.controller.thread_status
        symbol_map = {"0": (".", "gray"), "1": ("~", "yellow"), "2": ("✔", "green"), "3": ("✖", "red")}
        for r in range(self.rows):
            for c in range(self.cols):
                idx = r * self.cols + c
                lbl = self.labels[r][c]
                status = status_dict.get(idx, "0")
                symbol, color = symbol_map.get(status, (".", "gray"))
                lbl.config(text=symbol, bg=color)
        # Prüfen, ob alle fertig sind
        if all(status in ("2", "3") for status in status_dict.values()):
            self.title("Alle Threads fertig!")
        else:
            self.after(self.interval, self.update_matrix)