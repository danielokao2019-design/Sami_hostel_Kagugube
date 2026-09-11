# **********************************************************************************
# Group 2 
# 1. Ranja Emmanuel Richard VU-BIT-2603-0939-DAY
# 2. ⁠Nuwagaba wilber VU-BIT-2603-1868-DAY
# 3. Kyeyune Gift Emmanuel VU-BCD-2603-1640-DAY
# 4. Odongo Emmanuel Lumumba  VU-BIT-2603-0625-DAY
# 5. Nankwastya Bennah VU-BSF-2603-3654-DAY
# 6. OKAO DANIEL VU-BIT-2603-1427-DAY                       
# 7. Opoka Taikun Denish VU-BIT-2603-2502-DAY
# 8. Nahishakiye Fiston Donvense VU-BIT-2603-3122-DAY
# 9. Abdus Sazid  VU-BIT-2603-1812-DAY
# 10. KATUMBA JOSHUA GEORGE VU-BCS-2603-2017-DAY

# SAMI HOSTEL KAGUGUBE - HOSTEL ROOM BOOKING & FEES MANAGEMENT SYSTEM
# Coursework: Programming Fundamentals (FST Year 1, Trimester 2)
# Lecturer: Kinyonyi David Hope
# Institution: Victoria University Kampala
# ******************************************************************************


#Importing libraries and data set up 
import json                 
import os                 


# DATA SETUP & FILE PERSISTENCE
# File paths and initial state variables
# ********************************************
DATA_FILE = "sami_hostel_data.json"

# Sami Hostel Layout: 4 Levels, 10 Rooms per Level, 2 Students per Room
TOTAL_LEVELS = 4
ROOMS_PER_LEVEL = 10
CAPACITY_PER_ROOM = 2

# Core Data Structures
rooms_data = {}      # Format: {"Level 1": {"101": {"capacity": 2, "occupants": ["VU-BIT-222-222-DAY"]}}}
students_data = {}   # Format: {"VU-BIT-222-222-DAY": {"name": "Okao", "level": "Level 1", "room": "101", "total_fee": 500000, "paid_fee": 450000}}


# Creating Hostel Rooms
def initialize_default_rooms():
    """Sets up the initial 4 levels, 10 rooms per level structure."""    #doc string
    grid = {}
    for level in range(1, TOTAL_LEVELS + 1):               
        level_name = f"Level {level}"
        grid[level_name] = {}
        for r in range(1, ROOMS_PER_LEVEL + 1): 
            # Room numbering: 101-110, 201-210, 301-310, 401-410
            room_number = f"{level}{r:02d}"
            grid[level_name][room_number] = {
                "capacity": CAPACITY_PER_ROOM,
                "occupants": []
            }
    return grid

# loading existing data
def load_data():
    """Loads system state from JSON file or initializes default structure if missing/corrupted."""
    global rooms_data, students_data           
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                payload = json.load(file)
                rooms_data = payload.get("rooms", initialize_default_rooms())
                students_data = payload.get("students", {})
                print("**************************************************")
                print("* Data loaded successfully from persistent storage.*")
                print("**************************************************")
        except (json.JSONDecodeError, OSError):
            print("**************************************************")
            print("* WARNING: File damaged or corrupted.            *")
            print("* Initializing clean system state...             *")
            print("**************************************************")
            rooms_data = initialize_default_rooms()
            students_data = {}
    else:
        print("**************************************************")
        print("* No existing database found. New setup created.  *")
        print("**************************************************")
        rooms_data = initialize_default_rooms()
        students_data = {}

# Saving data
def save_data():
    """Saves current state of rooms and students to a JSON file."""
    try:
        payload = {
            "rooms": rooms_data,
            "students": students_data
        }
        with open(DATA_FILE, "w") as file:
            json.dump(payload, file, indent=4)
        print("**************************************************")
        print("* Data successfully saved to file.               *")
        print("**************************************************")
    except OSError as err:
        print(f"* ERROR: Unable to save data: {err} *")

# ------------------------------------------------------------------------------
# CORE SYSTEM FUNCTIONS
# ------------------------------------------------------------------------------


# Occupancy overview
def print_occupancy_overview():
    """Prints a summary of total capacity vs current occupancy across levels."""
    print("\n**************************************************")
    print("*           CURRENT OCCUPANCY OVERVIEW           *")
    print("**************************************************")
    total_capacity = TOTAL_LEVELS * ROOMS_PER_LEVEL * CAPACITY_PER_ROOM
    total_occupied = 0

    for level, rooms in rooms_data.items():
        level_occupied = sum(len(details["occupants"]) for details in rooms.values())  #how many in this level
        total_occupied += level_occupied                        # Add this level's count to the grand total
        level_capacity = ROOMS_PER_LEVEL * CAPACITY_PER_ROOM
        print(f"* {level}: {level_occupied}/{level_capacity} beds taken")

    print("--------------------------------------------------")
    print(f"* Total Hostel Occupancy: {total_occupied}/{total_capacity} beds")
    print("**************************************************\n")


# Student registration and room allocation
def register_and_allocate_student():
    """Handles new student registration, room validation, and allocation."""
    print("\n**************************************************")
    print("*         STUDENT REGISTRATION & ALLOCATION      *")
    print("**************************************************")
    
    reg_no = input("Enter Student Registration Number: ").strip().upper()
    if not reg_no:
        print("* Error: Registration Number cannot be empty. *")
        return
    if reg_no in students_data:
        print("* Error: Student with this Registration Number already exists. *")
        return

    name = input("Enter Student Full Name: ").strip().title()
    if not name:
        print("* Error: Name cannot be empty. *")
        return

    # Select Level
    print("Available Levels: Level 1, Level 2, Level 3, Level 4")
    level_choice = input("Enter Level (e.g., Level 1): ").strip().title()
    if level_choice not in rooms_data:
        print("* Error: Invalid level selection. *")
        return

    # Select Room
    room_no = input("Enter Room Number (e.g., 101, 205): ").strip()
    if room_no not in rooms_data[level_choice]:
        print(f"* Error: Room {room_no} does not exist on {level_choice}. *")
        return

    target_room = rooms_data[level_choice][room_no]
    if len(target_room["occupants"]) >= target_room["capacity"]:
        print(f"\n* ALLOCATION REJECTED: Room {room_no} on {level_choice} is FULL. *")
        print(f"* Maximum capacity is {target_room['capacity']} students per room. *")
        return

    # Fee entry
    try:
        total_fee = float(input("Enter Total Term Fee (UGX): "))
        if total_fee <= 0:
            print("* Error: Fee must be a positive number. *")
            return
    except ValueError:
        print("* Error: Invalid fee input. Enter numbers only. *")
        return

    # Process successful allocation
    target_room["occupants"].append(reg_no)
    students_data[reg_no] = {
        "name": name,
        "level": level_choice,
        "room": room_no,
        "total_fee": total_fee,
        "paid_fee": 0.0
    }
    
    save_data()
    print("\n**************************************************")
    print(f"* SUCCESS: {name} ({reg_no}) allocated to {level_choice}, Room {room_no}. *")
    print("**************************************************")

# Fee payment management
def record_fee_payment():                                                   # defining function record_fee_payment
    """Records full or partial fee payments against a student account."""   # Doc String
    print("\n**************************************************")           # Design to specify headline
    print("*              RECORD FEE PAYMENT                *")
    print("**************************************************")
    reg_no = input("Enter Student Registration Number: ").strip().upper()    # Upper converts to upper case, strip removes unnecessary spaces

    if reg_no not in students_data:                                          # Making sure student exists in the database
        print("* Error: Student record not found. *")
        return                                                               # Returns to main menu

    student = students_data[reg_no]                                          # means student record exist, square brackets for dictionary look-up
    balance = student["total_fee"] - student["paid_fee"]

    print(f"* Student: {student['name']}")                                   # f tells python we want to insert a value in the string. The curly bracket contains the value you want  to insert, name means accessing name field in the dictionary
    print(f"* Total Fee: UGX {student['total_fee']:,.2f}")                   #:,.2f formating the number for readability. The , separates 1000s while .2f diplays the number to 2 decimal places
    print(f"* Paid so far: UGX {student['paid_fee']:,.2f}")
    print(f"* Outstanding Balance: UGX {balance:,.2f}")
    print("--------------------------------------------------")

    if balance <= 0:
        print("* This student has already cleared all fees. *")
        return

    try:
        amount = float(input("Enter Payment Amount (UGX): "))
        if amount <= 0:
            print("* Error: Payment amount must be greater than zero. *")
            return
        if amount > balance:
            print(f"* Warning: Payment exceeds balance of UGX {balance:,.2f}. Adjusting to cover balance exact. *")
            amount = balance
    except ValueError:
        print("* Error: Invalid numeric entry. *")
        return

    student["paid_fee"] += amount
    new_balance = student["total_fee"] - student["paid_fee"]

    save_data()
    print("\n**************************************************")
    print(f"* PAYMENT RECORDED: UGX {amount:,.2f}")
    print(f"* Remaining Balance for {student['name']}: UGX {new_balance:,.2f}")
    print("**************************************************")

# Student search Function
def search_student():
    """Searches for a student by full name, partial name, or registration number."""
    print("\n**************************************************")
    print("*                 SEARCH STUDENT                 *")
    print("**************************************************")
    query = input("Enter Name or Registration Number to search: ").strip().lower()

    if not query:
        print("* Search query cannot be blank. *")
        return

    matches = []
    for reg, details in students_data.items():
        if query in reg.lower() or query in details["name"].lower():
            matches.append((reg, details))

    if not matches:
        print("* No matching records found. *")
        return

    print(f"\nFound {len(matches)} matching student(s):")
    print("--------------------------------------------------")
    for reg, details in matches:
        bal = details["total_fee"] - details["paid_fee"]
        print(f"* Reg No: {reg}")
        print(f"* Name:   {details['name']}")
        print(f"* Room:   {details['level']}, Room {details['room']}")
        print(f"* Status: Paid: UGX {details['paid_fee']:,.2f} | Due: UGX {bal:,.2f}")
        print("--------------------------------------------------")

# Report Generation
def generate_reports():
    """Generates occupancy reports or fee defaulter lists."""
    print("\n**************************************************")
    print("*               REPORTS GENERATION               *")
    print("**************************************************")
    print("* 1. Full Occupancy Report                       *")
    print("* 2. Fee Defaulters List                         *")
    print("**************************************************")
    sub_choice = input("Select Option (1 or 2): ").strip()

    if sub_choice == "1":
        print("\n**************************************************")
        print("*            FULL HOSTEL OCCUPANCY REPORT        *")
        print("**************************************************")
        for level, rooms in rooms_data.items():
            print(f"\n--- {level} ---")
            for room_no, details in rooms.items():
                occ_count = len(details["occupants"])
                names = [students_data[r]["name"] for r in details["occupants"] if r in students_data]
                student_str = ", ".join(names) if names else "Empty"
                print(f"  Room {room_no} [{occ_count}/{details['capacity']}]: {student_str}")

    elif sub_choice == "2":
        try:
            threshold = float(input("Enter minimum outstanding balance threshold (UGX): "))
        except ValueError:
            print("* Error: Invalid threshold input. *")
            return

        print("\n**************************************************")
        print(f"*   FEE DEFAULTERS REPORT (Due > UGX {threshold:,.2f})  *")
        print("**************************************************")
        defaulter_count = 0

        for reg, details in students_data.items():
            bal = details["total_fee"] - details["paid_fee"]
            if bal > threshold:
                defaulter_count += 1
                print(f"* {details['name']} ({reg})")
                print(f"  Room: {details['level']} {details['room']} | Balance: UGX {bal:,.2f}")
                print("--------------------------------------------------")

        if defaulter_count == 0:
            print("* No students found exceeding the debt threshold. *")
        else:
            print(f"* Total Defaulters Found: {defaulter_count} *")
    else:
        print("* Invalid report selection. *")

# ------------------------------------------------------------------------------
# DRIVER PROGRAMME & MENU
# ------------------------------------------------------------------------------

# Main menu, program flow                                                (#This is a comment. Anything after # on a line is ignored by Python.Comments are written for humans to explain what the code is doing.)
def main():                                                              # def means define a function. A function is a named block of code that performs a particular task.  # “The code below controls the main menu and how the program flows.” The colon tells Python: “The block of code belonging to this function starts here.” Everything underneath it must be indented.
    """Main execution loop for the hostel warden."""                     #This is called a docstring. A docstring describes what a function does. Here it says: "Main execution loop for the hostel warden." In simple terms: This function controls the main menu that the hostel warden uses. The triple quotation marks: """ """allow Python to store a longer description.# The main() function contains the main part of your hostel management system.
    load_data()                                                          # This tells Python to call another function called: load_data()
    
    while True:                                                          # while means: Repeat something while a condition is true. True is a Boolean value. Since True is always true, this creates an infinite loop.(Keep displaying the hostel menu again and again until we tell Python to stop.)
        print("\n**************************************************")    # Prints the top border
        print("*           SAMI HOSTEL KAGUGUBE SYSTEM          *")      # Prints the heading (Hostel management System Name)
        print("**************************************************")      # Prints the bottom border
        print("* 1. View Hostel Occupancy Overview              *")       
        print("* 2. Register Student & Allocate Room            *")
        print("* 3. Record Fee Payment                          *")
        print("* 4. Search Student                              *")
        print("* 5. Generate Reports                            *")
        print("* 6. Save & Exit                                 *")
        print("**************************************************")       #Extreme Bottom border
        
        choice = input("Enter your choice (1-6): ").strip()               # Allows us to input a choice between 1 and 6. .strip() removes unnecessary spaces from the beginning and end of the user's input.
        
        if choice == "1":
            print_occupancy_overview()                                    # Commands python to print occupancy overview once one selects option 1
        elif choice == "2":
            register_and_allocate_student()                               # Commands python to register and allocate student once one selects option 2
        elif choice == "3":
            record_fee_payment()                                          # Commands python to record fee payment once one selects option 3
        elif choice == "4":
            search_student()                                              # Commands python to search for student once one selects option 4
        elif choice == "5":
            generate_reports()                                            # Commands python to Generate reports once one selects option 5
        elif choice == "6":
            save_data()
            print("\n**************************************************")
            print("* Exiting system. Thank you, Warden!             *")
            print("**************************************************\n")
            break                                                           # Immediately stop the loop.
        else:
            print("\n* Invalid selection! Please enter a number from 1 to 6. *")

if __name__ == "__main__":
    main()