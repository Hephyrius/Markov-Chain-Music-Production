import numpy as np

def generateScales():
    #create a set of rules that are used
    scales = []
    
    
    #Scales as a list:
    cMajor = [0,2,4,5,9,11,12]
    scales.append(cMajor)
    dMajor = [2,4,6,9,13,14]
    scales.append(dMajor)
    eMajor = [4,6,8,9,11,13,15,16]
    scales.append(eMajor)
    fMajor = [5,7,9,11,12,14,17]
    scales.append(fMajor)
    bMajor = [11,13,15,16,18,20,22,23]
    scales.append(bMajor)
    gMajor = [7,9,11,12,14,16,18,19]
    scales.append(gMajor)
    aMajor = [9,11,13,14,16,18,20,21]
    scales.append(aMajor)
    
    return scales

def randomScaleToOctave(scales, octaveNumber):
    
    selectedScale = scales[np.random.randint(len(scales))]
    octave = octaveNumber
    
    scaleInOctave = []
    
    for i in selectedScale:
        adjusted = 12*octave
        
        note = i+ adjusted
        scaleInOctave.append(note)
    
    return scaleInOctave

def transpose(noteNumber):
    
    a =    [9,21,33,45,57,69,81,93,105,117,129]
    ash =  [10,22,34,46,58,70,82,94,106,118,130]
    b =    [11,23,35,47,59,71,83,95,107,119,131]    
    c =    [0,12,24,36,48,60,72,84,96,108,120]
    cs =   [1,13,25,37,49,61,73,85,97,109,121]
    d =    [2,14,26,38,50,62,74,86,98,110,122]
    ds =   [3,15,27,39,51,63,75,87,99,111,123]
    e =    [4,16,28,40,52,64,76,88,100,112,124]
    f =    [5,17,29,41,53,65,77,89,101,113,125]
    fs =   [6,18,30,42,54,66,78,90,102,114,126]
    g =    [7,19,31,43,55,67,79,91,103,115,127]
    gs =   [8,20,32,44,56,68,80,92,104,116,128]

    notes = [a,ash,b,c,cs,d,ds,e,f,fs,g,gs]
    
    for i in range(len(notes)):
        if noteNumber in notes[i]:
            noteNumber = notes[i][0]
    
    return noteNumber
    
    
    
    
    
    
    
    

def generateChords():
    
    #Cords as a list
    chords = []
    #MajorCords
    cM = [0,4,7]
    chords.append(cM)
    cMi = [0,3,7]
    chords.append(cMi)
    dM = [2,6,9]
    chords.append(dM)
    dMi = [2,5,9]
    chords.append(dMi)
    eM = [4,8,11]
    chords.append(eM)
    eMi = [4,7,11]
    chords.append(eMi)
    fM = [5,9,12]
    chords.append(fM)
    fMi = [5,8,12]
    chords.append(fMi)
    gM = [7,11,14]
    chords.append(gM)
    gMi = [7,10,14]
    chords.append(gMi)
    aM = [9,13,16]
    chords.append(aM)
    aMi = [9,12,16]
    chords.append(aMi)
    bM = [11,15,18]
    chords.append(bM)
    bMi = [11,14,18]
    chords.append(bMi)
    
    return chords
