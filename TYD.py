import json
from datetime import datetime

# -----------------------------
# COLOURS
# -----------------------------

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
GREY = "\033[90m"
RESET = "\033[0m"
# -----------------------------
# LOAD YARD DATA
# -----------------------------

try:

    with open("yard.json", "r") as file:

        roads = json.load(file)

except FileNotFoundError:

    roads = [

    # ARRIVAL / DEPARTURE

    {
        "road": "A/D Road",
        "yard": "Arrival/Departure",
        "status": "Empty",
        "train": "",
        "operator": "",
        "type": "",
        "length": 0,
        "arrival": "",
        "departure": "",
        "capacity": 1500
    },

    # EAST YARD

    {"road":"East 1","yard":"East Yard","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":369},
    {"road":"East 2","yard":"East Yard","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":369},
    {"road":"East 3","yard":"East Yard","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":967},
    {"road":"East 4","yard":"East Yard","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":995},
    {"road":"East 5","yard":"East Yard","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":1067},
    {"road":"East 6","yard":"East Yard","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":304},
    {"road":"East 7","yard":"East Yard","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":183},
    {"road":"East 8","yard":"East Yard","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":1062},

    # WEST YARD

    {"road":"West 3","yard":"West Yard","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":1231},
    {"road":"West 4","yard":"West Yard","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":1200},
    {"road":"West 5","yard":"West Yard","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":773},
    {"road":"West 5A","yard":"West Yard","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":423},
    {"road":"West 6","yard":"West Yard","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":1207},

    # FIRST CLASSIFICATION

    {"road":"1st Class 8","yard":"1st Classification","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":472},
    {"road":"1st Class 9","yard":"1st Classification","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":421},
    {"road":"1st Class 10","yard":"1st Classification","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":387},
    {"road":"1st Class 11","yard":"1st Classification","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":357},
    {"road":"1st Class 12","yard":"1st Classification","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":331},

    # SECOND CLASSIFICATION

    {"road":"2nd Class 13","yard":"2nd Classification","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":372},
    {"road":"2nd Class 14","yard":"2nd Classification","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":435},
    {"road":"2nd Class 15","yard":"2nd Classification","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":414},
    {"road":"2nd Class 16","yard":"2nd Classification","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":388},
    {"road":"2nd Class 17","yard":"2nd Classification","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":357},
    {"road":"2nd Class 18","yard":"2nd Classification","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":335},
    {"road":"2nd Class 19","yard":"2nd Classification","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":304},
    {"road":"2nd Class 20","yard":"2nd Classification","status":"Empty","train":"","operator":"","type": "","length":0,"arrival":"","departure":"","capacity":282}
]

# -----------------------------
# SAVE FUNCTION
# -----------------------------

def save_yard():
    def log_movement(message):

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = f"{timestamp} - {message}"

    log_movement(
        f"ALLOCATED {train} TO {road_name}"
    )
    log_movement(
        f"REMOVED {train} FROM {road['road']}"
    )
    log_movement(
        f"BOOKED OUT {road_name}"
    )
    log_movement(
        f"RETURNED TO SERVICE {road_name}"
    )
    log_movement(
        f"ARRIVED {arrival['train']} INTO {planned_road}"
    )
    with open("movement_log.txt", "a") as file:

        file.write(entry + "\n")

    with open("yard.json", "w") as file:

        json.dump(roads, file, indent=4)
# -----------------------------
# VIEW YARD
# -----------------------------

def view_yard():

    print()

    print(
        f"{'ROAD':<15}"
        f"{'STATUS':<15}"
        f"{'TRAIN':<10}"
        f"{'TYPE':<15}"
        f"{'OPERATOR':<10}"
        f"{'ARR':<8}"
        f"{'DEP':<8}"
        f"{'CAP'}"
    )

    print("-" * 90)

    for road in roads:

        print(
            f"{road['road']:<15}"
            f"{road['status']:<15}"
            f"{road['train']:<10}"
            f"{road['type']:<15}"
            f"{road['operator']:<10}"
            f"{road['arrival']:<8}"
            f"{road['departure']:<8}"
            f"{road['capacity']}m"
        )
def show_statistics():

    occupied = 0
    empty = 0
    booked = 0
    reserved = 0

    for road in roads:

        if road["status"] == "Occupied":
            occupied += 1

        elif road["status"] == "Empty":
            empty += 1

        elif road["status"] == "Booked Out":
            booked += 1

        elif road["status"] == "Reserved":
            reserved += 1

    total = len(roads)

    utilisation = round(
        (occupied / total) * 100
    )

    print()
    print("YARD STATISTICS")
    print("=" * 40)

    print("Total Roads:", total)
    print("Occupied:", occupied)
    print("Empty:", empty)
    print("Booked Out:", booked)
    print("Reserved:", reserved)
    print("Utilisation:", utilisation, "%")
def find_train():

    train_search = input("Train ID: ")

    found = False

    for road in roads:

        if road["train"] == train_search:

            found = True

            print()
            print("TRAIN FOUND")
            print("=" * 40)
            print("Road:", road["road"])
            print("Yard:", road["yard"])
            print("Operator:", road["operator"])
            print("Type:", road["type"])
            print("Length:", road["length"])

    if not found:

        print("Train not found")
def show_movement_log():

    print()
    print("MOVEMENT LOG")
    print("=" * 40)

    if len(movements) == 0:

        print("No movements recorded")

    else:

        for movement in movements:

            print(movement)
def show_expected_arrivals():

    print()
    print("EXPECTED ARRIVALS")
    print("=" * 60)

    for arrival in expected_arrivals:

        print(
            f"{arrival['train']:<10}"
            f"{arrival['operator']:<10}"
            f"{arrival['eta']:<10}"
            f"{arrival['planned_road']}"
        )
def occupancy_report():

    occupied_length = 0
    total_capacity = 0

    print()
    print("YARD OCCUPANCY REPORT")
    print("=" * 40)

    for road in roads:

        total_capacity += road["capacity"]

        if road["status"] == "Occupied":

            occupied_length += road["length"]

            print(
                road["road"],
                "-",
                road["train"],
                "-",
                str(road["length"]) + "m"
            )

    print()

    print("Occupied Length:", occupied_length)
    print("Total Capacity:", total_capacity)

    utilisation = round(
        (occupied_length / total_capacity) * 100
    )

    print(
        "Length Utilisation:",
        utilisation,
        "%"
    )
def operator_summary():

    operators = {}

    for road in roads:

        if road["operator"] != "":

            if road["operator"] not in operators:

                operators[road["operator"]] = 0

            operators[road["operator"]] += 1

    print()
    print("OPERATOR SUMMARY")
    print("=" * 40)

    for operator in operators:

        print(
            operator,
            "-",
            operators[operator],
            "train(s)"
        )
def yard_area_summary():

    areas = {}

    for road in roads:

        yard = road["yard"]

        if yard not in areas:

            areas[yard] = 0

        if road["status"] == "Occupied":

            areas[yard] += 1

    print()
    print("YARD AREA SUMMARY")
    print("=" * 40)

    for yard in areas:

        print(
            yard,
            "-",
            areas[yard],
            "occupied road(s)"
        )
def train_type_summary():

    types = {}

    for road in roads:

        if road["type"] != "":

            if road["type"] not in types:

                types[road["type"]] = 0

            types[road["type"]] += 1

    print()
    print("TRAIN TYPE SUMMARY")
    print("=" * 40)

    for train_type in types:

        print(
            train_type,
            "-",
            types[train_type],
            "train(s)"
        )
def capacity_hotspots():

    print()
    print("CAPACITY HOTSPOTS")
    print("=" * 40)

    for road in roads:

        if road["status"] == "Occupied":

            usage = round(
                (road["length"] /
                 road["capacity"]) * 100
            )

            if usage >= 80:

                print(
                    road["road"],
                    "-",
                    str(usage) + "%"
                )
def empty_road_report():

    print()
    print("EMPTY ROADS")
    print("=" * 40)

    for road in roads:

        if road["status"] == "Empty":

            print(
                road["road"],
                "-",
                str(road["capacity"]) + "m"
            )
def stable_train():

    train = input("Train ID: ")
    operator = input("Operator: ")

    print()
    print("TRAIN TYPES")
    print("Intermodal")
    print("Grain")
    print("Steel")
    print("Container")
    print("Ballast")
    print("Infrastructure")
    print("Locomotive")
    print()

    train_type = input("Train Type: ")

    locomotives = input("Locomotives: ")
    wagons = int(input("Number Of Wagons: "))
    length = int(input("Train Length (m): "))
    arrival = input("Arrival Time: ")
    departure = input("Departure Time: ")

    conflict = False

    for road in roads:

        if road["train"] == train:

            print(
                "WARNING - Train already stabled in",
                road["road"]
            )

            conflict = True
            break

    if conflict:
        return

    print()
    print("SUITABLE ROADS")
    print("=" * 40)

    suitable_roads = []

    for road in roads:

        if road["status"] == "Empty":

            if road["capacity"] >= length:

                suitable_roads.append(road)

    suitable_roads.sort(
        key=lambda x: x["capacity"]
    )

    for road in suitable_roads:

        print(
            f"{road['yard']:<20}"
            f"{road['road']:<15}"
            f"{road['capacity']}m"
        )

    road_name = input("\nAllocate To Road: ")

    allocated = False

    for road in roads:

        if road["road"] == road_name:

            if road["status"] != "Empty":

                print("Road unavailable")
                return

            if length > road["capacity"]:

                print("Train exceeds road capacity")
                return

            road["status"] = "Occupied"
            road["train"] = train
            road["operator"] = operator
            road["type"] = train_type
            road["locomotives"] = locomotives
            road["wagons"] = wagons
            road["length"] = length
            road["arrival"] = arrival
            road["departure"] = departure

            save_yard()

            usage = round(
                (length / road["capacity"]) * 100
            )

            print(
                "Road Utilisation:",
                usage,
                "%"
            )

            if usage >= 90:

                print(
                    "WARNING - Road Capacity Nearly Exhausted"
                )

            movements.append(
                f"ALLOCATED {train} TO {road['road']}"
            )

            print("Train allocated")

            allocated = True
            break

    if not allocated:

        print("Allocation failed")
def remove_train():

    train = input("Train ID: ")

    for road in roads:

        if road["train"] == train:

            road["status"] = "Empty"
            road["train"] = ""
            road["operator"] = ""
            road["type"] = ""
            road["locomotives"] = ""
            road["wagons"] = 0
            road["length"] = 0
            road["arrival"] = ""
            road["departure"] = ""

            save_yard()

            movements.append(
                f"REMOVED {train} FROM {road['road']}"
            )

            print("Train removed")

            return

    print("Train not found")
def book_out_road():

    road_name = input("Road: ")

    for road in roads:

        if road["road"] == road_name:

            road["status"] = "Booked Out"

            save_yard()

            movements.append(
                f"BOOKED OUT {road_name}"
            )

            print("Road booked out")

            return

    print("Road not found")
def return_road_to_service():

    road_name = input("Road: ")

    for road in roads:

        if road["road"] == road_name:

            road["status"] = "Empty"

            save_yard()

            movements.append(
                f"RETURNED TO SERVICE {road_name}"
            )

            print("Road returned")

            return

    print("Road not found")
def reserve_road():

    road_name = input("Road: ")
    train = input("Reserved For Train: ")

    for road in roads:

        if road["road"] == road_name:

            road["status"] = "Reserved"
            road["train"] = train

            save_yard()

            movements.append(
                f"RESERVED {road_name} FOR {train}"
            )

            print(
                road_name,
                "reserved for",
                train
            )

            return

    print("Road not found")
def depart_train():

    train = input("Train ID Departing: ")

    for road in roads:

        if road["train"] == train:

            road["status"] = "Empty"
            road["train"] = ""
            road["operator"] = ""
            road["type"] = ""
            road["locomotives"] = ""
            road["wagons"] = 0
            road["length"] = 0
            road["arrival"] = ""
            road["departure"] = ""

            save_yard()

            movements.append(
                f"DEPARTED {train} FROM {road['road']}"
            )

            print(
                train,
                "departed from",
                road["road"]
            )

            return

    print("Train not found")
# -----------------------------
# SUPPORT DATA
# -----------------------------

movements = []

expected_arrivals = [
    {
        "train": "6MC2",
        "operator": "SCT",
        "eta": "14:10",
        "planned_road": "Road 3"
    },
    {
        "train": "9141",
        "operator": "PN",
        "eta": "16:25",
        "planned_road": "Road 1"
    }
]

# -----------------------------
# MAIN LOOP
# -----------------------------

while True:

    print()
    print("=" * 60)
    print("TOTTENHAM FREIGHT YARD")
    print("=" * 60)

    print("1  - View Yard")
    print("2 - Suitable Road Finder")
    print("3  - Stable Train")
    print("4  - Remove Train")
    print("5  - Book Out Road")
    print("6  - Return Road To Service")
    print("7 - Train Register")
    print("8  - Statistics")
    print("9  - Find Train")
    print("10  - Movement Log")
    print("11  - Expected Arrivals")
    print("12 - Add Expected Arrival")
    print("13 - Arrive Expected Train")
    print("14 - Yard Occupancy Report")
    print("15 - Reserve Road")
    print("16 - Depart Train")
    print("17 - Train Detail Report")
    print("18 - Yard Diagram")
    print("19 - Operator Summary")
    print("20 - Yard Area Summary")
    print("21 - Train Type Summary")
    print("22 - Capacity Hotspots")
    print("23 - Empty Road Report")
    print("24 - Dailt Train Plan")
    print("25 - Exit")

    choice = input("\nSelect Option: ")

    # -------------------------
    # VIEW YARD
    # -------------------------

    if choice == "1":

        view_yard()
    # -------------------------
    # SUITABLE ROAD FINDER
    # -------------------------
    elif choice == "22":

        length = int(input("Train Length (m): "))

        print()
        print("SUITABLE ROADS")
        print("=" * 40)

        found = False

        for road in roads:

            if road["status"] == "Empty":

                if road["capacity"] >= length:

                    found = True

                    print(
                        f"{road['road']:<15}"
                        f"{road['capacity']}m"
                    )

        if not found:

            print("No suitable roads available")
    # -------------------------
    # STABLE TRAIN
    # -------------------------

    elif choice == "3":

        stable_train()

    # -------------------------
    # REMOVE TRAIN
    # -------------------------

    elif choice == "4":

        remove_train()

    # -------------------------
    # BOOK OUT ROAD
    # -------------------------

    elif choice == "5":

        book_out_road()

    # -------------------------
    # RETURN ROAD TO SERVICE
    # -------------------------

    elif choice == "6":

        return_road_to_service()
    # -------------------------
    # TRAIN REGISTER
    # -------------------------

    elif choice == "7":

        print()
        print("=" * 120)
        print("TRAIN REGISTER")
        print("=" * 120)

        print(
            f"{'TRAIN':<10}"
            f"{'TYPE':<15}"
            f"{'OPERATOR':<10}"
            f"{'ROAD':<15}"
            f"{'YARD':<20}"
            f"{'LENGTH':<10}"
            f"{'ARRIVAL':<10}"
            f"{'DEPARTURE'}"
        )

        print("-" * 120)

        trains_found = 0

        sorted_roads = sorted(
            roads,
            key=lambda x: (x["yard"], x["road"])
        )

        for road in sorted_roads:

            if road["status"] == "Occupied":

                trains_found += 1

                print(
                    f"{road['train']:<10}"
                    f"{road['type']:<15}"
                    f"{road['operator']:<10}"
                    f"{road['road']:<15}"
                    f"{road['yard']:<20}"
                    f"{str(road['length']) + 'm':<10}"
                    f"{str(round((road['length'] / road['capacity']) * 100)) + '%':<8}"
                    f"{road['arrival']:<10}"
                    f"{road['departure']}"
                    f"{'UTIL':<8}"
                )

        if trains_found == 0:

            print("No trains currently stabled.")
    # -------------------------
    # STATISTICS
    # -------------------------

    elif choice == "8":

        show_statistics()

    # -------------------------
    # FIND TRAIN
    # -------------------------

    elif choice == "9":

        find_train()

    # -------------------------
    # MOVEMENT LOG
    # -------------------------

    elif choice == "10":

        show_movement_log()

    # -------------------------
    # EXPECTED ARRIVALS
    # -------------------------

    elif choice == "11":

        show_expected_arrivals()

    # -------------------------
    # ADD EXPECTED ARRIVAL
    # -------------------------

    elif choice == "12":

        train = input("Train ID: ")
        operator = input("Operator: ")
        eta = input("ETA: ")
        planned_road = input("Planned Road: ")

        expected_arrivals.append(
            {
                "train": train,
                "operator": operator,
                "eta": eta,
                "planned_road": planned_road
            }
        )

        print("Arrival added")

    # -------------------------
    # ARRIVE EXPECTED TRAIN
    # -------------------------

    elif choice == "13":

        train_id = input("Train ID Arriving: ")

        for arrival in expected_arrivals:

            if arrival["train"] == train_id:

                print(
                    arrival["train"],
                    "arrived into",
                    arrival["planned_road"]
                )

                movements.append(
                    f"ARRIVED {arrival['train']}"
                )

                expected_arrivals.remove(arrival)

                break

    # -------------------------
    # OCCUPANCY REPORT
    # -------------------------

    elif choice == "14":

        occupancy_report()

    # -------------------------
    # RESERVE ROAD
    # -------------------------

    elif choice == "15":

        reserve_road()
    # -------------------------
    # DEPART TRAIN
    # -------------------------
    elif choice == "16":

        depart_train()
    # -------------------------
    # Train Detail Report
    # -------------------------
    elif choice == "17":
        train_search = input("Train ID: ")
        for road in roads:
            if road["train"] == train_search:

                print()
                print("TRAIN DETAILS")
                print("=" * 40)
                usage = round(
                    (road["length"] / road["capacity"]) * 100
                )

                print("Train:", road["train"])
                print("Operator:", road["operator"])
                print("Type:", road["type"])
                print("Direction:", road["direction"])
                print("Locomotives:", road["locomotives"])
                print("Wagons:", road["wagons"])
                print("Length:", road["length"], "m")
                print("Road:", road["road"])
                print("Yard:", road["yard"])
                print("Road Capacity:", road["capacity"], "m")
                print("Road Utilisation:", usage, "%")
                print("Arrival:", road["arrival"])
                print("Departure:", road["departure"])
                break
    # -------------------------
    # Yard Diagram
    # -------------------------
    elif choice == "18":

        print()
        print("=" * 60)
        print("TOTTENHAM FREIGHT YARD")
        print("=" * 60)

        for road in roads:

            if road["yard"] != current_yard:

                current_yard = road["yard"]

                print()
                print(current_yard.upper())
                print("-" * 40)

            if road["status"] == "Occupied":

                usage = round(
                    (road["length"] / road["capacity"]) * 100
                )

                if usage >= 90:
                    rating = "FULL"

                elif usage >= 70:
                    rating = "HIGH"

                elif usage >= 40:
                    rating = "MEDIUM"

                else:
                    rating = "LOW"

                print(
                    f"{RED}"
                    f"{road['road']:<15}"
                    f"[OCCUPIED] "
                    f"{road['train']:<10} "
                    f"{usage}% "
                    f"{rating}"
                    f"{RESET}"
                )

            elif road["status"] == "Reserved":

                print(
                    f"{YELLOW}"
                    f"{road['road']:<15}"
                    f"[RESERVED] "
                    f"{road['train']}"
                    f"{RESET}"
                )

            elif road["status"] == "Booked Out":

                print(
                    f"{GREY}"
                    f"{road['road']:<15}"
                    f"[BOOKED OUT]"
                    f"{RESET}"
                )

            else:

                print(
                    f"{GREEN}"
                    f"{road['road']:<15}"
                    f"[EMPTY]"
                    f"{RESET}"
                )
    # -------------------------
    # Operator Summary
    # -------------------------
    elif choice == "19":

        operator_summary()
    # -------------------------
    # Yard Area Summary
    # -------------------------
    elif choice == "20":

        yard_area_summary()
    # -------------------------
    # Train Type Summary
    # -------------------------
    elif choice == "21":

        train_type_summary()
    # -------------------------
    # CAPACITY HOTSPOTS
    # -------------------------
    elif choice == "22":

        capacity_hotspots()
    # -------------------------
    # EMPTY ROAD REPORT
    # -------------------------
    elif choice == "23":

        empty_road_report()
    # -------------------------
    # DAILY TRAIN PLAN
    # -------------------------
    elif choice == "24":

        active_trains = []

        for road in roads:

            if road["status"] == "Occupied":

                active_trains.append(road)

        active_trains.sort(
            key=lambda x: x["departure"]
        )

        print()
        print("DAILY TRAIN PLAN")
        print("=" * 40)

        for train in active_trains:

            print(
                train["departure"],
                train["train"],
                train["road"]
            )
    # -------------------------
    # EXIT
    # -------------------------

    elif choice == "25":

        print("Goodbye")

        break

    else:

        print("Invalid Option")
