import os, sys

def find_files(path):
    return [f for f in os.listdir() if os.path.isfile(f)]

def get_extensions(files):
    return [f.lower().split('.')[-1] for f in files]

def main():
    if len(sys.argv) < 2:
        path = os.getcwd()
    else:
        path = sys.argv[1]
    
    if not os.path.exists(path):
        print("ERROR: Path does not exist")
        exit()

if __name__ == "__main__":
    main()