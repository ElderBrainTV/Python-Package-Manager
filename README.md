# Pip Package Updater

The Pip Package Updater is a Python application that provides a graphical user interface (GUI) for upgrading Python packages installed via pip, creating backups of the package list, and restoring packages from a backup file.

## Features

- Select and upgrade specific packages from a list
- Choose between interactive mode (prompt for confirmation) or non-interactive mode
- View upgrade progress with a progress bar
- Create backups of installed packages
- Restore packages from a backup file
- Check available disk space before starting the upgrade process

## Requirements

- Python 3.x
- tkinter library (usually included with Python installations)

## Usage

1. Clone the repository:

```bash
git clone https://github.com/ElderBrainTV/Pip-Package-Updater.git
```

2. Change to the repository directory:

```
cd pip-package-updater
```

3. Install the required dependencies:
```
pip install -r requirements.txt
```
4. Run the application
```
python main.py
```
5.The GUI window will appear, allowing you to select packages for upgrade, choose upgrade mode, and perform backup and restore operations.


## Logging

The application logs events and errors to the `app.log` file in the repository. You can refer to this log file for troubleshooting or debugging purposes.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details
