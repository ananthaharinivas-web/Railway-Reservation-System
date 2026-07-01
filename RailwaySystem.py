from RailwayData import Train_Config, Passenger_Database

print("=============================================================================")
print("\t\t**--- Indian Express Railway Sim ---**")

while True:
    print("\n\n")
    print("\t\t=======---- Railway Reservation Dashboard ----=======")
    print("===========================================================================")
    print("1.) Create Passenger & Book Ticket")
    print("2.) Cancel Ticket")
    print("3.) View Ticket Profile")
    print("4.) View All Passengers")
    print("5.) Check Seat Availability")
    print("6.) Search Passenger by Name")
    print("7.) Total Revenue Generated")
    print("0.) Exit")
    try:
        choice = int(input("Enter Here : "))
    except ValueError:
        print("Invalid input. Please enter a valid menu number.")
        continue
    if choice == 1:
        try:
            if Train_Config["Available_Seats"] <= 0:
                print("Error: Train is fully booked! No seats available.")
                print("================================================================")
                continue
            name = input("Enter Passenger Name: ")
            age = int(input("Enter Age: "))
            gender = input("Enter Gender (Male/Female/Other): ")
            new_ticket_id = max(Passenger_Database.keys()) + 1 if Passenger_Database else 1001
            taken_seats = [info["Seat_No"] for info in Passenger_Database.values()]
            assigned_seat = 1
            while assigned_seat in taken_seats:
                assigned_seat += 1
            Passenger_Database[new_ticket_id] = {
                "Passenger_Name": name,
                "Age": age,
                "Gender": gender,
                "Seat_No": assigned_seat,
                "Status": "Confirmed"
            }
            Train_Config["Available_Seats"] -= 1
            with open("RailwayData.py", "w") as file:
                file.write("# RailwayData.py\n\n")
                file.write(f"Train_Config = {Train_Config}\n\n")
                file.write("Passenger_Database = {\n")
                for t_id, info in Passenger_Database.items():
                    file.write(f"    {t_id}: {{\n")
                    file.write(f'        "Passenger_Name": "{info["Passenger_Name"]}",\n')
                    file.write(f'        "Age": {info["Age"]},\n')
                    file.write(f'        "Gender": "{info["Gender"]}",\n')
                    file.write(f'        "Seat_No": {info["Seat_No"]},\n')
                    file.write(f'        "Status": "{info["Status"]}"\n')
                    file.write("    },\n")
                file.write("}\n")
            print(f"Successfully Booked! Ticket ID: {new_ticket_id} | Assigned Seat: {assigned_seat}")
            print("================================================================")
            with open("railway_logs.txt", "a") as log_file:
                log_file.write(f"Ticket: {new_ticket_id} | Booked | Name: {name} | Seat: {assigned_seat}\n")
        except ValueError:
            print("Invalid Input. Age must be a numerical integer.")
    elif choice == 2:
        try:
            cancel_id = int(input("Enter Ticket ID to Cancel: "))
            if cancel_id not in Passenger_Database:
                print("Error: Ticket ID not found in database!")
                print("================================================================")
                continue
            passenger = Passenger_Database[cancel_id]
            freed_seat = passenger["Seat_No"]
            passenger_name = passenger["Passenger_Name"]
            del Passenger_Database[cancel_id]
            Train_Config["Available_Seats"] += 1
            with open("RailwayData.py", "w") as file:
                file.write("# RailwayData.py\n\n")
                file.write(f"Train_Config = {Train_Config}\n\n")
                file.write("Passenger_Database = {\n")
                for t_id, info in Passenger_Database.items():
                    file.write(f"    {t_id}: {{\n")
                    file.write(f'        "Passenger_Name": "{info["Passenger_Name"]}",\n')
                    file.write(f'        "Age": {info["Age"]},\n')
                    file.write(f'        "Gender": "{info["Gender"]}",\n')
                    file.write(f'        "Seat_No": {info["Seat_No"]},\n')
                    file.write(f'        "Status": "{info["Status"]}"\n')
                    file.write("    },\n")
                file.write("}\n")
            print(f"Ticket ID {cancel_id} successfully cancelled. Seat {freed_seat} is now vacant.")
            print("Refund processed successfully.")
            print("================================================================")
            with open("railway_logs.txt", "a") as log_file:
                log_file.write(f"Ticket: {cancel_id} | Cancelled | Name: {passenger_name} | Freed Seat: {freed_seat}\n")
        except ValueError:
            print("Invalid Input. Ticket ID must be an integer.")
    elif choice == 3:
        try:
            search_id = int(input("Enter Ticket ID: "))
            print("\n=== Ticket Profile Information ===")
            if search_id in Passenger_Database:
                info = Passenger_Database[search_id]
                print(f"Ticket ID: {search_id}")
                print(f"Name: {info['Passenger_Name']}")
                print(f"Age: {info['Age']} | Gender: {info['Gender']}")
                print(f"Assigned Seat Number: {info['Seat_No']}")
                print(f"Reservation Status: {info['Status']}")
            else:
                print("No ticket manifest matches that reference ID.")
            print("================================================================")
        except ValueError:
            print("Invalid Input. ID must be numerical.")
    elif choice == 4:
        print("\n=== Current Passenger Manifest ===")
        if not Passenger_Database:
            print("No passengers currently booked on this journey.")
        for t_id, info in Passenger_Database.items():
            print(f"ID: {t_id} | Name: {info['Passenger_Name']} | Age: {info['Age']} | Seat: {info['Seat_No']} | Status: {info['Status']}")
        print("================================================================")
    elif choice == 5:
        print("\n=== Current Berth Allocations ===")
        booked = Train_Config["Total_Seats"] - Train_Config["Available_Seats"]
        print(f"Total Capacity: {Train_Config['Total_Seats']} Seats")
        print(f"Confirmed Bookings: {booked} Seats Allocated")
        print(f"Vacant Berths Remaining: {Train_Config['Available_Seats']} Seats Left")
        print("================================================================")
    elif choice == 6:
        search_name = input("Enter Passenger Name to search: ").lower()
        print("\n=== Search Queries Found ===")
        found = False
        for t_id, info in Passenger_Database.items():
            if search_name in info["Passenger_Name"].lower():
                print(f"Match Found -> Ticket ID: {t_id} | Name: {info['Passenger_Name']} | Seat No: {info['Seat_No']}")
                found = True
        if not found:
            print("No passengers matching that name query found aboard.")
        print("================================================================")
    elif choice == 7:
        total_tickets = len(Passenger_Database)
        revenue = total_tickets * Train_Config["Ticket_Price"]
        print(f"\n=== Financial Audit Manifest ===")
        print(f"Active Tickets Issued: {total_tickets}")
        print(f"Price per Berth: Rs. {Train_Config['Ticket_Price']}")
        print(f"Total Live Gross Revenue Generated: Rs. {revenue}")
        print("================================================================")
    elif choice == 0:
        print("================================================================")
        print("\t\tChose us again Thank you ")
        break
    else:
        print("Invalid Choice. Choose options between 0-7.")