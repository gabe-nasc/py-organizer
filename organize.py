import os, sys

categories = {
    "Images":["jpg", "jpeg", "jpe", "jif", "jfif", "jfi", "png", "gif", "webp", "tiff", "tif", "psd", "raw", "arw", "cr2", "nrw", "k25", "bmp", "svg", "svgz"],
    "Audio":["mp3", "flac", "ogg", "wav", "aac", "aa", "aax", "3gp", "m4a", "m4b", "m4p", "oga"],
    "Video":["webm", "mp4", "avi", "mkv", "flv", "ogv", "gifv", "mov", "qt", "mpg", "mp2", "mpeg", "mpv", "3gp"],
    "Code":["py", "c", "cpp", "js", "html", "css", "java", "go", "php"],
    "Docs":["doc", "dot", "docx", "docm", "xls", "xlt", "xlsx", "xlsm", "xltx", "xltm", "ppt", "pptx", "pptm", "pps", "potx", "potm", "ppsx", "pdf", "epub", "mobi"],
    "Executables":["exe", "run"],
}

def find_files(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

def get_extensions(files):
    return [(f,f.lower().split('.')[-1]) for f in files]

def categorize(files):
    file_ext = get_extensions(files)

    categorized_files = {
        "Executables":[],
        "Images":[],
        "Audio":[],
        "Video":[],
        "Code":[],
        "Docs":[],
        "Unknown":[],
    }

    for file, ext in file_ext:
        for cat in categories:
            if ext in categories[cat]:
                categorized_files[cat].append(file)
                break
        else:
            categorized_files["Unknown"].append(file)
    
    return categorized_files

def main():
    if len(sys.argv) < 2:
        path = os.getcwd()
    else:
        path = sys.argv[1]
    
    if not os.path.exists(path):
        print("ERROR: Path does not exist")
        exit()

    print("Files for: ", path)

    file_names = find_files(path)
    cf = categorize(file_names)

if __name__ == "__main__":
    main()