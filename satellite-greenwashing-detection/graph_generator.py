import matplotlib.pyplot as plt

def create_graph(veg, nonveg):

    labels = ["Vegetation","Non Vegetation"]
    values = [veg, nonveg]

    plt.figure(figsize=(6,4))
    plt.bar(labels, values)

    plt.title("Land Coverage Analysis")
    plt.ylabel("Percentage")

    plt.savefig("coverage_graph.png")
    plt.close()