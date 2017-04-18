from barbell import Barbell

environment_name = "CartPole-v0"

b = Barbell.new(environment_name)

for i in xrange(1000):
    action = Barbell.action_space.sample()
    observation, reward, done, info = Barbell.step(action)
