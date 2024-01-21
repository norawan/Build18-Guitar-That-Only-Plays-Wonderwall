from constants import *

validChords = ["Em", "G", "D", "Asus4", "C", "-"]

Intro = "Em Em G G D D Asus4 Asus4, Em Em G G D D Asus4 Asus4, Em Em G G D D Asus4 Asus4, Em Em G G D D Asus4 Asus4"
Verse1 = "Em Em G G D D Asus4 Asus4, Em Em G G D D Asus4 Asus4, Em Em G G D D Asus4 Asus4, C C D D Asus4 Asus4 Asus4 Asus4"
Verse2 = "Em Em G G D D Asus4 Asus4, Em Em G G D D Asus4 Asus4, Em Em G G D D Asus4 Asus4, Em Em G G D D Asus4 Asus4"
PreChorus = "C C D D Em Em Em Em, C C D D Em Em Em Em, C C D D G D Em D, Asus4 Asus4 Asus4 Asus4 Asus4 Asus4 Asus4 Asus4"
Chorus_A = "C C Em Em D D Em Em, C C Em Em D D Em Em, C C Em Em D D Em Em, C C Em Em D D Em -"
Rest = "- - - - - - - -"
Verse3 = "Em Em G G D D Asus4 Asus4, Em Em G G D D Asus4 Asus4, Em Em G G D D Asus4 Asus4, Em Em G G D D Asus4 Asus4"
Chorus_B = "C C Em Em D D Em Em, C C Em Em D D Em Em, C C Em Em D D Em Em, C C Em Em D D Em Em"

strings = [Intro, Verse1, Verse2, PreChorus, Chorus_A, Rest, Verse3, PreChorus, Chorus_B, Chorus_B, Chorus_B]
song = ','.join(strings)

def getWonderwallLyrics(numMeasures):
    lyrics = [""] * (numMeasures + 1)
    lyrics[0] = "(Intro)"
    lyrics[1] = "(Intro)"
    lyrics[2] = "(Intro)"
    lyrics[3] = "(Intro)"
    lyrics[4] = "Today is gonna be the day\nthat they're gonna throw it back to you"
    lyrics[5] = "And by now, you should've somehow\nrealised what you gotta do"
    lyrics[6] = "I don't believe that anybody\nfeels the way I do about you now"
    lyrics[8] = "And backbeat, the word is\non the street that the\nfire in your heart is out"
    lyrics[9] = "I'm sure you've heard it all before,\nbut you never really had a doubt"
    lyrics[10] = "I don't believe that anybody\nfeels the way I do about you now"
    lyrics [12] = "And all the roads we\nhave to walk are winding"
    lyrics[13] = "And all the lights that\nlead us there are blinding"
    lyrics[14] = "There are many things\nthat I would like to say to you,\nbut I don't know how" 
    lyrics[16] = "Because maybe"
    lyrics[17] = "You're gonna be the one that saves me"
    lyrics[18] = "And after all"
    lyrics[19] = "You're my wonderwall"
    lyrics[20] = "(Rest)"
    lyrics[21] = "Today was gonna be the day,\nbut they'll never throw it back to you"
    lyrics[22] = "And by now, you should've somehow\nrealised what you're not to do"
    lyrics[23] = "I don't believe that anybody\nfeels the way I do about you now"
    lyrics[25] = "And all the roads that lead\nyou there were winding"
    lyrics[26] = "And all the lights that\nlight the way are blinding"
    lyrics[27] = "There are many things\nthat I would like to say to you,\nbut I don't know how"
    lyrics[29] = "I said maybe"
    lyrics[30] = "You're gonna be the one that saves me"
    lyrics[31] = "And after all"
    lyrics[32] = "You're my wonderwall"
    lyrics[33] = "I said maybe (I said maybe)"
    lyrics[34] = "You're gonna be the one that saves me"
    lyrics[35] = "And after all"
    lyrics[36] = "You're my wonderwall"
    lyrics[37] = "I said maybe (I said maybe)"
    lyrics[38] = "You're gonna be the one that saves me\n(saves me)"
    lyrics[39] = "You're gonna be the one that saves me\n(saves me)"
    lyrics[40] = "You're gonna be the one that saves me\n(saves me)"
    lyrics[41] = ""
    
    return lyrics

def getWonderwallDict():
    result = dict()
    measures = song.split(",")
    numMeasures = len(measures)

    quarterLength_ns = NUM_NS_IN_ONE_MINUTE / (TEMPO)
    eighthNote_ns = quarterLength_ns / 2
    sixteenthNote_ns = eighthNote_ns / 2
    print(sixteenthNote_ns)

    offsetInterval = 1 / 32

    beatNumber = 0
    for i in range(numMeasures):
        measure = measures[i]
        chordDict = dict()
        offset = 0
        for chord in measure.split(" "):
            if chord not in validChords: continue

            match beatNumber % 8:
                case 0:
                    chordDict[offset] = chord
                    chordDict[offset + 2 * offsetInterval] = chord
                case 1:
                    chordDict[offset] = chord
                    chordDict[offset + 2 * offsetInterval] = chord
                    chordDict[offset + 3 * offsetInterval] = chord
                case 2:
                    chordDict[offset] = chord
                    chordDict[offset + offsetInterval] = chord
                    chordDict[offset + 2 * offsetInterval] = chord
                case 3:
                    chordDict[offset] = chord
                    chordDict[offset + 2 * offsetInterval] = chord
                    chordDict[offset + 3 * offsetInterval] = chord
                case 4:
                    chordDict[offset] = chord
                    chordDict[offset + offsetInterval] = chord
                    chordDict[offset + 2 * offsetInterval] = chord
                case 5:
                    chordDict[offset] = chord
                    chordDict[offset + 2 * offsetInterval] = chord
                    chordDict[offset + 3 * offsetInterval] = chord
                case 6:
                    chordDict[offset + offsetInterval] = chord
                    chordDict[offset + 3 * offsetInterval] = chord
                case 7:
                    chordDict[offset] = chord
                    chordDict[offset + offsetInterval] = chord
                    chordDict[offset + 2 * offsetInterval] = chord
                    chordDict[offset + 3 * offsetInterval] = chord
                case _:
                    pass

            offset += (4 * offsetInterval)
            beatNumber = (beatNumber + 1) % NUM_BEATS_IN_MEASURE
        result[i] = chordDict
    
    lyrics = getWonderwallLyrics(numMeasures)

    return result, numMeasures, lyrics