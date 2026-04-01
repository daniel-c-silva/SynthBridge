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
    <p><strong>Chord Progression:</strong> Enter chords in the first field using the format "Note_Type" (e.g., <strong>C_maj7</strong>). Separate with commas. Choose an instrument and set the duration (seconds per chord) before clicking "Send."</p>
    
    <p><strong>Melody:</strong> Enter notes in the first field (e.g., <strong>A, Cs, E</strong>). Separate with commas. Pick your instrument and set the duration (seconds per note) to generate your sequence.</p>

    <h3>Valid Instruments:</h3>
    <p>saxophone, piano, violin, flute, trumpet, cello, electric_bass, clarinet, church_organ</p>

    <h3>Valid Notes:</h3>
    <p>A, As, B, C, Cs, D, Ds, E, F, Fs, G, Gs</p>

    <h3>Valid Chord Types:</h3>
    <ul>
        <li><strong>Triads:</strong> _maj, _min, _dim, _aug</li>
        <li><strong>7th Chords:</strong> 7 (Dominant), _maj7, _m7, _m7b5</li>
    </ul>
    
    <p><em>Tip: For a smooth Sax sound, try a duration of 2 and use "C_maj7, A_m7, D_m7, G7"!</em></p>

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
