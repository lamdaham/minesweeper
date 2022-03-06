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
            
            options = input("Ranking (i.e. a,b,c): ").lower().replace(" ", "").split(",")
            
            for option in options:
                self.selection_vals[option] += 3 - options.index(option)

            print("\n" * 30)
    
    def results(self):
        print("Final Results: ")
        sorted_vals = {k: v for k, v in sorted(self.selection_vals.items(), key=lambda item: item[1], reverse=True)}
        for k, n in dict(zip(sorted_vals.keys(), range(1, len(self.selections) + 1))).items():
            print(str(n) + ". " + self.selections[k])

        print()
        if input("See raw? (y/n): ").lower().strip() == "y":
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