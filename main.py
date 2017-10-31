import barbell

barbell = barbell.from_file("world.yaml")

while barbell.running:
    if 119 in barbell.events:
        barbell.parts["torso"].apply_force("local", (0.0, 1100.0))
    barbell.step()
# print(barbell)
