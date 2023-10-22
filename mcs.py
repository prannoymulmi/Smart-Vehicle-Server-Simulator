import random


def simulate_challenge_response(num_simulations):
    successful_authentications = 0
    for _ in range(num_simulations):
        challenge = random.randint(1, 1000)  # Simulating a challenge
        correct_response = challenge + 1  # Assuming the correct response is challenge + 1

        # Simulating the client's response
        # A malicious client might be able to guess the correct response with a 0.1% chance
        client_response = correct_response if random.random() > 0.001 else random.randint(1, 1000)

        if client_response == correct_response:
            successful_authentications += 1

    return successful_authentications / num_simulations

if __name__ == "__main__":
    num_simulations = 100000
    authentication_rate = simulate_challenge_response(num_simulations)
    print("Authentication success rate:", authentication_rate)

