import subprocess
import logging
import os
import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from subprocess import run, PIPE

class ToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.add_tooltip()

    def add_tooltip(self):
        self.widget.bind('<Enter>', self.show_tooltip)
        self.widget.bind('<Leave>', self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox('insert')
        x += self.widget.winfo_rootx() + 20
        y += self.widget.winfo_rooty() + 20

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f'+{x}+{y}')

        label = tk.Label(self.tooltip, text=self.text, background='#ffffff', relief='solid', borderwidth=1,
                         wraplength = 180)
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)  # add this line
        self.master = master
        self.pack()
        self.create_widgets()
        self.load_state()
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=10)
        style.configure("TCheckbutton", font=("Helvetica", 12), padding=10)
        style.configure("TLabel", font=("Helvetica", 12), padding=10)
        style.configure("TEntry", font=("Helvetica", 12), padding=10)
        style.configure("TListbox", font=("Helvetica", 12), padding=10)
        style.configure("TProgressbar", thickness=25)
        self.columnconfigure(0, weight=1)
        for i in range(5):
            self.rowconfigure(i, weight=1)
        self.master.bind("<Control-q>", lambda event: self.master.destroy())
        self.master.bind("<Control-b>", lambda event: self.backup_packages())
        self.master.bind("<Control-r>", lambda event: self.restore_packages())

    def populate_listbox(self):
        self.listbox.delete(0, "end")
        packages = self.get_pip_packages()
        for i, package in enumerate(packages):
            self.listbox.insert(i, package)
            if i in self.selected_packages:
                self.listbox.select_set(i)

    def update_packages(self):
        packages = self.listbox.curselection()
        for package in packages:
            self.upgrade_package(self.listbox.get(package))
        self.populate_listbox() # update listbox after updating packages

    def backup_packages(self):
        with open("backup.txt", "w") as f:
            packages = "\n".join([self.listbox.get(package) for package in self.listbox.curselection()])
            f.write(packages)
        messagebox.showinfo("Success", "Packages have been backed up!")

    def restore_packages(self):
        try:
            with open("backup.txt", "r") as f:
                packages = f.read().splitlines()
                for package in packages:
                    self.upgrade_package(package)
            self.populate_listbox() # update listbox after restoring packages
        except FileNotFoundError:
            self.show_error("No backup file found!")



    def create_widgets(self):
        self.config_frame = tk.Frame(self)
        self.config_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)

        self.interpreter_frame = ttk.Frame(self.config_frame)
        self.interpreter_frame.grid(row=0, column=0, sticky="ew")

        self.upgrade_frame = ttk.Frame(self.config_frame)
        self.upgrade_frame.grid(row=1, column=0, sticky="ew")

        self.progress_frame = ttk.Frame(self.config_frame)
        self.progress_frame.grid(row=2, column=0, sticky="ew")

        self.backup_restore_frame = ttk.Frame(self.config_frame)
        self.backup_restore_frame.grid(row=3, column=0, sticky="ew")

        self.quit = ttk.Button(self.config_frame, text="QUIT", style="TButton", command=self.master.destroy)
        self.quit.grid(row=4, column=0, sticky="ew")

        self.interpreter_label = ttk.Label(self.interpreter_frame, text="Python Interpreter:")
        self.interpreter_label.grid(row=0, column=0, sticky="ew")

        self.interpreter_combo = ttk.Combobox(self.interpreter_frame, values=["python", "python3"], state="readonly")
        self.interpreter_combo.grid(row=0, column=1, sticky="ew")

        self.listbox = tk.Listbox(self.upgrade_frame, selectmode=tk.MULTIPLE)
        self.listbox.grid(row=0, column=0, sticky="ew")
        self.update_button = ttk.Button(self.upgrade_frame, text="Update Selected Packages", command=self.update_packages)
        self.update_button.grid(row=1, column=0, sticky="ew")

        self.progress = ttk.Progressbar(self.progress_frame, orient="horizontal", length=200, mode="determinate")
        self.progress.grid(row=0, column=0, sticky="ew")

        self.backup_button = ttk.Button(self.backup_restore_frame, text="Backup Packages", command=self.backup_packages)
        self.backup_button.grid(row=0, column=0, sticky="ew")

        self.restore_button = ttk.Button(self.backup_restore_frame, text="Restore Packages", command=self.restore_packages)
        self.restore_button.grid(row=0, column=1, sticky="ew")


    def get_python_interpreter(self):
        return self.interpreter_entry.get()

    def update_packages(self):
        packages = [self.listbox.get(i) for i in self.listbox.curselection()]
        total = len(packages)
        successful = 0
        for i, package in enumerate(packages):
            if self.upgrade_package(package):
                successful += 1
            self.progress['value'] = ((i + 1) / total) * 100
            self.master.update_idletasks()
        messagebox.showinfo("Update Report", f"{successful} out of {total} packages were successfully updated.")

    def upgrade_package(self, package):
        MAX_RETRIES = 3
        for attempt in range(MAX_RETRIES):
            try:
                command = [self.get_python_interpreter(), "-m", "pip", "install", "--upgrade", package]
                result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode == 0:
                    logging.info(f'Successfully upgraded {package}')
                    return True
                else:
                    logging.error(f'Error occurred while upgrading package {package} (attempt {attempt + 1}): {result.stderr.decode()}')
                    self.show_error(f'Error occurred while upgrading package {package}: {result.stderr.decode()}')
            except Exception as e:
                logging.error(f'Error occurred while upgrading package {package} (attempt {attempt + 1}): {str(e)}')
                self.show_error(f'Error occurred while upgrading package {package}: {str(e)}')
        return False



    def get_pip_packages(self):
        try:
            result = subprocess.run([self.get_python_interpreter(), "-m", "pip", "freeze"], stdout=subprocess.PIPE, text=True)
            result.check_returncode()
            packages = [package_version.split('==')[0] for package_version in result.stdout.splitlines()]
            return [pkg.split("==")[0] for pkg in result.stdout.splitlines() if "==" in pkg]
        except FileNotFoundError:
            messagebox.showerror("Error", "The Python interpreter could not be found. Please make sure it's installed and correctly set up in your system's PATH.")
            return []
        except subprocess.CalledProcessError as e:
            logging.error(f'Error occurred: {str(e)}')
            self.show_error(f'Error occurred: {str(e)}')
            packages = []
        return packages

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def save_state_and_quit(self):
        state = {
            "interpreter": self.interpreter_combo.get(),  # use combobox get method
            "selected_packages": self.listbox.curselection()
        }
        with open("app_state.json", "w") as f:
            json.dump(state, f)
        self.quit()

    def get_python_interpreter(self):
        return self.interpreter_combo.get()

    def load_state(self):
        try:
            with open("app_state.json", "r") as f:
                state = json.load(f)
                self.interpreter_combo.set(state.get("interpreter", "python"))  # use combobox set method
                self.selected_packages = state.get("selected_packages", [])
        except FileNotFoundError:
            self.interpreter_combo.set("python")
            self.selected_packages = []
        self.populate_listbox()

def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
