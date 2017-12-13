import sys
import os
import random
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import barbell  # NOQA
from cartpole_functions import CartpoleIntelligence  # NOQA

if len(sys.argv) < 2:
    sys.exit("""
            USAGE:
                python cartpole learn => generate random weights and learn from them
                python cartpole evaluate => run environment with previously learned weights (file weights.txt MUST EXIST)
          """)

if sys.argv[1] == 'learn':
    ai = CartpoleIntelligence()
    cartpole = barbell.from_file(os.path.join(os.path.dirname(__file__), 'cartpole.yaml'), render=False)
    cartpole.set_action_function(ai.action_function)
    cartpole.set_reset_function(ai.reset_function)
    cartpole.set_reward_function(ai.reward_function)

    while cartpole.running:
        current_state = cartpole.step()
        if current_state["current_iteration"] == 0:
            cartpole.agent.start_pole((random.randint(-10, 10), 0))

elif sys.argv[1] == 'evaluate':
    try:
        f = open(os.path.join(os.path.dirname(__file__), 'weights.txt'))
        weights = [float(x) for x in f.read().split('\n')[0:-1]]
    except FileNotFoundError:
        print('deu ruim')
        exit()
    ai = CartpoleIntelligence(initialize_weights=False, weights=weights)
    cartpole = barbell.from_file(os.path.join(os.path.dirname(__file__), 'cartpole.yaml'), render=True)
    cartpole.set_reset_function(ai.reset_function)
    cartpole.set_action_function(ai.action_function)
    cartpole.set_reward_function(ai.fake_reward)

    while cartpole.running:
        current_state = cartpole.step()
        if current_state["current_iteration"] == 0:
            cartpole.agent.start_pole((random.randint(-10, 10), 0))
