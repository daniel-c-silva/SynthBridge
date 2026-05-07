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
  
  <div style={{display: 'flex', gap: '1rem', marginBottom: '1rem'}}>
    <div style={{flex: 1, background: '#f5f5f5', borderRadius: '8px', padding: '1rem'}}>
      <h3>Chord Progression</h3>
      <p>Stack notes simultaneously to build harmony across a sequence of chords.</p>
    </div>
    <div style={{flex: 1, background: '#f5f5f5', borderRadius: '8px', padding: '1rem'}}>
      <h3>Melody</h3>
      <p>Play individual notes one after another to form a melodic line.</p>
    </div>
  </div>

  <h4>Instruments</h4>
  <div style={{display: 'flex', flexWrap: 'wrap', gap: '6px', marginBottom: '1rem'}}>
    {['saxophone','piano','violin','flute','trumpet','cello','electric_bass','clarinet','church_organ'].map(i => (
      <code key={i} style={{background: '#eee', borderRadius: '4px', padding: '2px 8px'}}>{i}</code>
    ))}
  </div>

  <h4>Notes</h4>
  <div style={{display: 'flex', flexWrap: 'wrap', gap: '6px', marginBottom: '0.5rem'}}>
    {['A','As','B','C','Cs','D','Ds','E','F','Fs','G','Gs'].map(n => (
      <code key={n} style={{background: '#eee', borderRadius: '4px', padding: '2px 8px'}}>{n}</code>
    ))}
  </div>
  <p style={{fontSize: '13px', color: '#666'}}>s = sharp (e.g. Cs = C♯, Fs = F♯)</p>

  <h4>Chord types — format: Note_Type</h4>
  <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '6px', marginBottom: '1rem'}}>
    {[['_maj','major triad'],['_min','minor triad'],['_dim','diminished'],['_aug','augmented'],
      ['7','dominant 7th'],['_maj7','major 7th'],['_m7','minor 7th'],['_m7b5','half-diminished']].map(([suffix, label]) => (
      <div key={suffix}><code style={{background: '#eee', borderRadius: '4px', padding: '2px 8px'}}>{suffix}</code> {label}</div>
    ))}
  </div>

  <h4>Duration</h4>
  <p>Whole number in seconds per note or chord — e.g. <code>1</code>, <code>2</code>, <code>4</code></p>

  <div style={{background: '#e8f0fe', borderRadius: '8px', padding: '0.75rem 1rem', marginTop: '1rem'}}>
    💡 Try: instrument <code>saxophone</code>, duration <code>2</code>, chords <code>C_maj7,A_m7,D_m7,G7</code>
  </div>
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
