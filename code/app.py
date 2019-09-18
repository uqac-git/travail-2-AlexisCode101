from flask import Flask, render_template, request
import hashlib
from ssl import SSLContext, PROTOCOL_SSLv23

secret_hash = '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'

app = Flask(__name__)

# If GET, display normal page
@app.route('/', methods=['GET'])
def form(name=None):
    return render_template('index.html')

# If POST, an answer has been submit
@app.route('/', methods=['POST'])
def decrypt_me(name=None):
    hex_dig = None
    passwd_input = request.form['passwd_input']
    hash_input = request.form['hash_input']

    # Use appropriate Hash function
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

    # If not in previous list, hes cheating
    else:
        return render_template('answer.html', result='Dont cheat!')

    #  Found secret hash
    if hex_dig == secret_hash:
        result_msg = 'Bravo vous avez trouvé!'
    # Didnt find secret hash
    else:
        result_msg = 'Erreur, réessayez'

    return render_template('answer.html', entered_hash=hex_dig, entered_hash_type=hash_input, result=result_msg)

# If page not found, display this html
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404_error.html", page_name=request.path.split('/')[1])

# When called, run the server
if __name__ == '__main__':
    context = SSLContext(PROTOCOL_SSLv23)
    context.load_cert_chain('./SSL.crt', './SSL.key')
    app.run(debug=True, port=5000, ssl_context=context)


