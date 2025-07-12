"""
BPM Sort - Windows Optimized Audio File Organizer

This module provides the main functionality for analyzing audio files and organizing them
by their BPM (Beats Per Minute) values. It uses the librosa library for accurate tempo
detection and creates an organized folder structure for music collections.

The program is optimized for Windows but maintains cross-platform compatibility.
"""

import os
from os.path import exists
import sys
import shutil
import librosa  # Audio processing library for BPM detection and analysis
import settings  # Configuration settings

class BpmFolders:
    """
    A class to handle BPM analysis and sorting of music files.
    
    This class provides methods to analyze audio files for their BPM values,
    create appropriate directory structures, and organize files by tempo.
    
    Attributes:
        bpm (int): The detected BPM value of the audio file
        musicfile (str): Path to the audio file being processed
        path (str): Path to the destination folder for this BPM value
        newfile (str): Path to the copied file in the destination folder
    """
    
    def __init__(self, musicfile):
        """
        Initialize the BpmFolders instance.
        
        Args:
            musicfile (str): Path to the audio file to be processed
        """
        self.bpm = None
        self.musicfile = musicfile
        self.path = None
        self.newfile = None

    def get_bpm(self):
        """
        Analyzes the audio file to detect its BPM (Beats Per Minute).
        
        Uses librosa's beat tracking algorithm to estimate the tempo of the audio file.
        The detected BPM is rounded to the nearest whole number for folder organization.
        
        Returns:
            int: The detected BPM value rounded to the nearest integer
            
        Raises:
            Exception: If the audio file cannot be loaded or processed
        """
        try:
            # Load audio file with original sample rate and convert to mono
            audio, sr = librosa.load(self.musicfile, sr=None, mono=True)
            
            # Estimate tempo (BPM) using librosa's beat tracking algorithm
            # Returns tuple: (tempo, beat_frames)
            tempo, beat_frames = librosa.beat.beat_track(y=audio, sr=sr)
            
            # Extract the BPM value from the tempo (first element of tuple)
            extracted_tempo = tempo
            
            if settings.SHOW_BPM_DETECTION:
                print(f"Detected BPM: {extracted_tempo}")
            
            # Round to nearest integer for folder organization
            self.bpm = round(extracted_tempo.item())
            
            return self.bpm
            
        except Exception as e:
            if settings.VERBOSE_OUTPUT:
                print(f"Error processing {self.musicfile}: {e}")
            # Set default BPM if detection fails
            self.bpm = settings.DEFAULT_BPM
            if settings.SHOW_BPM_DETECTION:
                print(f"Using default BPM: {self.bpm}")
            return self.bpm

    def make_dir(self):
        """
        Creates a directory structure for organizing files by BPM value.
        
        Creates a parent folder and a subfolder named after the BPM value.
        Uses settings to determine folder names and structure.
        
        Returns:
            str: Path to the created BPM-specific directory
        """
        # Create parent folder using settings
        parentfolder = settings.get_output_folder_path()
        if not exists(parentfolder):
            os.mkdir(parentfolder)
            if settings.VERBOSE_OUTPUT:
                print(f"Created output folder: {parentfolder}")
            
        # Create BPM-specific subfolder using settings
        bpm_folder_name = settings.get_bmp_folder_name(self.bpm)
        directory = os.path.join(settings.OUTPUT_FOLDER_NAME, bpm_folder_name)
        self.path = os.path.join(sys.path[0], directory)

        # Create the BPM folder if it doesn't exist
        if not exists(self.path):
            os.mkdir(self.path)
            if settings.VERBOSE_OUTPUT:
                print(f"Created BPM folder: {self.path}")
            
        return self.path

    def move_music_file(self):
        """
        Copies the music file to the appropriate BPM folder.
        
        Creates a copy of the original file in the BPM-specific directory.
        If the file already exists in the destination, it skips the copy operation.
        
        Returns:
            str: Path to the copied file in the destination folder
        """
        if exists(self.path):
            filename = os.path.basename(self.musicfile)
            self.newfile = os.path.join(self.path, filename)
            
            # Check if file already exists in destination
            if os.path.exists(self.newfile) and settings.SKIP_EXISTING_FILES:
                if settings.SHOW_FILE_OPERATIONS:
                    print(f'{filename} already exists in {self.bpm} BPM Folder - skipping')
                return self.newfile
                
            # Copy or move file to BPM folder based on settings
            if settings.COPY_FILES:
                if settings.SHOW_FILE_OPERATIONS:
                    print(f'{filename} copied to {self.bpm} BPM Folder')
                shutil.copy(self.musicfile, self.newfile)
            else:
                if settings.SHOW_FILE_OPERATIONS:
                    print(f'{filename} moved to {self.bpm} BPM Folder')
                shutil.move(self.musicfile, self.newfile)
            
        return self.newfile

def bpm_read_folder(target_folder):
    """
    Processes all audio files in the target folder and its subdirectories.
    
    Recursively walks through the directory structure, analyzes each audio file
    for BPM, creates appropriate directories, and organizes files by tempo.
    
    Args:
        target_folder (str): Path to the folder containing audio files to process
    """
    processed_count = 0
    skipped_count = 0
    
    if settings.VERBOSE_OUTPUT:
        print(f"Processing folder: {target_folder}")
    
    for root, dirs, files in os.walk(target_folder):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                # Check if file is a supported audio format
                if settings.is_audio_file(file):
                    try:
                        # Process each audio file
                        music_processor = BpmFolders(musicfile=file_path)
                        
                        # Analyze BPM, create directory, and organize file
                        music_processor.get_bpm()
                        music_processor.make_dir()
                        music_processor.move_music_file()
                        processed_count += 1
                        
                    except Exception as e:
                        if settings.VERBOSE_OUTPUT:
                            print(f"Error processing {file}: {e}")
                        skipped_count += 1
                else:
                    if settings.VERBOSE_OUTPUT:
                        print(f"Skipping non-audio file: {file}")
                    skipped_count += 1
    
    if settings.VERBOSE_OUTPUT:
        print("\nProcessing complete:")
        print(f"- Files processed: {processed_count}")
        print(f"- Files skipped: {skipped_count}")

def review_target_folder(target_folder):
    """
    Reviews the target folder and confirms that files are present.
    
    Args:
        target_folder (str): Path to the folder to check
        
    Returns:
        bool: True if folder contains files, False otherwise
    """
    if os.listdir(target_folder):
        return True
    return False

def bpm_win(target_folder):
    """
    Main function for the BPM Sort program on Windows.
    
    Processes the target folder containing music files, analyzes their BPM values,
    and organizes them into appropriate directories.
    
    Args:
        target_folder (str): Path to the folder containing music files to process
    """
    musicfoldername = target_folder

    if settings.VERBOSE_OUTPUT:
        print("Starting BPM Sort process...")
        print(f"Target folder: {musicfoldername}")
        print(f"Output folder: {settings.OUTPUT_FOLDER_NAME}")
        print(f"Copy files: {settings.COPY_FILES}")
        print(f"Skip existing: {settings.SKIP_EXISTING_FILES}")
        print("-" * 50)

    if review_target_folder(musicfoldername):
        # Begin processing files in the folder
        bpm_read_folder(musicfoldername)
        
        if settings.VERBOSE_OUTPUT:
            print("BPM Sort process completed!")
    else:
        # Exit if no files are found
        print(f"There are no files in {musicfoldername}.")
        sys.exit("Exiting program. Please add files to folder and try again.")

def folder_request():
    """
    Prompts the user to enter a music folder path and initiates BPM sorting.
    
    Interactive function that requests folder input from the user and
    starts the BPM analysis and sorting process.
    """
    print("BPM Sort - Music File Organizer")
    print("=" * 40)
    
    if settings.VERBOSE_OUTPUT:
        print("\nCurrent Settings:")
        print(settings.get_settings_summary())
        print("=" * 40)
    
    target_folder = input("Please enter the path to the music folder: ")
    
    if not target_folder.strip():
        print(f"No folder specified. Using default: {settings.DEFAULT_INPUT_FOLDER}")
        target_folder = settings.DEFAULT_INPUT_FOLDER
    
    bpm_win(target_folder)
