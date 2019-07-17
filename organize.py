import platform
import sys
import os


categories = {
    "Images": ["jpg", "jpeg", "jpe", "jif", "jfif", "jfi", "png", "gif", "webp", "tiff", "tif", "psd", "raw", "arw", "cr2", "nrw", "k25", "bmp", "svg", "svgz"],
    "Audio": ["mp3", "flac", "ogg", "wav", "aac", "aa", "aax", "3gp", "m4a", "m4b", "m4p", "oga"],
    "Video": ["webm", "mp4", "avi", "mkv", "flv", "ogv", "gifv", "mov", "qt", "mpg", "mp2", "mpeg", "mpv", "3gp"],
    "Code": ["py", "c", "cpp", "js", "html", "css", "java", "go", "php"],
    "Docs": ["doc", "dot", "docx", "docm", "xls", "xlt", "xlsx", "xlsm", "xltx", "xltm", "ppt", "pptx", "pptm", "pps", "potx", "potm", "ppsx", "pdf", "epub", "mobi"],
    "Executables": ["exe", "run"],
}

# Get the default user folder's (Videos, Pictures, Documents, etc) path for Windows
def windows_user_paths():
    from win32com.shell import shell, shellcon  # BAD PRACTICE, haven't found a better way getting around this, sue me

    paths = {
        "Images": shell.SHGetFolderPath(0, shellcon.CSIDL_MYPICTURES, None, 0),
        "Audio": shell.SHGetFolderPath(0, shellcon.CSIDL_MYMUSIC, None, 0),
        "Video": shell.SHGetFolderPath(0, shellcon.CSIDL_MYVIDEOS, None, 0),
        "Docs": shell.SHGetFolderPath(0, shellcon.CSIDL_MYDOCUMENTS, None, 0),
    }

    return paths

# Get the default user folder's (Videos, Pictures, Documents, etc) path for Windows
def linux_user_paths():
    from gi.repository import GLib

    paths = {
        "Images": GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_PICTURES),
        "Audio": GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_MUSIC),
        "Video": GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_VIDEOS),
        "Docs": GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOCUMENTS),
    }

    return paths

# Get the name of each file in the given path, but only at the root
def find_files(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

# Extract the extension for each filename given
def get_extensions(files):
    return [(f, f.lower().split('.')[-1]) for f in files]

# Categorize files based on their extensions and groups them
def categorize(files):
    file_ext = get_extensions(files)

    categorized_files = {
        "Executables": [],
        "Images": [],
        "Audio": [],
        "Video": [],
        "Code": [],
        "Docs": [],
        "Unknown": [],
    }

    for file, ext in file_ext:
        for cat in categories:
            if ext in categories[cat]:
                categorized_files[cat].append(file)
                break
        else:
            categorized_files["Unknown"].append(file)

    return {key: value for key, value in categorized_files.items() if len(value) > 0}

# Create folders described by key on the given path
def create_folders(path, keys):
    for folder in keys:
        new_path = os.path.join(path, folder)
        try:
            os.mkdir(new_path)
        except FileExistsError:
            pass

# Move categorized files to the given path
# If 'user' argument is true, move to the default user folder
def move_files(path, cfiles, user):
    if not user:
        create_folders(path, cfiles.keys())
        for folder, files in cfiles.items():
            for f in files:
                start = os.path.join(path, f)
                destination = os.path.join(path, folder, f)

                os.rename(start, destination)

                print("\nFile:", start, "\nMoved to:", destination)

    else:
        if platform.system() == "Linux":
            user_paths = linux_user_paths()
        else:
            user_paths = windows_user_paths()

        create_folders(path, [folder for folder in cfiles if folder not in user_paths])

        for folder, files in cfiles.items():
            for f in files:
                start = os.path.join(path, f)

                if folder in user_paths:
                    destination = os.path.join(user_paths[folder], f)
                else:
                    destination = os.path.join(path, folder, f)

                os.rename(start, destination)

                print("\nFile:", start, "\nMoved to:", destination)

def main():
    if len(sys.argv[1:]) and not os.path.exists(sys.argv[-1]):
        path = os.getcwd()
        print("No valid path found as argument, organizing:", )
    else:
        path = sys.argv[-1]

    if "-u" in sys.argv:
        user = True
    else:
        user = False

    print("Files for:", path)

    file_names = find_files(path)
    cf = categorize(file_names)

    move_files(path, cf, user)

    print("\n", len(file_names), "files were moved.")

if __name__ == "__main__":
    main()
