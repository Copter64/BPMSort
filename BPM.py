import essentia.standard as es
from tempfile import TemporaryDirectory
from math import ceil
import os
from os.path import exists
import sys
import shutil

# Loading an audio file.

class BpmFolders:
    def __init__(self,musicfile):
        self.bpm = None
        self.musicfile = musicfile
        self.path = None
        self.newfile = None


    def BPM(self):
        audio = es.MonoLoader(filename=self.musicfile)()
        # Compute beat positions and BPM.
        rhythm_extractor = es.RhythmExtractor2013(method="multifeature")
        bpm, beats, beats_confidence, _, beats_intervals = rhythm_extractor(audio)

        # print("Beat positions (sec.):", beats)
        # print("Beat estimation confidence:", beats_confidence)
        marker = es.AudioOnsetsMarker(onsets=beats, type='beep')
        marked_audio = marker(audio)

        # self.bpm = round(bpm)
        self.bpm = bpm

        return self.bpm


    def MakeDirs(self):
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

        return

    def MoveMusicFile(self):
        if exists(self.path):
            filename = os.path.basename(self.musicfile)
            self.newfile = os.path.join(self.path,filename)
            print(f'{filename} Moved into {self.bpm} BPM Folder')
            shutil.copy(self.musicfile,self.newfile)
        return

#Main code starts here ----------------------
musicfoldername = 'Music Examples'
musicfolderpath = os.path.join(sys.path[0],musicfoldername)
songdict = {}

#Loops over files in the musicfoldername directory
for file in os.listdir(musicfolderpath):
    f = os.path.join(musicfolderpath,file)
    if os.path.isfile(f):
        musictest = BpmFolders(musicfile=f)
    songdict.update({file:musictest.BPM()})

print(songdict)







# # Write to an audio file in a temporary directory.
# temp_dir = TemporaryDirectory()
# es.MonoWriter(filename=temp_dir.name + f'{BPM(musicfile)}')(marked_audio)