import MusicTheory as mt
import numpy as np
import pandas as pd
import mido
import os
import sys
import random
from mido import MidiFile, MidiTrack, Message

def MidiChannelConvert(Midifile, channelNumber):
    
    activeNotes = []
    time = float(0)
    timestep = 0
    prevstep = 0
    prev = float(0)

    ResString = []
    for msg in Midifile:
        
        if not msg.is_meta:
            if time != time+msg.time:
                prevTime = time
                time = time+msg.time
            timestep = timestep+1
        
        if msg.type == 'note_off':
            if msg.channel == channelNumber:
                note = msg.bytes() 
                note = note[1:3]
    
                musicNote = mt.transpose(note[0])
                activeNotes.remove(musicNote)
        if msg.type == 'note_on':
            channel = msg.channel
            note = msg.bytes() 
            note = note[1:3]

            musicNote = mt.transpose(note[0])
            musicVelocity = note[1]

            noteData = pd.Series([timestep, channel, musicNote, musicVelocity], index=['time','channel','note','velocity'])
            if channel == channelNumber:
                
                activeNotes.append(musicNote)
        if prevstep != timestep:
            if activeNotes!= []:
                ResString.append(activeNotes.copy())
            else:
                ResString.append([13])
        prevstep = timestep
    
    notes = ResString
    return notes

def generateNoteSequencesTable(directory, filename):
    
    Columns = {'MidiFileName', 'Channel', 'Note Sequence'}
    NoteTable = pd.DataFrame(columns=Columns)
    lowerfile = filename.lower()
    if lowerfile.endswith(".mid"):
        
        
        
        MidiFilename = directory+filename        
        numChannel = CountChannels(MidiFilename) 
        
        midiFile = MidiFile(directory+filename)
        
        for i in range(0, numChannel+1):
            NoteSequence = MidiChannelConvert(midiFile, i)
            result=pd.Series([filename, i, NoteSequence], index=['MidiFileName', 'Channel', 'Note Sequence'])
            NoteTable = NoteTable.append(result, ignore_index=True)
    
    return NoteTable
        

def CountChannels (MidiFilename):
    
    midiFile = MidiFile(MidiFilename)
        
    channel = 0
    
    for msg in midiFile:
        if not msg.is_meta:
            if msg.channel > channel:
                channel = msg.channel

    return channel

def getMidiFile(filename):
    
    midiFile = MidiFile(filename)
    return midiFile


def generateTrainingData(notelength, step, table):
    
    maxlen = notelength
    step = step
    
    x = []
    y = []
    
    for row in table.iterrows():
        #if table['Channel'] == 0:
        noteSequences = table['Note Sequence'].iloc[0]
        
        for i in range(0,len(noteSequences)-(maxlen+1),step):
            
            seq = []
            label = []
            
            for j in range(0,maxlen):
                
                seq.append(noteSequences[i+j])
                
            yy = noteSequences[i+maxlen]
            yyy = yy[0]
            label.append(yyy)
            x.append(seq)
            y.append(label)
    
    return x, y

def generateSequenceStats(table):
    
    Columns = {'Note Number', 'Count', 'Same Played', 'Followed On', 'Combination Size'}
    statistics = pd.DataFrame(columns=Columns)
    
    for index, row in table.iterrows():
        noteSequences = table['Note Sequence'].iloc[index]
        
        for notenumber in range(13):
            count = 0
            same = []
            following = []
            combinations = []
            
            for k in range(13):
                combinations.append(0)
                same.append(0)
                following.append(0)
            
            for i in range(0, len(noteSequences)-1):
                
                if notenumber in noteSequences[i] :
                    notes = noteSequences[i]

                    sizing = len(notes)
                    
                    if(sizing > 10):
                        sizing = 10
                    combinations[sizing] = combinations[sizing]+1
                    
                    count = count+1
                    for j in range(13):
                        
                        if j in noteSequences[i]:
                            if j != notenumber:
                                same[j] = same[j]+1
                        
                        if j in noteSequences[i+1]:
                            
                            following[j] = following[j]+1
            
            result=pd.Series([notenumber,count, same, following, combinations], index=['Note Number', 'Count', 'Same Played', 'Followed On', 'Combination Size'])
            statistics = statistics.append(result, ignore_index=True)
            
            
    return statistics
            
def ammendSequence(table):
    
    noteSequences = []
    
    for row in table.iterrows():
        notes = table['Note Sequence'].iloc[0]
        
        for i in notes:
            noteSequences.append(i)
    
    Columns = {'Note Sequence'}
    NoteTable = pd.DataFrame(columns=Columns)
    result=pd.Series([noteSequences], index=['Note Sequence'])
    NoteTable = NoteTable.append(result, ignore_index=True)
    return NoteTable
            
            


def generateProbailities(table):
    
    Columns = {'Note Number', 'Probabilities Same', 'Probabilities Followed On', 'Combination Size Probability'}
    probabilities = pd.DataFrame(columns=Columns)
    
    for index , row in table.iterrows():
        NoteNumber = table['Note Number'].iloc[index]
        Count = table['Count'].iloc[index]
        SamePlayed = table['Same Played'].iloc[index]
        FollowedOn = table['Followed On'].iloc[index]
        Combinations =  table['Combination Size'].iloc[index]
        same = []
        combo = []
        following = []
        
        
        if Count > 0 :
            
            
            
            for k in range(13):
                same.append(0)
                following.append(0)
                combo.append(0)
            
            for i in range(len(FollowedOn)):
                    
                following[i] = FollowedOn[i]/Count
                same[i] = SamePlayed[i]/Count
                combo[i] = Combinations[i]/Count
                
        
        result=pd.Series([NoteNumber, same, following, combo], index=['Note Number', 'Probabilities Same', 'Probabilities Followed On', 'Combination Size Probability'])
        probabilities = probabilities.append(result, ignore_index=True)
    
    return probabilities
        

def generateRandomProbilityBased(table):
    
    
    Sequence = ""
    seq = []
    lastnote = 5
    activeNotes = [lastnote]
    seq.append(activeNotes)
    
    for i in range(100):
        
        
        Following = table['Probabilities Followed On'].iloc[lastnote]
        
        FollowProba = []
        Follow = []
        proba = 0
        index = 0
        for j in range(len(Following)):
            
            if Following[j] > 0:
                Follow.append(j)
                proba = proba + Following[j]
                FollowProba.append(proba)
        
        FollowRand = random.uniform(0,1);
        for j in range(len(Follow)):
            lower = 0
            upper = 0
            if j == 0:
                upper = FollowProba[j]
            elif j == len(Follow):
                lower = FollowProba[j]
                upper = 1
            else:
                lower = FollowProba[j-1]
                upper = FollowProba[j]
            
            if FollowRand > lower and FollowRand < upper:
                index = j
        
        nextnote =  Follow[index]
        
        Same = table['Probabilities Same'].iloc[nextnote]
        ComboSize = table['Combination Size Probability'].iloc[nextnote]
        
        
        sizeProba = []
        sizes = []
        proba = 0
        sizeindex = 0
        for j in range(len(ComboSize)):
            
            if ComboSize[j] > 0:
                sizes.append(j)
                proba = proba + ComboSize[j]
                sizeProba.append(proba)
        
        SizeRand = random.uniform(0,1);
        
        for j in range(len(sizes)):
            lower = 0
            upper = 0
            if j == 0:
                upper = sizeProba[j]
            elif j == len(sizes):
                lower = sizeProba[j]
                upper = 1
            else:
                lower = sizeProba[j-1]
                upper = sizeProba[j]
            
            if SizeRand > lower and SizeRand < upper:
                sizeindex = j
        
        activeNotes = []
        activeNotes.append(nextnote)
        
        attempts = 0
        
        while (len(activeNotes)-1) < sizes[sizeindex] and attempts<5:
            attempts =attempts+1
            SameProba = []
            Sames = []
            proba = 0
            index = 0
            for j in range(len(Same)):
                
                if Same[j] > 0:
                    Sames.append(j)
                    proba = proba + Same[j]
                    SameProba.append(proba)
            
            SameRand = random.uniform(0,1);
            
            for j in range(len(Sames)):
                lower = 0
                upper = 0
                if j == 0:
                    upper = SameProba[j]
                elif j == len(Sames):
                    lower = FollowProba[j]
                    upper = 1
                else:
                    lower = SameProba[j-1]
                    upper = SameProba[j]
                
                if SameRand > lower and SameRand < upper:
                    index = j
                    
            notesInSeq = Sames[index]
            
            if not(notesInSeq in activeNotes):
                
                activeNotes.append(notesInSeq)
            
        
        
        if(len(activeNotes) >1 ):
            lastnote = random.randint(0,len(activeNotes)-1)
            lastnote = activeNotes[lastnote]
        elif (len(activeNotes) == 1):
            
            lastnote = activeNotes[1]
            
        else:
            lastnote = activeNotes[0]
            
        seq.append(activeNotes)
        
    
    for i in range(len(seq)):
        
        active = seq[i]
        for j in active:
            if j == 13:
                Sequence = Sequence+' '
            else:
                Sequence = Sequence + chr(j+60)
        Sequence = Sequence + ' ' 
        
    return Sequence

def generateSimplifiedSingle():

    Columns = {'MidiFileName', 'Channel', 'Note Sequence'}
    CompleteTable = pd.DataFrame(columns=Columns)
    
    directory = "Midi/"
    
    for filename in os.listdir(directory):
        Table = generateNoteSequencesTable(directory, filename)
        dataframes = [CompleteTable, Table]
        CompleteTable = pd.concat(dataframes, axis=0)
        CompleteTable = CompleteTable.reset_index(drop=True)
    
    print("Gathering Data")
    sequences = ammendSequence(CompleteTable)
    statistical = generateSequenceStats(sequences)
    proba = generateProbailities(statistical)
    
    print("Generating")
    sequences = generateRandomProbilityBased(proba)
    try:
        filename = str(random.randint(0,999)) + str(random.randint(999,9999))+chr(random.randint(60,127))
        print("saving as " + filename + ".mid in the output folder")
        convertSequenceToMidi(sequences, "Outputs/"+filename, 400)
    except Exception as e:
        print(e)
        print("File name error, retrying")
        filename = str(random.randint(0,999)) + str(random.randint(999,9999))+chr(random.randint(60,127))
        print("saving as " + filename + ".mid in the output folder")
        convertSequenceToMidi(sequences, "Outputs/"+filename, 400)
    
def convertSequenceToMidi(generatedSequence, filename, timetick):
        #code to convert back to midi
    print("converting back to midi")
    
    result = []
    for character in generatedSequence:
        if character == ' ':
            result.append(' ')
        else:
            s = ord(character)
            result.append(s)

    prevNotes = []
    notes = []
    pr = np.asarray(notes)
    
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    time = 0
    
    for n in result:

    
        if n ==' ':
            time = timetick
            msg = mido.Message('note_off')
            mgtime = int(time)
            msg.time = mgtime
            track.append(msg)
            no = np.asarray(notes)
            for x in no:
                
                if not (x in pr):
                    msg = mido.Message('note_on', note=x, velocity=100)
                    track.append(msg)
            
            for x in pr:
                
                if not (x in no):
                    msg = mido.Message('note_off', note=x)

                    track.append(msg)
                
            pr = no.copy()
            notes = []
        else:
            notes.append(n)
    
    mid.save(filename+'.mid') 
    
generateSimplifiedSingle()