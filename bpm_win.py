"""jade-spector: This file is the main entry point for the BPM Sort program on Windows."""
#jade-spector: added docstring to clarify the purpose of the file.
import os
from os.path import exists
import sys
import shutil
import librosa #jade-spector: Added librosa for audio processing on windows.
# jade-spector: This should also work on linux, but I'll need to test it later.

class BpmFolders:
    """jade-spector: Class to handle BPM sorting of music files."""
    #Added a docstring to the class for clarity
    def __init__(self,musicfile):
        self.bpm = None
        self.musicfile = musicfile
        self.path = None
        self.newfile = None

# jade-spector: Changed the name of the function to conform to PEP 8 standards.
    def get_bpm(self):
        """jade-spector: Loads the audio file using librosa"""
        audio, sr = librosa.load(self.musicfile, sr=None, mono=True)
        #estimate tempo (BPM) and beat frames
        tempo= librosa.beat.beat_track(y=audio, sr=sr)
        # Extract the value from the tempo tuple

        extracted_tempo = tempo[0]
        print(extracted_tempo)
        self.bpm = round(extracted_tempo.item())

        # Return the BPM value
        return self.bpm

    # jade-spector: Changed the name of the function to conform to PEP 8 standards.
    def make_dir(self):
        """jade-spector: Creates a directory for the inputed BPM Value. If
        the directory already exists, it will not create a new one."""

        parentfolder = os.path.join(sys.path[0],'BPMSorted')
        if not exists(parentfolder):
            os.mkdir(parentfolder)
        # Directory
        directory = os.path.join('BPMSorted', f'{self.bpm} BPM Songs')
        # Joins Parent Directory path to current working directory
        self.path = os.path.join(sys.path[0], directory)

        exists(self.path)

        if not exists(self.path):
            os.mkdir(self.path)
        return self.path

# jade-spector: Changed the name of the function to conform to PEP 8 standards.
    def move_music_file(self):
        """jade-spector: Moves the target music file to the file titled with the BPM Value that
        matches is close to its BPM Value."""
        if exists(self.path):
            filename = os.path.basename(self.musicfile)
            self.newfile = os.path.join(self.path,filename)
            if os.path.exists(self.newfile):
                return self.newfile
            print(f'{filename} Moved into {self.bpm} BPM Folder')
            shutil.copy(self.musicfile,self.newfile)
        return self.newfile

def bpm_read_folder(target_folder):
    """Loops over files in the target folder directory"""
    for root, files in os.walk(target_folder):
        for file in files:
            f = os.path.join(root,file)
            if os.path.isfile(f):
                musictest = BpmFolders(musicfile=f)
                # jade-spector: If the file is in the target folder then it will
                # get the BPM Value, make a directory for the value (if it does
                # not already exist), and then move the file to the directory.
                musictest.get_bpm()
                musictest.make_dir()
                musictest.move_music_file()

def review_target_folder(target_folder):
    """jade-spector: Reviews the target folder and confirms that there are files present.
    Returns True or False."""
    if os.listdir(target_folder):
        return True
    return False

def bpm_win(target_folder):
    """jade-spector: Main function for the BPM Sort program on Windows."""
    #if target_folder.isempty():
        # jade-spector: If the user has provided a target folder, use it.
    #    musicfoldername = 'BPMSort-main\\Music Examples'
    musicfoldername = target_folder


    if review_target_folder(musicfoldername):
        # jade-spector: If True begin reading the folder.
        bpm_read_folder(musicfoldername)
    else:
        # jade-spector: If False, print message and exit.
        print(f"There are no music files in {musicfoldername}.")
        sys.exit("Exiting program. Please add music files to folder and try again.")

def folder_request():
    """jade-spector: Reuests the to point to which music folder to parse through."""
    target_folder = input("Please enter the path to the music folder: ")
    bpm_win(target_folder)
