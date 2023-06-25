import wave

path = "C:/Users/User/Desktop/kt_coaching_project/kt_05_18/kt_coaching_base/rpg/static/voice/19_0.wav"

def check_wav_file(file_path):
    try:
        # This will raise an error if the file is not valid
        with wave.open(file_path, 'rb') as wav_file:
            print("The file was read successfully")
    except Exception as e:
        print(f"Error reading file: {e}")

check_wav_file(path)  # replace with your file path