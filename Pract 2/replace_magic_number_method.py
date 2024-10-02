# Код до рефакторингу
class Order:
    def calculate_final_price(self, base_price, category):
        if category == 'goods':
            discount = base_price * 0.1  # 10% знижка
        elif category == 'cloth':
            discount = base_price * 0.2  # 20% знижка
        elif category == 'devices':
            discount = base_price * 0.15  # 15% знижка
        else:
            discount = 0

        final_price = base_price - discount
        return final_price

# Код після рефакторингу  
class Order:
    ELECTRONICS_DISCOUNT = 0.1  # 10% знижка
    CLOTHING_DISCOUNT = 0.2      # 20% знижка
    BOOKS_DISCOUNT = 0.15        # 15% знижка

    def calculate_final_price(self, base_price, category):
        if category == 'goods':
            discount = base_price * self.ELECTRONICS_DISCOUNT
        elif category == 'cloth':
            discount = base_price * self.CLOTHING_DISCOUNT
        elif category == 'devices':
            discount = base_price * self.BOOKS_DISCOUNT
        else:
            discount = 0

        final_price = base_price - discount
        return final_price