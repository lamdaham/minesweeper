import string

n = int(input("People: "))

options_dict = {ascii_lowercsae[x]: 0 for x in range(n)}

for i in range(n):
    print("a) Daddys Home\nb) Zootopia\nc) A New Hope\nd) Fantastic Beasts")
    options = input("Movie Ranking (i.e. a,b,c,d): ").strip().split(",")
    
    for option in options:
        options_dict[option] += 4 - options.index(option)

    print("\n" * 30)
    
print({k: v for k, v in sorted(options_dict.items(), key=lambda item: item[1], reverse=True)})