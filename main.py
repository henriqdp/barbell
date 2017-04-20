from barbell import Barbell

environment_name = "CartPole-v0"

b = Barbell(environment_name)

for i in range(1000):
    b.env.render()
    action = b.action_space.sample()
    observation, reward, done, info = b.step(action)
    if done:
        b.reset()
