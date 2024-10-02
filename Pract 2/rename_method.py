# Код до рефакторингу
class Order:
    def t(self):
        # Розрахунок загальної суми замовлення
        total = 0
        for item in self.items:
            total += item.price * item.quantity
        return total
    
    def calc(self, price, discount):
        # Розрахунок знижки замовлення
        return price - (price * discount)
    
# Код після рефакторингу 
class Order:
    def calculate_total(self):
        # Розрахунок загальної суми замовлення
        total = 0
        for item in self.items:
            total += item.price * item.quantity
        return total
    
    def calculate_discounted_price(self, price, discount):
        # Розрахунок знижки замовлення
        return price - (price * discount)