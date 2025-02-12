from flask import Flask, render_template, request
from flask import send_from_directory
import speech_recognition as sr
from googletrans import Translator
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

rec = sr.Recognizer()
translator = Translator()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/uploads', methods=['POST'])
def uploads():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    if 'file' not in request.files:
        return render_template('index.html', error='No file part')

    file = request.files['file']

    if file.filename == '':
        return render_template('index.html', error='No selected file')

    if file:
        # Save the file to the uploads folder
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(audio_path)

        # Log the audio file path on the pycharm terminal
        print(f"Audio file captured: {audio_path}")

        try:
            # Perform speech-to-text conversion and transliteration
            with sr.AudioFile(audio_path) as source:
                audio_data = rec.listen(source)
                text2 = rec.recognize_google(audio_data, language='mr-IN')
                text3 = rec.recognize_google(audio_data)
                # text = rec.recognize_google(audio_data)

            # Translate and transliterate the text (did not work)
            # translation = translator.translate(text, dest='en').text
            # transliteration = translator.translate(text, dest='en', src='mr').pronunciation

            # Render the result on the webpage
            return render_template('result.html', filename=file.filename, text_marathi=text2, text_english=text3, audio_path=audio_path)

        except sr.UnknownValueError:
            return render_template('index.html', error='Could not understand the audio file')
        except sr.RequestError as e:
            return render_template('index.html', error=f'Error with the speech recognition service: {e}')
        except Exception as e:
            return render_template('index.html', error=f'Error processing audio file: {e}')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
