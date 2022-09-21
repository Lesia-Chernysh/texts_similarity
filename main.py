
#!/usr/bin/env python
# coding: utf-8

from tkinter import *
from tkinter import messagebox
import sqlite3
import re
import pymorphy2
from math import sqrt

conn = sqlite3.connect('main.db')
cursor = conn.cursor()


# THE FUNCTION IS CALLED WHEN THE OK BUTTON IS PRESSED AFTER THE USER SELECTS THE NUMBER OF TEXTS
# IT CREATES THE NECESSARY NUMBER OF SPACES FOR INSERTING TEXTS
def createPlaceForTexts():
    def showError():
        messagebox.showerror('Error!', 'Please, enter a number between 2 and 5!')
    global frame
    global btnCompare
    amount = entryAmount.get() # number of texts selected by the user
    w = 1550
    h = 850

    frame = Frame(root)
    frame.place(x=5, y = 30, width=w, heigh=h)

    def place_for_text1():
        global text1
        text1 = Text(frame, font = ("Times New Roman", 10))
        text1.place(x = 10, y = 30, width = w/5-15, heigh=350)
        scroll1 = Scrollbar(text1, command=text1.yview, orient=VERTICAL)
        scroll1.place(relx=0.95, rely=0, heigh=350)
        text1.config(yscrollcommand=scroll1.set)

    def place_for_text2():
        global text2
        text2 = Text(frame, font = ("Times New Roman", 10))
        text2.place(x = w/5+5, y = 30, width = w/5-15, heigh=350)
        scroll2 = Scrollbar(text2, command=text2.yview, orient=VERTICAL)
        scroll2.place(relx=0.95, rely=0, heigh=350)
        text2.config(yscrollcommand=scroll2.set)

    def place_for_text3():
        global text3
        text3 = Text(frame, font = ("Times New Roman", 10))
        text3.place(x = 2*(w/5)+5, y = 30, width = w/5-15, heigh=350)
        scroll3 = Scrollbar(text3, command=text3.yview, orient=VERTICAL)
        scroll3.place(relx=0.95, rely=0, heigh=350)
        text3.config(yscrollcommand=scroll3.set)

    def place_for_text4():
        global text4
        text4 = Text(frame, font = ("Times New Roman", 10))
        text4.place(x = 3*(w/5)+5, y = 30, width = w/5-15, heigh=350)
        scroll4 = Scrollbar(text4, command=text4.yview, orient=VERTICAL)
        scroll4.place(relx=0.95, rely=0, heigh=350)
        text4.config(yscrollcommand=scroll4.set)

    def place_for_text5():
        global text5
        text5 = Text(frame, font = ("Times New Roman", 10))
        text5.place(x = 4*(w/5)+5, y = 30, width = w/5-15, heigh=350)
        scroll5 = Scrollbar(text5, command=text5.yview, orient=VERTICAL)
        scroll5.place(relx=0.95, rely=0, heigh=350)
        text5.config(yscrollcommand=scroll5.set)

    if int(amount) >5:
        showError()
    if int(amount) ==5:
        place_for_text1()
        place_for_text2()
        place_for_text3()
        place_for_text4()
        place_for_text5()

    if int(amount) ==4:
        place_for_text1()
        place_for_text2()
        place_for_text3()
        place_for_text4()

    if int(amount)==3:
        place_for_text1()
        place_for_text2()
        place_for_text3()

    if int(amount)==2:
        place_for_text1()
        place_for_text2()

    if int(amount)<2:
        showError()
    btnCompare = Button(frame, text = 'Compare', bg = "darkblue", font = ("Times New Roman", 10), fg ="white", command = main)
    btnCompare.place(x=10, y=380, width=70)

def dropTables():
    cursor.execute("""drop table Словоформи""")
    conn.commit()
    cursor.execute("""drop table Словоформи2""")
    conn.commit()
    cursor.execute("""drop table Словоформи3""")
    conn.commit()
    cursor.execute("""drop table Словоформи4""")
    conn.commit()
    cursor.execute("""drop table Словоформи5""")
    conn.commit()
    cursor.execute("""drop table Частини_Мови""")
    conn.commit()
    cursor.execute("""drop table Частини_Мови2""")
    conn.commit()
    cursor.execute("""drop table Частини_Мови3""")
    conn.commit()
    cursor.execute("""drop table Частини_Мови4""")
    conn.commit()
    cursor.execute("""drop table Частини_Мови5""")
    conn.commit()
    cursor.execute("""drop table Частота_Частин_Мови""")
    conn.commit()
    cursor.execute("""drop table Частота_Частин_Мови2""")
    conn.commit()
    cursor.execute("""drop table Частота_Частин_Мови3""")
    conn.commit()
    cursor.execute("""drop table Частота_Частин_Мови4""")
    conn.commit()
    cursor.execute("""drop table Частота_Частин_Мови5""")
    conn.commit()
    cursor.execute("""drop table Леми""")
    conn.commit()
    cursor.execute("""drop table Леми2""")
    conn.commit()
    cursor.execute("""drop table Леми3""")
    conn.commit()
    cursor.execute("""drop table Леми4""")
    conn.commit()
    cursor.execute("""drop table Леми5""")
    conn.commit()
    cursor.execute("""drop table Частота_Лем""")
    conn.commit()
    cursor.execute("""drop table Частота_Лем2""")
    conn.commit()
    cursor.execute("""drop table Частота_Лем3""")
    conn.commit()
    cursor.execute("""drop table Частота_Лем4""")
    conn.commit()
    cursor.execute("""drop table Частота_Лем5""")
    conn.commit()

# THE FUNCTION IS CALLED WHEN THE "COMPARE" BUTTON IS PRESSED
# IT PERFORMS SEVERAL ACTIONS AT ONCE
# 1) DESTROYES PREVIOUS WIDGETS, IE CLEARS THE WINDOW
# 2) CREATES TABLES - FREQUENCY DICTIONARIES OF WORD FORMS, LEMMAS AND PARTS OF SPEECH. IT ALSO CREATES INTERMEDIATE FREQUENCY DICTIONARIES
# OF PARTS OF SPEECH AND LEMMAS FOR THE USER TO CHECK THE CORRECTNESS OF THEIR AUTOMATIC DETERMINATION
# 3) COMPLETES TABLES
# 4) CALCULATES ALL THE NECESSARY VALUES AND DISPLAYS THEM IN A DIALOG WINDOW
def main():
    amount = entryAmount.get()
    btnCompare.destroy()
    def createTables():
        cursor.execute('''CREATE TABLE IF NOT EXISTS Словоформи
                          (словоформа TEXT PRIMARY KEY NOT NULL,
                          Загальна_Частота INTEGER)
        ''')
        conn.commit()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Частини_Мови
                          (слово TEXT,
                          частина_мови TEXT,
                          Загальна_Частота INTEGER)
        ''')
        conn.commit()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Частота_Частин_Мови
                      (частина_мови TEXT PRIMARY KEY NOT NULL,
                      Загальна_Частота INTEGER)
        ''')
        conn.commit()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Леми
                      (слово TEXT,
                      лема TEXT,
                      Загальна_Частота INTEGER)
        ''')
        conn.commit()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Частота_Лем
                      (лема TEXT PRIMARY KEY NOT NULL,
                      Загальна_Частота INTEGER)
        ''')
        conn.commit()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Словоформи2
                      (словоформа TEXT PRIMARY KEY NOT NULL,
                      Загальна_Частота INTEGER)
        ''')
        conn.commit()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Частини_Мови2
                      (слово TEXT,
                      частина_мови TEXT,
                      Загальна_Частота INTEGER)
        ''')
        conn.commit()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Частота_Частин_Мови2
                      (частина_мови TEXT PRIMARY KEY NOT NULL,
                      Загальна_Частота INTEGER)
        ''')
        conn.commit()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Леми2
                      (слово TEXT,
                      лема TEXT,
                      Загальна_Частота INTEGER)
        ''')
        conn.commit()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Частота_Лем2
                      (лема TEXT PRIMARY KEY NOT NULL,
                      Загальна_Частота INTEGER)
        ''')
        conn.commit()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Словоформи3
                      (словоформа TEXT PRIMARY KEY NOT NULL,
                      Загальна_Частота INTEGER)
        ''')
        conn.commit()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Частини_Мови3
                      (слово TEXT,
                      частина_мови TEXT,
                      Загальна_Частота INTEGER)
         ''')
        conn.commit()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Частота_Частин_Мови3
                      (частина_мови TEXT PRIMARY KEY NOT NULL,
                      Загальна_Частота INTEGER)
        ''')
        conn.commit()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Леми3
                      (слово TEXT,
                      лема TEXT,
                      Загальна_Частота INTEGER)
        ''')
        conn.commit()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Частота_Лем3
                      (лема TEXT PRIMARY KEY NOT NULL,
                      Загальна_Частота INTEGER)
        ''')
        conn.commit()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Словоформи4
                      (словоформа TEXT PRIMARY KEY NOT NULL,
                      Загальна_Частота INTEGER)
        ''')
        conn.commit()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Частини_Мови4
                      (слово TEXT,
                      частина_мови TEXT,
                      Загальна_Частота INTEGER)
         ''')
        conn.commit()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Частота_Частин_Мови4
                      (частина_мови TEXT PRIMARY KEY NOT NULL,
                      Загальна_Частота INTEGER)
        ''')
        conn.commit()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Леми4
                      (слово TEXT,
                      лема TEXT,
                      Загальна_Частота INTEGER)
        ''')
        conn.commit()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Частота_Лем4
                      (лема TEXT PRIMARY KEY NOT NULL,
                      Загальна_Частота INTEGER)
        ''')
        conn.commit()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Словоформи5
                      (словоформа TEXT PRIMARY KEY NOT NULL,
                      Загальна_Частота INTEGER)
        ''')
        conn.commit()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Частини_Мови5
                      (слово TEXT,
                      частина_мови TEXT,
                      Загальна_Частота INTEGER)
         ''')
        conn.commit()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Частота_Частин_Мови5
                      (частина_мови TEXT PRIMARY KEY NOT NULL,
                      Загальна_Частота INTEGER)
        ''')
        conn.commit()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Леми5
                      (слово TEXT,
                      лема TEXT,
                      Загальна_Частота INTEGER)
        ''')
        conn.commit()
        cursor.execute('''CREATE TABLE Частота_Лем5
                      (лема TEXT PRIMARY KEY NOT NULL,
                      Загальна_Частота INTEGER)
        ''')
        conn.commit()
    createTables()

    # CREATE A FUNCTION THAT TAKES TEXT AS A PARAMETER AND CREATES LISTS OF LISTS WITH UNITS AND THEIR FREQUENCIES
    def parse_text(get_text):
        global values1_ordered
        global part_of_speech
        global values2_ordered
        global values3_ordered
        global lemmas_edited_ordered
        global part_of_speech_freq
        edited = re.sub('\.', '', get_text.lower())
        edited = re.sub(',', '', edited)
        edited = re.sub('!', '', edited)
        edited = re.sub('\?', '', edited)
        edited = re.sub(':', '', edited)
        edited = re.sub(';', '', edited)
        edited = re.sub('\.\.', '', edited)
        edited = re.sub('\(', '', edited)
        edited = re.sub('\)', '', edited)
        edited = re.sub('[a-zA-Z]+', '', edited)
        edited = re.sub('"', '', edited)
        edited = re.sub("'", '', edited)
        edited = re.sub("«", '', edited)
        edited = re.sub("»", '', edited)
        edited = re.sub('\[', '', edited)
        edited = re.sub('\]', '', edited)
        edited = re.sub('\d', '', edited)
        edited = re.sub('%', '', edited)
        edited = re.sub('\\\\', '', edited)
        edited = re.sub('//', '', edited)
        edited = re.sub('\n', ' ', edited)
        edited = re.sub("'\]", '', edited)
        edited = re.sub("\['", '', edited)
        edited = re.sub('\s-\s', ' ', edited)
        edited = re.sub('\s–\s', ' ', edited)
        edited = re.sub('\s—\s', ' ', edited)

        splitted_1 = str(edited).split(' ')

        #delete empty words
        splitted_1 = list(filter(None, splitted_1))
        #print(splitted_1)

        #Add words to the list
        count = 0
        edited_list = []
        for word in splitted_1:
            edited_list.append(word)

        sample_1_dict = {}
        sample_1_list = []

        #List of frequencies
        for word in edited_list:
            sample_1_list.append(word)
            if word in sample_1_dict:
                sample_1_dict[word][1] += 1
            else:
                sample_1_dict[word] = [word]
                sample_1_dict[word].append(1)

        values1 = list(sample_1_dict.values())

        # Create a frequency dictionary of word forms
        values1_ordered = []
        for i in values1:
            values1_ordered.append(i)
        count = 0
        while count in range(0, len(values1_ordered)-1):
            if values1_ordered[count][1] < values1_ordered[count+1][1]:
                values1_ordered[count], values1_ordered[count+1] = values1_ordered[count+1], values1_ordered[count]
            count += 1

        morph = pymorphy2.MorphAnalyzer(lang='uk')
        part_of_speech_freq = []
        part_of_speech = {}

        # Compile a dictionary of parts of speech
        for i in sample_1_list:
            parsed1 = morph.parse(i)[0]
            part_of_sp = parsed1.tag.POS
            if i in part_of_speech:
                part_of_speech[i][2] +=1
            else:
                part_of_speech[i]=[i, part_of_sp, 1]



        lemmas = {}
        for i in sample_1_list:
            normal_form = morph.parse(i)[0].normal_form
            if normal_form in lemmas:
                lemmas[normal_form][2] += 1
            else:
                lemmas[normal_form] = [i]
                lemmas[normal_form].append(normal_form)
                lemmas[normal_form].append(1)

        values3 = list(lemmas.values())

        values3_ordered = []
        for i in values3:
            values3_ordered.append(i)
            count = 0
            while count in range(0, len(values3_ordered)-1):
                if values3_ordered[count][2] < values3_ordered[count+1][2]:
                    values3_ordered[count], values3_ordered[count+1] = values3_ordered[count+1], values3_ordered[count]
                count += 1
            #print(values3_ordered)

    def insertIntoDataBase():
        amount = entryAmount.get()
        def insertForText1():
            get_text1 = str(text1.get(1.0, END)) # receive the texts entered by the user
            text1.destroy()
            parse_text(get_text1) # call the function to process the first text
            for i in values1_ordered:
                cursor.execute("""INSERT INTO Словоформи
                                       VALUES (?, ?)""", i)
            conn.commit()

            for i in part_of_speech.values():
                cursor.execute("""INSERT INTO Частини_Мови
                                          VALUES (?, ?, ?)""", i)
            conn.commit()


            # Create a frequency dictionary of parts of speech
            cursor.execute("select * from Частини_Мови")
            rows = cursor.fetchall()

            # Compile a frequency dictionary of parts of speech
            values2 = {}
            for row in rows:
                part_of_speech_freq.append(row[1:3])

            for i in part_of_speech_freq:
                if i[0] in values2:
                    values2[i[0]][1] += i[1]
                else:
                    values2[i[0]] = [i[0], i[1]]

            values2 = list(values2.values())

            for i in values2:
                if i[0] == None:
                    values2.remove(i)

            values2_ordered = []
            for i in values2:
                values2_ordered.append(i)
            count=0
            while count in range(0, len(values2_ordered)-1):
                if values2_ordered[count][1] < values2_ordered[count+1][1]:
                    values2_ordered[count], values2_ordered[count+1] = values2_ordered[count+1], values2_ordered[count]
                count += 1


            for i in values2_ordered:
                cursor.execute("""INSERT INTO Частота_Частин_Мови
                                          VALUES (?, ?)""", i)
            conn.commit()


            for i in values3_ordered:
                    cursor.execute("""INSERT INTO Леми
                                       VALUES (?, ?, ?)""", i)
            conn.commit()


            cursor.execute("select * from Леми")
            rows = cursor.fetchall()
            lemmas_freq = []
            lemmas_edited = {}
            for row in rows:
                lemmas_freq.append(row[1:3])

            for i in lemmas_freq:
                if i[0] in lemmas_edited:
                    lemmas_edited[i[0]][1] += i[1]
                else:
                    lemmas_edited[i[0]] = [i[0], i[1]]

            lemmas_edited = list(lemmas_edited.values())

            for i in lemmas_edited:
                if i[0] == None:
                    lemmas_edited.remove(i)

            lemmas_edited_ordered = []
            for i in lemmas_edited:
                    lemmas_edited_ordered.append(i)
            count=0
            while count in range(0, len(lemmas_edited_ordered)-1):
                if lemmas_edited_ordered[count][1] < lemmas_edited_ordered[count+1][1]:
                        lemmas_edited_ordered[count], lemmas_edited_ordered[count+1] = lemmas_edited_ordered[count+1], lemmas_edited_ordered[count]
                count += 1

            for i in lemmas_edited_ordered:
                cursor.execute("""INSERT INTO Частота_Лем
                                        VALUES (?, ?)""", i)
            conn.commit()
        def insertForText2():
            get_text2 = str(text2.get(1.0, END))
            text2.destroy()
            parse_text(get_text2)
            for i in values1_ordered:
                    cursor.execute("""INSERT INTO Словоформи2
                                       VALUES (?, ?)""", i)
            conn.commit()

            for i in part_of_speech.values():
                       cursor.execute("""INSERT INTO Частини_Мови2
                                          VALUES (?, ?, ?)""", i)
            conn.commit()


                # Create a frequency dictionary of parts of speech
            cursor.execute("select * from Частини_Мови2")
            rows = cursor.fetchall()

                #compile a frequency dictionary of parts of speech
            values2 = {}
            for row in rows:
                    part_of_speech_freq.append(row[1:3])

            for i in part_of_speech_freq:
                    if i[0] in values2:
                        values2[i[0]][1] += i[1]
                    else:
                        values2[i[0]] = [i[0], i[1]]

            values2 = list(values2.values())

            for i in values2:
                    if i[0] == None:
                        values2.remove(i)

            values2_ordered = []
            for i in values2:
                    values2_ordered.append(i)
            for i in values2_ordered:
                    count = 0
                    while count in range(0, len(values2_ordered)-1):
                        if values2_ordered[count][1] < values2_ordered[count+1][1]:
                            values2_ordered[count], values2_ordered[count+1] = values2_ordered[count+1], values2_ordered[count]
                        count += 1


            for i in values2_ordered:
                    cursor.execute("""INSERT INTO Частота_Частин_Мови2
                                          VALUES (?, ?)""", i)
            conn.commit()


            for i in values3_ordered:
                       cursor.execute("""INSERT INTO Леми2
                                       VALUES (?, ?, ?)""", i)
            conn.commit()
            cursor.execute("""select * from Леми2""")
            rows = cursor.fetchall()


            cursor.execute("select * from Леми2")
            rows = cursor.fetchall()
            lemmas_freq = []
            lemmas_edited = {}
            for row in rows:
                    lemmas_freq.append(row[1:3])
                    #print(lemmas_edited)

            for i in lemmas_freq:
                    if i[0] in lemmas_edited:
                        lemmas_edited[i[0]][1] += i[1]
                    else:
                        lemmas_edited[i[0]] = [i[0], i[1]]

            lemmas_edited = list(lemmas_edited.values())
                #print(lemmas_edited)

            for i in lemmas_edited:
                    if i[0] == None:
                        lemmas_edited.remove(i)

            lemmas_edited_ordered = []
            for i in lemmas_edited:
                       lemmas_edited_ordered.append(i)
            for i in lemmas_edited_ordered:
                    count = 0
                    while count in range(0, len(lemmas_edited_ordered)-1):
                        if lemmas_edited_ordered[count][1] < lemmas_edited_ordered[count+1][1]:
                              lemmas_edited_ordered[count], lemmas_edited_ordered[count+1] = lemmas_edited_ordered[count+1], lemmas_edited_ordered[count]
                        count += 1
                  

            for i in lemmas_edited_ordered:
                        cursor.execute("""INSERT INTO Частота_Лем2
                                        VALUES (?, ?)""", i)
            conn.commit()
        def insertForText3():
            get_text3 = str(text3.get(1.0, END))
            text3.destroy()
            parse_text(get_text3)
            for i in values1_ordered:
                    cursor.execute("""INSERT INTO Словоформи3
                                       VALUES (?, ?)""", i)
            conn.commit()

            for i in part_of_speech.values():
                       cursor.execute("""INSERT INTO Частини_Мови3
                                          VALUES (?, ?, ?)""", i)
            conn.commit()


                # create a frequency dictionary of parts of speech
            cursor.execute("select * from Частини_Мови3")
            rows = cursor.fetchall()

                #compile a frequency dictionary of parts of speech
            values2 = {}
            for row in rows:
                    part_of_speech_freq.append(row[1:3])

            for i in part_of_speech_freq:
                    if i[0] in values2:
                        values2[i[0]][1] += i[1]
                    else:
                        values2[i[0]] = [i[0], i[1]]

            values2 = list(values2.values())

            for i in values2:
                    if i[0] == None:
                        values2.remove(i)

            values2_ordered = []
            for i in values2:
                    values2_ordered.append(i)
            for i in values2_ordered:
                    count = 0
                    while count in range(0, len(values2_ordered)-1):
                        if values2_ordered[count][1] < values2_ordered[count+1][1]:
                            values2_ordered[count], values2_ordered[count+1] = values2_ordered[count+1], values2_ordered[count]
                        count += 1


            for i in values2_ordered:
                    cursor.execute("""INSERT INTO Частота_Частин_Мови3
                                          VALUES (?, ?)""", i)
            conn.commit()


            for i in values3_ordered:
                       cursor.execute("""INSERT INTO Леми3
                                       VALUES (?, ?, ?)""", i)
            conn.commit()
            cursor.execute("""select * from Леми3""")
            rows = cursor.fetchall()


            cursor.execute("select * from Леми3")
            rows = cursor.fetchall()
            lemmas_freq = []
            lemmas_edited = {}
            for row in rows:
                    lemmas_freq.append(row[1:3])

            for i in lemmas_freq:
                    if i[0] in lemmas_edited:
                        lemmas_edited[i[0]][1] += i[1]
                    else:
                        lemmas_edited[i[0]] = [i[0], i[1]]

            lemmas_edited = list(lemmas_edited.values())

            for i in lemmas_edited:
                    if i[0] == None:
                        lemmas_edited.remove(i)

            lemmas_edited_ordered = []
            for i in lemmas_edited:
                       lemmas_edited_ordered.append(i)
            for i in lemmas_edited_ordered:
                    count = 0
                    while count in range(0, len(lemmas_edited_ordered)-1):
                        if lemmas_edited_ordered[count][1] < lemmas_edited_ordered[count+1][1]:
                              lemmas_edited_ordered[count], lemmas_edited_ordered[count+1] = lemmas_edited_ordered[count+1], lemmas_edited_ordered[count]
                        count += 1

            for i in lemmas_edited_ordered:
                        cursor.execute("""INSERT INTO Частота_Лем3
                                        VALUES (?, ?)""", i)
            conn.commit()
        def insertForText4():
            get_text4 = str(text4.get(1.0, END))
            text4.destroy()
            parse_text(get_text4)
            for i in values1_ordered:
                    cursor.execute("""INSERT INTO Словоформи4
                                       VALUES (?, ?)""", i)
            conn.commit()

            for i in part_of_speech.values():
                       cursor.execute("""INSERT INTO Частини_Мови4
                                          VALUES (?, ?, ?)""", i)
            conn.commit()


                # create a frequency dictionary of parts of speech
            cursor.execute("select * from Частини_Мови4")
            rows = cursor.fetchall()

                #compile a frequency dictionary of parts of speech
            values2 = {}
            for row in rows:
                    part_of_speech_freq.append(row[1:3])

            for i in part_of_speech_freq:
                    if i[0] in values2:
                        values2[i[0]][1] += i[1]
                    else:
                        values2[i[0]] = [i[0], i[1]]

            values2 = list(values2.values())

            for i in values2:
                    if i[0] == None:
                        values2.remove(i)

            values2_ordered = []
            for i in values2:
                    values2_ordered.append(i)
            for i in values2_ordered:
                    count = 0
                    while count in range(0, len(values2_ordered)-1):
                        if values2_ordered[count][1] < values2_ordered[count+1][1]:
                            values2_ordered[count], values2_ordered[count+1] = values2_ordered[count+1], values2_ordered[count]
                        count += 1


            for i in values2_ordered:
                    cursor.execute("""INSERT INTO Частота_Частин_Мови4
                                          VALUES (?, ?)""", i)
            conn.commit()


            for i in values3_ordered:
                       cursor.execute("""INSERT INTO Леми4
                                       VALUES (?, ?, ?)""", i)
            conn.commit()
            cursor.execute("""select * from Леми4""")
            rows = cursor.fetchall()


            cursor.execute("select * from Леми4")
            rows = cursor.fetchall()
            lemmas_freq = []
            lemmas_edited = {}
            for row in rows:
                    lemmas_freq.append(row[1:3])

            for i in lemmas_freq:
                    if i[0] in lemmas_edited:
                        lemmas_edited[i[0]][1] += i[1]
                    else:
                        lemmas_edited[i[0]] = [i[0], i[1]]

            lemmas_edited = list(lemmas_edited.values())

            for i in lemmas_edited:
                    if i[0] == None:
                        lemmas_edited.remove(i)

            lemmas_edited_ordered = []
            for i in lemmas_edited:
                       lemmas_edited_ordered.append(i)
            for i in lemmas_edited_ordered:
                    count = 0
                    while count in range(0, len(lemmas_edited_ordered)-1):
                        if lemmas_edited_ordered[count][1] < lemmas_edited_ordered[count+1][1]:
                              lemmas_edited_ordered[count], lemmas_edited_ordered[count+1] = lemmas_edited_ordered[count+1], lemmas_edited_ordered[count]
                        count += 1

            for i in lemmas_edited_ordered:
                        cursor.execute("""INSERT INTO Частота_Лем4
                                        VALUES (?, ?)""", i)
            conn.commit()
        def insertForText5():
            get_text5 = str(text5.get(1.0, END))
            text5.destroy()
            parse_text(get_text5)
            for i in values1_ordered:
                    cursor.execute("""INSERT INTO Словоформи5
                                       VALUES (?, ?)""", i)
            conn.commit()

            for i in part_of_speech.values():
                       cursor.execute("""INSERT INTO Частини_Мови5
                                          VALUES (?, ?, ?)""", i)
            conn.commit()


                # create a frequency dictionary of parts of speech
            cursor.execute("select * from Частини_Мови5")
            rows = cursor.fetchall()

                #compile a frequency dictionary of parts of speech
            values2 = {}
            for row in rows:
                    part_of_speech_freq.append(row[1:3])

            for i in part_of_speech_freq:
                    if i[0] in values2:
                        values2[i[0]][1] += i[1]
                    else:
                        values2[i[0]] = [i[0], i[1]]

            values2 = list(values2.values())

            for i in values2:
                    if i[0] == None:
                        values2.remove(i)

            values2_ordered = []
            for i in values2:
                    values2_ordered.append(i)
            for i in values2_ordered:
                    count = 0
                    while count in range(0, len(values2_ordered)-1):
                        if values2_ordered[count][1] < values2_ordered[count+1][1]:
                            values2_ordered[count], values2_ordered[count+1] = values2_ordered[count+1], values2_ordered[count]
                        count += 1


            for i in values2_ordered:
                    cursor.execute("""INSERT INTO Частота_Частин_Мови5
                                          VALUES (?, ?)""", i)
            conn.commit()


            for i in values3_ordered:
                       cursor.execute("""INSERT INTO Леми5
                                       VALUES (?, ?, ?)""", i)
            conn.commit()
            cursor.execute("""select * from Леми5""")
            rows = cursor.fetchall()


            cursor.execute("select * from Леми5")
            rows = cursor.fetchall()
            lemmas_freq = []
            lemmas_edited = {}
            for row in rows:
                    lemmas_freq.append(row[1:3])

            for i in lemmas_freq:
                    if i[0] in lemmas_edited:
                        lemmas_edited[i[0]][1] += i[1]
                    else:
                        lemmas_edited[i[0]] = [i[0], i[1]]

            lemmas_edited = list(lemmas_edited.values())

            for i in lemmas_edited:
                    if i[0] == None:
                        lemmas_edited.remove(i)

            lemmas_edited_ordered = []
            for i in lemmas_edited:
                       lemmas_edited_ordered.append(i)
            for i in lemmas_edited_ordered:
                    count = 0
                    while count in range(0, len(lemmas_edited_ordered)-1):
                        if lemmas_edited_ordered[count][1] < lemmas_edited_ordered[count+1][1]:
                              lemmas_edited_ordered[count], lemmas_edited_ordered[count+1] = lemmas_edited_ordered[count+1], lemmas_edited_ordered[count]
                        count += 1

            for i in lemmas_edited_ordered:
                        cursor.execute("""INSERT INTO Частота_Лем5
                                        VALUES (?, ?)""", i)
            conn.commit()
        if int(amount)==5:
            insertForText1()
            insertForText2()
            insertForText3()
            insertForText4()
            insertForText5()
        if int(amount)==4:
            insertForText1()
            insertForText2()
            insertForText3()
            insertForText4()
        if int(amount)==3:
            insertForText1()
            insertForText2()
            insertForText3()
        if int(amount)==2:
            insertForText1()
            insertForText2()
    insertIntoDataBase()

    def common():
       # EXTRACT DATA FROM TABLES
        def getDataFromDataBase():
            global words_freq1
            global words_freq2
            global words_freq3
            global words_freq4
            global words_freq5
            global parts_of_speech_freq1
            global parts_of_speech_freq2
            global parts_of_speech_freq3
            global parts_of_speech_freq4
            global parts_of_speech_freq5
            global lemmas_freq1
            global lemmas_freq2
            global lemmas_freq3
            global lemmas_freq4
            global lemmas_freq5
            cursor.execute('select * from Словоформи')
            rows = cursor.fetchall()
            words_freq1 = []
            for row in rows:
                words_freq1.append([row[0], row[1]])
            words_freq1 = tuple(words_freq1) # since the functions change the parameters, we convert the data into an immutable data type - tuple
            #print(words_freq1)
            cursor.execute('select * from Словоформи2')
            rows = cursor.fetchall()
            words_freq2 = []
            for row in rows:
                words_freq2.append([row[0], row[1]])
            #print(words_freq2)
            words_freq2 = tuple(words_freq2)
            cursor.execute('select * from Словоформи3')
            rows = cursor.fetchall()
            words_freq3 = []
            for row in rows:
                words_freq3.append([row[0], row[1]])
            words_freq3 = tuple(words_freq3)
            cursor.execute('select * from Словоформи4')
            rows = cursor.fetchall()
            words_freq4 = []
            for row in rows:
                words_freq4.append([row[0], row[1]])
            words_freq4 = tuple(words_freq4)
            cursor.execute('select * from Словоформи5')
            rows = cursor.fetchall()
            words_freq5 = []
            for row in rows:
                words_freq5.append([row[0], row[1]])
            words_freq5 = tuple(words_freq5)
            #print(words_freq1)

            cursor.execute('select * from Частота_Частин_Мови')
            rows = cursor.fetchall()
            parts_of_speech_freq1 = []
            for row in rows:
                parts_of_speech_freq1.append(row)
            cursor.execute('select * from Частота_Частин_Мови2')
            rows = cursor.fetchall()
            parts_of_speech_freq2 = []
            for row in rows:
                parts_of_speech_freq2.append(row)
            cursor.execute('select * from Частота_Частин_Мови3')
            rows = cursor.fetchall()
            parts_of_speech_freq3 = []
            for row in rows:
                parts_of_speech_freq3.append(row)
            cursor.execute('select * from Частота_Частин_Мови4')
            rows = cursor.fetchall()
            parts_of_speech_freq4 = []
            for row in rows:
                parts_of_speech_freq4.append(row)
            cursor.execute('select * from Частота_Частин_Мови5')
            rows = cursor.fetchall()
            parts_of_speech_freq5 = []
            for row in rows:
                parts_of_speech_freq5.append(row)

            cursor.execute('select * from Частота_Лем')
            rows = cursor.fetchall()
            lemmas_freq1 = []
            for row in rows:
                lemmas_freq1.append(row)

            cursor.execute('select * from Частота_Лем2')
            rows = cursor.fetchall()
            lemmas_freq2 = []
            for row in rows:
                lemmas_freq2.append(row)

            cursor.execute('select * from Частота_Лем3')
            rows = cursor.fetchall()
            lemmas_freq3 = []
            for row in rows:
                lemmas_freq3.append(row)

            cursor.execute('select * from Частота_Лем4')
            rows = cursor.fetchall()
            lemmas_freq4 = []
            for row in rows:
                lemmas_freq4.append(row)

            cursor.execute('select * from Частота_Лем5')
            rows = cursor.fetchall()
            lemmas_freq5 = []
            for row in rows:
                lemmas_freq5.append(row)
        getDataFromDataBase()

        # CREATE A FUNCTION FOR CALCULATING EUCLIDE, JACCARD AND COSINE DISTANCES, WHICH ACCEPTS WORD FORMS WITH FREQUENCY AS PARAMETERS
        def countValues(words_freq_1, words_freq_2):
            global euclidean_distance
            global jacquard_distance
            global cosine_distance

            double_freq_dict = {i[0]: [i[1]] for i in words_freq_1}
            keys = []
            for i in words_freq_1:
                keys.append(i[0])

            for i in words_freq_2:
                if i[0] not in keys:
                    double_freq_dict[i[0]] = [0]
                    double_freq_dict[i[0]].append(i[1])
                else:
                     double_freq_dict[i[0]].append(i[1])

            for i in double_freq_dict:
                if len(double_freq_dict[i]) < 2:
                    double_freq_dict[i].append(0)

            double_freq_list = list(double_freq_dict.values())
            double_freq_list.sort()
            count = 0
            while count in range(0, len(double_freq_list)-1):
                if double_freq_list[count][0] < double_freq_list[count+1][0]:
                    double_freq_list[count], double_freq_list[count+1] = double_freq_list[count+1], double_freq_list[count]
                count += 1


            # Calculate the Euclidean distance, cosine similarity and cosine distance
            ai_minus_bi_squared = []
            ai_multiply_bi = []
            ai_squared = []
            bi_squared = []
            intersection_of_a_b = []
            for i in double_freq_list:
                ai_minus_bi_squared.append((i[0]-i[1])**2)
                ai_multiply_bi.append(i[0]*i[1])
                ai_squared.append(i[0]**2)
                bi_squared.append(i[1]**2)
            euclidean_distance = round(sqrt(sum(ai_minus_bi_squared)), 3)
            cosine_similarity = round(sum(ai_multiply_bi)/(sqrt(sum(ai_squared))*sqrt(sum(bi_squared))), 3)
            cosine_distance = round(1-cosine_similarity, 3)


            # Calculate the Jaccard index and distance
            for i in double_freq_list:
                if 0 not in i:
                    intersection_of_a_b.append(i[0])
            jacquard_index = round(len(intersection_of_a_b)/len(double_freq_list), 3)
            jacquard_distance = round(1-jacquard_index, 3)


        # CREATE A FUNCTION FOR CALCULATING INDICES, WHICH ACCEPTS PARTS OF LANGUAGE WITH FREQUENCY AS PARAMETERS
        def countIndexes(parts_of_speech_freq):
            global epitet_index
            global verb_attribute_index
            global degree_of_nominality
            global sum_noun
            global sum_adj
            global sum_advb
            global sum_verb
            sum_noun = None
            sum_adj = None
            sum_advb = None
            sum_verb = None
            for i in parts_of_speech_freq:
                if i[0] == 'NOUN':
                    sum_noun = i[1]
                if i[0] == 'ADJF':
                    sum_adj = i[1]
                if i[0] == 'ADVB':
                    sum_advb = i[1]
                if i[0] == 'VERB':
                    sum_verb = i[1]
            if sum_noun == None:
                epitet_index = str(sum_noun)+'/' + str(sum_adj)
            elif sum_adj==None:
                epitet_index = str(sum_noun) + '/' + str(sum_adj)
            else:
                epitet_index = str(sum_noun) + "/" +str(sum_adj) + ' = ' +  str(round(sum_noun/sum_adj, 3))

            if sum_advb == None:
                verb_attribute_index = str(sum_advb) + '/' + str(sum_verb)
            elif sum_verb==None:
                verb_attribute_index = str(sum_advb) + '/' + str(sum_verb)
            else:
                verb_attribute_index = str(sum_advb) + "/" +str(sum_verb) + ' = ' +  str(round(sum_advb/sum_verb, 3))

            if sum_noun == None:
                degree_of_nominality = str(sum_noun) +'/' + str(sum_verb)
            elif sum_verb==None:
                degree_of_nominality = str(sum_noun) + '/' + str(sum_verb)
            else:
                degree_of_nominality = str(sum_noun) + "/" +str(sum_verb) + ' = ' +  str(round(sum_noun/sum_verb, 3))


        # CREATE A FUNCTION FOR CALCULATING PARAMETERS, WHICH ACCEPTS WORD FORMS AND LEMMAS WITH FREQUENCY AS PARAMETERS
        def counParameters(words_freq, lemmas_freq):
            global N
            global V
            global V1
            global V10_text
            global V10_dict
            global L
            words = []

            for i in words_freq:
                words.append(i[1])
            N = sum(words)
            slovoformy = []
            for i in words_freq:
                slovoformy.append(i[0])
            V = len(slovoformy)
            V1 = []
            for i in words_freq:
                if i[1] == 1:
                    V1.append(i[1])
            V1 = len(V1)
            V10_text = []
            for i in words_freq:
                if i[1] > 10:
                    V10_text.append(i[1])
            V10_text = sum(V10_text)
            V10_dict = []
            for i in words_freq:
                if i[1] > 10:
                    V10_dict.append(i[1])
            V10_dict = len(V10_dict)
            L = []
            for i in lemmas_freq:
                L.append(i[0])
            L = len(L)



        # CREATE A FUNCTION WHICH ACCEPTS THE TEXT NUMBER AND POSITION BY x AS PARAMETERS, CREATES "TABLES" WITH INDEXES AND TEXT PARAMETERS
        def printIndexesAndParameters(number, x):
            global lblIndexes1
            global lblIndexes2
            global lblParameters1
            global lblParameters2
            lblIndexes1 = Label(root, text='Індекси '+str(number)+' тексту', font = ("Times New Roman", 12), fg='darkblue', bg = "white")
            lblIndexes1.place(x=x, y=340, width=280)
            lblIndexes2 = Label(root, text='\n' + 'Індекси епітетизації (Noun/Adjf): ' + str(epitet_index) +
                                    '\n' +'Індекс дієслівних' +'\n'+'означень (Advb/Verb): ' + str(verb_attribute_index) +
                                    '\n' + 'Ступінь номінальності (Noun/Verb): '
                                    + str(degree_of_nominality), font = ("Times New Roman", 10), bg = "white")
            lblIndexes2.place(x=x, y=370, width=280)


            lblParameters1 = Label(root, text='Параметри '+str(number)+' тексту', font = ("Times New Roman", 12), fg='darkblue', bg = "white")
            lblParameters1.place(x=x, y=460, width=280)
            lblParameters2 = Label(root, text= '\n' + 'Багатство словника (V/N): ' + str(round( V/N, 3)) +
                                    '\n' + 'Середня частота N/V: ' + str(round(N/V ,3)) + '\n' + 'Середня частота N/L: ' +
                                    str(round(N/L ,3)) + '\n' + 'Відношення числа різних'+'\n'+' лексем до числа різних словоформ: ' +
                                    str(round(L/V ,3)) + '\n' + 'Індекс винятковості (V1/N): ' + str(round(V1/N ,3)) + '\n' +
                                    'Індекс концентрації у тексті (V10т/V): ' + str(round(V10_text/N ,3)) + '\n'
                                    + 'Індекс концентрації у словнику (V10сл/V): ' + str(round(V10_dict/V ,3)),
                                    font = ("Times New Roman", 10), bg = "white")
            lblParameters2.place(x=x, y=490, width=280)

        # DEPENDING ON THE NUMBER OF TEXTS, FOR EACH TEXT WE CALL THE FUNCTIONS THAT COUNT THE INDEXES AND PARAMETERS,
        # AND THEN THE FUNCTION THAT RECORDS THEM IN THE "TABLE" AND DISPLAYS THEM IN A DIALOG WINDOW
        def getValuesIndexesParameters():
            if int(amount)==5:
                countIndexes(parts_of_speech_freq1)
                counParameters(words_freq1, lemmas_freq1)
                printIndexesAndParameters(1, 30)
                countIndexes(parts_of_speech_freq2)
                counParameters(words_freq2, lemmas_freq2)
                printIndexesAndParameters(2, 330)
                countIndexes(parts_of_speech_freq3)
                counParameters(words_freq3, lemmas_freq3)
                printIndexesAndParameters(3, 630)
                countIndexes(parts_of_speech_freq4)
                counParameters(words_freq4, lemmas_freq4)
                printIndexesAndParameters(4, 930)
                countIndexes(parts_of_speech_freq5)
                counParameters(words_freq5, lemmas_freq5)
                printIndexesAndParameters(5, 1230)

            if int(amount)==4:
                countIndexes(parts_of_speech_freq1)
                counParameters(words_freq1, lemmas_freq1)
                printIndexesAndParameters(1, 30)
                countIndexes(parts_of_speech_freq2)
                counParameters(words_freq2, lemmas_freq2)
                printIndexesAndParameters(2, 330)
                countIndexes(parts_of_speech_freq3)
                counParameters(words_freq3, lemmas_freq3)
                printIndexesAndParameters(3, 630)
                countIndexes(parts_of_speech_freq4)
                counParameters(words_freq4, lemmas_freq4)
                printIndexesAndParameters(4, 930)
            if int(amount)==3:
                countIndexes(parts_of_speech_freq1)
                counParameters(words_freq1, lemmas_freq1)
                printIndexesAndParameters(1, 30)
                countIndexes(parts_of_speech_freq2)
                counParameters(words_freq2, lemmas_freq2)
                printIndexesAndParameters(2, 330)
                countIndexes(parts_of_speech_freq3)
                counParameters(words_freq3, lemmas_freq3)
                printIndexesAndParameters(3, 630)
            if int(amount)==2:
                countIndexes(parts_of_speech_freq1)
                counParameters(words_freq1, lemmas_freq1)
                printIndexesAndParameters(1, 30)
                countIndexes(parts_of_speech_freq2)
                counParameters(words_freq2, lemmas_freq2)
                printIndexesAndParameters(2, 330)
        getValuesIndexesParameters()

        # DEPENDING ON THE NUMBER OF TEXTS, WE CREATE "TABLES" WITH DISTANCE DATA
        # SINCE IT IS NOT POSSIBLE TO INSERT A TABLE, THEY CONSIST OF LABLES
        # COLUMNS: (Xmin-1) - Xmax
        # LINES: Xmin - (Xmax-1)
        def drawTables():
            if int(amount)==5:
                    # create a frame where we will place the first "table" and labels that will contain row/column names or will be empty
                    frameEuclideusDistance = Frame(root)
                    frameEuclideusDistance.place(x=30, y=30, width=250, heigh=300)
                    lblName = Label(frameEuclideusDistance, text='Евклідова відстань' ,font = ("Times New Roman", 12), fg='darkblue', bg = "white") # ярлик з назвою
                    lblName.place(relx=0, rely=0, width=250, heigh=50)
                    lbl0 = Label(frameEuclideusDistance, bg = "white")
                    lbl0.place(relx=0, rely=0.17, width=50, heigh=50)
                    lbl2 = Label(frameEuclideusDistance, text='Текст 2' ,font = ("Times New Roman", 10), bg = "white")
                    lbl2.place(relx=0.2, rely=0.17, width=50, heigh=50)
                    lbl3 = Label(frameEuclideusDistance, text='Текст 3' ,font = ("Times New Roman", 10), bg = "white")
                    lbl3.place(relx=0.4, rely=0.17, width=50, heigh=50)
                    lbl4 = Label(frameEuclideusDistance, text='Текст 4' ,font = ("Times New Roman", 10), bg = "white")
                    lbl4.place(relx=0.6, rely=0.17, width=50, heigh=50)
                    lbl5 = Label(frameEuclideusDistance, text='Текст 5' ,font = ("Times New Roman", 10), bg = "white")
                    lbl5.place(relx=0.8, rely=0.17, width=50, heigh=50)
                    lbl1 = Label(frameEuclideusDistance, text='Текст 1' ,font = ("Times New Roman", 10), bg = "white")
                    lbl1.place(relx=0, rely=0.34, width=50, heigh=50)

                    # create a frame where we will place the second "table" and labels that will contain row/column names or will be empty
                    frameCosineDistance = Frame(root)
                    frameCosineDistance.place(x=330, y=30, width=250, heigh=300)
                    lblName = Label(frameCosineDistance, text='Косинусна відстань' ,font = ("Times New Roman", 12), fg='darkblue', bg = "white")
                    lblName.place(relx=0, rely=0, width=250, heigh=50)
                    lbl0 = Label(frameCosineDistance, bg = "white")
                    lbl0.place(relx=0, rely=0.17, width=50, heigh=50)
                    lbl2 = Label(frameCosineDistance, text='Текст 2' ,font = ("Times New Roman", 10), bg = "white")
                    lbl2.place(relx=0.2, rely=0.17, width=50, heigh=50)
                    lbl3 = Label(frameCosineDistance, text='Текст 3' ,font = ("Times New Roman", 10), bg = "white")
                    lbl3.place(relx=0.4, rely=0.17, width=50, heigh=50)
                    lbl4 = Label(frameCosineDistance, text='Текст 4' ,font = ("Times New Roman", 10), bg = "white")
                    lbl4.place(relx=0.6, rely=0.17, width=50, heigh=50)
                    lbl5 = Label(frameCosineDistance, text='Текст 5' ,font = ("Times New Roman", 10), bg = "white")
                    lbl5.place(relx=0.8, rely=0.17, width=50, heigh=50)
                    lbl1 = Label(frameCosineDistance, text='Текст 1' ,font = ("Times New Roman", 10), bg = "white")
                    lbl1.place(relx=0, rely=0.34, width=50, heigh=50)

                    # create a frame where we will place the third "table" and labels that will contain row/column names or will be empty
                    frameJacquardDistance = Frame(root)
                    frameJacquardDistance.place(x=630, y=30, width=250, heigh=300)
                    lblName = Label(frameJacquardDistance, text='Відстань Жаккарда' ,font = ("Times New Roman", 12), fg='darkblue', bg = "white")
                    lblName.place(relx=0, rely=0, width=250, heigh=50)
                    lbl0 = Label(frameJacquardDistance, bg = "white")
                    lbl0.place(relx=0, rely=0.17, width=50, heigh=50)
                    lbl2 = Label(frameJacquardDistance, text='Текст 2' ,font = ("Times New Roman", 10), bg = "white")
                    lbl2.place(relx=0.2, rely=0.17, width=50, heigh=50)
                    lbl3 = Label(frameJacquardDistance, text='Текст 3' ,font = ("Times New Roman", 10), bg = "white")
                    lbl3.place(relx=0.4, rely=0.17, width=50, heigh=50)
                    lbl4 = Label(frameJacquardDistance, text='Текст 4' ,font = ("Times New Roman", 10), bg = "white")
                    lbl4.place(relx=0.6, rely=0.17, width=50, heigh=50)
                    lbl5 = Label(frameJacquardDistance, text='Текст 5' ,font = ("Times New Roman", 10), bg = "white")
                    lbl5.place(relx=0.8, rely=0.17, width=50, heigh=50)
                    lbl1 = Label(frameJacquardDistance, text='Текст 1' ,font = ("Times New Roman", 10), bg = "white")
                    lbl1.place(relx=0, rely=0.34, width=50, heigh=50)

                    # call the function that calculates the distances for the first and second texts
                    countValues(words_freq1, words_freq2)
                    # створюємо ярлики зі значеннями 3 відстаней для першого і другого текстів
                    lbl1_2 = Label(frameEuclideusDistance, text=str(euclidean_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl1_2.place(relx=0.2, rely=0.34, width=50, heigh=50)
                    lbl1_2 = Label(frameCosineDistance, text=str(cosine_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl1_2.place(relx=0.2, rely=0.34, width=50, heigh=50)
                    lbl1_2 = Label(frameJacquardDistance, text=str(jacquard_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl1_2.place(relx=0.2, rely=0.34, width=50, heigh=50)

                    # call the function that calculates the distances for the second and third texts
                    countValues(words_freq1, words_freq3)
                    # створюємо ярлики зі значеннями 3 відстаней для другого і третього текстів
                    lbl1_3 = Label(frameEuclideusDistance, text=str(euclidean_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl1_3.place(relx=0.4, rely=0.34, width=50, heigh=50)
                    lbl1_3 = Label(frameCosineDistance, text=str(cosine_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl1_3.place(relx=0.4, rely=0.34, width=50, heigh=50)
                    lbl1_3 = Label(frameJacquardDistance, text=str(jacquard_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl1_3.place(relx=0.4, rely=0.34, width=50, heigh=50)

                    countValues(words_freq1, words_freq4)
                    lbl1_4 = Label(frameEuclideusDistance, text=str(euclidean_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl1_4.place(relx=0.6, rely=0.34, width=50, heigh=50)
                    lbl1_4 = Label(frameCosineDistance, text=str(cosine_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl1_4.place(relx=0.6, rely=0.34, width=50, heigh=50)
                    lbl1_4 = Label(frameJacquardDistance, text=str(jacquard_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl1_4.place(relx=0.6, rely=0.34, width=50, heigh=50)

                    countValues(words_freq1, words_freq5)
                    lbl1_5 = Label(frameEuclideusDistance, text=str(euclidean_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl1_5.place(relx=0.8, rely=0.34, width=50, heigh=50)
                    lbl1_5 = Label(frameCosineDistance, text=str(cosine_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl1_5.place(relx=0.8, rely=0.34, width=50, heigh=50)
                    lbl1_5 = Label(frameJacquardDistance, text=str(jacquard_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl1_5.place(relx=0.8, rely=0.34, width=50, heigh=50)

                    countValues(words_freq2, words_freq3)
                    lbl2 = Label(frameEuclideusDistance, text='Текст 2' ,font = ("Times New Roman", 10), bg = "white")
                    lbl2.place(relx=0, rely=0.51, width=50, heigh=50)
                    lbl2_2 = Label(frameEuclideusDistance,font = ("Times New Roman", 10), bg = "white")
                    lbl2_2.place(relx=0.2, rely=0.51, width=50, heigh=50)
                    lbl2_3 = Label(frameEuclideusDistance, text=str(euclidean_distance), font = ("Times New Roman", 10), bg = "white")
                    lbl2_3.place(relx=0.4, rely=0.51, width=50, heigh=50)
                    lbl2 = Label(frameCosineDistance, text='Текст 2' ,font = ("Times New Roman", 10), bg = "white")
                    lbl2.place(relx=0, rely=0.51, width=50, heigh=50)
                    lbl2_2 = Label(frameCosineDistance,font = ("Times New Roman", 10), bg = "white")
                    lbl2_2.place(relx=0.2, rely=0.51, width=50, heigh=50)
                    lbl2_3 = Label(frameCosineDistance, text=str(cosine_distance), font = ("Times New Roman", 10), bg = "white")
                    lbl2_3.place(relx=0.4, rely=0.51, width=50, heigh=50)
                    lbl2 = Label(frameJacquardDistance, text='Текст 2' ,font = ("Times New Roman", 10), bg = "white")
                    lbl2.place(relx=0, rely=0.51, width=50, heigh=50)
                    lbl2_2 = Label(frameJacquardDistance,font = ("Times New Roman", 10), bg = "white")
                    lbl2_2.place(relx=0.2, rely=0.51, width=50, heigh=50)
                    lbl2_3 = Label(frameJacquardDistance, text=str(jacquard_distance), font = ("Times New Roman", 10), bg = "white")
                    lbl2_3.place(relx=0.4, rely=0.51, width=50, heigh=50)

                    countValues(words_freq2, words_freq4)
                    lbl2_4 = Label(frameEuclideusDistance, text=str(euclidean_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl2_4.place(relx=0.6, rely=0.51, width=50, heigh=50)
                    lbl2_4 = Label(frameCosineDistance, text=str(cosine_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl2_4.place(relx=0.6, rely=0.51, width=50, heigh=50)
                    lbl2_4 = Label(frameJacquardDistance, text=str(jacquard_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl2_4.place(relx=0.6, rely=0.51, width=50, heigh=50)

                    countValues(words_freq2, words_freq5)
                    lbl2_5 = Label(frameEuclideusDistance, text=str(euclidean_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl2_5.place(relx=0.8, rely=0.51, width=50, heigh=50)
                    lbl2_5 = Label(frameCosineDistance, text=str(cosine_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl2_5.place(relx=0.8, rely=0.51, width=50, heigh=50)
                    lbl2_5 = Label(frameJacquardDistance, text=str(jacquard_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl2_5.place(relx=0.8, rely=0.51, width=50, heigh=50)

                    countValues(words_freq3, words_freq4)
                    lbl3 = Label(frameEuclideusDistance, text='Текст 3' ,font = ("Times New Roman", 10), bg = "white")
                    lbl3.place(relx=0, rely=0.68, width=50, heigh=50)
                    lbl3_2 = Label(frameEuclideusDistance ,font = ("Times New Roman", 10), bg = "white")
                    lbl3_2.place(relx=0.2, rely=0.68, width=50, heigh=50)
                    lbl3_3 = Label(frameEuclideusDistance,font = ("Times New Roman", 10), bg = "white")
                    lbl3_3.place(relx=0.4, rely=0.68, width=50, heigh=50)
                    lbl3_4 = Label(frameEuclideusDistance, text=str(euclidean_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl3_4.place(relx=0.6, rely=0.68, width=50, heigh=50)
                    lbl3 = Label(frameCosineDistance, text='Текст 3' ,font = ("Times New Roman", 10), bg = "white")
                    lbl3.place(relx=0, rely=0.68, width=50, heigh=50)
                    lbl3_2 = Label(frameCosineDistance ,font = ("Times New Roman", 10), bg = "white")
                    lbl3_2.place(relx=0.2, rely=0.68, width=50, heigh=50)
                    lbl3_3 = Label(frameCosineDistance,font = ("Times New Roman", 10), bg = "white")
                    lbl3_3.place(relx=0.4, rely=0.68, width=50, heigh=50)
                    lbl3_4 = Label(frameCosineDistance, text=str(cosine_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl3_4.place(relx=0.6, rely=0.68, width=50, heigh=50)
                    lbl3 = Label(frameJacquardDistance, text='Текст 3' ,font = ("Times New Roman", 10), bg = "white")
                    lbl3.place(relx=0, rely=0.68, width=50, heigh=50)
                    lbl3_2 = Label(frameJacquardDistance ,font = ("Times New Roman", 10), bg = "white")
                    lbl3_2.place(relx=0.2, rely=0.68, width=50, heigh=50)
                    lbl3_3 = Label(frameJacquardDistance,font = ("Times New Roman", 10), bg = "white")
                    lbl3_3.place(relx=0.4, rely=0.68, width=50, heigh=50)
                    lbl3_4 = Label(frameJacquardDistance, text=str(jacquard_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl3_4.place(relx=0.6, rely=0.68, width=50, heigh=50)

                    countValues(words_freq3, words_freq5)
                    lbl3_5 = Label(frameEuclideusDistance, text=str(euclidean_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl3_5.place(relx=0.8, rely=0.68, width=50, heigh=50)
                    lbl3_5 = Label(frameCosineDistance, text=str(cosine_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl3_5.place(relx=0.8, rely=0.68, width=50, heigh=50)
                    lbl3_5 = Label(frameJacquardDistance, text=str(jacquard_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl3_5.place(relx=0.8, rely=0.68, width=50, heigh=50)

                    countValues(words_freq4, words_freq5)
                    lbl4 = Label(frameEuclideusDistance, text='Текст 4' ,font = ("Times New Roman", 10), bg = "white")
                    lbl4.place(relx=0, rely=0.85, width=50, heigh=50)
                    lbl4_2 = Label(frameEuclideusDistance ,font = ("Times New Roman", 10), bg = "white")
                    lbl4_2.place(relx=0.2, rely=0.85, width=50, heigh=50)
                    lbl4_3 = Label(frameEuclideusDistance,font = ("Times New Roman", 10), bg = "white")
                    lbl4_3.place(relx=0.4, rely=0.85, width=50, heigh=50)
                    lbl4_4 = Label(frameEuclideusDistance ,font = ("Times New Roman", 10), bg = "white")
                    lbl4_4.place(relx=0.6, rely=0.85, width=50, heigh=50)
                    lbl4_5 = Label(frameEuclideusDistance, text=str(euclidean_distance), font = ("Times New Roman", 10), bg = "white")
                    lbl4_5.place(relx=0.8, rely=0.85, width=50, heigh=50)
                    lbl4 = Label(frameCosineDistance, text='Текст 4' ,font = ("Times New Roman", 10), bg = "white")
                    lbl4.place(relx=0, rely=0.85, width=50, heigh=50)
                    lbl4_2 = Label(frameCosineDistance ,font = ("Times New Roman", 10), bg = "white")
                    lbl4_2.place(relx=0.2, rely=0.85, width=50, heigh=50)
                    lbl4_3 = Label(frameCosineDistance,font = ("Times New Roman", 10), bg = "white")
                    lbl4_3.place(relx=0.4, rely=0.85, width=50, heigh=50)
                    lbl4_4 = Label(frameCosineDistance ,font = ("Times New Roman", 10), bg = "white")
                    lbl4_4.place(relx=0.6, rely=0.85, width=50, heigh=50)
                    lbl4_5 = Label(frameCosineDistance, text=str(cosine_distance), font = ("Times New Roman", 10), bg = "white")
                    lbl4_5.place(relx=0.8, rely=0.85, width=50, heigh=50)
                    lbl4 = Label(frameJacquardDistance, text='Текст 4' ,font = ("Times New Roman", 10), bg = "white")
                    lbl4.place(relx=0, rely=0.85, width=50, heigh=50)
                    lbl4_2 = Label(frameJacquardDistance ,font = ("Times New Roman", 10), bg = "white")
                    lbl4_2.place(relx=0.2, rely=0.85, width=50, heigh=50)
                    lbl4_3 = Label(frameJacquardDistance,font = ("Times New Roman", 10), bg = "white")
                    lbl4_3.place(relx=0.4, rely=0.85, width=50, heigh=50)
                    lbl4_4 = Label(frameJacquardDistance ,font = ("Times New Roman", 10), bg = "white")
                    lbl4_4.place(relx=0.6, rely=0.85, width=50, heigh=50)
                    lbl4_5 = Label(frameJacquardDistance, text=str(jacquard_distance), font = ("Times New Roman", 10), bg = "white")
                    lbl4_5.place(relx=0.8, rely=0.85, width=50, heigh=50)

            if int(amount)==4:
                    frameEuclideusDistance = Frame(root)
                    frameEuclideusDistance.place(x=30, y=30, width=250, heigh=300)
                    lblName = Label(frameEuclideusDistance, text='Евклідова відстань' ,font = ("Times New Roman", 12), fg='darkblue', bg = "white")
                    lblName.place(relx=0, rely=0, width=200, heigh=50)
                    lbl0 = Label(frameEuclideusDistance, bg = "white")
                    lbl0.place(relx=0, rely=0.17, width=50, heigh=50)
                    lbl2 = Label(frameEuclideusDistance, text='Текст 2' ,font = ("Times New Roman", 10), bg = "white")
                    lbl2.place(relx=0.2, rely=0.17, width=50, heigh=50)
                    lbl3 = Label(frameEuclideusDistance, text='Текст 3' ,font = ("Times New Roman", 10), bg = "white")
                    lbl3.place(relx=0.4, rely=0.17, width=50, heigh=50)
                    lbl4 = Label(frameEuclideusDistance, text='Текст 4' ,font = ("Times New Roman", 10), bg = "white")
                    lbl4.place(relx=0.6, rely=0.17, width=50, heigh=50)
                    lbl1 = Label(frameEuclideusDistance, text='Текст 1' ,font = ("Times New Roman", 10), bg = "white")
                    lbl1.place(relx=0, rely=0.34, width=50, heigh=50)

                    frameCosineDistance = Frame(root)
                    frameCosineDistance.place(x=330, y=30, width=250, heigh=300)
                    lblName = Label(frameCosineDistance, text='Косинусна відстань' ,font = ("Times New Roman", 12), fg='darkblue', bg = "white")
                    lblName.place(relx=0, rely=0, width=200, heigh=50)
                    lbl0 = Label(frameCosineDistance, bg = "white")
                    lbl0.place(relx=0, rely=0.17, width=50, heigh=50)
                    lbl2 = Label(frameCosineDistance, text='Текст 2' ,font = ("Times New Roman", 10), bg = "white")
                    lbl2.place(relx=0.2, rely=0.17, width=50, heigh=50)
                    lbl3 = Label(frameCosineDistance, text='Текст 3' ,font = ("Times New Roman", 10), bg = "white")
                    lbl3.place(relx=0.4, rely=0.17, width=50, heigh=50)
                    lbl4 = Label(frameCosineDistance, text='Текст 4' ,font = ("Times New Roman", 10), bg = "white")
                    lbl4.place(relx=0.6, rely=0.17, width=50, heigh=50)
                    lbl1 = Label(frameCosineDistance, text='Текст 1' ,font = ("Times New Roman", 10), bg = "white")
                    lbl1.place(relx=0, rely=0.34, width=50, heigh=50)

                    frameJacquardDistance = Frame(root) #jacquard_distance
                    frameJacquardDistance.place(x=610, y=30, width=250, heigh=300)
                    lblName = Label(frameJacquardDistance, text='Відстань Жаккарда' ,font = ("Times New Roman", 12), fg='darkblue', bg = "white")
                    lblName.place(relx=0, rely=0, width=200, heigh=50)
                    lbl0 = Label(frameJacquardDistance, bg = "white")
                    lbl0.place(relx=0, rely=0.17, width=50, heigh=50)
                    lbl2 = Label(frameJacquardDistance, text='Текст 2' ,font = ("Times New Roman", 10), bg = "white")
                    lbl2.place(relx=0.2, rely=0.17, width=50, heigh=50)
                    lbl3 = Label(frameJacquardDistance, text='Текст 3' ,font = ("Times New Roman", 10), bg = "white")
                    lbl3.place(relx=0.4, rely=0.17, width=50, heigh=50)
                    lbl4 = Label(frameJacquardDistance, text='Текст 4' ,font = ("Times New Roman", 10), bg = "white")
                    lbl4.place(relx=0.6, rely=0.17, width=50, heigh=50)
                    lbl1 = Label(frameJacquardDistance, text='Текст 1' ,font = ("Times New Roman", 10), bg = "white")
                    lbl1.place(relx=0, rely=0.34, width=50, heigh=50)

                    countValues(words_freq1, words_freq2)
                    lbl1_2 = Label(frameEuclideusDistance, text=str(euclidean_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl1_2.place(relx=0.2, rely=0.34, width=50, heigh=50)
                    lbl1_2 = Label(frameCosineDistance, text=str(cosine_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl1_2.place(relx=0.2, rely=0.34, width=50, heigh=50)
                    lbl1_2 = Label(frameJacquardDistance, text=str(jacquard_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl1_2.place(relx=0.2, rely=0.34, width=50, heigh=50)

                    countValues(words_freq1, words_freq3)
                    lbl1_3 = Label(frameEuclideusDistance, text=str(euclidean_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl1_3.place(relx=0.4, rely=0.34, width=50, heigh=50)
                    lbl1_3 = Label(frameCosineDistance, text=str(cosine_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl1_3.place(relx=0.4, rely=0.34, width=50, heigh=50)
                    lbl1_3 = Label(frameJacquardDistance, text=str(jacquard_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl1_3.place(relx=0.4, rely=0.34, width=50, heigh=50)

                    countValues(words_freq1, words_freq4)
                    lbl1_4 = Label(frameEuclideusDistance, text=str(euclidean_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl1_4.place(relx=0.6, rely=0.34, width=50, heigh=50)
                    lbl1_4 = Label(frameCosineDistance, text=str(cosine_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl1_4.place(relx=0.6, rely=0.34, width=50, heigh=50)
                    lbl1_4 = Label(frameJacquardDistance, text=str(jacquard_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl1_4.place(relx=0.6, rely=0.34, width=50, heigh=50)

                    countValues(words_freq2, words_freq3)
                    lbl2 = Label(frameEuclideusDistance, text='Текст 2' ,font = ("Times New Roman", 10), bg = "white")
                    lbl2.place(relx=0, rely=0.51, width=50, heigh=50)
                    lbl2_2 = Label(frameEuclideusDistance,font = ("Times New Roman", 10), bg = "white")
                    lbl2_2.place(relx=0.2, rely=0.51, width=50, heigh=50)
                    lbl2_3 = Label(frameEuclideusDistance, text=str(euclidean_distance), font = ("Times New Roman", 10), bg = "white")
                    lbl2_3.place(relx=0.4, rely=0.51, width=50, heigh=50)
                    lbl2 = Label(frameCosineDistance, text='Текст 2' ,font = ("Times New Roman", 10), bg = "white")
                    lbl2.place(relx=0, rely=0.51, width=50, heigh=50)
                    lbl2_2 = Label(frameCosineDistance,font = ("Times New Roman", 10), bg = "white")
                    lbl2_2.place(relx=0.2, rely=0.51, width=50, heigh=50)
                    lbl2_3 = Label(frameCosineDistance, text=str(cosine_distance), font = ("Times New Roman", 10), bg = "white")
                    lbl2_3.place(relx=0.4, rely=0.51, width=50, heigh=50)
                    lbl2 = Label(frameJacquardDistance, text='Текст 2' ,font = ("Times New Roman", 10), bg = "white")
                    lbl2.place(relx=0, rely=0.51, width=50, heigh=50)
                    lbl2_2 = Label(frameJacquardDistance,font = ("Times New Roman", 10), bg = "white")
                    lbl2_2.place(relx=0.2, rely=0.51, width=50, heigh=50)
                    lbl2_3 = Label(frameJacquardDistance, text=str(jacquard_distance), font = ("Times New Roman", 10), bg = "white")
                    lbl2_3.place(relx=0.4, rely=0.51, width=50, heigh=50)

                    countValues(words_freq2, words_freq4)
                    lbl2_4 = Label(frameEuclideusDistance, text=str(euclidean_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl2_4.place(relx=0.6, rely=0.51, width=50, heigh=50)
                    lbl2_4 = Label(frameCosineDistance, text=str(cosine_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl2_4.place(relx=0.6, rely=0.51, width=50, heigh=50)
                    lbl2_4 = Label(frameJacquardDistance, text=str(jacquard_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl2_4.place(relx=0.6, rely=0.51, width=50, heigh=50)

                    countValues(words_freq3, words_freq4)
                    lbl3 = Label(frameEuclideusDistance, text='Текст 3' ,font = ("Times New Roman", 10), bg = "white")
                    lbl3.place(relx=0, rely=0.68, width=50, heigh=50)
                    lbl3_2 = Label(frameEuclideusDistance ,font = ("Times New Roman", 10), bg = "white")
                    lbl3_2.place(relx=0.2, rely=0.68, width=50, heigh=50)
                    lbl3_3 = Label(frameEuclideusDistance,font = ("Times New Roman", 10), bg = "white")
                    lbl3_3.place(relx=0.4, rely=0.68, width=50, heigh=50)
                    lbl3_4 = Label(frameEuclideusDistance, text=str(euclidean_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl3_4.place(relx=0.6, rely=0.68, width=50, heigh=50)
                    lbl3 = Label(frameCosineDistance, text='Текст 3' ,font = ("Times New Roman", 10), bg = "white")
                    lbl3.place(relx=0, rely=0.68, width=50, heigh=50)
                    lbl3_2 = Label(frameCosineDistance ,font = ("Times New Roman", 10), bg = "white")
                    lbl3_2.place(relx=0.2, rely=0.68, width=50, heigh=50)
                    lbl3_3 = Label(frameCosineDistance,font = ("Times New Roman", 10), bg = "white")
                    lbl3_3.place(relx=0.4, rely=0.68, width=50, heigh=50)
                    lbl3_4 = Label(frameCosineDistance, text=str(cosine_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl3_4.place(relx=0.6, rely=0.68, width=50, heigh=50)
                    lbl3 = Label(frameJacquardDistance, text='Текст 3' ,font = ("Times New Roman", 10), bg = "white")
                    lbl3.place(relx=0, rely=0.68, width=50, heigh=50)
                    lbl3_2 = Label(frameJacquardDistance ,font = ("Times New Roman", 10), bg = "white")
                    lbl3_2.place(relx=0.2, rely=0.68, width=50, heigh=50)
                    lbl3_3 = Label(frameJacquardDistance,font = ("Times New Roman", 10), bg = "white")
                    lbl3_3.place(relx=0.4, rely=0.68, width=50, heigh=50)
                    lbl3_4 = Label(frameJacquardDistance, text=str(jacquard_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl3_4.place(relx=0.6, rely=0.68, width=50, heigh=50)

            if int(amount)==3:
                    frameEuclideusDistance = Frame(root)
                    frameEuclideusDistance.place(x=30, y=30, width=250, heigh=300)
                    lblName = Label(frameEuclideusDistance, text='Евклідова відстань' ,font = ("Times New Roman", 12), fg='darkblue', bg = "white")
                    lblName.place(relx=0, rely=0, width=150, heigh=50)
                    lbl0 = Label(frameEuclideusDistance, bg = "white")
                    lbl0.place(relx=0, rely=0.17, width=50, heigh=50)
                    lbl2 = Label(frameEuclideusDistance, text='Текст 2' ,font = ("Times New Roman", 10), bg = "white")
                    lbl2.place(relx=0.2, rely=0.17, width=50, heigh=50)
                    lbl3 = Label(frameEuclideusDistance, text='Текст 3' ,font = ("Times New Roman", 10), bg = "white")
                    lbl3.place(relx=0.4, rely=0.17, width=50, heigh=50)
                    lbl1 = Label(frameEuclideusDistance, text='Текст 1' ,font = ("Times New Roman", 10), bg = "white")
                    lbl1.place(relx=0, rely=0.34, width=50, heigh=50)

                    frameCosineDistance = Frame(root)
                    frameCosineDistance.place(x=330, y=30, width=250, heigh=300)
                    lblName = Label(frameCosineDistance, text='Косинусна відстань' ,font = ("Times New Roman", 12), fg='darkblue', bg = "white")
                    lblName.place(relx=0, rely=0, width=150, heigh=50)
                    lbl0 = Label(frameCosineDistance, bg = "white")
                    lbl0.place(relx=0, rely=0.17, width=50, heigh=50)
                    lbl2 = Label(frameCosineDistance, text='Текст 2' ,font = ("Times New Roman", 10), bg = "white")
                    lbl2.place(relx=0.2, rely=0.17, width=50, heigh=50)
                    lbl3 = Label(frameCosineDistance, text='Текст 3' ,font = ("Times New Roman", 10), bg = "white")
                    lbl3.place(relx=0.4, rely=0.17, width=50, heigh=50)
                    lbl1 = Label(frameCosineDistance, text='Текст 1' ,font = ("Times New Roman", 10), bg = "white")
                    lbl1.place(relx=0, rely=0.34, width=50, heigh=50)

                    frameJacquardDistance = Frame(root) #jacquard_distance
                    frameJacquardDistance.place(x=610, y=30, width=250, heigh=300)
                    lblName = Label(frameJacquardDistance, text='Відстань Жаккарда' ,font = ("Times New Roman", 12), fg='darkblue', bg = "white")
                    lblName.place(relx=0, rely=0, width=150, heigh=50)
                    lbl0 = Label(frameJacquardDistance, bg = "white")
                    lbl0.place(relx=0, rely=0.17, width=50, heigh=50)
                    lbl2 = Label(frameJacquardDistance, text='Текст 2' ,font = ("Times New Roman", 10), bg = "white")
                    lbl2.place(relx=0.2, rely=0.17, width=50, heigh=50)
                    lbl3 = Label(frameJacquardDistance, text='Текст 3' ,font = ("Times New Roman", 10), bg = "white")
                    lbl3.place(relx=0.4, rely=0.17, width=50, heigh=50)
                    lbl1 = Label(frameJacquardDistance, text='Текст 1' ,font = ("Times New Roman", 10), bg = "white")
                    lbl1.place(relx=0, rely=0.34, width=50, heigh=50)


                    countValues(words_freq1, words_freq2)
                    lbl1_2 = Label(frameEuclideusDistance, text=str(euclidean_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl1_2.place(relx=0.2, rely=0.34, width=50, heigh=50)
                    lbl1_2 = Label(frameCosineDistance, text=str(cosine_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl1_2.place(relx=0.2, rely=0.34, width=50, heigh=50)
                    lbl1_2 = Label(frameJacquardDistance, text=str(jacquard_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl1_2.place(relx=0.2, rely=0.34, width=50, heigh=50)

                    countValues(words_freq1, words_freq3)
                    lbl1_3 = Label(frameEuclideusDistance, text=str(euclidean_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl1_3.place(relx=0.4, rely=0.34, width=50, heigh=50)
                    lbl1_3 = Label(frameCosineDistance, text=str(cosine_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl1_3.place(relx=0.4, rely=0.34, width=50, heigh=50)
                    lbl1_3 = Label(frameJacquardDistance, text=str(jacquard_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl1_3.place(relx=0.4, rely=0.34, width=50, heigh=50)

                    countValues(words_freq2, words_freq3)
                    lbl2 = Label(frameEuclideusDistance, text='Текст 2' ,font = ("Times New Roman", 10), bg = "white")
                    lbl2.place(relx=0, rely=0.51, width=50, heigh=50)
                    lbl2_2 = Label(frameEuclideusDistance,font = ("Times New Roman", 10), bg = "white")
                    lbl2_2.place(relx=0.2, rely=0.51, width=50, heigh=50)
                    lbl2_3 = Label(frameEuclideusDistance, text=str(euclidean_distance), font = ("Times New Roman", 10), bg = "white")
                    lbl2_3.place(relx=0.4, rely=0.51, width=50, heigh=50)
                    lbl2 = Label(frameCosineDistance, text='Текст 2' ,font = ("Times New Roman", 10), bg = "white")
                    lbl2.place(relx=0, rely=0.51, width=50, heigh=50)
                    lbl2_2 = Label(frameCosineDistance,font = ("Times New Roman", 10), bg = "white")
                    lbl2_2.place(relx=0.2, rely=0.51, width=50, heigh=50)
                    lbl2_3 = Label(frameCosineDistance, text=str(cosine_distance), font = ("Times New Roman", 10), bg = "white")
                    lbl2_3.place(relx=0.4, rely=0.51, width=50, heigh=50)
                    lbl2 = Label(frameJacquardDistance, text='Текст 2' ,font = ("Times New Roman", 10), bg = "white")
                    lbl2.place(relx=0, rely=0.51, width=50, heigh=50)
                    lbl2_2 = Label(frameJacquardDistance,font = ("Times New Roman", 10), bg = "white")
                    lbl2_2.place(relx=0.2, rely=0.51, width=50, heigh=50)
                    lbl2_3 = Label(frameJacquardDistance, text=str(jacquard_distance), font = ("Times New Roman", 10), bg = "white")
                    lbl2_3.place(relx=0.4, rely=0.51, width=50, heigh=50)


            if int(amount)==2:
                    frameEuclideusDistance = Frame(root)
                    frameEuclideusDistance.place(x=30, y=30, width=250, heigh=300)
                    lblName = Label(frameEuclideusDistance, text='Евклідова' + '\n'+  'відстань' ,font = ("Times New Roman", 12), fg='darkblue', bg = "white")
                    lblName.place(relx=0, rely=0, width=100, heigh=50)
                    lbl0 = Label(frameEuclideusDistance, bg = "white")
                    lbl0.place(relx=0, rely=0.17, width=50, heigh=50)
                    lbl2 = Label(frameEuclideusDistance, text='Текст 2' ,font = ("Times New Roman", 10), bg = "white")
                    lbl2.place(relx=0.2, rely=0.17, width=50, heigh=50)
                    lbl1 = Label(frameEuclideusDistance, text='Текст 1' ,font = ("Times New Roman", 10), bg = "white")
                    lbl1.place(relx=0, rely=0.34, width=50, heigh=50)

                    frameCosineDistance = Frame(root)
                    frameCosineDistance.place(x=330, y=30, width=250, heigh=300)
                    lblName = Label(frameCosineDistance, text='Косинусна' + '\n'+ 'відстань' ,font = ("Times New Roman", 12), fg='darkblue', bg = "white")
                    lblName.place(relx=0, rely=0, width=100, heigh=50)
                    lbl0 = Label(frameCosineDistance, bg = "white")
                    lbl0.place(relx=0, rely=0.17, width=50, heigh=50)
                    lbl2 = Label(frameCosineDistance, text='Текст 2' ,font = ("Times New Roman", 10), bg = "white")
                    lbl2.place(relx=0.2, rely=0.17, width=50, heigh=50)
                    lbl1 = Label(frameCosineDistance, text='Текст 1' ,font = ("Times New Roman", 10), bg = "white")
                    lbl1.place(relx=0, rely=0.34, width=50, heigh=50)

                    frameJacquardDistance = Frame(root) #jacquard_distance
                    frameJacquardDistance.place(x=610, y=30, width=250, heigh=300)
                    lblName = Label(frameJacquardDistance, text='Відстань' + '\n'+  'Жаккарда' ,font = ("Times New Roman", 12), fg='darkblue', bg = "white")
                    lblName.place(relx=0, rely=0, width=100, heigh=50)
                    lbl0 = Label(frameJacquardDistance, bg = "white")
                    lbl0.place(relx=0, rely=0.17, width=50, heigh=50)
                    lbl2 = Label(frameJacquardDistance, text='Текст 2' ,font = ("Times New Roman", 10), bg = "white")
                    lbl2.place(relx=0.2, rely=0.17, width=50, heigh=50)
                    lbl1 = Label(frameJacquardDistance, text='Текст 1' ,font = ("Times New Roman", 10), bg = "white")
                    lbl1.place(relx=0, rely=0.34, width=50, heigh=50)


                    countValues(words_freq1, words_freq2)
                    lbl1_2 = Label(frameEuclideusDistance, text=str(euclidean_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl1_2.place(relx=0.2, rely=0.34, width=50, heigh=50)
                    lbl1_2 = Label(frameCosineDistance, text=str(cosine_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl1_2.place(relx=0.2, rely=0.34, width=50, heigh=50)
                    lbl1_2 = Label(frameJacquardDistance, text=str(jacquard_distance) ,font = ("Times New Roman", 10), bg = "white")
                    lbl1_2.place(relx=0.2, rely=0.34, width=50, heigh=50)
        drawTables()

        def drawTips():
            lblTips = Label(root, text='Основні статистичні характеристики', font = ("Times New Roman", 12), fg='white', bg = "LightSkyBlue4")
            lblTips.place(x=900, y=30, width=365)
            lblTips2=Label(root, text='N - обсяг тексту, на основі якого укладено словник'+'\n'+
                        'V - обсяг словника словоформ'+'\n'+'L - обсяг словника лексем'+'\n'+'V1 - кількість слів, що зустрілися 1 раз'
                        +'\n'+'V10т - кількість слів у тексті з частотою більше 10'+
                        '\n'+'V10 - кількість слів у тсловнику з частотою більше 10', font = ("Times New Roman", 12), fg='white', bg = "LightSkyBlue4")
            lblTips2.place(x=900, y=60)
        drawTips()

        btnDropTables=Button(root, text='Очисити словники', command=dropTables , font = ("Times New Roman", 12), fg='white', bg = "red4")
        btnDropTables.place(x=1300, y=30)
    common()

    # AFTER PRESSING THE BUTTON WITH THE NAME OF A SPECIFIC DICTIONARY, ITS CONTENTS ARE DISPLAYED ON THE SCREEN
     # THERE ARE ALSO BUTTONS TO CHANGE THE CONTENTS OF DICTIONARIES
    def lablesShowTables():
        def lablesShowTable1():
            btnShowTables1 = Button(root, text='Переглянути частотні словники 1 вірша', bg = "darkblue", font = ("Times New Roman", 10),
                                                fg ="white", command =showTables1)
            btnShowTables1.place(x=30, y=630)
        def lablesShowTable2():
            btnShowTables2 = Button(root, text='Переглянути частотні словники 2 вірша', bg = "darkblue", font = ("Times New Roman", 10),
                                                fg ="white", command =showTables2)
            btnShowTables2.place(x=30, y=670)
        def lablesShowTable3():
            btnShowTables3 = Button(root, text='Переглянути частотні словники 3 вірша', bg = "darkblue", font = ("Times New Roman", 10),
                                                fg ="white", command =showTables3)
            btnShowTables3.place(x=30, y=710)
        def lablesShowTable4():
            btnShowTables4 = Button(root, text='Переглянути частотні словники 4 вірша', bg = "darkblue", font = ("Times New Roman", 10),
                                                fg ="white", command =showTables4)
            btnShowTables4.place(x=30, y=750)
        def lablesShowTable5():
            btnShowTables5 = Button(root, text='Переглянути частотні словники 5 вірша', bg = "darkblue", font = ("Times New Roman", 10),
                                                fg ="white", command =showTables5)
            btnShowTables5.place(x=30, y=790)
        if int(amount)==5:
            lablesShowTable1()
            lablesShowTable2()
            lablesShowTable3()
            lablesShowTable4()
            lablesShowTable5()

        if int(amount)==4:
            lablesShowTable1()
            lablesShowTable2()
            lablesShowTable3()
            lablesShowTable4()

        if int(amount)==3:
            lablesShowTable1()
            lablesShowTable2()
            lablesShowTable3()

        if int(amount)==2:
            lablesShowTable1()
            lablesShowTable2()


    # CREATE FUNCTIONS WHICH MAKE CHANGES INTRODUCED BY THE USER IN THE DATABASES
    def change1_2():
            word = entry1.get()
            partOfSp = listbox.get(ANCHOR)
            sql = (""" update Частини_Мови
                                set частина_мови=?
                                where слово=?""")
            cursor.execute(sql, (partOfSp, word))
            conn.commit()

            # updating the frequency dictionary of parts of speech
            cursor.execute("select * from Частини_Мови")
            rows = cursor.fetchall()
            values2 = {}
            part_of_speech_freq = []
            #print(part_of_speech_freq)
            for row in rows:
                part_of_speech_freq.append(row[1:3])

            for i in part_of_speech_freq:
                    if i[0] in values2:
                        values2[i[0]][1] += i[1]
                    else:
                        values2[i[0]] = [i[0], i[1]]

            values2 = list(values2.values())

            for i in values2:
                if i[0] == None:
                    values2.remove(i)

            values2_ordered = []
            for i in values2:
                    values2_ordered.append(i)
            for i in values2_ordered:
                    count = 0
                    while count in range(0, len(values2_ordered)-1):
                        if values2_ordered[count][1] < values2_ordered[count+1][1]:
                            values2_ordered[count], values2_ordered[count+1] = values2_ordered[count+1], values2_ordered[count]
                        count += 1
                    sql = (""" update Частота_Частин_Мови
                                        set Загальна_Частота=?
                                        where частина_мови=?""")
                    cursor.execute(sql, (i[1], i[0]))
                    conn.commit()


            cursor.execute('''SELECT * FROM Частини_Мови''')
            rows=cursor.fetchall()
            print_records = ''
            for row in rows:
                     print_records += str(row[0]) + '\t' + '\t' +str(row[1]) + '\t' + '\t' +str(row[2]) +  '\n'
            txtTable1 = Text(children, font = ("Times New Roman", 12), bg='white')
            txtTable1.place(x=610, y=70, width = 300, height=600)
            txtTable1.insert(1.0, print_records)

    def change1_1():
            word = entry1.get()
            lemma = entry2.get()
            sql = (""" update Леми
                                set лема=?
                                where слово=?""")
            cursor.execute(sql, (lemma, word))
            conn.commit()

             # updating the frequency dictionary of lemmas
            cursor.execute("select * from Леми")
            rows = cursor.fetchall()
            values2 = {}
            part_of_speech_freq = []
            #print(part_of_speech_freq)
            for row in rows:
                part_of_speech_freq.append(row[1:3])

            for i in part_of_speech_freq:
                    if i[0] in values2:
                        values2[i[0]][1] += i[1]
                    else:
                        values2[i[0]] = [i[0], i[1]]

            values2 = list(values2.values())

            for i in values2:
                if i[0] == None:
                    values2.remove(i)

            values2_ordered = []
            for i in values2:
                    values2_ordered.append(i)
            for i in values2_ordered:
                    count = 0
                    while count in range(0, len(values2_ordered)-1):
                        if values2_ordered[count][1] < values2_ordered[count+1][1]:
                            values2_ordered[count], values2_ordered[count+1] = values2_ordered[count+1], values2_ordered[count]
                        count += 1
                    sql = (""" update Частота_Лем
                                        set Загальна_Частота=?
                                        where лема=?""")
                    cursor.execute(sql, (i[1], i[0]))
                    conn.commit()

            cursor.execute('''SELECT * FROM Леми''')
            rows=cursor.fetchall()
            print_records = ''
            for row in rows:
                     print_records += str(row[0]) + '\t' + '\t' +str(row[1]) + '\t' + '\t' +str(row[2]) +  '\n'
            txtTable1 = Text(children, font = ("Times New Roman", 12), bg='white')
            txtTable1.place(x=280, y=70, width = 300, height=600)
            txtTable1.insert(1.0, print_records)

    def change2_2():
            word = entry1.get()
            partOfSp = listbox.get(ANCHOR)
            sql = (""" update Частини_Мови2
                                set частина_мови=?
                                where слово=?""")
            cursor.execute(sql, (partOfSp, word))
            conn.commit()

            # updating the frequency dictionary of parts of speech
            cursor.execute("select * from Частини_Мови2")
            rows = cursor.fetchall()


            values2 = {}
            part_of_speech_freq = []
            #print(part_of_speech_freq)
            for row in rows:
                part_of_speech_freq.append(row[1:3])

            for i in part_of_speech_freq:
                    if i[0] in values2:
                        values2[i[0]][1] += i[1]
                    else:
                        values2[i[0]] = [i[0], i[1]]

            values2 = list(values2.values())

            for i in values2:
                if i[0] == None:
                    values2.remove(i)

            values2_ordered = []
            for i in values2:
                    values2_ordered.append(i)
            for i in values2_ordered:
                    count = 0
                    while count in range(0, len(values2_ordered)-1):
                        if values2_ordered[count][1] < values2_ordered[count+1][1]:
                            values2_ordered[count], values2_ordered[count+1] = values2_ordered[count+1], values2_ordered[count]
                        count += 1
                    sql = (""" update Частота_Частин_Мови2
                                        set Загальна_Частота=?
                                        where частина_мови=?""")
                    cursor.execute(sql, (i[1], i[0]))
                    conn.commit()

            cursor.execute('''SELECT * FROM Частини_Мови2''')
            rows=cursor.fetchall()
            print_records = ''
            for row in rows:
                     print_records += str(row[0]) + '\t' + '\t' +str(row[1]) + '\t' + '\t' +str(row[2]) +  '\n'
            txtTable1 = Text(children, font = ("Times New Roman", 12), bg='white')
            txtTable1.place(x=610, y=70, width = 300, height=600)
            txtTable1.insert(1.0, print_records)

    def change2_1():
            word = entry1.get()
            lemma = entry2.get()
            sql = (""" update Леми2
                                set лема=?
                                where слово=?""")
            cursor.execute(sql, (lemma, word))
            conn.commit()

             # updating the frequency dictionary of lemmas
            cursor.execute("select * from Леми2")
            rows = cursor.fetchall()
            values2 = {}
            part_of_speech_freq = []
            #print(part_of_speech_freq)
            for row in rows:
                part_of_speech_freq.append(row[1:3])

            for i in part_of_speech_freq:
                    if i[0] in values2:
                        values2[i[0]][1] += i[1]
                    else:
                        values2[i[0]] = [i[0], i[1]]

            values2 = list(values2.values())

            for i in values2:
                if i[0] == None:
                    values2.remove(i)

            values2_ordered = []
            for i in values2:
                    values2_ordered.append(i)
            for i in values2_ordered:
                    count = 0
                    while count in range(0, len(values2_ordered)-1):
                        if values2_ordered[count][1] < values2_ordered[count+1][1]:
                            values2_ordered[count], values2_ordered[count+1] = values2_ordered[count+1], values2_ordered[count]
                        count += 1
                    sql = (""" update Частота_Лем2
                                        set Загальна_Частота=?
                                        where лема=?""")
                    cursor.execute(sql, (i[1], i[0]))
                    conn.commit()

            cursor.execute('''SELECT * FROM Леми2''')
            rows=cursor.fetchall()
            print_records = ''
            for row in rows:
                     print_records += str(row[0]) + '\t' + '\t' +str(row[1]) + '\t' + '\t' +str(row[2]) +  '\n'
            txtTable1 = Text(children, font = ("Times New Roman", 12), bg='white')
            txtTable1.place(x=280, y=70, width = 300, height=600)
            txtTable1.insert(1.0, print_records)

    def change3_2():
            word = entry1.get()
            partOfSp = listbox.get(ANCHOR)
            sql = (""" update Частини_Мови3
                                set частина_мови=?
                                where слово=?""")
            cursor.execute(sql, (partOfSp, word))
            conn.commit()

            # updating the frequency dictionary of parts of speech
            cursor.execute("select * from Частини_Мови3")
            rows = cursor.fetchall()


            values2 = {}
            part_of_speech_freq = []
            #print(part_of_speech_freq)
            for row in rows:
                part_of_speech_freq.append(row[1:3])

            for i in part_of_speech_freq:
                    if i[0] in values2:
                        values2[i[0]][1] += i[1]
                    else:
                        values2[i[0]] = [i[0], i[1]]

            values2 = list(values2.values())

            for i in values2:
                if i[0] == None:
                    values2.remove(i)

            values2_ordered = []
            for i in values2:
                    values2_ordered.append(i)
            for i in values2_ordered:
                    count = 0
                    while count in range(0, len(values2_ordered)-1):
                        if values2_ordered[count][1] < values2_ordered[count+1][1]:
                            values2_ordered[count], values2_ordered[count+1] = values2_ordered[count+1], values2_ordered[count]
                        count += 1
                    sql = (""" update Частота_Частин_Мови3
                                        set Загальна_Частота=?
                                        where частина_мови=?""")
                    cursor.execute(sql, (i[1], i[0]))
                    conn.commit()

            cursor.execute('''SELECT * FROM Частини_Мови3''')
            rows=cursor.fetchall()
            print_records = ''
            for row in rows:
                     print_records += str(row[0]) + '\t' + '\t' +str(row[1]) + '\t' + '\t' +str(row[2]) +  '\n'
            txtTable1 = Text(children, font = ("Times New Roman", 12), bg='white')
            txtTable1.place(x=610, y=70, width = 300, height=600)
            txtTable1.insert(1.0, print_records)

    def change3_1():
            word = entry1.get()
            lemma = entry2.get()
            sql = (""" update Леми3
                                set лема=?
                                where слово=?""")
            cursor.execute(sql, (lemma, word))
            conn.commit()

             # updating the frequency dictionary of lemmas
            cursor.execute("select * from Леми3")
            rows = cursor.fetchall()
            values2 = {}
            part_of_speech_freq = []
            #print(part_of_speech_freq)
            for row in rows:
                part_of_speech_freq.append(row[1:3])

            for i in part_of_speech_freq:
                    if i[0] in values2:
                        values2[i[0]][1] += i[1]
                    else:
                        values2[i[0]] = [i[0], i[1]]

            values2 = list(values2.values())

            for i in values2:
                if i[0] == None:
                    values2.remove(i)

            values2_ordered = []
            for i in values2:
                    values2_ordered.append(i)
            for i in values2_ordered:
                    count = 0
                    while count in range(0, len(values2_ordered)-1):
                        if values2_ordered[count][1] < values2_ordered[count+1][1]:
                            values2_ordered[count], values2_ordered[count+1] = values2_ordered[count+1], values2_ordered[count]
                        count += 1
                    sql = (""" update Частота_Лем3
                                        set Загальна_Частота=?
                                        where лема=?""")
                    cursor.execute(sql, (i[1], i[0]))
                    conn.commit()

            cursor.execute('''SELECT * FROM Леми3''')
            rows=cursor.fetchall()
            print_records = ''
            for row in rows:
                     print_records += str(row[0]) + '\t' + '\t' +str(row[1]) + '\t' + '\t' +str(row[2]) +  '\n'
            txtTable1 = Text(children, font = ("Times New Roman", 12), bg='white')
            txtTable1.place(x=280, y=70, width = 300, height=600)
            txtTable1.insert(1.0, print_records)

    def change4_2():
            word = entry1.get()
            partOfSp = listbox.get(ANCHOR)
            sql = (""" update Частини_Мови4
                                set частина_мови=?
                                where слово=?""")
            cursor.execute(sql, (partOfSp, word))
            conn.commit()

            # updating the frequency dictionary of parts of speech
            cursor.execute("select * from Частини_Мови4")
            rows = cursor.fetchall()
            values2 = {}
            part_of_speech_freq = []
            #print(part_of_speech_freq)
            for row in rows:
                part_of_speech_freq.append(row[1:3])

            for i in part_of_speech_freq:
                    if i[0] in values2:
                        values2[i[0]][1] += i[1]
                    else:
                        values2[i[0]] = [i[0], i[1]]

            values2 = list(values2.values())

            for i in values2:
                if i[0] == None:
                    values2.remove(i)

            values2_ordered = []
            for i in values2:
                    values2_ordered.append(i)
            for i in values2_ordered:
                    count = 0
                    while count in range(0, len(values2_ordered)-1):
                        if values2_ordered[count][1] < values2_ordered[count+1][1]:
                            values2_ordered[count], values2_ordered[count+1] = values2_ordered[count+1], values2_ordered[count]
                        count += 1
                    sql = (""" update Частота_Частин_Мови4
                                        set Загальна_Частота=?
                                        where частина_мови=?""")
                    cursor.execute(sql, (i[1], i[0]))
                    conn.commit()

            cursor.execute('''SELECT * FROM Частини_Мови4''')
            rows=cursor.fetchall()
            print_records = ''
            for row in rows:
                     print_records += str(row[0]) + '\t' + '\t' +str(row[1]) + '\t' + '\t' +str(row[2]) +  '\n'
            txtTable1 = Text(children, font = ("Times New Roman", 12), bg='white')
            txtTable1.place(x=610, y=70, width = 300, height=600)
            txtTable1.insert(1.0, print_records)

    def change4_1():
            word = entry1.get()
            lemma = entry2.get()
            sql = (""" update Леми4
                                set лема=?
                                where слово=?""")
            cursor.execute(sql, (lemma, word))
            conn.commit()

             # updating the frequency dictionary of lemmas
            cursor.execute("select * from Леми4")
            rows = cursor.fetchall()
            values2 = {}
            part_of_speech_freq = []
            #print(part_of_speech_freq)
            for row in rows:
                part_of_speech_freq.append(row[1:3])

            for i in part_of_speech_freq:
                    if i[0] in values2:
                        values2[i[0]][1] += i[1]
                    else:
                        values2[i[0]] = [i[0], i[1]]

            values2 = list(values2.values())

            for i in values2:
                if i[0] == None:
                    values2.remove(i)

            values2_ordered = []
            for i in values2:
                    values2_ordered.append(i)
            for i in values2_ordered:
                    count = 0
                    while count in range(0, len(values2_ordered)-1):
                        if values2_ordered[count][1] < values2_ordered[count+1][1]:
                            values2_ordered[count], values2_ordered[count+1] = values2_ordered[count+1], values2_ordered[count]
                        count += 1
                    sql = (""" update Частота_Лем4
                                        set Загальна_Частота=?
                                        where лема=?""")
                    cursor.execute(sql, (i[1], i[0]))
                    conn.commit()

            cursor.execute('''SELECT * FROM Леми4''')
            rows=cursor.fetchall()
            print_records = ''
            for row in rows:
                     print_records += str(row[0]) + '\t' + '\t' +str(row[1]) + '\t' + '\t' +str(row[2]) +  '\n'
            txtTable1 = Text(children, font = ("Times New Roman", 12), bg='white')
            txtTable1.place(x=280, y=70, width = 300, height=600)
            txtTable1.insert(1.0, print_records)

    def change5_2():
            word = entry1.get()
            partOfSp = listbox.get(ANCHOR)
            sql = (""" update Частини_Мови5
                                set частина_мови=?
                                where слово=?""")
            cursor.execute(sql, (partOfSp, word))
            conn.commit()

            # updating the frequency dictionary of parts of speech
            cursor.execute("select * from Частини_Мови5")
            rows = cursor.fetchall()
            values2 = {}
            part_of_speech_freq = []
            #print(part_of_speech_freq)
            for row in rows:
                part_of_speech_freq.append(row[1:3])

            for i in part_of_speech_freq:
                    if i[0] in values2:
                        values2[i[0]][1] += i[1]
                    else:
                        values2[i[0]] = [i[0], i[1]]

            values2 = list(values2.values())

            for i in values2:
                if i[0] == None:
                    values2.remove(i)

            values2_ordered = []
            for i in values2:
                    values2_ordered.append(i)
            for i in values2_ordered:
                    count = 0
                    while count in range(0, len(values2_ordered)-1):
                        if values2_ordered[count][1] < values2_ordered[count+1][1]:
                            values2_ordered[count], values2_ordered[count+1] = values2_ordered[count+1], values2_ordered[count]
                        count += 1
                    sql = (""" update Частота_Частин_Мови5
                                        set Загальна_Частота=?
                                        where частина_мови=?""")
                    cursor.execute(sql, (i[1], i[0]))
                    conn.commit()

            cursor.execute('''SELECT * FROM Частини_Мови5''')
            rows=cursor.fetchall()
            print_records = ''
            for row in rows:
                     print_records += str(row[0]) + '\t' + '\t' +str(row[1]) + '\t' + '\t' +str(row[2]) +  '\n'
            txtTable1 = Text(children, font = ("Times New Roman", 12), bg='white')
            txtTable1.place(x=610, y=70, width = 300, height=600)
            txtTable1.insert(1.0, print_records)

    def change5_1():
            word = entry1.get()
            lemma = entry2.get()
            sql = (""" update Леми5
                                set лема=?
                                where слово=?""")
            cursor.execute(sql, (lemma, word))
            conn.commit()

            # updating the frequency dictionary of lemmas
            cursor.execute("select * from Леми5")
            rows = cursor.fetchall()
            values2 = {}
            part_of_speech_freq = []
            #print(part_of_speech_freq)
            for row in rows:
                part_of_speech_freq.append(row[1:3])

            for i in part_of_speech_freq:
                    if i[0] in values2:
                        values2[i[0]][1] += i[1]
                    else:
                        values2[i[0]] = [i[0], i[1]]

            values2 = list(values2.values())

            for i in values2:
                if i[0] == None:
                    values2.remove(i)

            values2_ordered = []
            for i in values2:
                    values2_ordered.append(i)
            for i in values2_ordered:
                    count = 0
                    while count in range(0, len(values2_ordered)-1):
                        if values2_ordered[count][1] < values2_ordered[count+1][1]:
                            values2_ordered[count], values2_ordered[count+1] = values2_ordered[count+1], values2_ordered[count]
                        count += 1
                    sql = (""" update Частота_Лем5
                                        set Загальна_Частота=?
                                        where лема=?""")
                    cursor.execute(sql, (i[1], i[0]))
                    conn.commit()

            cursor.execute('''SELECT * FROM Леми5''')
            rows=cursor.fetchall()
            print_records = ''
            for row in rows:
                print_records += str(row[0]) + '\t' + '\t' +str(row[1]) + '\t' + '\t' +str(row[2]) +  '\n'
            txtTable1 = Text(children, font = ("Times New Roman", 12), bg='white')
            txtTable1.place(x=280, y=70, width = 300, height=600)
            txtTable1.insert(1.0, print_records)


    # CREATE FUNCTIONS THAT CREATE A CHILD WINDOW AND DISPLAY BUTTONS IN IT WITH THE NAMES OF FREQUENCY DICTIONARIES OF THE SELECTED TEXT
    def createChildren():
        global children
        children = Toplevel(root)
        children.title('Частотні словники')
        children.minsize(width=500, height=400)

    def showTables1():
        def printTable1():
            cursor.execute('''SELECT * FROM Словоформи''')
            rows=cursor.fetchall()
            print_records = ''
            for row in rows:
                print_records += str(row[0]) + '\t' +'\t' + str(row[1]) + '\n'
            txtTable1 = Text(children, font = ("Times New Roman", 12), bg='white')
            txtTable1.place(x=30, y=70, width = 230, height=700)
            txtTable1.insert(1.0, print_records)
            scroll = Scrollbar(txtTable1, command=txtTable1.yview, orient=VERTICAL)
            scroll.place(relx=0.94, rely=0, heigh=700)
            txtTable1.config(yscrollcommand=scroll.set)

        def printTable2():
            global entry1
            global entry2
            cursor.execute('''SELECT * FROM Леми''')
            rows=cursor.fetchall()
            print_records = ''
            for row in rows:
                print_records += str(row[0]) + '\t' + '\t' +str(row[1]) + '\t' + '\t' +str(row[2]) +  '\n'
            txtTable1 = Text(children, font = ("Times New Roman", 12), bg='white')
            txtTable1.place(x=280, y=70, width = 300, height=600)
            txtTable1.insert(1.0, print_records)
            scroll = Scrollbar(txtTable1, command=txtTable1.yview, orient=VERTICAL)
            scroll.place(relx=0.95, rely=0, heigh=600)
            txtTable1.config(yscrollcommand=scroll.set)
            lblSet1 = Label(children, text='Введіть слово', font = ("Times New Roman", 10), bg='darkblue', fg='white')
            lblSet1.place(x=300, y=680)
            entry1 = Entry(children)
            entry1.place(x=420, y=680)
            lblSet2 = Label(children, text='Введіть лему', font = ("Times New Roman", 10), bg='darkblue', fg='white')
            lblSet2.place(x=300, y=710)
            entry2 = Entry(children)
            entry2.place(x=420, y=710, width=50)
            btnChange = Button(children, text='Змінити', font = ("Times New Roman", 10), bg='darkblue', fg='white', command=change1_1) # викликає команду, яка вносить зміни до бази даних
            btnChange.place(x=520, y=740)

        def printTable3():
            global entry1
            global listbox
            cursor.execute('''SELECT * FROM Частини_Мови''')
            rows=cursor.fetchall()
            print_records = ''
            for row in rows:
                print_records += str(row[0]) + '\t' + '\t' + str(row[1]) + '\t' + '\t' +str(row[2]) + ' '+ '\n'
            txtTable1 = Text(children, font = ("Times New Roman", 12), bg='white')
            txtTable1.place(x=610, y=70, width = 300, height=600)
            txtTable1.insert(1.0, print_records)
            scroll = Scrollbar(txtTable1, command=txtTable1.yview, orient=VERTICAL)
            scroll.place(relx=0.95, rely=0, heigh=600)
            txtTable1.config(yscrollcommand=scroll.set)
            lblSet1 = Label(children, text='Введіть слово', font = ("Times New Roman", 10), bg='darkblue', fg='white')
            lblSet1.place(x=610, y=680)
            entry1 = Entry(children)
            entry1.place(x=750, y=680)
            lblSet2 = Label(children, text='Введіть частину мови', font = ("Times New Roman", 10), bg='darkblue', fg='white')
            lblSet2.place(x=610, y=710)
            listbox = Listbox(children)
            listbox.place(x=750, y=710, width=75, heigh=100)
            for i in ('INTJ', 'PRCL', 'CONJ', 'PREP', 'NPRO', 'PRED', 'ADVB', 'NUMR', 'GRND', 'PRTS', 'PRTF', 'INFN', 'VERB', 'COMP', 'ADJS', 'ADJF', 'NOUN'):
                listbox.insert(0, i)
            scroll = Scrollbar(listbox, command=listbox.yview, orient=VERTICAL)
            scroll.place(relx=0.80, rely=0, heigh=100)
            listbox.config(yscrollcommand=scroll.set)
            btnChange = Button(children, text='Змінити', font = ("Times New Roman", 10), bg='darkblue', fg='white', command=change1_2)
            btnChange.place(x=830, y=740)

        createChildren()
        btnWordsDict = Button(children, text='Частотний словник словоформ', font = ("Times New Roman", 12), fg='darkblue',
                                      bg = "white", command=printTable1)
        btnWordsDict.place(x=30, y=20, width=230)
        btnLemmasDict = Button(children, text='Частотний словник лем', font = ("Times New Roman", 12), fg='darkblue',
                                       bg = "white", command=printTable2)
        btnLemmasDict.place(x=280, y=20, width=300 )
        btnPartOfSpDict = Button(children, text='Частотний словник частин мови', font = ("Times New Roman", 12),
                                         fg='darkblue', bg = "white", command=printTable3)
        btnPartOfSpDict.place(x=610, y=20, width=300)

        btnApplyChanges = Button(children, text='Застосувати зміни', font = ("Times New Roman", 12), fg='white',
                                       bg = "darkblue", command=applyChanges)
        btnApplyChanges.place(x=910, y=20)

    def showTables2():
        def printTable1():
            cursor.execute('''SELECT * FROM Словоформи2''')
            rows=cursor.fetchall()
            print_records = ''
            for row in rows:
                print_records += str(row[0]) + '\t' +  '\t' + str(row[1])+ '\n'
            txtTable1 = Text(children, font = ("Times New Roman", 12), bg='white')
            txtTable1.place(x=30, y=70, width = 230, height=700)
            txtTable1.insert(1.0, print_records)
            scroll = Scrollbar(txtTable1, command=txtTable1.yview, orient=VERTICAL)
            scroll.place(relx=0.97, rely=0, heigh=700)
            txtTable1.config(yscrollcommand=scroll.set)

        def printTable2():
            global entry1
            global entry2
            cursor.execute('''SELECT * FROM Леми2''')
            rows=cursor.fetchall()
            print_records = ''
            for row in rows:
                print_records += str(row[0]) + '\t' + '\t' +str(row[1]) + '\t' + '\t' +str(row[2]) +  '\n'
            txtTable1 = Text(children, font = ("Times New Roman", 12), bg='white')
            txtTable1.place(x=280, y=70, width = 300, height=600)
            txtTable1.insert(1.0, print_records)
            scroll = Scrollbar(txtTable1, command=txtTable1.yview, orient=VERTICAL)
            scroll.place(relx=0.95, rely=0, heigh=600)
            txtTable1.config(yscrollcommand=scroll.set)
            lblSet1 = Label(children, text='Введіть слово', font = ("Times New Roman", 10), bg='darkblue', fg='white')
            lblSet1.place(x=300, y=680)
            entry1 = Entry(children)
            entry1.place(x=420, y=680)
            lblSet2 = Label(children, text='Введіть лему', font = ("Times New Roman", 10), bg='darkblue', fg='white')
            lblSet2.place(x=300, y=710)
            entry2 = Entry(children)
            entry2.place(x=420, y=710, width=50)
            btnChange = Button(children, text='Змінити', font = ("Times New Roman", 10), bg='darkblue', fg='white', command=change2_1) # викликає команду, яка вносить зміни до бази даних
            btnChange.place(x=520, y=740)

        def printTable3():
            global entry1
            global listbox
            cursor.execute('''SELECT * FROM Частини_Мови2''')
            rows=cursor.fetchall()
            print_records = ''
            for row in rows:
                print_records += str(row[0]) + '\t' + '\t' + str(row[1]) + '\t' + '\t' +str(row[2]) + ' '+ '\n'
            txtTable1 = Text(children, font = ("Times New Roman", 12), bg='white')
            txtTable1.place(x=610, y=70, width = 300, height=600)
            txtTable1.insert(1.0, print_records)
            scroll = Scrollbar(txtTable1, command=txtTable1.yview, orient=VERTICAL)
            scroll.place(relx=0.95, rely=0, heigh=600)
            txtTable1.config(yscrollcommand=scroll.set)
            lblSet1 = Label(children, text='Введіть слово', font = ("Times New Roman", 10), bg='darkblue', fg='white')
            lblSet1.place(x=610, y=680)
            entry1 = Entry(children)
            entry1.place(x=750, y=680)
            lblSet2 = Label(children, text='Введіть частину мови', font = ("Times New Roman", 10), bg='darkblue', fg='white')
            lblSet2.place(x=610, y=710)
            listbox = Listbox(children)
            listbox.place(x=750, y=710, width=75, heigh=100)
            for i in ('INTJ', 'PRCL', 'CONJ', 'PREP', 'NPRO', 'PRED', 'ADVB', 'NUMR', 'GRND', 'PRTS', 'PRTF', 'INFN', 'VERB', 'COMP', 'ADJS', 'ADJF', 'NOUN'):
                listbox.insert(0, i)
            scroll = Scrollbar(listbox, command=listbox.yview, orient=VERTICAL)
            scroll.place(relx=0.80, rely=0, heigh=100)
            listbox.config(yscrollcommand=scroll.set)
            btnChange = Button(children, text='Змінити', font = ("Times New Roman", 10), bg='darkblue', fg='white', command=change2_2)
            btnChange.place(x=830, y=740)

        createChildren()
        btnWordsDict = Button(children, text='Частотний словник словоформ', font = ("Times New Roman", 12), fg='darkblue',
                                      bg = "white", command=printTable1)
        btnWordsDict.place(x=30, y=20, width=230)
        btnLemmasDict = Button(children, text='Частотний словник лем', font = ("Times New Roman", 12), fg='darkblue',
                                       bg = "white", command=printTable2)
        btnLemmasDict.place(x=280, y=20, width=300 )
        btnPartOfSpDict = Button(children, text='Частотний словник частин мови', font = ("Times New Roman", 12),
                                         fg='darkblue', bg = "white", command=printTable3)
        btnPartOfSpDict.place(x=610, y=20, width=300)

        btnApplyChanges = Button(children, text='Застосувати зміни', font = ("Times New Roman", 12), fg='white',
                                       bg = "darkblue", command=applyChanges)
        btnApplyChanges.place(x=910, y=20)

    def showTables3():
        def printTable1():
                cursor.execute('''SELECT * FROM Словоформи3''')
                rows=cursor.fetchall()
                print_records = ''
                for row in rows:
                    print_records += str(row[0]) + '\t' +'\t' + str(row[1]) + '\n'
                txtTable1 = Text(children, font = ("Times New Roman", 12), bg='white')
                txtTable1.place(x=30, y=70, width = 230, height=700)
                txtTable1.insert(1.0, print_records)
                scroll = Scrollbar(txtTable1, command=txtTable1.yview, orient=VERTICAL)
                scroll.place(relx=0.97, rely=0, heigh=700)
                txtTable1.config(yscrollcommand=scroll.set)

        def printTable2():
            global entry1
            global entry2
            cursor.execute('''SELECT * FROM Леми3''')
            rows=cursor.fetchall()
            print_records = ''
            for row in rows:
                print_records += str(row[0]) + '\t' + '\t' +str(row[1]) + '\t' + '\t' +str(row[2]) +  '\n'
            txtTable1 = Text(children, font = ("Times New Roman", 12), bg='white')
            txtTable1.place(x=280, y=70, width = 300, height=600)
            txtTable1.insert(1.0, print_records)
            scroll = Scrollbar(txtTable1, command=txtTable1.yview, orient=VERTICAL)
            scroll.place(relx=0.95, rely=0, heigh=600)
            txtTable1.config(yscrollcommand=scroll.set)
            lblSet1 = Label(children, text='Введіть слово', font = ("Times New Roman", 10), bg='darkblue', fg='white')
            lblSet1.place(x=300, y=680)
            entry1 = Entry(children)
            entry1.place(x=420, y=680)
            lblSet2 = Label(children, text='Введіть лему', font = ("Times New Roman", 10), bg='darkblue', fg='white')
            lblSet2.place(x=300, y=710)
            entry2 = Entry(children)
            entry2.place(x=420, y=710, width=50)
            btnChange = Button(children, text='Змінити', font = ("Times New Roman", 10), bg='darkblue', fg='white', command=change3_1) # викликає команду, яка вносить зміни до бази даних
            btnChange.place(x=520, y=740)

        def printTable3():
            global entry1
            global listbox
            cursor.execute('''SELECT * FROM Частини_Мови3''')
            rows=cursor.fetchall()
            print_records = ''
            for row in rows:
                print_records += str(row[0]) + '\t' + '\t' + str(row[1]) + '\t' + '\t' +str(row[2]) + ' '+ '\n'
            txtTable1 = Text(children, font = ("Times New Roman", 12), bg='white')
            txtTable1.place(x=610, y=70, width = 300, height=600)
            txtTable1.insert(1.0, print_records)
            scroll = Scrollbar(txtTable1, command=txtTable1.yview, orient=VERTICAL)
            scroll.place(relx=0.95, rely=0, heigh=600)
            txtTable1.config(yscrollcommand=scroll.set)
            lblSet1 = Label(children, text='Введіть слово', font = ("Times New Roman", 10), bg='darkblue', fg='white')
            lblSet1.place(x=610, y=680)
            entry1 = Entry(children)
            entry1.place(x=750, y=680)
            lblSet2 = Label(children, text='Введіть частину мови', font = ("Times New Roman", 10), bg='darkblue', fg='white')
            lblSet2.place(x=610, y=710)
            listbox = Listbox(children)
            listbox.place(x=750, y=710, width=75, heigh=100)
            for i in ('INTJ', 'PRCL', 'CONJ', 'PREP', 'NPRO', 'PRED', 'ADVB', 'NUMR', 'GRND', 'PRTS', 'PRTF', 'INFN', 'VERB', 'COMP', 'ADJS', 'ADJF', 'NOUN'):
                listbox.insert(0, i)
            scroll = Scrollbar(listbox, command=listbox.yview, orient=VERTICAL)
            scroll.place(relx=0.80, rely=0, heigh=100)
            listbox.config(yscrollcommand=scroll.set)
            btnChange = Button(children, text='Змінити', font = ("Times New Roman", 10), bg='darkblue', fg='white', command=change3_2)
            btnChange.place(x=830, y=740)

        createChildren()
        btnWordsDict = Button(children, text='Частотний словник словоформ', font = ("Times New Roman", 12), fg='darkblue',
                                      bg = "white", command=printTable1)
        btnWordsDict.place(x=30, y=20, width=230)
        btnLemmasDict = Button(children, text='Частотний словник лем', font = ("Times New Roman", 12), fg='darkblue',
                                       bg = "white", command=printTable2)
        btnLemmasDict.place(x=280, y=20, width=300 )
        btnPartOfSpDict = Button(children, text='Частотний словник частин мови', font = ("Times New Roman", 12),
                                         fg='darkblue', bg = "white", command=printTable3)
        btnPartOfSpDict.place(x=610, y=20, width=300)

        btnApplyChanges = Button(children, text='Застосувати зміни', font = ("Times New Roman", 12), fg='white',
                                       bg = "darkblue", command=applyChanges)
        btnApplyChanges.place(x=910, y=20)

    def showTables4():
        def printTable1():
                cursor.execute('''SELECT * FROM Словоформи4''')
                rows=cursor.fetchall()
                print_records = ''
                for row in rows:
                    print_records += str(row[0]) + '\t' +'\t' + str(row[1]) + '\n'
                txtTable1 = Text(children, font = ("Times New Roman", 12), bg='white')
                txtTable1.place(x=30, y=70, width = 230, height=700)
                txtTable1.insert(1.0, print_records)
                scroll = Scrollbar(txtTable1, command=txtTable1.yview, orient=VERTICAL)
                scroll.place(relx=0.97, rely=0, heigh=700)
                txtTable1.config(yscrollcommand=scroll.set)

        def printTable2():
            global entry1
            global entry2
            cursor.execute('''SELECT * FROM Леми4''')
            rows=cursor.fetchall()
            print_records = ''
            for row in rows:
                print_records += str(row[0]) + '\t' + '\t' +str(row[1]) + '\t' + '\t' +str(row[2]) +  '\n'
            txtTable1 = Text(children, font = ("Times New Roman", 12), bg='white')
            txtTable1.place(x=280, y=70, width = 300, height=600)
            txtTable1.insert(1.0, print_records)
            scroll = Scrollbar(txtTable1, command=txtTable1.yview, orient=VERTICAL)
            scroll.place(relx=0.95, rely=0, heigh=600)
            txtTable1.config(yscrollcommand=scroll.set)
            lblSet1 = Label(children, text='Введіть слово', font = ("Times New Roman", 10), bg='darkblue', fg='white')
            lblSet1.place(x=300, y=680)
            entry1 = Entry(children)
            entry1.place(x=420, y=680)
            lblSet2 = Label(children, text='Введіть лему', font = ("Times New Roman", 10), bg='darkblue', fg='white')
            lblSet2.place(x=300, y=710)
            entry2 = Entry(children)
            entry2.place(x=420, y=710, width=50)
            btnChange = Button(children, text='Змінити', font = ("Times New Roman", 10), bg='darkblue', fg='white', command=change4_1) # викликає команду, яка вносить зміни до бази даних
            btnChange.place(x=520, y=740)

        def printTable3():
            global entry1
            global listbox
            cursor.execute('''SELECT * FROM Частини_Мови4''')
            rows=cursor.fetchall()
            print_records = ''
            for row in rows:
                print_records += str(row[0]) + '\t' + '\t' + str(row[1]) + '\t' + '\t' +str(row[2]) + ' '+ '\n'
            txtTable1 = Text(children, font = ("Times New Roman", 12), bg='white')
            txtTable1.place(x=610, y=70, width = 300, height=600)
            txtTable1.insert(1.0, print_records)
            scroll = Scrollbar(txtTable1, command=txtTable1.yview, orient=VERTICAL)
            scroll.place(relx=0.95, rely=0, heigh=600)
            txtTable1.config(yscrollcommand=scroll.set)
            lblSet1 = Label(children, text='Введіть слово', font = ("Times New Roman", 10), bg='darkblue', fg='white')
            lblSet1.place(x=610, y=680)
            entry1 = Entry(children)
            entry1.place(x=750, y=680)
            lblSet2 = Label(children, text='Введіть частину мови', font = ("Times New Roman", 10), bg='darkblue', fg='white')
            lblSet2.place(x=610, y=710)
            listbox = Listbox(children)
            listbox.place(x=750, y=710, width=75, heigh=100)
            for i in ('INTJ', 'PRCL', 'CONJ', 'PREP', 'NPRO', 'PRED', 'ADVB', 'NUMR', 'GRND', 'PRTS', 'PRTF', 'INFN', 'VERB', 'COMP', 'ADJS', 'ADJF', 'NOUN'):
                listbox.insert(0, i)
            scroll = Scrollbar(listbox, command=listbox.yview, orient=VERTICAL)
            scroll.place(relx=0.80, rely=0, heigh=100)
            listbox.config(yscrollcommand=scroll.set)
            btnChange = Button(children, text='Змінити', font = ("Times New Roman", 10), bg='darkblue', fg='white', command=change4_2)
            btnChange.place(x=830, y=740)

        createChildren()
        btnWordsDict = Button(children, text='Частотний словник словоформ', font = ("Times New Roman", 12), fg='darkblue',
                                      bg = "white", command=printTable1)
        btnWordsDict.place(x=30, y=20, width=230)
        btnLemmasDict = Button(children, text='Частотний словник лем', font = ("Times New Roman", 12), fg='darkblue',
                                       bg = "white", command=printTable2)
        btnLemmasDict.place(x=280, y=20, width=300 )
        btnPartOfSpDict = Button(children, text='Частотний словник частин мови', font = ("Times New Roman", 12),
                                         fg='darkblue', bg = "white", command=printTable3)
        btnPartOfSpDict.place(x=610, y=20, width=300)

        btnApplyChanges = Button(children, text='Застосувати зміни', font = ("Times New Roman", 12), fg='white',
                                       bg = "darkblue", command=applyChanges)
        btnApplyChanges.place(x=910, y=20)

    def showTables5():
        def printTable1():
            cursor.execute('''SELECT * FROM Словоформи5''')
            rows=cursor.fetchall()
            print_records = ''
            for row in rows:
                print_records += str(row[0]) + '\t' +'\t' + str(row[1]) + '\n'
            txtTable1 = Text(children, font = ("Times New Roman", 12), bg='white')
            txtTable1.place(x=30, y=70, width = 230, height=700)
            txtTable1.insert(1.0, print_records)
            scroll = Scrollbar(txtTable1, command=txtTable1.yview, orient=VERTICAL)
            scroll.place(relx=0.97, rely=0, heigh=700)
            txtTable1.config(yscrollcommand=scroll.set)

        def printTable2():
            global entry1
            global entry2
            cursor.execute('''SELECT * FROM Леми5''')
            rows=cursor.fetchall()
            print_records = ''
            for row in rows:
                print_records += str(row[0]) + '\t' + '\t' +str(row[1]) + '\t' + '\t' +str(row[2]) +  '\n'
            txtTable1 = Text(children, font = ("Times New Roman", 12), bg='white')
            txtTable1.place(x=280, y=70, width = 300, height=600)
            txtTable1.insert(1.0, print_records)
            scroll = Scrollbar(txtTable1, command=txtTable1.yview, orient=VERTICAL)
            scroll.place(relx=0.95, rely=0, heigh=600)
            txtTable1.config(yscrollcommand=scroll.set)
            lblSet1 = Label(children, text='Введіть слово', font = ("Times New Roman", 10), bg='darkblue', fg='white')
            lblSet1.place(x=300, y=680)
            entry1 = Entry(children)
            entry1.place(x=420, y=680)
            lblSet2 = Label(children, text='Введіть лему', font = ("Times New Roman", 10), bg='darkblue', fg='white')
            lblSet2.place(x=300, y=710)
            entry2 = Entry(children)
            entry2.place(x=420, y=710, width=50)
            btnChange = Button(children, text='Змінити', font = ("Times New Roman", 10), bg='darkblue', fg='white', command=change5_1) # викликає команду, яка вносить зміни до бази даних
            btnChange.place(x=520, y=740)

        def printTable3():
            global entry1
            global listbox
            cursor.execute('''SELECT * FROM Частини_Мови5''')
            rows=cursor.fetchall()
            print_records = ''
            for row in rows:
                print_records += str(row[0]) + '\t' + '\t' + str(row[1]) + '\t' + '\t' +str(row[2]) + ' '+ '\n'
            txtTable1 = Text(children, font = ("Times New Roman", 12), bg='white')
            txtTable1.place(x=610, y=70, width = 300, height=600)
            txtTable1.insert(1.0, print_records)
            scroll = Scrollbar(txtTable1, command=txtTable1.yview, orient=VERTICAL)
            scroll.place(relx=0.95, rely=0, heigh=600)
            txtTable1.config(yscrollcommand=scroll.set)
            lblSet1 = Label(children, text='Введіть слово', font = ("Times New Roman", 10), bg='darkblue', fg='white')
            lblSet1.place(x=610, y=680)
            entry1 = Entry(children)
            entry1.place(x=750, y=680)
            lblSet2 = Label(children, text='Введіть частину мови', font = ("Times New Roman", 10), bg='darkblue', fg='white')
            lblSet2.place(x=610, y=710)
            listbox = Listbox(children)
            listbox.place(x=750, y=710, width=75, heigh=100)
            for i in ('INTJ', 'PRCL', 'CONJ', 'PREP', 'NPRO', 'PRED', 'ADVB', 'NUMR', 'GRND', 'PRTS', 'PRTF', 'INFN', 'VERB', 'COMP', 'ADJS', 'ADJF', 'NOUN'):
                listbox.insert(0, i)
            scroll = Scrollbar(listbox, command=listbox.yview, orient=VERTICAL)
            scroll.place(relx=0.80, rely=0, heigh=100)
            listbox.config(yscrollcommand=scroll.set)
            btnChange = Button(children, text='Змінити', font = ("Times New Roman", 10), bg='darkblue', fg='white', command=change5_2)
            btnChange.place(x=830, y=740)

        createChildren()
        btnWordsDict = Button(children, text='Частотний словник словоформ', font = ("Times New Roman", 12), fg='darkblue',
                                      bg = "white", command=printTable1)
        btnWordsDict.place(x=30, y=20, width=230)
        btnLemmasDict = Button(children, text='Частотний словник лем', font = ("Times New Roman", 12), fg='darkblue',
                                       bg = "white", command=printTable2)
        btnLemmasDict.place(x=280, y=20, width=300 )
        btnPartOfSpDict = Button(children, text='Частотний словник частин мови', font = ("Times New Roman", 12),
                                         fg='darkblue', bg = "white", command=printTable3)
        btnPartOfSpDict.place(x=610, y=20, width=300)

        btnApplyChanges = Button(children, text='Застосувати зміни', font = ("Times New Roman", 12), fg='white',
                                       bg = "darkblue", command=applyChanges)
        btnApplyChanges.place(x=910, y=20)
    lablesShowTables()


    def applyChanges():
         common()



# CREATE A DIALOG WINDOW WITH INITIAL WIDGETS
root = Tk()
root.title("Параметризація")
root.geometry('1500x800+50+16')

lblAmountOfTexts = Label(root, text = 'Скільки текстів ви хочете порівняти? Введіть число від 2 до 5',
                         font = ("Times New Roman", 10), bg = "darkblue", fg ="white")
lblAmountOfTexts.place(x =10, y=0, width=350)
entryAmount = Entry(root)
entryAmount.place(x =370, y=0, width=30)
btnOk = Button(root, text = 'OK', bg = "darkblue", font = ("Times New Roman", 7), fg ="white", command = createPlaceForTexts)
btnOk.place(x=410, y=0, width=30)


root.mainloop()



# DELETE ALL TABLES TO BE ABLE TO RUN THE PROGRAM MANY TIMES

dropTables()
