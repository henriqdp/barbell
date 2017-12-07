import barbell

barbell = barbell.from_file("examples/cartpole.yaml")

print_state = True

while barbell.running:
    if 114 in barbell.events:
        barbell.reset()
    if 97 in barbell.events:
        barbell.parts["cart"].apply_force("local", (-10000.0, 0.0))
    if 100 in barbell.events:
        barbell.parts["cart"].apply_force("local", (10000.0, 0.0))
    result = barbell.step()
    if print_state:
        print(result)
        print_state = False
