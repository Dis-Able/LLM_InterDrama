import requests
from urllib.parse import urljoin
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def upload_file(url, token, file_path):
    url = urljoin(url,'/api/v1/files/')
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }
    files = {'file': open(file_path, 'rb')}
    response = requests.post(url, headers=headers, files=files)
    return response.json()

def add_file_to_knowledge(url,token, knowledge_id, file_id):
    url = urljoin(url,f'/api/v1/knowledge/{knowledge_id}/file/add')
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    data = {'file_id': file_id}
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def chat_with_file(url,token, model, query, file_id):
    url = urljoin(url,'/api/chat/completions')
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': model,
        'messages': [{'role': 'user', 'content': query}],
        'files': [{'type': 'file', 'id': file_id}]
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def chat_with_collection(url,token, model, query, collection_id):
    url = urljoin(url,'/api/chat/completions')
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': model,
        'messages': [{'role': 'user', 'content': query}],
        'files': [{'type': 'collection', 'id': collection_id}]
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

#def chat(url, model, system_prompt, query):
def chat(url, token, model, system_prompt, query):
    url = urljoin(url, '/api/chat/completions')
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': model,
        'messages': [
            {
                'role': 'system',
                'content': system_prompt
            },
            {
                'role': 'user',
                'content': query
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()


def init_chat(system_prompt):

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]
    return messages

def continue_chat(url, token, model, messages, user_input):


    messages.append({
        "role": "user",
        "content": user_input
    })
    

    url = urljoin(url, '/api/chat/completions')
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': model,
        'messages': messages
    }
    

    response = requests.post(url, headers=headers, json=payload)
    response_json = response.json()
    

    if 'choices' in response_json and len(response_json['choices']) > 0:
        assistant_response = response_json['choices'][0]['message']['content']
        messages.append({
            "role": "assistant",
            "content": assistant_response
        })
    
    return messages, response_json


