import random

def player(prev_play="", opponent_history=[], name_history=[], my_history=[], play_order={}):
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}

    if prev_play:
        opponent_history.append(prev_play)

    # Reset all variables after 1000 rounds
    if len(opponent_history) > 1000:
        opponent_history.clear()
        name_history.clear()
        my_history.clear()
        play_order.clear()

    # Default play_order initialization
    if not play_order:
        play_order.update({"RR": 0, "RP": 0, "RS": 0, "PR": 0, "PP": 0, "PS": 0, "SR": 0, "SP": 0, "SS": 0})

    # Identify bot type in the first 3 rounds
    if len(opponent_history) <= 3:
        move = ["R", "P", "S"][len(opponent_history) % 3]
        my_history.append(move)
        return move

    # Determine bot type after first 3 moves
    if len(name_history) == 0:
        code_to_bot = {"RPP": "quincy", "PPP": "abbey", "PPS": "kris", "RRR": "mrugesh"}
        bot_name = code_to_bot.get("".join(opponent_history[:3]), "unknown")
        name_history.append(bot_name)

    bot_name = name_history[-1]

    if bot_name == "unknown":
        # Default to random if the bot is unrecognized
        guess = random.choice(["R", "P", "S"])

    elif bot_name == "quincy":
        # Predict using Quincy's repeating pattern
        quincy_pattern = ["R", "R", "P", "P", "S"]
        next_move = quincy_pattern[len(opponent_history) % 5]
        guess = ideal_response[next_move]

    elif bot_name == "abbey":
        # Use frequency analysis for Abbey
        if len(my_history) >= 2:
            last_two = my_history[-2] + my_history[-1]
            play_order[last_two] += 1
        potential_next = [my_history[-1] + move for move in "RPS"]
        prediction = max(potential_next, key=lambda x: play_order.get(x, 0))[-1]
        guess = ideal_response[prediction]

    elif bot_name == "kris":
        # Counter Kris's last move
        guess = ideal_response[my_history[-1]]

    elif bot_name == "mrugesh":
        # Look for most frequent pair in opponent history
        for i in range(len(opponent_history) - 1):
            pair = opponent_history[i] + opponent_history[i + 1]
            play_order[pair] += 1
        most_frequent = max(play_order, key=play_order.get, default="RR")[-1]
        guess = ideal_response[most_frequent]

    my_history.append(guess)
    return guess
