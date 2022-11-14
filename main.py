from flask import Flask
from flask import render_template
from flask import request
import time
import requests

# Init first message
current_messages = {
		"users": ["Samantha", "You"],
		"chats": [{
			"from": 'Samantha',
			"msg": 'Hola',
			"action": ''
		}]
	}
current_messages['chats'][0]['time'] = str(round(time.time()*500))
print(str(round(time.time()*500)), flush=True)
API_TOKEN = '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' 
# Define query function
def query(payload, model_id, api_token):
    headers = {"Authorization": f"Bearer {api_token}"}
    API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

## Create app

app = Flask(__name__,template_folder='templates')

@app.route('/', methods=['GET','POST'])
def page():
    global current_messages
    global API_TOKEN
    if request.method == 'GET':
        return render_template('chat.html', chat = current_messages)
    if request.method == 'POST':
        current_messages = request.json
        msg = current_messages['chats'][-1]['msg']
        responses = query(msg,'flair/ner-spanish-large',API_TOKEN)['conversation']['generated_responses']
        response = responses[-1]
        current_messages['chats'].append({'from': 'Samantha', 'msg': response, 'time': str(round(time.time()*500)), 'action': ''})
        return current_messages
    

if __name__ == '__main__':
  app.run(debug=True)
  
