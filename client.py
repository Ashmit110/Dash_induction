import socket
import json

def read_inputs(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def write_json(responses, outfile_path):
    with open(outfile_path, "w") as outfile:
        json.dump(responses, outfile, indent=4)
    print(f"Responses saved to {outfile_path}")

def main(server_ip="127.0.0.1", server_port=65432, text_file_path="level_1.txt", output_file="client_responses.json"):
    prompts = read_inputs(text_file_path)
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))
    
    client.send(json.dumps(prompts).encode())
    
    response_data = client.recv(4096).decode()
    responses = json.loads(response_data)
    
    write_json(responses, output_file)
    client.close()

if __name__ == "__main__":
    main()
