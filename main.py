import barbell

barbell = barbell.from_file("world.yaml")

while barbell.running:
    barbell.step()
# print(barbell)
