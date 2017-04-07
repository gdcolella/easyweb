from flask import Flask, jsonify, render_template, send_from_directory
import texting_service
import contacts
import services
from os import path


app = Flask(__name__)

pictures_dir = path.abspath(path.join(__file__, '../pictures'))

contact_prov = contacts.ContactProvider()
service_prov = services.MessagingSystem(contact_prov, [
    texting_service.TwilioService()
])

@app.route('/contact_photo/<file>')
def contact_photo(file):
    print(pictures_dir)
    return send_from_directory(pictures_dir, file)

@app.route('/view_messages')
def view_messages():
    return render_template('messages.html')

@app.route('/contacts')
def contacts():
    contacts = []
    streams = service_prov.get_messages()
    for stream in streams:
        contacts.append(stream.contact.to_dict())
    return jsonify({'contacts': contacts})

@app.route('/messages/<key>')
def messages(key):
    stream = service_prov.get_messages_with(key)
    res = []
    for message in stream.messages:
        res.append(message.to_json())
    return jsonify({'messages': res})



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
