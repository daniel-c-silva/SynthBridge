import numpy as np
from scipy.io import wavfile
from flask import Flask, request, jsonify, send_file
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

# ! NOTES AND CHORDS DICts
notes = {
    'C': 261.63, 'Cs': 277.18, 'D': 293.66, 'Ds': 311.13, 'E': 329.63, 'F': 349.23,
    'Fs': 369.99, 'G': 392.00, 'Gs': 415.30, 'A': 440.00, 'As': 466.16, 'B': 493.88,
}

chords = {
    # * Major Triads (Full Chromatic Scale)
    'C_maj': ['C', 'E', 'G'],    'Cs_maj': ['Cs', 'F', 'Gs'], 'D_maj': ['D', 'Fs', 'A'],
    'Ds_maj': ['Ds', 'G', 'As'], 'E_maj': ['E', 'Gs', 'B'],   'F_maj': ['F', 'A', 'C'],
    'Fs_maj': ['Fs', 'As', 'Cs'],'G_maj': ['G', 'B', 'D'],    'Gs_maj': ['Gs', 'C', 'Ds'],
    'A_maj': ['A', 'Cs', 'E'],   'As_maj': ['As', 'D', 'F'],  'B_maj': ['B', 'Ds', 'Fs'],

    # * Minor Triads (Full Chromatic Scale)
    'C_min': ['C', 'Ds', 'G'],   'Cs_min': ['Cs', 'E', 'Gs'], 'D_min': ['D', 'F', 'A'],
    'Ds_min': ['Ds', 'Fs', 'As'],'E_min': ['E', 'G', 'B'],    'F_min': ['F', 'Gs', 'C'],
    'Fs_min': ['Fs', 'A', 'Cs'], 'G_min': ['G', 'As', 'D'],   'Gs_min': ['Gs', 'B', 'Ds'],
    'A_min': ['A', 'C', 'E'],    'As_min': ['As', 'Cs', 'F'], 'B_min': ['B', 'D', 'Fs'],

    # * Dominant 7ths (The tension chords)
    'C7': ['C', 'E', 'G', 'As'],  'D7': ['D', 'Fs', 'A', 'C'], 'E7': ['E', 'Gs', 'B', 'D'],
    'F7': ['F', 'A', 'C', 'Ds'],  'G7': ['G', 'B', 'D', 'F'],  'A7': ['A', 'Cs', 'E', 'G'],
    'B7': ['B', 'Ds', 'Fs', 'A'],

    # * Major 7ths (Bossa Nova vibe)
    'C_maj7': ['C', 'E', 'G', 'B'],   'D_maj7': ['D', 'Fs', 'A', 'Cs'],
    'E_maj7': ['E', 'Gs', 'B', 'Ds'], 'F_maj7': ['F', 'A', 'C', 'E'],
    'G_maj7': ['G', 'B', 'D', 'Fs'],  'A_maj7': ['A', 'Cs', 'E', 'Gs'],
    'Bb_maj7': ['As', 'D', 'F', 'A'],

    # * Minor 7ths
    'C_m7': ['C', 'Ds', 'G', 'As'], 'D_m7': ['D', 'F', 'A', 'C'],
    'E_m7': ['E', 'G', 'B', 'D'],   'F_m7': ['F', 'Gs', 'C', 'Ds'],
    'G_m7': ['G', 'As', 'D', 'F'],  'A_m7': ['A', 'C', 'E', 'G'],
    'B_m7': ['B', 'D', 'Fs', 'A'],

    # * Diminished & Augmented
    'C_dim': ['C', 'Ds', 'Fs'], 'B_dim': ['B', 'D', 'F'],
    'G_aug': ['G', 'B', 'Ds'],  'C_aug': ['C', 'E', 'Gs'],
    'B_m7b5': ['B', 'D', 'F', 'A'] # Half-diminished
}

# ! Presets dict

presets = {
   "saxophone": [1.0, 0.8, 0.5, 0.3],
   "violin": [1.0, 0.6, 0.4, 0.2],
   "piano": [1.0, 0.4, 0.2, 0.1]
}




# ! HElPER FUNCTIONS:

# ! Melody maker, makes note in progression
def melody_maker(note_list, note_duration):
    
    sample_rate = 44100
    melody_complete = []

    for note in note_list:
        frequency = notes[note]

        time = np.linspace(0, note_duration, sample_rate * note_duration) # * stop, start, ensure theres enough samples till the stop

        wave = np.sin(2 * np.pi * frequency * time) # * generate the sound wave with this formula, 2pi makes it a full wave, frequency for pitch, time is where in the wave the sound is at the moment

        

        melody_complete.append(wave) # * add each wave, each representing a note to the empty list.

    full_wave = np.concatenate(melody_complete) 

    wave_int = np.int16(full_wave * 32767)

    # ? Save as WAV file
        # * BECAUSE FLASK CONFUSES the paths.
    current_dir = os.path.dirname(os.path.abspath(__file__)) # * find folder where main.py is.
    filename = os.path.join(current_dir, "melody.wav") # * add the name of the file to that path for it to be sved in the same folder of main.py/ choose its name

    wavfile.write(filename, sample_rate, wave_int) # * write(filename, rate, data) saves the audio data to a WAV file with the specified filename and sample rate.
    return(filename) # * return the file
    


# ! chord maker, makes chords. stacks notes on top of eachother
def chord_maker(chord, note_duration, instrument):
    note_list = chords[chord]
 
    sample_rate = 44100 # cd quality or so ive heard

    harmonics = presets[instrument]

    time = np.linspace(0, note_duration, sample_rate * note_duration) # * stop, start, ensure theres enough samples till the stop
    combined_wave = np.zeros(len(time)) # * start blank

    for note in note_list:
        frequency = notes[note] 
        wave = np.zeros(len(time)) # * start blank for this note

        for harmonic in range(len(harmonics)):
            volume = harmonics[harmonic]
            harmonic_id = harmonic + 1


            wave += volume * np.sin(2 * np.pi * frequency * harmonic_id * time) # * generate wave actual sound making a wave, difining pitch, tell u where in time u are in wave
        


        combined_wave += wave / (len(note_list) * len(harmonics)) # * add the value of each note to the combined note as a np list so it can be played as a chord and not sequence and divide
    

    return combined_wave

   #wavfile.write('8bitchords.wav', sample_rate, wave_convert) # * write(filename, rate, data) saves the audio data to a WAV file with the specified filename and sample rate.
    # print("8bitchords.wav") # * return the file a confirmation message
  




# ! Chord_progression, has chord maker as a helper function to generate it's chords, and uses the same logic as melody maker to create a sequence
def chord_progression(chord_list, chord_duration, instrument): 
    sample_rate = 44100 
    full_progression = [] # * create an empty list

    for chord in chord_list:
        returned = chord_maker(chord, chord_duration, instrument) # * for every chord call chord maker and make and let it do its job
        full_progression.append(returned) # * after every chord add it to the empty list

    full_wave = np.concatenate(full_progression) # * concatenate basically takes the three small arrays that are inside  full progression [array[chord1], array[chord2], array[chord3]] and fuses them into a big one, so it can be read by np yatayata
    wave_convert = np.int16(full_wave * 32767 ) # * convert the wave to 16 cuz it has been separated  // the 0.5 is to lower the volume quick fix
    
    
    # * BECAUSE FLASK CONFUSES the paths.
    current_dir = os.path.dirname(os.path.abspath(__file__)) # * find folder where main.py is.
    filename = os.path.join(current_dir, "chord_progression.wav") # * add the name of the file to that path for it to be sved in the same folder of main.py/ choose its name

    wavfile.write(filename, sample_rate, wave_convert) # * save the file in the same folder as main.py with the name chord_progression.wav
    return(filename) # return




# ! ROUTES

@app.route("/")
def home():
    return "homepage"


@app.route("/api/create_chord_progression/<chord_list>/<chord_duration>/<instrument>")

def route_chord_progression(chord_list, chord_duration, instrument):
    try:
        chords = chord_list.split(",") # this transforms "C_maj, G_min" into ["C_maj", "G_min"]
        chord_duration = int(chord_duration) # convert the string it recieves into an INT
    
        filename = chord_progression(chords, chord_duration, instrument)

        return send_file(filename, mimetype="audio/wav")
    except Exception as error:
        return jsonify ({"error": str(error)})


@app.route("/api/create_melody/<note_list>/<note_duration>")
def route_melody(note_list, note_duration):
    try:
        notes_sequence = note_list.split(",")
        note_duration = int(note_duration)

        filename = melody_maker(notes_sequence, note_duration)

        return send_file(filename, mimetype="audio/wav")
    except Exception as error:
        return jsonify ({"error": str(error)})







if __name__ == "__main__":
    app.run(debug=True, port=5000)



    