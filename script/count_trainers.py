count = 0

with open("trainer_parties.h", "r") as file:
    for line in file:
        if "// Name:" in line:
            count += 1

print(count)
