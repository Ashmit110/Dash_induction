import socket
import json
import time
from huggingface_hub import InferenceClient

def handle_client(client_socket, client_address, api_key):
    prompts = client_socket.recv(1024).decode()
    prompts = json.loads(prompts)
    print(prompts)
    
    responses = []
    client = InferenceClient(
        "google/gemma-1.1-2b-it",
        token=api_key,
    )
    
    for input_text in prompts:
        time_sent = int(time.time())
        response_content = ""
        
        for message in client.chat_completion(
            messages=[{"role": "user", "content": input_text}],
            max_tokens=500,
            stream=True,
        ):
            response_content += message.choices[0].delta.content
            
        time_recvd = int(time.time())
        
        responses.append({
            "Prompt": input_text,
            "Message": response_content,
            "TimeSent": time_sent,
            "TimeRecvd": time_recvd,
            "Source": "gemma-1.1-2b"
        })
    
    client_socket.send(json.dumps(responses).encode())
    client_socket.close()

def main(api_key, server_ip="127.0.0.1", server_port=65432):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen(5)
    print(f"[*] Listening on {server_ip}:{server_port}")
    
    while True:
        client_socket, client_address = server.accept()
        print(f"[*] Accepted connection from {client_address}")
        handle_client(client_socket, client_address, api_key)

if __name__ == "__main__":
    api_key = 'your_api_key_here'
    main(api_key)
