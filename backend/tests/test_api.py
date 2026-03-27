import requests

response = requests.post(
    'http://localhost:5000/api/create_chord_progression',
    json={
        'chord_list': ['C_maj', 'D_min'],
        'chord_duration': 1
    }
)

# Save the audio file
with open('test_audio.wav', 'wb') as f:
    f.write(response.content)