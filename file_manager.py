import sqlite3

import base64

import imageio

import cv2


# this application only works for macOS and Linux
# for windows, please adjust the path of your files
 

PASSWORD = "Add your password here"



connect = input("What is your password?\n")



while connect != PASSWORD:

    connect = input("What is your password?\n")

    if connect == "q":

        break



if connect == PASSWORD:

    conn = sqlite3.connect('mysafe.db')

    try:

        conn.execute('''CREATE TABLE SAFE

            (FULL_NAME TEXT PRIMARY KEY NOT NULL,

            NAME TEXT NOT NULL,

            EXTENSION TEXT NOT NULL,

            FILES TEXT NOT NULL);''')

        print("Your safe has been created!\nWhat would you like to store in it today?")

    except:

        print("You have a safe, what would you like to do today?")

    

    

    while True:

        print("\n"+ "*"*15)

        print("Commands:")

        print("q = quit program")

        print("o = open file")

        print("s = store file")

        print("*"*15)

        input_ = input(":")



        if input_ == "q":

            break

        if input_ == "o":

            # open the file

            file_type = input("What is the filetype of the file you want to open?\n")

            file_name = input("What is the name of the file you want to open?\n")

            FILE_ = file_name + "." + file_type

            try:

                cursor = conn.execute("SELECT * from SAFE WHERE FULL_NAME=" + '"' + FILE_ + '"')



                file_string = ""

                for row in cursor:

                    file_string = row[3]

                with open(FILE_, 'wb') as f_output:

                    print(file_string)

                    f_output.write(base64.b64decode(file_string))

            except:

                print("This file does not exist. Please try it again.")

                Exception()







        if input_ == "s":

            # store file

            PATH = input("Type in the full path to the file you want to store.\nExample: /Users/marvin/Desktop/myfile.py\n")



            FILE_TYPES = {

                "txt": "TEXT",

                "java": "TEXT",

                "dart": "TEXT",

                "py": "TEXT",

                "jpg": "IMAGE",

                "png": "IMAGE",

                "jpeg": "IMAGE"

            }


            try:
    
                file_name = PATH.split("/")

                file_name = file_name[len(file_name) - 1]

                file_string = ""



                NAME = file_name.split(".")[0]

                EXTENSION = file_name.split(".")[1]



                try:

                    EXTENSION = FILE_TYPES[EXTENSION]

                except:

                    Exception()





                if EXTENSION == "IMAGE":

                    IMAGE = cv2.imread(PATH)

                    file_string = base64.b64encode(cv2.imencode('.jpg', IMAGE)[1]).decode()



                elif EXTENSION == "TEXT":

                    file_string = open(PATH, "r").read()

                    file_string = base64.b64encode(file_string)



                EXTENSION = file_name.split(".")[1]

                

                command = 'INSERT INTO SAFE (FULL_NAME, NAME, EXTENSION, FILES) VALUES (%s, %s, %s, %s);' %('"' + file_name +'"', '"' + NAME +'"', '"' + EXTENSION +'"', '"' + file_string +'"')

                

                conn.execute(command)

                conn.commit()

            except:

                print("This file does not exist. Please try again.")

                Exception()