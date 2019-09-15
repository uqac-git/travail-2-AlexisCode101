from flask import Flask, render_template, url_for, request
from OpenSSL import SSL, crypto
import os
import hashlib

secret_hash = '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'

# cert = crypto.load_certificate(
#     crypto.FILETYPE_PEM,
#     open('SSL.crt').read()
# )
#
# key = crypto.load_privatekey(
#     crypto.FILETYPE_PEM,
#     open('SSL.key').read()
# )
#
# context = SSL.Context(SSL.SSLv23_METHOD)
# context.use_certificate(cert)
# context.use_privatekey(key)

app = Flask(__name__)

# For CSS update
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

@app.route('/', methods=['GET'])
def form(name=None):
    return render_template('index.html', bool_answer="Bravo!")

@app.route('/', methods=['POST'])
def decrypt_me(name=None):
    hex_dig = None
    passwd_input = request.form['passwd_input']
    hash_input = request.form['hash_input']
    if hash_input == 'MD5':
        hash_object = hashlib.md5(str(passwd_input).encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        print(hex_dig)
    elif hash_input == 'SHA1':
        hash_object = hashlib.sha1(str(passwd_input).encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        print(hex_dig)
    elif hash_input == 'SHA224':
        hash_object = hashlib.sha224(str(passwd_input).encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        print(hex_dig)
    elif hash_input == 'SHA256':
        hash_object = hashlib.sha256(str(passwd_input).encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        print(hex_dig)
    elif hash_input == 'SHA384':
        hash_object = hashlib.sha384(str(passwd_input).encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        print(hex_dig)
    elif hash_input == 'SHA512':
        hash_object = hashlib.sha512(str(passwd_input).encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        print(hex_dig)
    else:
        return render_template('answer.html', result='Dont cheat!')

    if hex_dig == secret_hash:
        result_msg = 'Bravo vous avez trouvé!'
    else:
        result_msg = 'Erreur, réessayez'

    return render_template('answer.html', entered_hash=hex_dig, entered_hash_type=hash_input, result=result_msg)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404_error.html", page_name=request.path.split('/')[1])

if __name__ == '__main__':
    context = ('SSL.crt', 'SSL.key')
    app.run(debug=True, port=5000, ssl_context=context)


