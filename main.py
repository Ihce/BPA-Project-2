import detectLoops as dl
import argparse
def createArgs():
    # Creates the argument parser and displays the custom user manager
    parser = argparse.ArgumentParser(description='A simple tool to display loops within a CFG using angr.', usage=msg())
    parser.add_argument('filepath')
    args = parser.parse_args()
    
    # Checks that user put a file path
    if not args.filepath:
        parser.print_usage()
        exit()
    
    # Sets the program to print all components if just the file path is supplie
    dl.clear_images_directory()
    dl.detectLoops(args.filepath)

def msg():
    return '''python main.py <options> "full path to file"'''

if __name__ == '__main__':
    createArgs()  