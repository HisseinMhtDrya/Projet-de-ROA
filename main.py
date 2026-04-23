import random
import tkinter as tk

# 1) MODELISTATION DU RESEAU SOCIAL

# Graphe orienté : dictionnaire d'adjacence
# Format : sommet -> liste de (voisin, probabilité)
graph = {
    1: [(2, 0.4), (3, 0.5)],
    2: [(4, 0.3), (5, 0.6)],
    3: [(5, 0.5), (6, 0.4)],
    4: [(7, 0.7)],
    5: [(7, 0.5), (8, 0.6)],
    6: [(8, 0.5)],
    7: [(9, 0.4)],
    8: [(9, 0.6), (10, 0.5)],
    9: [],
    10: []
}

# Coût d’activation de chaque sommet
costs = {
    1: 4,
    2: 2,
    3: 2,
    4: 1,
    5: 2,
    6: 1,
    7: 2,
    8: 1,
    9: 1,
    10: 1
}

# Budget total
B = 5

# 2) MODELE INDEPENDENT CASCADE

def simulate_ic(graph, seeds, iterations=100):
    """
    Simule la diffusion selon le modèle Independent Cascade
    et retourne le nombre moyen de nœuds activés.
    """
    total_activated = 0
    last_activated_set = set()

    for _ in range(iterations):
        activated = set(seeds)
        new_activated = set(seeds)

        while new_activated:
            next_activated = set()

            for node in new_activated:
                for neighbor, prob in graph[node]:
                    if neighbor not in activated:
                        if random.random() <= prob:
                            next_activated.add(neighbor)

            activated.update(next_activated)
            new_activated = next_activated

        total_activated += len(activated)
        last_activated_set = activated

    average = total_activated / iterations
    return average, last_activated_set

# 3) ALGORITHME GLOUTON (GREEDY)

def greedy_influence_maximization(graph, costs, budget):
    """
    Sélection gloutonne des seeds sous contrainte budgétaire.
    Critère : influence marginale / coût
    """
    seeds = []
    remaining_budget = budget
    nodes = list(graph.keys())

    while True:
        best_node = None
        best_ratio = 0
        best_influence = 0

        for node in nodes:
            if node not in seeds and costs[node] <= remaining_budget:

                current_influence, _ = simulate_ic(graph, seeds)
                new_influence, _ = simulate_ic(graph, seeds + [node])

                marginal_gain = new_influence - current_influence
                ratio = marginal_gain / costs[node]

                if ratio > best_ratio:
                    best_ratio = ratio
                    best_node = node
                    best_influence = new_influence

        if best_node is None:
            break

        seeds.append(best_node)
        remaining_budget -= costs[best_node]

    final_avg, activated_nodes = simulate_ic(graph, seeds)

    return seeds, remaining_budget, final_avg, activated_nodes

# 4) AFFICHAGE DES RESULTATS

seeds, budget_rest, avg_influence, activated_nodes = greedy_influence_maximization(
    graph, costs, B
)

cout_total = B - budget_rest

print("RESULTATS")
print("Seeds choisis :", seeds)
print("Coût total :", cout_total)
print("Budget restant :", budget_rest)
print("Nombre moyen de nœuds influencés :", round(avg_influence, 2))
print("Nœuds activés après diffusion :", activated_nodes)

# 5) AFFICHAGE DU GRAPHE FINAL (TKINTER)
def draw_graph(graph, seeds, activated):
    """
    Affiche le graphe final :
    - rouge : seeds
    - vert : activés
    - gris : non activés
    """
    root = tk.Tk()
    root.title("Diffusion d'information dans le réseau social")

    canvas = tk.Canvas(root, width=800, height=500)
    canvas.pack()

    # Position fixe des sommets
    positions = {
        1: (100, 100),
        2: (250, 50),
        3: (250, 150),
        4: (400, 50),
        5: (400, 150),
        6: (400, 250),
        7: (550, 100),
        8: (550, 200),
        9: (700, 100),
        10: (700, 200)
    }

    # Dessiner les arêtes
    for node in graph:
        x1, y1 = positions[node]

        for neighbor, prob in graph[node]:
            x2, y2 = positions[neighbor]

            canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST)
            canvas.create_text((x1+x2)//2, (y1+y2)//2 - 10,
                               text=str(prob), font=("Arial", 8))

    # Dessiner les sommets
    for node, (x, y) in positions.items():

        if node in seeds:
            color = "red"
        elif node in activated:
            color = "green"
        else:
            color = "lightgray"

        canvas.create_oval(x-20, y-20, x+20, y+20, fill=color)
        canvas.create_text(x, y, text=str(node), font=("Arial", 12, "bold"))

    root.mainloop()

# Lancer l'affichage
draw_graph(graph, seeds, activated_nodes)
