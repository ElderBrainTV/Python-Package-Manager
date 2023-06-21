import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext, simpledialog, ttk
import threading
import subprocess
import os
import sys
import logging
import shutil

logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Interpreter Entry
        self.interpreter_label = tk.Label(self, text="Python Interpreter:")
        self.interpreter_label.pack(side="top")
        self.interpreter_entry = tk.Entry(self)
        self.interpreter_entry.pack(side="top")
        self.interpreter_entry.insert(0, "python")

        # Interactive Mode Checkbox
        self.interactive_var = tk.BooleanVar()
        self.interactive_checkbutton = tk.Checkbutton(self, text="Interactive Mode", variable=self.interactive_var)
        self.interactive_checkbutton.pack(side="top")

        # Selective Upgrade Listbox
        self.listbox_label = tk.Label(self, text="Packages (Select to Upgrade):")
        self.listbox_label.pack(side="top")
        self.listbox = tk.Listbox(self, selectmode="multiple", exportselection=False)
        self.listbox.pack(side="top")

        self.update_button = tk.Button(self)
        self.update_button["text"] = "Update Selected Packages"
        self.update_button["command"] = self.update_packages
        self.update_button.pack(side="top")

        # Progress Bar
        self.progress = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        self.progress.pack(side="top")

        # Backup and Restore Buttons
        self.backup_button = tk.Button(self, text="Backup Packages", command=self.backup_packages)
        self.backup_button.pack(side="top")

        self.restore_button = tk.Button(self, text="Restore Packages", command=self.restore_packages)
        self.restore_button.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

        # Populate the listbox with installed pip packages
        self.populate_listbox()

    def populate_listbox(self):
        packages = self.get_pip_packages()
        for package in packages:
            self.listbox.insert(tk.END, package)

    def update_packages(self):
        if self.check_disk_space():
            threading.Thread(target=self.perform_update).start()
        else:
            messagebox.showwarning("Warning", "Not enough disk space.")
            logger.warning('Not enough disk space')

    def perform_update(self):
        selected_indices = self.listbox.curselection()
        selected_packages = [self.listbox.get(i) for i in selected_indices]

        if selected_packages:
            self.progress["maximum"] = len(selected_packages)
            self.progress["value"] = 0

            success_count = 0
            failure_count = 0
            for package in selected_packages:
                if self.interactive_var.get():
                    answer = messagebox.askyesno("Confirmation", f"Do you want to upgrade {package}?")
                    if answer and self.upgrade_package(package):
                        success_count += 1
                    else:
                        failure_count += 1
                else:
                    if self.upgrade_package(package):
                        success_count += 1
                    else:
                        failure_count += 1

                self.progress["value"] += 1
                self.update_idletasks()

            messagebox.showinfo("Info", "Upgrade process completed.")
            logger.info('Upgrade process completed')
            self.show_report(len(selected_packages), success_count, failure_count)
        else:
            messagebox.showinfo("Info", "No package selected to upgrade.")
            logger.info('No package selected to upgrade.')

    def show_report(self, total, success, failure):
        report_window = tk.Toplevel(self)
        report_window.title("Upgrade Report")
        report_label = tk.Label(report_window, text=f"Total packages: {total}\nSuccessful upgrades: {success}\nFailed upgrades: {failure}")
        report_label.pack()

    def get_python_interpreter(self):
        return self.interpreter_entry.get()

    def get_pip_packages(self):
        try:
            result = subprocess.run([self.get_python_interpreter(), "-m", "pip", "freeze"], stdout=subprocess.PIPE, text=True)
            result.check_returncode()
            packages = [package_version.split('==')[0] for package_version in result.stdout.splitlines()]
        except subprocess.CalledProcessError as e:
            logging.error(f'Error occurred: {str(e)}')
            packages = []
        return packages

    def upgrade_package(self, package):
        MAX_RETRIES = 3
        for attempt in range(MAX_RETRIES):
            try:
                command = [self.get_python_interpreter(), "-m", "pip", "install", "--upgrade", package]
                subprocess.check_call(command)
                logger.info(f'Successfully upgraded {package}')
                return True
            except Exception as e:
                logger.error(f'Error occurred while upgrading package {package} (attempt {attempt + 1}): {str(e)}')
        return False

    def backup_packages(self):
        try:
            filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")], title="Choose filename")
            if filepath:
                command = [self.get_python_interpreter(), "-m", "pip", "freeze"]
                with open(filepath, "w") as file:
                    subprocess.call(command, stdout=file)
                messagebox.showinfo("Info", "Packages backed up successfully.")
                logger.info('Packages backed up successfully')
        except Exception as e:
            logging.error(f'Error occurred during backup: {str(e)}')

    def restore_packages(self):
        try:
            filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")], title="Choose file")
            if filepath:
                command = [self.get_python_interpreter(), "-m", "pip", "install", "-r", filepath]
                subprocess.call(command)
                messagebox.showinfo("Info", "Packages restored successfully.")
                logger.info('Packages restored successfully')
        except Exception as e:
            logging.error(f'Error occurred during restore: {str(e)}')

    def check_disk_space(self):
        total, used, free = shutil.disk_usage(__file__)
        return free > 500 * 1024 * 1024  # at least 500MB


def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
