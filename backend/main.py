import numpy as np
from scipy.io import wavfile
from flask import Flask, request, jsonify, send_file
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

# ! Dictionaries
# ! Updated Dictionaries (Using 's' for sharps)
notes = {
    'C': 261.63,  'Cs': 277.18,
    'D': 293.66,  'Ds': 311.13,
    'E': 329.63,
    'F': 349.23,  'Fs': 369.99,
    'G': 392.00,  'Gs': 415.30,
    'A': 440.00,  'As': 466.16,
    'B': 493.88,
}

chords = {
    # * triads
    'C_maj': ['C', 'E', 'G'],    'C_min': ['C', 'Ds', 'G'],
    'D_maj': ['D', 'Fs', 'A'],   'D_min': ['D', 'F', 'A'],
    'E_maj': ['E', 'Gs', 'B'],   'E_min': ['E', 'G', 'B'],
    'F_maj': ['F', 'A', 'C'],    'F_min': ['F', 'Gs', 'C'],
    'G_maj': ['G', 'B', 'D'],    'G_min': ['G', 'As', 'D'],
    'A_maj': ['A', 'Cs', 'E'],   'A_min': ['A', 'C', 'E'],
    'B_maj': ['B', 'Ds', 'Fs'],  'B_min': ['B', 'D', 'F'],
    
    # * (bossa nova)
    'C_maj7': ['C', 'E', 'G', 'B'],
    'A_m7':   ['A', 'C', 'E', 'G'],
    'G_7':    ['G', 'B', 'D', 'F'], 
    
    # * diminished
    'B_dim': ['B', 'D', 'F'],
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
  



# ! Chord_progression, has chord maker as a helper function to generate it's chords, and uses the same logic as melody maker to create a sequence
def chord_progression(chord_list, chord_duration): 
    sample_rate = 44100 
    full_progression = [] # * create an empty list

    for chord in chord_list:
        returned = chord_maker(chord, chord_duration) # * for every chord call chord maker and make and let it do its job
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


@app.route("/api/create_chord_progression/<chord_list>/<chord_duration>")

def route_chord_progression(chord_list, chord_duration):
    try:
        chords = chord_list.split(",") # this transforms "C_maj, G_min" into ["C_maj", "G_min"]
        chord_duration = int(chord_duration) # convert the string it recieves into an INT
    
        filename = chord_progression(chords, chord_duration)

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



    