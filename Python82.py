'''Дополнить телефонный справочник возможностью изменения и удаления данных. Пользователь также может ввести имя или фамилию, и Вы должны 
реализовать функционал для изменения и удаления данных.'''

'''Как работать со справочником: Кнопка (1) - загружает записи из файла spravka.txt (!) справочник использует файл spravka.txt как рабочий, 
                                т.е. постоянно перезаписывает (сохраняет) данные только в этом файле
                                Кнопка (2) - добавляет новую запись в справочник (файл spravka.txt)
                                Кнопка (3) - Дает возможность за один раз исправить одну запись. Для этого эту запись надо кликнуть 2 раза
                                и в поле вввода исправить ее. Но обязательным условием для исправления записи является то, что исправляемая запись
                                должна быть выделена (иметь фокус (выделение))
                                Кнопка (4) - удаляет выделенную (выбранную) запись в справочнике
                                Кнопка (5) - Очищает строку ввода/поиска
                                Кнопка (6) - поиск введенной информации в строке ввода/поиска справочнике
                                Кнопка (7) - дает возможность сохранить справочник в другой текстовый (*.txt) файл'''

from tkinter import *                                   #Загрузка библиотек
from tkinter import filedialog
from tkinter.messagebox import showinfo
import re
 
root = Tk()      ########################################Формирование интерфейса справочника#############################
root.title("ТЕЛЕФОННЫЙ СПРАВОЧНИК ver.1.0")

root.geometry('800x520')

lst1 = []
list_zapisi = []
#global count4
count4 = 0

listbox = Listbox(root, height=15, width=125)
listbox.pack()

Name = StringVar()
frame = Frame()
frame.pack(padx=10,pady=20)

Label(frame, text = 'Добавление записи (введите ФИО, номер телефона (через пробел))/ Поиск (введите информацию для поиска) ', font='arial 10 bold').pack()
Entry(frame, textvariable = Name, font='arial 12 bold', width=140).pack()
Label(frame, text = 'Кнопки для изменения содержимого телефонного справочника ', font='arial 10 bold').pack()
      ########################################Формирование интерфейса справочника#############################

def read_data():                                                                #Чтение файла без пустых строк
    global count4
    count4 +=1
    if count4 == 1:
        with open('spravka.txt', 'r', encoding='utf-8') as file:
            lines = list(line for line in (l.strip() for l in file) if line)        #Чтение без пустых строк

        for item in lines:
            listbox.insert(END, item)

def write_data(filename):                                                       #Запись файла без пустых строк
    with open(filename, 'wt', encoding='utf-8') as f:
        list_zapisi = listbox.get(0, END)  
        f.writelines("\n"+ place for place in list_zapisi)
        with open(filename) as f:
            lines = f.readlines()
            non_empty_lines = (line for line in lines if not line.isspace())
            with open(filename, 'wt') as n_f:
                n_f.writelines(non_empty_lines)

def add_user():                                                                     #Добавление записей (ФИО № тлф) в справочник
    if Name.get() == '':
        return 0
    lst1.append(Name.get())
    if check_tnumber() == True:
        for item in lst1:
            listbox.insert(END, item)
        with open('spravka.txt', 'a', newline='',  encoding='utf-8') as f:
            f.writelines("\n"+ str(Name.get()))
            lst1.clear()
            Name.set('')
    else:                                                                       #Вывод предупреждения о неправильном формате номера телефона
        showinfo(title="ПРЕДУПРЕЖДЕНИЕ! НЕПРАВИЛЬНЫЙ ВВОД: ", message='Попытка ввода записи с неправильным форматом номера телефона (правильный формат - 8********** ,всего 11 цифр) ')
        lst1.clear()

def search_data():                                                              #Поиск информации в справочнике
    count1 = 0
    count2 = 0
    count3 = 0
    search_count = 0
    poisk =''
    if Name.get() == '':
        return 0
    list_zapisi = listbox.get(0, "end")
    poisk_fraza = Name.get()
    for elem in list_zapisi:
        count1 +=1
        if poisk_fraza in elem:
            search_count +=1
            Name.set(elem.strip())
            
            poisk = listbox.get(count1-1)
            if (count1 - 1) == 0:
                 showinfo(title="Результат поиска: ", message='Совпадение есть записью №1') #Условие для первой строки
                 count3=count1 -1
            count2 = count1
    if (count3 -1) ==0:
        showinfo(title="Результат поиска: ", message='Последнее совпадение (номер в списке-'+ str(count2) +') \n')
    else:
        showinfo(title="Результат поиска: ", message='Последнее совпадение (номер в списке-'+ str(count2) +') \n'+ poisk +'\n Найдено '+str(search_count)+' совпадений с заданным поиском '+ str(poisk_fraza))

def delete_data():                                                                        #Удаление записи из справочника
    selected_checkboxs = listbox.curselection()
    Name.set('')
    for selected_checkbox in selected_checkboxs[::-1]:
        listbox.delete(selected_checkbox)
    list_zapisi = listbox.get(0, END)

    filename = 'spravka.txt'
    write_data(filename)

def reset():                                                                       #Очистка строки ввода/поиска
    Name.set('')

def rewrite_data():                                                                #Исправление выбранной (2 клика) информации в справочнике

    selected_listboxs2 = listbox.curselection()
    if Name.get() == '':
        return 0
    if selected_listboxs2:
        listbox.delete(selected_listboxs2)
    else:
        showinfo(title="ПРЕДУПРЕЖДЕНИЕ! НЕ ХВАТАЕТ ПАРАМЕТРОВ ", message='НЕ ВЫБРАН ЭЛЕМЕНТ СПИСКА НА ИЗМЕНЕНИЕ')
    
    listbox.insert(selected_listboxs2, Name.get())
    filename = 'spravka.txt'
    write_data(filename)
    Name.set('')
    
def save_file_as():                                                                 #Диалог сохранения файла
    filename =  filedialog.asksaveasfilename(initialdir = "Python8",title = "Select file",filetypes = (("Текстовые документы (*.txt)","*.txt"),("all files","*.*")))
    print (filename)
    write_data(filename)

def check_tnumber():                                                                 #Проверка правильности ввода номера телефона (8**********)
    instring = ''
    instring = Name.get()
    instring2 = re.sub(r'\D', '', instring)
    regex_pattern =r'(?:\+7|8)(?:\d{2,3}){4}'
    result = bool(re.match( regex_pattern, instring2))
    if ((result) and (len(instring2) == 11)): 
        return 1
    else:
        return 0

########################################Формирование интерфейса справочника#############################
Button(root,text="1.Загрузить",font="arial 12 bold",command=read_data).place(x= 150, y=90)
Button(root,text="2.Новая запись",font="arial 12 bold",command=add_user).place(x= 280, y=90)
Button(root,text="4.Удалить",font="arial 12 bold",command=delete_data).place(x= 580, y=90)
Button(root,text="6.Поиск записей",font="arial 12 bold",command=search_data).place(x= 560, y=140)
Button(root,text="5.Очистить поле Ввода записей/Поиск записей",font="arial 12 bold",command=reset).place(x= 110, y=140)
Button(root,text="3.Исправить",font="arial 12 bold",command=rewrite_data).place(x=440, y=90)
Button(root,text="                  7.Сохранить как                  ",font="arial 12 bold",command=save_file_as).place(x= 235, y=460)
listbox.place(x=20,y=200)

scroll_bar = Scrollbar(root, orient="vertical", command=listbox.yview)
scroll_bar.pack(side=RIGHT, fill=Y)
listbox.bind('<Double-Button-1>', lambda e: Name.set(listbox.get(ACTIVE)))
########################################Формирование интерфейса справочника#############################

mainloop()