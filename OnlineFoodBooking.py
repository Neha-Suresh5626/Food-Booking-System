import mysql.connector
from getpass import getpass

mydb = mysql.connector.connect(host="localhost", user="root", password="password")
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS food_booking")
mycursor.execute("USE food_booking")
mylogged_in_user = None

# Create tables if they don't exist
mycursor.execute(
    """CREATE TABLE IF NOT EXISTS users (user_id INT AUTO_INCREMENT PRIMARY KEY,username VARCHAR(50) UNIQUE NOT NULL,password VARCHAR(100) NOT NULL)""")

mycursor.execute(
    """CREATE TABLE IF NOT EXISTS restaurants (restaurant_id INT AUTO_INCREMENT PRIMARY KEY,restaurant_name VARCHAR(100) NOT NULL,location VARCHAR(200) NOT NULL)""")

mycursor.execute(
    """CREATE TABLE IF NOT EXISTS menu_items (menu_item_id INT AUTO_INCREMENT PRIMARY KEY,restaurant_id INT NOT NULL,food VARCHAR(100) UNIQUE NOT NULL,price DECIMAL(10, 2) NOT NULL,FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id))""")

mycursor.execute(
    """CREATE TABLE IF NOT EXISTS orders (id INT AUTO_INCREMENT PRIMARY KEY,user_id INT NOT NULL,restaurant_id INT NOT NULL,menu_item_id INT NOT NULL,quantity INT NOT NULL,total_price DECIMAL(10, 2) NOT NULL,FOREIGN KEY (user_id) REFERENCES users(user_id), FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id),FOREIGN KEY (menu_item_id) REFERENCES menu_items(menu_item_id))""")
mydb.commit()


def register_user():
    username = input("Enter a username: ")
    password = getpass("Enter a password: ")

    try:
        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        values = (username, password,)
        mycursor.execute(sql, values)
        mydb.commit()
        print("Registration successful! You can now log in.")
    except mysql.connector.IntegrityError:
        print("Username already exists. Please choose a different username.")


def login_user():
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")

    sql = "SELECT user_id FROM users WHERE username=%s AND password=%s"
    values = (username, password,)
    mycursor.execute(sql, values)
    user_id = mycursor.fetchone()

    if user_id:
        global mylogged_in_user
        mylogged_in_user = user_id[0]
        print("Your user_id is", mylogged_in_user)
        print("Login successful! Welcome back.")
    else:
        print("Invalid username or password. Please try again")


def add_restaurant():
    name = input("Enter restaurant name: ")
    location = input("Enter restaurant location: ")
    sql = "INSERT INTO restaurants (restaurant_name,location) VALUES (%s, %s)"
    values = (name, location,)
    mycursor.execute(sql, values)
    mydb.commit()
    print("Restaurant added successfully.")


def add_menu_item():
    restaurant_id = int(input("Enter restaurant ID: "))
    name = input("Enter menu item name: ")
    price = float(input("Enter menu item price: "))

    sql = "INSERT INTO menu_items (restaurant_id, food, price) VALUES (%s, %s, %s)"
    values = (restaurant_id, name, price,)
    mycursor.execute(sql, values)
    mydb.commit()
    print("Menu item added successfully.")


def view_restaurants():
    sql = "SELECT * FROM restaurants"
    mycursor.execute(sql)
    restaurants = mycursor.fetchall()
    if restaurants:
        print("Available restaurants:")
        for restaurant in restaurants:
            print(f"ID: {restaurant[0]}, Restaurant: {restaurant[1]}")
    else:
        print("No restaurants found.")


def view_menu_items(restaurant_id):
    sql = "SELECT * FROM menu_items WHERE restaurant_id = %s"
    values = (restaurant_id,)
    mycursor.execute(sql, values)
    menu_items = mycursor.fetchall()
    if menu_items:
        print(f"Menu items for restaurant ID {restaurant_id}:")
        for item in menu_items:
            print(f"ID: {item[0]}, Item: {item[2]}, Price: {item[3]:.2f}")
    else:
        print("No menu items found for the restaurant.")


def place_order():
    global mylogged_in_user
    if mylogged_in_user:
        restaurant_id = int(input("Enter restaurant ID: "))
        menu_item_id = int(input("Enter menu item ID: "))
        quantity = int(input("Enter quantity: "))

        sql = "SELECT price FROM menu_items WHERE menu_item_id = %s"
        values = (menu_item_id,)
        mycursor.execute(sql, values)
        price = mycursor.fetchone()

        if price:
            userid = int(input("Enter your user_id: "))

            total_price = price[0] * quantity
            sql = "INSERT INTO orders (user_id, restaurant_id, menu_item_id, quantity, total_price) VALUES (%s, %s, %s, %s, %s)"
            values = (userid, restaurant_id, menu_item_id, quantity, total_price,)
            mycursor.execute(sql, values)
            mydb.commit()
            print(f"Order placed successfully. Total price: {total_price:.2f}")
        else:
            print("Menu item not found.")
    else:
        print("Please login first!")
        return


def view_orders():
    sql = "SELECT * FROM orders"
    mycursor.execute(sql)
    ordered = mycursor.fetchall()
    if ordered:
        print("Orders:")
        for order in ordered:
            print(
                f"ID: {order[0]}, User_id: {order[1]}, Restaurant_id: {order[2]}, menu_item_id: {order[3]}, Quantity: {order[4]}, Total_price:{order[5]:.2f}")
    else:
        print("No orders found.")


def update_username_passwd():
    global mylogged_in_user
    if mylogged_in_user:
        username1 = input("Enter your current username: ")
        username2 = input("Enter your new username: ")
        pwd1 = getpass("current password: ")
        pwd2 = getpass("new password: ")
        sql = "UPDATE users SET username=(%s),password=(%s) WHERE username=%s"
        values = (username2, pwd2, username1,)
        mycursor.execute(sql, values)
        mydb.commit()
        print("Username and password updated")

    else:
        print("Please login first!")
        return


def update_restaurant():
    rid = eval(input("Enter restaurant_id: "))
    new_restaurant = input("Enter new restaurant_name: ")
    sql = "UPDATE restaurants SET restaurant_name =(%s) WHERE restaurant_id =%s"
    values = (new_restaurant, rid,)
    mycursor.execute(sql, values)
    mydb.commit()
    print("Reastaurant details updated")


def update_item():
    mid = eval(input("Enter menu_item_id: "))
    new_item = input("Enter new item: ")
    new_price = input("Enter new price: ")
    sql = "UPDATE menu_items SET food =(%s),price =(%s) WHERE menu_item_id =%s"
    values = (new_item, new_price, mid,)
    mycursor.execute(sql, values)
    mydb.commit()
    print("Menu item updated")


def delete_restaurant():
    rid = eval(input("Enter restaurant_id: "))
    sql = "DELETE FROM restaurants WHERE restaurant_id =%s"
    values = (rid,)
    mycursor.execute(sql, values)
    mydb.commit()
    print("Restaurant deleted")


def delete_menu_item():
    mid = eval(input("Enter menu_item_id: "))
    sql = "DELETE FROM menu_items WHERE menu_item_id =%s "
    values = (mid,)
    mycursor.execute(sql, values)
    mydb.commit()
    print("Item deleted")


def logout_user():
    global mylogged_in_user
    if mylogged_in_user:
        oid = "SELECT id FROM orders WHERE user_id = %s"
        values = (mylogged_in_user,)
        mycursor.execute(oid, values, )
        ordered = mycursor.fetchall()
        if ordered:
            for i in ordered:
                id_no = i
                sqlo = "DELETE FROM orders WHERE id = %s"
                mycursor.execute(sqlo, id_no, )
                mydb.commit()
                continue
            sql = "DELETE FROM users WHERE user_id = %s"
            uid = (mylogged_in_user,)
            mycursor.execute(sql, uid)
            mydb.commit()


        else:
            sql = "DELETE FROM users WHERE user_id = %s"
            uid = (mylogged_in_user,)
            mycursor.execute(sql, uid)
            mydb.commit()

        print("Logout complete")

    else:
        print("Please login first!")
        return


def close_connection():
    mycursor.close()
    mydb.close()


print('1.Admin')
print('2.User')

c = eval(input('Enter your choice (1 or 2):'))

while c == 1:
    pwd = eval(input("Enter password:"))
    if pwd == 1234:
        print("\nFood Booking System")
        print('Admin Interface')
        print("1. Add Restaurant")
        print("2. Add Menu Item")
        print("3. View Restaurants")
        print("4. View Menu Items")
        print("5.Update restaurant details")
        print("6.Update Menu Items")
        print("7.Delete restaurant")
        print("8.Delete menu item")
        print("9.View Orders")
        print("10. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            add_restaurant()
        elif choice == 2:
            add_menu_item()
        elif choice == 3:
            view_restaurants()
        elif choice == 4:
            restaurant_id = int(input("Enter restaurant ID to view menu items: "))
            view_menu_items(restaurant_id)
        elif choice == 5:
            update_restaurant()
        elif choice == 6:
            update_item()
        elif choice == 7:
            delete_restaurant()
        elif choice == 8:
            delete_menu_item()
        elif choice == 9:
            view_orders()
        elif choice == 10:
            close_connection()
            break
        else:
            print("Invalid choice. Please try again.")
    else:
        print("Invalid password. Please try again.")

while c == 2:
    print("\nFood Booking System")
    print("1. Register")
    print("2. Login")
    print("3. View Restaurants")
    print("4. View Menu Items")
    print("5. Place Order")
    print("6. Update Username and password")
    print("7. Logout")
    print("8. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        register_user()
    elif choice == 2:
        login_user()
    elif choice == 3:
        view_restaurants()
    elif choice == 4:
        restaurant_id = int(input("Enter restaurant ID to view menu items: "))
        view_menu_items(restaurant_id)
    elif choice == 5:
        place_order()
    elif choice == 6:
        update_username_passwd()
    elif choice == 7:
        logout_user()
    elif choice == 8:
        close_connection()
        break
    else:
        print("Invalid choice. Please try again.")
