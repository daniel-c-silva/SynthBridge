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
    "saxophone": {
        "harmonics": [1.0, 0.7, 0.5, 0.4, 0.3, 0.2, 0.1],
        "attack": 0.05,    # 50ms
        "decay": 0.3       # 300ms
    },
    "piano": {
        "harmonics": [1.0, 0.4, 0.15, 0.05, 0.02],
        "attack": 0.01,    # 10ms
        "decay": 0.8       # 800ms
    },
    "violin": {
        "harmonics": [1.0, 0.7, 0.8, 0.6, 0.5, 0.4, 0.3, 0.2],
        "attack": 0.2,     # 200ms (slow bow)
        "decay": 0.05       # no decay (sustains)
    }
}


# ! HElPER FUNCTIONS:

# ! Melody maker, makes note in progression
def melody_maker(note_list, note_duration):
    
    sample_rate = 44100
    melody_complete = [] # * create an empty list to hold the notes waves

    for note in note_list: 
        frequency = notes[note]

        time = np.linspace(0, note_duration, sample_rate * note_duration) # * stop, start, ensure theres enough samples till the stop

        wave = np.sin(2 * np.pi * frequency * time) # * generate the sound wave with this formula, 2pi makes it a full wave, frequency for pitch, time is where in the wave the sound is at the moment

        melody_complete.append(wave) # * add each wave, each representing a note to the empty list.

    full_wave = np.concatenate(melody_complete)  

    # ! Normalizing melody to prevent clipping
    if np.max(np.abs(full_wave)) > 0: # * if the maximum value of the wave is above 0.
        full_wave = full_wave / np.max(np.abs(full_wave)) # * divide the wave by the max value to scale down 
    # !

    wave_int = np.int16(full_wave * 32767)

    # ? Save as WAV file
        # * BECAUSE FLASK CONFUSES the paths.
    current_dir = os.path.dirname(os.path.abspath(__file__)) # * find folder where main.py is.
    filename = os.path.join(current_dir, "melody.wav") # * add the name of the file to that path for it to be sved in the same folder of main.py/ choose its name

    wavfile.write(filename, sample_rate, wave_int) # * write(filename, rate, data) saves the audio data to a WAV file with the specified filename and sample rate.
    return(filename) # * return the file
    


# ! chord maker, makes chords. stacks notes on top of eachother
def chord_maker(chord, note_duration, instrument):
    note_list = chords[chord] # * get the list of notes that make the chord
 
    sample_rate = 44100 # cd quality or so ive heard

    harmonics_data = presets[instrument] # * get the preset data for the instrument, dict with harmonic,attack and decay.

    harmonics = harmonics_data["harmonics"]  # * Extract just the harmonics list

    attack = harmonics_data["attack"]  # ! Get attack time
    
    decay = harmonics_data["decay"]    # ! Get decay time

    time = np.linspace(0, note_duration, int(sample_rate * note_duration), endpoint=False) # * start, stop, ensure theres enough samples till the stop

    combined_wave = np.zeros(len(time)) # * create an array of zeros with the same lenght as time. (accumulates all notes (need one))

    for note in note_list: 
        frequency = notes[note] # * get the frequency for each note in chord.
        wave = np.zeros(len(time)) # * create an array of zeros with the same lenght as time.  holds one note at a time (need a fresh one for each note)

        for harmonic in range(len(harmonics)): # * fore ech index harmonic of that frequence(note). 
            volume = harmonics[harmonic] # * volume of the value of the index of that harmonic list.
            harmonic_id = harmonic + 1 # * harmonics start at 1 not 0 because the first harmonic is the main note.

            wave += volume * np.sin(2 * np.pi * frequency * harmonic_id * time) # * generate wave actual sound making a wave, difining pitch, tell u where in time u are in wave


                # ! APPLY ENVELOPE (Attack + Decay)
        # * Create attack (fade in)
        attack_samples = int(attack * sample_rate) # * calculate how many samples the atack should last based on attack time and sample rate
        attack_envelope = np.linspace(0, 1, attack_samples) # * use linespace to create a linear envelope that goes from 0 to 1 in the number of samples the attack should last. basically creates a fade in effect 
        
        # * Create decay (fade out)
        decay_samples = int(decay * sample_rate) # * calculate how many samples the decay should last based on decay time and sample rate
        decay_envelope = np.linspace(1, 0, decay_samples) # * use linespace to create a linear envelope that goes from 1 to 0 in the number of samples the decay should last. basically creates a fade out effect
        
        # * Add them to the wave
        wave[:attack_samples] *= attack_envelope # * wave[:attack_samples] = the first 2,205 samples of the wave multiplied by the attack envelope, this in short applies the fade in.
        wave[-decay_samples:] *= decay_envelope    # * wave[-decay_samples:] = the last 2,205 samples of the wave multiplied by the decay envelope, this in short applies the fade out
        
        combined_wave += wave # * add the value of each note to the combined note as a np list so it can be played as a chord and not sequence
    
    # ! REMOVED the division here because it was hiding the harmonics
    return combined_wave


# ! Chord_progression, has chord maker as a helper function to generate it's chords, and uses the same logic as melody maker to create a sequence
def chord_progression(chord_list, chord_duration, instrument): 
    sample_rate = 44100 
    full_progression = [] # * create an empty list

    for chord in chord_list:
        returned = chord_maker(chord, chord_duration, instrument) # * for every chord call chord maker and make and let it do its job
        full_progression.append(returned) # * after every chord add it to the empty list

    full_wave = np.concatenate(full_progression) # * concatenate basically takes the three small arrays that are inside  full progression [array[chord1], array[chord2], array[chord3]] and fuses them into a big one, so it can be read by np yatayata

    # ! NORMALIZATION: Scalng the big wave so it doesn't clip/distort
    max_val = np.max(np.abs(full_wave)) # * find the maximum value in the wave. if its above 0 normalize np.abs returns the absolute value np.max returns the maximum value
    if max_val > 0: # * if its above 0
        full_wave = full_wave / max_val # * divide to normalize.
    # !

    

    wave_convert = np.int16(full_wave * 32767 * 0.8) # * convert the wave to 16 cuz it has been separated  // the 0.8 is to keep the volume safe
    
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
        chords_split = chord_list.split(",") # * this transforms "C_maj, G_min" into ["C_maj", "G_min"]
        chord_duration = int(chord_duration) # * convert the string it recieves into an INT
    
        filename = chord_progression(chords_split, chord_duration, instrument) # * get whats returned from chord progression which is the file name and save it in a var

        return send_file(filename, mimetype="audio/wav") # * send the file to the frontend with the correct mimetype
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