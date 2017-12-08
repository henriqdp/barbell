import barbell

barbell = barbell.from_file("examples/cartpole.yaml")

print_state = True

while barbell.running:
    if 114 in barbell.events:
        barbell.reset()
    if 97 in barbell.events:
        barbell.agent.yahoo(50)
    result = barbell.step()

    barbell.agent.push_cart((10, 0))

    if print_state:
        print(result)
        print_state = False
