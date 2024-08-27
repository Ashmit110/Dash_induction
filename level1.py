import json
import time
from huggingface_hub import InferenceClient

def read_inputs(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def write_json(responses,outfile_path):
    with open(outfile_path, "w") as outfile:
        json.dump(responses, outfile, indent=4)

    print(f"Responses saved to {outfile_path}")
    
def main(api_key,text_file_path,output_file):
    prompts=read_inputs(text_file_path)
    responses = []
    client = InferenceClient(
    "google/gemma-1.1-2b-it",
    token=api_key,
    )
    for input_text in prompts:
        time_sent=int(time.time())
        
        
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
        
    write_json(responses,output_file)
    

if __name__ == "__main__":
    text_file = r'level_1.txt'
    api_key='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'
    output_file = 'client_responses.json'
    main(api_key,text_file, output_file)
