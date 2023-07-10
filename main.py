import random, math, operator
from pprint import pprint

random.seed(0)

class AlgoGen:
    def __init__(self, list_of_point:list[tuple]) -> None:
        """ Constructor for the class

        Args:
            list_of_point (list[tuple]): it's a list with coordinate
        """
        self.list_of_point = list_of_point
        self.population = []
        self.create_population()

    def create_population(self) -> None:
        """
            create a population of dictionary of indexes's list
        """
        for i in range(len(self.list_of_point)):
            temp_dico = {
                "chemin": [elt for elt in range(1, len(self.list_of_point))],
                "longueur": None
            }
            random.shuffle(temp_dico["chemin"])
            temp_dico["chemin"].insert(0, 0)

            self.population.append(temp_dico)
    
    def check_population(self) -> None:
        for individu in self.population:
            chemin = individu["chemin"]
            distance_total = 0
            one_befor = None

            for index_of_point in chemin:
                if one_befor is not None :
                    x1 = self.list_of_point[index_of_point][0]
                    y1 = self.list_of_point[index_of_point][1]

                    x2 = self.list_of_point[one_befor][0]
                    y2 = self.list_of_point[one_befor][1]
                
                    dist = math.sqrt((x1 - y1)**2 + (x2 - y2)**2)
                    distance_total += dist

                one_befor = index_of_point
            individu["longueur"] = distance_total

    def select_population(self) -> None:
        self.population = sorted(self.population, key=operator.itemgetter('longueur'))
        self.population = self.population[::len(self.population)//3]

    def breeding_and_mutation(self, mutation_rate) -> None:
        for index_person in range(len(self.population)):
            if random.randint(0, 100) <= mutation_rate and index_person > 3:
                n1 = random.randint(1, len(self.population) - 1)
                n2 = random.randint(1, len(self.population) - 1)
                self.population[index_person]["chemin"][n1], self.population[index_person]["chemin"][n2] = self.population[index_person]["chemin"][n2], self.population[index_person]["chemin"][n1]

            if index_person != len(self.population) - 1:
                list_dico0 = self.population[index_person]["chemin"]
                list_dico0 = list_dico0[::len(list_dico0)//2]

                list_dico1 = self.population[index_person + 1]["chemin"]

                cross = list_dico0 + [elt for elt in list_dico1 if elt not in list_dico0]

                dico = {
                    "chemin": cross,
                    "longueur": None
                }

                self.population.append(dico)

    def find_best_path(self, nb_it) -> dict:
        i = 0
        while i < nb_it:
            self.check_population()
            self.select_population()
            self.breeding_and_mutation(random.randint(0, 25))
            i += 1

        self.check_population()
        self.select_population()

        return self.population[0]

# -------------------------------------------------------------------------
# Main:
list_of_point = [(0, 0)]
list_of_point += [(random.randint(0, 50), random.randint(0, 50)) for _ in range(50)]

genetique = AlgoGen(list_of_point)

pprint(genetique.find_best_path(10_000))

print(genetique.population)