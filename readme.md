# ExifTool GUI

A simple graphical user interface for ExifTool that allows you to view and edit metadata in image and other media files.

![ExifTool GUI](https://via.placeholder.com/800x600?text=ExifTool+GUI)

## Features

- Select and process multiple files at once
- View all metadata tags for selected files
- Edit metadata values with a user-friendly form interface
- Option to overwrite original files or save to a new location
- Support for custom ExifTool command line options
- Scrollable interface for handling files with extensive metadata

## Requirements

- Python 3.6 or higher
- Tkinter (usually comes with Python)
- [ExifTool](https://exiftool.org/) installed and available in your system PATH

## Installation

### 1. Install ExifTool

Before using this GUI, you need to have ExifTool installed on your system:

#### Windows
- Download the Windows executable from [ExifTool's website](https://exiftool.org/)
- Extract the `.exe` file and rename it to `exiftool.exe`
- Add the location to your system PATH or place it in a directory that's already in your PATH

#### macOS
```
brew install exiftool
```
or
```
port install p5-image-exiftool
```

#### Linux
```
sudo apt install libimage-exiftool-perl    # Debian/Ubuntu
sudo yum install perl-Image-ExifTool       # Fedora/CentOS
sudo pacman -S perl-image-exiftool         # Arch Linux
```

### 2. Set up the ExifTool GUI

1. Clone or download this repository:
   ```
   git clone https://github.com/yourusername/exiftool-gui.git
   cd exiftool-gui
   ```

2. Install the required Python libraries:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python ExifGui.py
   ```

## Usage

### Viewing Metadata
1. Click "Browse Files" to select one or more files
2. The metadata from the first selected file will be displayed in the scrollable area
3. Browse through the metadata tags and their values

### Editing Metadata
1. Select files as described above
2. Modify the values in the text fields for any metadata tags you want to change
3. Choose your output options:
   - Check "Overwrite Original Files" to modify files in place
   - Or check "Save to new folder" and select a destination folder for the modified files
4. Add any custom ExifTool options in the "Custom Options" field if needed
5. Click "Apply Changes" to process your files

### Example Use Cases

- Update copyright information across multiple images
- Fix incorrect date/time stamps in photos
- Remove sensitive metadata before sharing files
- Add location information to a batch of images
- Fix or update camera and lens information

## Troubleshooting

- **"Command not found" error**: Make sure ExifTool is properly installed and in your system PATH
- **No metadata displays**: Verify that the selected file type is supported by ExifTool
- **Changes not applied**: Check the console output for more detailed error messages
- **Special characters in metadata**: If you encounter issues with special characters, try using the custom options field to add appropriate encoding parameters

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Phil Harvey for creating [ExifTool](https://exiftool.org/)
- This GUI is a simple wrapper and does not replicate all the functionality of the command-line ExifTool
