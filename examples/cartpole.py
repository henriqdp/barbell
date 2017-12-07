import gym
import numpy as np


def run_episode(env, weights):
    observation = env.reset()
    # env.render()
    total_reward = 0
    for _ in range(200):
        action = 0 if np.matmul(weights, observation) < 0 else 1
        result = env.step(action)
        observation, reward, done, info = result
        print(result)
        total_reward += reward

        if done:
            break

    return total_reward


def get_best_weights(submit):
    # set submit to False if training to get best weights, set to True if running episodes with best weights found

    env = gym.make('CartPole-v0')

    if submit:
        # log data
        env = gym.wrappers.Monitor(env, 'cartpole-experiments/', force=True)

    counter = 0
    noise_scaling = 0.2  # try changing this value for different results
    weights = np.random.rand(4) * 2 - 1
    best_reward = 0

    for _ in range(2000):
        counter += 1
        new_weights = weights + (np.random.rand(4) * 2 - 1) * noise_scaling
        reward = run_episode(env, new_weights)

        if reward > best_reward:
            best_reward = reward
            weights = new_weights

            if reward == 200:
                break

    if submit:
        # run episodes with the best weights
        for _ in range(100):
            run_episode(env, weights)

        env.monitor.close()

    return counter


best_weights_test = get_best_weights(submit=False)

print(best_weights_test)
