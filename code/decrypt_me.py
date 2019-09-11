from flask import Flask, render_template, url_for, request
import os
import hashlib

app = Flask(__name__)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.route('/', methods=['POST', 'GET'])
def decrypt_me(name=None):
    if request.method == 'POST':
        hex_dig = None
        passwd_input = request.form['passwd_input']
        if request.form['hash_input'] == 'MD5':
            hash_object = hashlib.md5(str(passwd_input).encode('utf-8'))
            hex_dig = hash_object.hexdigest()
            print(hex_dig)
        elif request.form['hash_input'] == 'SHA1':
            hash_object = hashlib.sha1(str(passwd_input).encode('utf-8'))
            hex_dig = hash_object.hexdigest()
            print(hex_dig)
        elif request.form['hash_input'] == 'SHA224':
            hash_object = hashlib.sha224(str(passwd_input).encode('utf-8'))
            hex_dig = hash_object.hexdigest()
            print(hex_dig)
        elif request.form['hash_input'] == 'SHA256':
            hash_object = hashlib.sha256(str(passwd_input).encode('utf-8'))
            hex_dig = hash_object.hexdigest()
            print(hex_dig)
        elif request.form['hash_input'] == 'SHA384':
            hash_object = hashlib.sha384(str(passwd_input).encode('utf-8'))
            hex_dig = hash_object.hexdigest()
            print(hex_dig)
        elif request.form['hash_input'] == 'SHA512':
            hash_object = hashlib.sha512(str(passwd_input).encode('utf-8'))
            hex_dig = hash_object.hexdigest()
            print(hex_dig)
        else:
            return render_template('index.html', name=name, result='Dont cheat!')

        if hex_dig == '21232f297a57a5a743894a0e4a801fc3':
            result_msg = 'Good job!'
        else:
            result_msg = 'Failed, try again'
        return render_template('index.html', name=name, entered_hash=hex_dig ,result=result_msg)

    else:
        return render_template('index.html', name=name)

if __name__ == '__main__':
    app.run()
