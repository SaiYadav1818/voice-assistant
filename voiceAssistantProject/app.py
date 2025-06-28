from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import subprocess

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Dummy user data
users = {
    'user1': 'password1',
    'user2': 'password2'
}

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid Credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/index')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def command():
    if 'username' not in session:
        return jsonify({'response': 'Please log in first.'})

    command = request.json.get('command', '').lower()
    response = ''
    if 'open instagram' in command:
        subprocess.Popen(['start', 'https://www.instagram.com'], shell=True)
        response = 'Opening Instagram'
    elif 'open youtube' in command:
        subprocess.Popen(['start', 'https://www.youtube.com'], shell=True)
        response = 'Opening YouTube'
    elif 'open windows store' in command:
        subprocess.Popen(['start', 'ms-windows-store://home'], shell=True)
        response = 'Opening Windows Store'
    elif 'open notepad' in command:
        subprocess.Popen(['notepad.exe'])
        response = 'Opening Notepad'
    elif 'open word' in command:
        subprocess.Popen(['start', 'winword'], shell=True)
        response = 'Opening Word'
    elif 'open chrome' in command:
        subprocess.Popen(['start', 'chrome'], shell=True)
        response = 'Opening Chrome'
    elif 'open whatsapp' in command:
        subprocess.Popen(['start', 'https://web.whatsapp.com'], shell=True)
        response = 'Opening WhatsApp'
    elif 'create a folder' in command:
        import os
        folder_name = "NewFolder"
        try:
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
                response = f'Folder "{folder_name}" created successfully.'
            else:
                response = f'Folder "{folder_name}" already exists.'
        except Exception as e:
            response = f'Failed to create folder: {str(e)}'
    else:
        response = 'I am sorry, I cannot do that yet.'

    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(debug=True, port=5001)



  
