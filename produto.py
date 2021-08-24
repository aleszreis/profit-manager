class Produto:
    def __init__(self, code, cost, price, received):
        self.code = code
        self.cost = cost
        self.price = price
        self.v_received = received


    def save_product(self):
        with open("produtos.csv", "a") as file:
            file.write({"Cod Produto": self.code,
                        "Nome Produto": None,
                        "Custo": self.cost})
