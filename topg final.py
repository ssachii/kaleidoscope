#!/usr/bin/env python
# coding: utf-8


# SmartMenu is an interactive menu and data visualisation & management tool for a hotel
# configures menu based on 1) customer type & 2) restaurant/service type + customer inputs
# restaurants are categorised by type and conference room is an additional service, which is provided based on previous booking
# visualised data presents existing statistics of the hotel and represents them pictorially

# hotel name: Marina Bay Hotel
# fine dining restaurant: Palm Springs
# cafe: Moka Pot
# poolside lounge: Shimmer
# conference halls: ambrosia, camelia, laurel, maple

# assigning variables
HOTEL = "Marina Bay Hotel"
config = {"member": False, "Living": False, "where_eating": None}

# importing libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# importing csv files
FOOD = pd.read_csv("FOOD.csv")
PEOPLE = pd.read_csv("PEOPLE.csv")
 
# while loop for incorrect input
def int_inp(inp_str="\nSelect option: "):
    while True:
        try:
            inp = int(input(inp_str))
            break
        except ValueError:
            print("Invalid option, try again.")
    return inp


def get_option(options, prompt="\nOptions"):
    print(prompt)
    for i, option in enumerate(options):
        print(f"{i+1} - {option}")
    while True:
        inp = int_inp()
        if inp > 0 and inp <= len(options):
            break
        print("Invalid option, try again.")
    return options[inp - 1]


# stores the two parameters of customer: living and member
# living allows entry to all restaurants, customers not living at the hotel cannot access shimmer and room service
# members get a 10% discount on every order, non-members do not
def member():
    res = input(f"\nIf you are living in this hotel press y, if not press n? (y/n): ")
    if res.lower() in ("y", "yes"):
        config["living"] = True
    else:
        config["living"] = False

    dh = input(f"\nAre you a member? (y/n/back): ")
    if dh.lower() in ("y", "yes"):
        config["member"] = True
    elif dh == "back":
        return member
    else:
        config["member"] = False

    return where_eat


# prompts user dining options
def where_eat():
    op = get_option(
        [
            "Palm Springs",
            "Moka Pot",
            "Shimmer",
            "Room Service",
            "Conference Hall",
            "Begin Again",
            "Back",
        ]
        if config.get("living")
        else ["Palm Springs", "Moka Pot", "Conference Hall"],
        """
Where would you like to eat?
Palm Springs: Fine dining family restaurant
Moka Pot: 24/7 Cafe
Shimmer: Rooftop Lounge
""",
    )

    if op == "Palm Springs":
        # instructions given to customer on choosing palm springs
        # moves to palm springs menu
        print("\nPlease proceed to the green door on the left")
        config["where_eating"] = "PS"
        return PS1

    elif op == "Moka Pot":
        # instructions given to user on choosing moka pot
        # moves to moka pot menu
        print("\nTurn right and then take the first staircase to find Moka Pot")
        config["where_eating"] = "MP"
        return MP1

    elif op == "Shimmer":
        # instructions given to user on choosing shimmer
        # moves to shimmer menu
        print("Please take the elevator on the left and proceed to the rooftop")
        config["where_eating"] = "SH"
        return SH1

    elif op == "Room Service":
        # moves to room service menu
        config["where_eating"] = "RS"
        return RS1

    elif op == "Conference Hall":
        # moves to conference hall menu
        return CH1

    elif op == "Begin Again":
        # reverts to the start of the program
        return start_prog

    elif op == "Back":
        # goes back to the last option
        return member


# palm springs menu
def PS1():
    print("\nwelcome to Palm Springs!")
    print(
        "If you want to return to previous option, enter -1, if you want to begin again enter -2"
    )
    inp = int_inp("How many people would you like a table for?: ")
    if inp > 0:
        return food_menu
        # moves to ordering section
    elif inp == -1:
        return where_eat
        # returns dining options
    elif inp == -2:
        return start_prog
        # reverts to the start of the program
    else:
        print("Enter valid input.")
        return PS1


# moka pot menu
def MP1():
    print("\nWelcome to Moka Pot")
    inp = int_inp("How many people would you like a table for?: ")
    if inp > 0:
        return food_menu
        # moves to ordering section
    elif inp == -1:
        return where_eat
        # returns dining options
    elif inp == -2:
        return start_prog
        # reverts to the start of the program
    else:
        print("Enter valid input.")
        return MP1


# shimmer menu
def SH1():
    print("\nWelcome to Shimmer")
    inp = int_inp("How many people would you like a table for?: ")
    if inp > 0:
        return food_menu
        # moves to ordering section
    elif inp == -1:
        return where_eat
        # returns dining options
    elif inp == -2:
        return start_prog
        # reverts to the start of the program
    else:
        print("Enter valid input.")
        return SH1


# room service menu
def RS1():
    print("\nRoom Service")

    return food_menu
    # moves to ordering section


# conference hall menu
def CH1():
    res = int(input("\nEnter your room number: "))
    # prompts room number input and checks value from PEOPLE.csv
    room = PEOPLE.loc[PEOPLE["Room Number"] == res, :]
    if room.empty:
        print("Invalid room number")
        return where_eat
        # returns dining options
    else:
        if room["Conference Booking"][0] == "T":
            # shows booking details for booking=true
            print("\nBooking found under:")
            print("Name:", room["Name"][0])
            print("Name of Hall:", room["Name of Hall"][0])
            print("\nProceeding to Conference hall")
            druv = input("Do you want to begin again?(y/n)")
            if druv == "y":
                return start_prog
                # reverts to the start of the program
            elif druv == "n":
                print("Have a nice day!")
            else:
                print("Enter valid input")
                return CH1
                # goes back to conference hall menu
        elif room["Conference Booking"][0] == "F":
            # executes print statement for booking=false
            print("No booking found for that room.")


# brings customer back to main menu
def osa8():
    osa = input("Do you want to begin again?(y/n)")
    if osa == "y":
        return start_prog
    elif osa == "n":
        print("Have a nice day!")
    else:
        print("Enter valid inputs")
        return osa8


# ordering section: food menu
def food_menu():
    print("What type of cuisines would you like to try?")
    res = get_option(
        ["indian", "italian", "continental", "japanese", "Begin again", "back"]
    )
    # lists all cuisine types
    if res == "back":
        return where_eat
        # returns to dining options
    elif res == "Begin again":
        return start_prog
        # reverts to start of the program

    checks = {
        "PS": "Availability in Palm Springs",
        "MP": "Availability in Moka Pot",
        "SH": "Availability in Shimmer",
        "RS": "Availability in Room Service",
    }
    # checks food item availability from FOOD.csv

    # displaying menu
    print(f"\nDisplaying {res} category menu:")
    _food = FOOD[FOOD[checks.get(config.get("where_eating"))] == "T"]
    menu = (
        _food.loc[FOOD["Type of Cuisine"] == res]
        .loc[:, ["Name of Dish", "Category", "Price"]]
        .loc[FOOD["Category"].isin(["soup", "starter", "snack", "meal"])]
    )
    menu = pd.concat(
        [
            menu,
            _food.loc[:, ["Name of Dish", "Category", "Price"]].loc[
                FOOD["Category"].isin(["drinks", "dessert"])
            ],
        ]
    )
    print(menu)

    # takes order input from customer
    orders = []
    while True:
        print("\nWhat would you like to order?")
        print("<dish id> - ID of Dish\nstop - Stop ordering")
        res = input("--> ")
        if res.lower() == "stop":
            break
        try:
            res = int(res)
            if res in menu.index:
                orders.append(res)
                continue
        except ValueError:
            pass
        print("Enter valid id and try again.")

    # generates bill for non-members
    if len(orders) != 0:
        print("\nYour order:")
        for order in orders:
            print(
                menu.loc[order, "Name of Dish"].ljust(30, "_"), menu.loc[order, "Price"]
            )
        total = menu.loc[orders, "Price"].sum()
        print("Total:", total)

        # generates bill for members
        if config.get("member"):
            total = (total * 0.9).round(2)
            print("Member discount: 10%")
            print("Total price:", total)

        print("\nYour order will arrive shortly. Bon Apetit!")

    # prompts the following when nothing is ordered by the customer
    elif len(orders) == 0:
        prin = input(
            "You have not ordered anything, do you want to go back?(y/[anything else])"
        )
        if prin == "y":
            return food_menu
        else:
            print("We are sorry")
    return osa8


# data visualisation section

# line graph for no. of customers per year from 2012-2022
def beta():
    n = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
    m = [1015, 1894, 2049, 2234, 2683, 2991, 3245, 4677, 104, 1042, 4998]
    plt.xlabel("Year")
    plt.ylabel("No. of Customers")
    plt.title("No. of customers per year from opening till 2022")
    plt.plot(n, m, marker="d", markersize=10, markeredgecolor="red")
    plt.show()
    osa1 = input("Do you want to do?(back/begin again)")
    if osa1 == "back":
        return visualized
    elif osa1 == "begin again":
        return start_prog
    else:
        print("Enter valid Input")
        return beta


# line graph for rough average of customers by month
def gamma():
    a = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    b = [204, 343, 452, 499, 773, 844, 643, 494, 321, 500, 792, 623]
    plt.xlabel("Month")
    plt.ylabel("Rough Average number of customers")
    plt.title("Rough average number of customers by month")
    plt.plot(a, b, marker="d", markersize=10, markeredgecolor="red")
    plt.show()
    osa1 = input("Do you want to do?(back/begin again)")
    if osa1 == "back":
        return visualized
    elif osa1 == "begin again":
        return start_prog
    else:
        print("Enter valid Input")
        return gamma


# line graph for number of employees per year
def delta():
    c = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
    d = [100, 150, 225, 250, 350, 350, 475, 470, 80, 310, 450]
    plt.xlabel("Year")
    plt.ylabel("No. of Employees")
    plt.title("No. of employees per year")
    plt.plot(c, d, marker="d", markersize=10, markeredgecolor="red")
    plt.show()
    osa1 = input("Do you want to do?(back/begin again)")
    if osa1 == "back":
        return visualized
    elif osa1 == "begin again":
        return start_prog
    else:
        print("Enter valid Input")
        return delta


# bar graph for number of customers per season
def epsilon():
    seasons = ["Winter", "Spring", "Summer", "Autumn"]
    guests = [467, 376, 883, 642]
    plt.xlabel("Season")
    plt.ylabel("No. of customers")
    plt.title("No. of customers per season")
    plt.bar(seasons, guests)
    plt.show()
    osa1 = input("Do you want to do?(back/begin again)")
    if osa1 == "back":
        return visualized
    elif osa1 == "begin again":
        return start_prog
    else:
        print("Enter valid Input")
        return epsilon


# bar graph for popularity of types of dishes served
def zeta():
    dishes = ["Indian", "Italian", "Continental", "Japanese"]
    pop = [23.4, 46.3, 22.9, 7.4]
    plt.xlabel("Dishes")
    plt.ylabel("Popularity percentage")
    plt.title("Popularity of types of dishes served")
    plt.ylim(0, 100)
    plt.bar(dishes, pop)
    plt.show()
    osa1 = input("Do you want to do?(back/begin again)")
    if osa1 == "back":
        return visualized
    elif osa1 == "begin again":
        return start_prog
    else:
        print("Enter valid Input")
        return zeta


# bar graph for popularity of restaurants
def eta():
    rest = ["Palm Springs", "Moka Pot", "Shimmer", "Room Service"]
    popu = [32.1, 56.2, 10, 2.7]
    plt.xlabel("Restaurant")
    plt.ylabel("Popularity percentage")
    plt.title("Popularity of Restaurants")
    plt.ylim(0, 100)
    plt.bar(rest, popu)
    plt.show()
    osa1 = input("Do you want to do?(back/begin again)")
    if osa1 == "back":
        return visualized
    elif osa1 == "begin again":
        return start_prog
    else:
        print("Enter valid Input")
        return eta


# pie chart for conference hall capacities
def ip():
    df = pd.read_csv("HALL.csv")
    hall = df["Hall"]
    cap = df["Capacity"]
    colors = ("pink", "green", "blue", "orange")
    plt.pie(
        cap,
        labels=hall,
        colors=colors,
        autopct="%1.1f%%",
        explode=[0, 0, 0, 0.1],
        shadow=True,
    )
    plt.title("Hall Capacity")
    plt.legend()
    plt.show()
    osa1 = input("Do you want to do?(back/begin again)")
    if osa1 == "back":
        return visualized
    elif osa1 == "begin again":
        return start_prog
    else:
        print("Enter valid Input")
        return ip


# visualisation menu
def visualized():
    bil = get_option(
        [
            "No. of customers per year from opening till 2022",
            "Rough average number of customers by month",
            "No. of employees per year",
            "No. of customers per season",
            "Popularity of types of dishes served",
            "Popularity of Restaurants",
            "Hall Capacity",
            "Restart Program",
        ],
        # all data visualisation options are prompted
        "Enter the Number of the following data you want to view",
    )

    # customer is taken to respective graph based on input
    if bil == "No. of customers per year from opening till 2022":
        return beta
    elif bil == "Rough average number of customers by month":
        return gamma
    elif bil == "No. of employees per year":
        return delta
    elif bil == "No. of customers per season":
        return epsilon
    elif bil == "Popularity of types of dishes served":
        return zeta
    elif bil == "Popularity of Restaurants":
        return eta
    elif bil == "Hall Capacity":
        return ip
    elif bil == "Restart Program":
        return start_prog


# statements executed at the start of the program on customer entry
def start_prog():
    print(f"Welcome to {HOTEL}!")
    alpha = get_option(["Hotel Services", "Visualized Data", "Exit Program"])
    if alpha == "Hotel Services":
        return member
        # goes to the dining options//simulator
    elif alpha == "Visualized Data":
        return visualized
        # goes to the data visualisation section//hotel management
    elif alpha == "Exit Program":
        return False


current = start_prog
while current:
    current = current()
