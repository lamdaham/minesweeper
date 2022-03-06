import string

class Poll:
    def __init__(self, people, selections):
        self.people = people
        self.selection_vals = {string.ascii_lowercase[x]: 0 for x in range(len(selections))}
        self.selections = dict(zip(self.selection_vals.keys(), selections))
    
    def rank(self):
        for _ in range(self.people):
            for movie in self.selections.keys():
                print(movie + ") " + self.selections[movie])
            
            while True:
                options = input("Ranking (i.e. a,b,c): ").lower().replace(" ", "").split(",")
                if not all(elem in options  for elem in list(self.selection_vals.keys())) or len(options) != len(self.selections):
                    print("Ranking cannot have duplicates or missing selections.")
                else:
                    break
            
            for option in options:
                self.selection_vals[option] += 3 - options.index(option)

            print("\n" * 30)


    def results(self):
        print("Final Results: ")
        vals = sorted([i for n, i in enumerate(list(self.selection_vals.values())) if i not in list(self.selection_vals.values())[:n]], reverse=True)
        for i in range(len(vals)):
            keys = [self.selections[k] for k in [k for k,v in self.selection_vals.items() if v == vals[i]]]
            print(str(i + 1) + ". " + ", ".join(keys))

        print()
        if input("See raw? (y/n): ").lower().strip() == "y":
            print(self.selections)
            print(self.selection_vals)

if __name__ == "__main__":
    people = int(input("People: "))

    movie_input = input("Movies (Comma separated): ").title().replace(" ", "")
    if not movie_input.isalnum:
        raise Exception("Input error. Please try again.")
    movie_input = movie_input.split(",")

    poll = Poll(people, movie_input)
    poll.rank()
    poll.results()