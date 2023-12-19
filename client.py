import socket
import re
from policy_admin import *

file_path = "policy.json"
json_data = load_json_from_file(file_path)

def extract_numbers(s):
    pattern = r"[-+]?\d*\.\d+|\d+"  # Regular expression pattern for floating-point numbers
    matches = re.findall(pattern, s)
    if len(matches) >= 2:
        return [float(match) for match in matches[:2]]
    else:
        return None

def start_client():
    host = "127.0.0.1"
    port = 8888

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Start by typing in 'hello' to let server know communication is open")
    while True:
        user_input = input("-> ")
        if user_input.lower() == "exit":
            break
        client_socket.send(user_input.encode("utf-8"))
        response = client_socket.recv(1024).decode("utf-8")
        print("Server response:", response)
        if "fixed" in response:
            print("Look up if response exists in policy.json")
            action = extract_numbers(response)
            if str(action[0]) in json_data:
                print("action exists:", json_data[str(action[0])])
        if "Increase" in response or "Decrease" in response:
            actions = extract_numbers(response)
            print("actions from string:",actions)  

            new_action = actions[1]
            old_action = actions[0]

            if "Increase" in response:
                new_action = float(new_action)/100 + float(old_action)
            else:
                new_action = float(new_action)/100 - float(old_action)
            new_action = str(new_action)
            print("Client response: Changed probability of action to", new_action)
            client_socket.send(new_action.encode("utf-8"))
            response = client_socket.recv(1024).decode("utf-8")
            print("Server response:", response)
        # Need code to store policy when "best" received from server.
        if "best" in response:
            print("Add to policy")
            actions = extract_numbers(response)
            print("actions from string:",actions)  
            if str(actions[1]) in json_data:
                print("action exists, update it") # This maybe redundant, as you already would have the correct entry
                update_item(json_data, str(actions[1]), actions[0])
            else:
                print("action does not exist, so create it")
                create_item(json_data,str(actions[1]), actions[0])
                save_json_to_file(json_data, file_path)
            
            client_socket.send("wait".encode("utf-8"))
            response = client_socket.recv(1024).decode("utf-8")
            print("Server response:", response)
            if "fixed" in response:
                print("Look up if response exists in policy.json")
                action = extract_numbers(response)
                if str(action[0]) in json_data:
                    print("action exists:", json_data[str(action[0])])

    client_socket.close()

if __name__ == "__main__":
    start_client()
