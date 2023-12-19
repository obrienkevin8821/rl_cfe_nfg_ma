import socket
import threading

strategy = 0 # 0 for client fixed, 1 for client mixed
ports = []
actions = [0, 0] # just contain two values - 1 for first client - with mixed strategy, and 1 for second client with fixed strategy
first_msg = 0
second_msg = 0
client_socket1 = 0
client_socket2 = 0
resp1 = "initial"
resp2 = "initial"
row_values = []
col_values = []
incr_values = []
best_response = 0

# Stag
# payoffs = [
#     [[5, 5], [0, 2]],
#     [[2, 0], [1, 1]]
# ]


# prisoner dilemma
payoffs = [
    [[2, 2], [0, 3]],
    [[3, 0], [1, 1]]
]

def best_action_responses():

    incr_inner = 0.1
    incr_outer = incr_inner
    count = 0
    row_values = []
    col_values = []
    incr_values = []

    while count < 2: # two players

        action_outer = 0

        while action_outer <= 1:
            if count == 0:
                incr_values.append(action_outer)
            action_inner = 0
            best_payoff = 0
            best_action_value = 0

            while action_inner <= 1:
                if count == 0: # row player fixed
                    values = calc_values(action_outer, action_inner, payoffs)
                    value = values[9] # for column player total payoff at values[9]
                else: # column player fixed
                    values = calc_values(action_inner, action_outer, payoffs)
                    value = values[6] # for row player total payoff at values[6]                
                if value > best_payoff:
                    best_payoff = value
                    best_action_value = action_inner
                action_inner += incr_inner

            if count == 0:
                col_values.append(best_action_value)
            else:
                row_values.append(best_action_value)

            action_outer += incr_outer

        count += 1

    return row_values, col_values, incr_values

# code to test best_action_responses
# row_values, col_values, incr_values = best_action_responses()

def calc_values(x_prob, y_prob, rewards):
    # array to store all values - probabilities, payoffs and incentives to change
    values = []
    # calculate and set probability values
    x_prob_first = x_prob # e.g. stag value for player 1 - row
    x_prob_second = y_prob # e.g. stag value for player 2 - column
    y_prob_first = 1 - x_prob # e.g. hare value for player 1 - row
    y_prob_second = 1 - y_prob # e.g. hare value for player 2 - column

    # assign and calculate reward/payoff values
    row_e_x = (rewards[0][0][0] * x_prob_second) + (rewards[0][1][0] * y_prob_second) 
    row_e_y = (rewards[1][0][0] * x_prob_second) + (rewards[1][1][0] * y_prob_second) 
    row_e_total = (row_e_x * x_prob_first) + (row_e_y * y_prob_first)
    col_e_x = (rewards[0][0][1] * x_prob_first) + (rewards[1][0][1] * y_prob_first)
    col_e_y = (rewards[0][1][1] * x_prob_first) + (rewards[1][1][1] * y_prob_first)
    col_e_total = (col_e_x * x_prob_second) + (col_e_y * y_prob_second)

    # assign and calculate incentive values for changing probabilities
    # These change variables, if set to 0, then no incentive to 
    # change these values - equilibrium achieved
    x_first_change = max(0, row_e_x - row_e_total)
    y_first_change = max(0, row_e_y - row_e_total)
    x_second_change = max(0, col_e_x - col_e_total)
    y_second_change = max(0, col_e_y - col_e_total)

    # get sum of payoff and sum of incentives to change
    sum_change = x_first_change + y_first_change + x_second_change + y_second_change 
    sum_payoff = row_e_total + col_e_total
    sum_second_change = x_second_change + y_second_change # get sum of incentives to change for second player(column) only, useful for advising col player

    # add values to array and return this array from the function
    values.extend([x_prob_first, x_prob_second, y_prob_first, y_prob_second])
    values.extend([row_e_x, row_e_y, row_e_total, col_e_x, col_e_y, col_e_total])
    values.extend([x_first_change, y_first_change, x_second_change, y_second_change])
    values.extend([sum_change, sum_payoff, sum_second_change])

    return values

def handle_client(client_socket, addr):
    
    global first_msg, second_msg, client_socket1, client_socket2, best_response
    global row_values, col_values, incr_values
    
    while True:
        try:
            request = client_socket.recv(1024).decode("utf-8")
            if not request:
                break

            # second responses to clients. Have it here as second_msg == 1 after first, and don't want it to run on first response to clients    
            if second_msg == 1:
                if addr[1] == ports[1]:
                    second_msg = 2 # This ensures if client 2 sends another message it will be ignored
                    actions[1] = float(request)
                    #resp2 = "No further input required from you. Thank you."
                    resp1 = f"You are playing against a fixed strategy with action {actions[1]}. Enter a number from 0 to 1 inclusive."
                    
                    # best_action_responses() need only run once - For first game for opponents first action 
                    if len(incr_values) == 0:
                        row_values, col_values, incr_values = best_action_responses()
                        # rounding to 1 decimal place but may increase to 4 for smaller increments e.g. 0.0001
                        row_values = [round(num, 1) for num in row_values]
                        col_values = [round(num, 1) for num in col_values]
                        incr_values = [round(num, 1) for num in incr_values]
                    #print("incr_Values", incr_values)
                    best_response = col_values[incr_values.index(actions[1])]
                    client_socket1.send(resp1.encode("utf-8"))
                    #client_socket2.send(resp2.encode("utf-8"))

            # need to determine first responses to clients and advise on strategy
            if addr[1] == ports[0] and first_msg == 0: 
                first_msg = 1
                client_socket1 = client_socket
            elif addr[1] == ports[1] and second_msg == 0:
                second_msg = 1
                resp2 = "Enter a number from 0 to 1 inclusive."
                client_socket2 = client_socket
                client_socket2.send(resp2.encode("utf-8"))
            if addr[1] == ports[0]:
                if second_msg == 2:
                    # Check number sent from first client in order to advise them
                    if(float(request) < best_response):
                        resp1 = f"Increase probability of action {float(request)} by {round((best_response - float(request)) * 100)}%\n"
                    elif (float(request) > best_response):
                        resp1 = f"Decrease probability of action {float(request)} by {round((float(request) - best_response) * 100)}%\n"
                    else:
                        actions[0] = float(request)
                        resp1 = f"You have picked the best value {actions[0]}.\nYour opponent is playing {actions[1]}.\n\n"
                        resp2 = f"Enter another number from 0 to 1"
                        second_msg = 1 # resetting, so row can send in another value and it won't be ignored
                        client_socket2.send(resp2.encode("utf-8"))
                    client_socket1.send(resp1.encode("utf-8"))
                    
                    #record CFE
                    cfe_log_file = open('cfe.log', 'a')
                    cfe_log_file.write(resp1)
                    cfe_log_file.close()
                    
                    #first_msg += 1
            #print("client_socket1", client_socket1, "client_socket2", client_socket2, "client_socket", client_socket)
        except Exception as e:
            print(f"Error: {e}")
            break
    client_socket.close()

def start_server():
    global ports
    host = "127.0.0.1"
    port = 8888
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connected on port {addr[1]}") # e.g. addr is ('127.0.0.1', 50437) so addr[1] would be 50437
        ports.append(addr[1])
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    start_server()
