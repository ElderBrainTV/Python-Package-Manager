# Python Package Manager

This program provides a graphical user interface for managing Python packages. With it, you can easily update, backup, and restore Python packages. 

![Pip Package Upgrader GUI](https://github.com/ElderBrainTV/Pip-Package-Updater/blob/125ec645854b9211312ba2436a77919f8027e828/Pip%20Package%20Upgrader%20GUI.png "Pip Pachage Upgrader GUI")
## Features

- Display all installed Python packages
- Update selected Python packages
- Backup selected Python packages to a file
- Restore Python packages from a backup file
- Configure which Python interpreter to use
- Hotkeys for quick access to functionalities

## How to Use

1. Run the Python script `python3 package_manager.py`. A GUI will appear showing a list of installed Python packages. 
2. To select multiple packages, hold down the Control key and click on the packages you want to select.
3. After selecting the packages, click on the "Update Selected Packages" button to update the packages. The progress of the updates will be shown in the progress bar. Once the updates are finished, a report will appear showing how many packages were successfully updated.
4. To backup the selected packages, click on the "Backup Packages" button. The packages will be saved in a file named `backup.txt`.
5. To restore packages from a backup, click on the "Restore Packages" button. The packages listed in `backup.txt` will be installed.
6. You can choose the Python interpreter used by the script with the dropdown menu at the top of the GUI.
7. The program state (selected interpreter and selected packages) is saved when the program exits and is loaded when the program starts.
8. There are hotkeys for quick access to functionalities:
    - Control-q: Quit the program
    - Control-b: Backup packages
    - Control-r: Restore packages

![Finished Job.png](https://github.com/ElderBrainTV/Pip-Package-Updater/blob/125ec645854b9211312ba2436a77919f8027e828/Finished%20Job.png "Finished Job")
## Requirements

- Python 3
- tkinter library
- pip (Python package manager)

## Issues and Contributions

If you find a bug or have an idea for a new feature, please open an issue or submit a pull request!

## License

This project is licensed under the terms of the MIT [License](LICENSE).
