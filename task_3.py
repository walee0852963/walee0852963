
store_name = "waled appo hgir Store"
discount_percentage = 10  

print("Welcome to ", store_name," !")

    
inventory = {
        "Apple": {"price": 0.5, "quantity": 50},
        "Banana": {"price": 0.3, "quantity": 30},
        "Carrot": {"price": 0.2, "quantity": 100},
        "Milk": {"price": 1.2, "quantity": 20},
        "Bread": {"price": 1.5, "quantity": 15}
    }

categories = {"Fruits", "Vegetables", "Dairy", "Bakery"}

cart = {}

while True:
        print("\nAvailable items:")
        for item, details in inventory.items():
            print(f"{item} - Price: ${details['price']} | Quantity: {details['quantity']}")

        print("\nType 'done' to finish shopping.")
        choice = input("Enter the item you'd like to add to your cart: ").strip()

        if choice.lower() == "done":
            break

        if choice not in inventory:
            print("Sorry, this item is not available.")
            continue

        quantity = input("How many "+choice+",s would you like to buy? ")

        if not quantity.isdigit():
            print("Please enter a valid number.")
            continue

        quantity = int(quantity)

        if quantity > inventory[choice]["quantity"]:
            print(f"Sorry, we only have {inventory[choice]['quantity']} {choice}s available.")
            continue

        if choice in cart:
            cart[choice]["quantity"] += quantity
        else:
            cart[choice] = {"price": inventory[choice]["price"], "quantity": quantity}

        inventory[choice]["quantity"] -= quantity

        print(f"Added {quantity} {choice}(s) to your cart.")

total_cost = 0
print("\nYour cart contains:")
for item, details in cart.items():
        item_total = details["price"] * details["quantity"]
        total_cost += item_total
        print(f"{item}: {details['quantity']} @ ${details['price']} each = ${item_total:.2f}")

        if len(cart) > 3:
         discount = (discount_percentage / 100) * total_cost
         total_cost -= discount
         print(f"\nDiscount applied: ${discount:.2f}")

        print(f"\nTotal cost: ${total_cost:.2f}")
        print(f"Thank you for shopping at {store_name}! Have a great day!")
y= input ()       
#Run the system
#grocery_store()
