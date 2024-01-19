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

    return result, numMeasures