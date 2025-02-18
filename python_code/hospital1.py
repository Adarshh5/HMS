import mysql.connector
from hospital import database
import datetime
import mysql.connector

def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            print("Invalid input! Please ensure you enter the correct data types.")
        except mysql.connector.IntegrityError as e:
            print("Integrity Error: ", e)
        except mysql.connector.Error as e:
            print("Database Error: ", e)
        except Exception as e:
            print("An unexpected error occurred: ", e)
    return wrapper


class pateint:
    def __init__(self):
        self.db = database()

    @handle_exceptions
    def Add_pateint(self):

        Patient_name = input("Enter patient name: ")
        Father_name = input('Enter patient father name: ')
        Age = int(input('Enter age: '))
        City = input("Enter city: ")
        Contect_number = input("Enter number: ")
        Disease_name = input("Enter disease_name: ")
        Gender = input("Enter gender: ")

        if Age >= 1 and len(Contect_number) == 10 and Contect_number.isdigit() and (Gender == "M" or Gender == "F"):

            self.db.mycursor.execute(
                "SELECT id, name FROM  Departments")
            departments = self.db.mycursor.fetchall()
            print("Available Departments ")
            for dept_id, dept_name in departments:
                print(f"id : {dept_id}  name: {dept_name}")
            Department_id = int(input("Enter Department_id"))


            sql = "INSERT INTO patients(patient_name, father_name, age, city, contact_number, disease_name, gender, department_id, enrollment_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())"
            val = (Patient_name, Father_name, Age, City, Contect_number, Disease_name, Gender, Department_id)
            self.db.mycursor.execute(sql, val)
            self.db.mydb.commit()
            print(f"Patient {Patient_name} added successfully.")
        else:
            print("age is 0 or nagtive or lenth of nunber is not 10 or  all  number is not digit Gender is not Correct  ")




class SecondClass:

    def __init__(self):
        self.db = database()

    @handle_exceptions
    def Second(self):
        query = "SELECT disease_name, COUNT(id) FROM Patients GROUP BY disease_name"
        self.db.mycursor.execute(query)
        out = self.db.mycursor.fetchall()
        l = []
        for obj  in out:
            l.append(obj[1])
        disease = None
        for obj in out:
            if obj[1] == max(l):
                disease = obj
        query = f"SELECT gender FROM Patients WHERE disease_name = '{disease[0]}'"
        self.db.mycursor.execute(query)
        genders = self.db.mycursor.fetchall()
        total_patients = 0
        f_count = 0
        m_count = 0
        for gender in genders:
           total_patients+=1
           if gender[0] == 'M':
               m_count+=1
           elif gender[0] =='F':
               f_count+=1
        f_percentage = (f_count / total_patients) * 100
        m_percentage = (m_count / total_patients) * 100
        print(f"Disease_name = {disease[0]} , The_number of Patient = {disease[1]} ,"
        f" Percentage of Females: {f_percentage:.2f}%,  Percentage of Males: {m_percentage:.2f}%")


    @handle_exceptions
    def Third(self):
        Year = input("Enter Year: ")
        if len(Year) == 4 and Year.isdigit():
            query = f"SELECT id, gender FROM Patients WHERE YEAR(enrollment_time)= {Year}"
            self.db.mycursor.execute(query)
            out = self.db.mycursor.fetchall()
            number = len(out)
            total_patients = 0
            f_count = 0
            m_count = 0
            for gender in out:
                total_patients += 1
                if gender[1] == 'M':
                    m_count += 1
                elif gender[1] == 'F':
                    f_count += 1
            f_percentage = (f_count / total_patients) * 100
            m_percentage = (m_count / total_patients) * 100
            print(f"Year = {Year} , The_number of Patient = {number} ,"
                  f" Percentage of Females: {f_percentage:.2f}%,  Percentage of Males: {m_percentage:.2f}%")
        else:
            print("please enter 4 digit input ")

    @handle_exceptions
    def Fourth(self):
        disease_name = input("Enter disease name: ")
        Year = input("Enter Year(Like- 2024): ")
        MinAge = input("Enter Min Age (optional): ")
        MaxAge = input("Enter Max Age (optional): ")
        Gender = input("Enter Gender Like-(M/F) (optional) : ")
        if MinAge.isdigit():
            MinAge = int(MinAge)
        else:MinAge=None
        if MaxAge.isdigit():
            MaxAge = int(MaxAge)
        else:MaxAge=None
        if len(Gender) == 1 and Gender.isalpha():
            Gender.upper()
        else: Gender=None

        if not (disease_name and disease_name.isalpha() and  len(Year) == 4 and Year.isdigit()):
            print("there is some mistake in disease_name or Year")
            return


        query = "SELECT * FROM patients WHERE disease_name = %s AND YEAR(enrollment_time) = %s"
        val = [disease_name, Year]
        if Gender:
            query += "AND gender = %s"
            val.append(Gender)
        if MinAge:
            query +=  "AND age >= %s"
            val.append(MinAge)
        if MaxAge:
            query += "AND age <= %s"
            val.append(MaxAge)

        self.db.mycursor.execute(query, tuple(val))
        out = self.db.mycursor.fetchall()
        print(f"for this disease_name = {disease_name},in this Year = {Year}, in this Gender = {Gender}, MinAge = {MinAge}, MaxAge = {MaxAge},   The_number of Patient = {len(out)} ")





class menu:
    def __init__(self):
        print("Welcome to Hospital Management System!")
        self.obj1 = pateint()
        self.obj2 = SecondClass()

    def __del__(self):
        print("Exiting the Hospital Management System. Goodbye!")
    def Action(self):
        while True:
            print("""
            1.) Enter 1 Add pateint
            2.) Enter 2 to see  for which disease Patients mostly come, Ratio of the gender for that disease.
            3.) Enter 3 and see how many patiant have come in this year, Ratio of the gender for that year.
            4.) Enter 4 and disease name and min and max age and year and gender. then see the number of paciant.     
            5.) Exit()
            """)
            try:
                choice = int(input("Enter Number: "))

                if choice == 1:
                   self.obj1.Add_pateint(

                elif choice == 2:
                    self.obj2.Second()
                elif choice == 3:
                    self.obj2.Third()
                elif choice ==4:
                    self.obj2.Fourth()
                elif choice ==5:
                    break
                else:
                    print("Invalid Choice. ")
            except ValueError:
               print("Invalid input! Please enter a valid number (1 or 2).")
            except Exception as e:
               print("An unexpected error occurred: ", e)


obj = menu()
obj.Action()