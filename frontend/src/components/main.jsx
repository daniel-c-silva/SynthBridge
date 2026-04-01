import { useState } from "react";


function Main() {
    

    // * Chords function vars
    const[chords, setChords] = useState("") //  * set chords for chords
    const[duration, setDuration] = useState("") // * set duration for duration
    // * Melody function vars
    const[notes, setNotes] = useState("")
    const[noteDuration, setNoteDuration] = useState("")
    // * instrument function
    const[instrument, setInstrument] = useState("")
    // * instrument function melody
    const[instrumentMelody, setInstrumentMelody] = useState("")

        // * Chords function 
        function handleChords() {
            const url = `${process.env.REACT_APP_API_URL}/api/create_chord_progression/${chords}/${duration}/${instrument}`;
            
            fetch(url)
             .then(response => response.blob()) // * when we get the response convert to blob (audio data in binary)
             .then(blob => { // * once converted run this: 
                  
                 const audioUrl = window.URL.createObjectURL(blob); // * converts the blob into a playble url the browser gets
                 const audio = new Audio(audioUrl) // * creates an audio player objet kinda like <audio> in html
                 audio.play(); // * plays it.
                 })
            }
        
        function handleMelody(){
            const url = `${process.env.REACT_APP_API_URL}/api/create_melody/${notes}/${noteDuration}/${instrumentMelody}`;

            fetch(url)
             .then(response => response.blob())
             .then(blob => {

                 const audioUrl = window.URL.createObjectURL(blob); // * converts the blob into a playble url the browser gets
                 const audio = new Audio(audioUrl) // * creates an audio player objet kinda like <audio> in html
                 audio.play(); // * plays it. 
             })





        }
        



  return (
    <div>

      <div className="instructions">
        <h2>Instructions:</h2>
        <p>To generate a chord progression, enter the chords in the first input field using the format: "ChordName_ChordType" (ex, C_maj for C major, A_min for A minor, B_dim for B diminished). Separatechords with commas. In the second input field, specify the duration of each chord in beats (ex, 1 for one beat, 4 for four beats). Then click the "Send" button to generate and play the chord progression.</p>
        <p>To generate a melody, enter the notes in the first input field using the format: "NoteName" (ex, A, B, D, Cs). Separate notes with commas. In the second input field, specify the duration of each note in beats (ex, 1 for one beat, 4 for four beats). Then click the "Send" button to generate and play the melody.</p>
        <p>valid chords: C_maj, C_min, D_maj, D_min, E_maj, E_min, F_maj, F_min, G_maj, G_min, A_maj, A_min, B_maj, B_min</p>
        <p>valid notes: A, As, B, C, Cs, D, Ds, E, F, Fs, G, Gs</p>
       
      </div>

      <div className="form-container">
        <button className="Button" id="send-button" onClick={handleChords}> Send</button>
        
        <input
         className="Input-field"
         id="instrument-input"
         type="text"
         placeholder="instrument, ex: violin, piano, saxophone"
         value={instrument}
         onChange={(userTyped) => setInstrument(userTyped.target.value)}
        />
      

        <input 
         className="Input-field"
         id="chords-input"
         type="text"
         placeholder="Chords, example: C_maj,A_min,B_dim"
         value={chords}
         onChange={(userTyped) => setChords(userTyped.target.value)}/>


        <input 
        className="Input-field"
        id="duration-input"
        type="text" 
        placeholder="Chord duration, example: 1 or 4"
        value={duration}
        onChange={(userTyped) => setDuration(userTyped.target.value)}/>
      </div>

      <div className="form-container-melody">
        <button className="Button" id="send-button" onClick={handleMelody}> Send</button>

        <input
          className="Input-field"
          id="instrument-input"   
          type="text"
          placeholder="instrument, ex: violin, piano, saxophone"
          value={instrumentMelody}
          onChange={(userTyped) => setInstrumentMelody(userTyped.target.value)} 
        />

        <input 
         className="Input-field"
         id="chords-input"
         type="text"
         placeholder="Notes, ex: A,B,D,Cs"
         value={notes}
         onChange={(userTyped) => setNotes(userTyped.target.value)}/>


        <input 
        className="Input-field"
        id="duration-input"
        type="text" 
        placeholder="Note duration, example: 1 or 4"
        value={noteDuration}
        onChange={(userTyped) => setNoteDuration(userTyped.target.value)}/>
      </div>


    </div>
  );
}

export default Main;
