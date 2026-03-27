import numpy as np
from scipy.io import wavfile
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

notes = {   
    'C': 261.63,
    'D': 293.66,
    'E': 329.63,
    'F': 349.23,
    'G': 392.00,
    'A': 440.00,
    'B': 493.88, }


chords = {
    'C_maj': ['C', 'E', 'G'],
    'D_min': ['D', 'F', 'A'],
    'E_min': ['E', 'G', 'B'],
    'F_maj': ['F', 'A', 'C'],
    'G_maj': ['G', 'B', 'D'],
    'A_min': ['A', 'C', 'E'],
    'B_dim': ['B', 'D', 'F'],
}





def melody_maker(note_list, note_duration):
    
    sample_rate = 44100
    melody_complete = []

    for note in note_list:
        frequency = notes[note]

        time = np.linspace(0, note_duration, sample_rate * note_duration)

        wave = np.sin(2 * np.pi * frequency * time)

        

        melody_complete.append(wave)

    full_wave = np.concatenate(melody_complete)

    wave_int = np.int16(full_wave * 32767)

    # ! Save as WAV file
    filename = "melody.wav"
    wavfile.write(filename, sample_rate, wave_int) # * write(filename, rate, data) saves the audio data to a WAV file with the specified filename and sample rate.
    return(filename) # * return the file
    
melody_maker(["E", "G", "A", "D", "E", "D", "C"], 1)


def chord_maker(chord, note_duration):
    note_list = chords[chord]

    sample_rate = 44100 # cd quality or so ive heard

    time = np.linspace(0, note_duration, sample_rate * note_duration) # * stop, start, ensure theres enough samples till the stop
    combined_wave = np.zeros(len(time)) # * start blank

    for note in note_list:
        frequency = notes[note] #

        
        wave = np.sin(2 * np.pi * frequency * time) # * generate wave actual sound making a wave, difining pitch, tell u where in time u are in wave
        


        combined_wave += wave / len(note_list) # * add the value of each note to the combined note as a np list so it can be played as a chord and not sequence and divide
    

    return combined_wave

   #wavfile.write('8bitchords.wav', sample_rate, wave_convert) # * write(filename, rate, data) saves the audio data to a WAV file with the specified filename and sample rate.
    # print("8bitchords.wav") # * return the file a confirmation message
  

chord_maker("C_maj", 1)


def chord_progression(chord_list, chord_duration): 
    sample_rate = 44100 
    full_progression = [] # * create an empty list

    for chord in chord_list:
        returned = chord_maker(chord, chord_duration) # * for every chord call chord maker and make and let it do its job
        full_progression.append(returned) # * after every chord add it to the empty list

    full_wave = np.concatenate(full_progression) # * concatenate basically takes the three small arrays that are inside  full progression [array[chord1], array[chord2], array[chord3]] and fuses them into a big one, so it can be read by np yatayata
    wave_convert = np.int16(full_wave * 32767 ) # * convert the wave to 16 cuz it has been separated  // the 0.5 is to lower the volume quick fix
    
    filename = "chord_progression.wav"
    wavfile.write(filename, sample_rate, wave_convert) # * write to file with the values
    return(filename) # return

chord_progression(["D_min", "D_min", "E_min", "D_min","F_maj", "F_maj", "A_min", "A_min", "F_maj", "G_maj", "C_maj"], 1)