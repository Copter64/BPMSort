"""
BPM Sort - Main Entry Point

This module serves as the main entry point for the BPM Sort application.
It imports the necessary functions from bpm_win and provides a clean
interface for running the BPM sorting program.
"""

import bpm_win

def main():
    """
    Main function to run the BPM Sort program.
    
    Initiates the interactive folder selection process and starts
    the BPM analysis and sorting workflow.
    """
    bpm_win.folder_request()

if __name__ == '__main__':
    main()
