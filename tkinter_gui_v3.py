_name_ = 'tkinter_gui_v2'

import time
from tkinter import *
from NS_API_v3 import *

root = Tk()
root['background'] = 'DarkGoldenrod1'
vertrek_overzicht_var = StringVar()
gebruiker_invoer_var = StringVar()

def toon_welkomst_frame():
    """Toont het welkomstframe, vergeet de andere frames"""
    invoer_frame.pack_forget()
    reisinfo_frame.pack_forget()
    welkomst_frame.pack()


def toon_invoer_frame():
    """Toont het invoerframe, vergeet de andere frames"""
    welkomst_frame.pack_forget()
    reisinfo_frame.pack_forget()
    invoer_frame.pack()


def toon_reisinfo_frame():
    """Toont het reisinfo frame, vergeet de andere frames"""
    welkomst_frame.pack_forget()
    invoer_frame.pack_forget()
    reisinfo_frame.pack()


def default_invoer():
    """Wanneer de eerste keer op de reisinfo button gedrukt wordt, zal reisinformatie van Utrecht worden weergegeven omdat de automaat daar staat"""
    invullen_stationsnaam('Utrecht')
    global gebruiker_invoer_var
    gebruiker_invoer_var.set('Utrecht')


def ingevulde_invoer():
    """De tweede keer dat op de reisinfo button wordt gedrukt wordt de invoer van de gebruiker gevraagd"""
    invullen_stationsnaam(gebruiker_invoer.get())
    global gebruiker_invoer_var
    gebruiker_invoer_var.set(gebruiker_invoer.get())


def invullen_stationsnaam(invoer):
    """Vult de ingevoerde naam in, in de back-end en krijgt het overzicht van vertrektijden terug"""
    # vertrek_overzicht = '\n'.join(stationscode(invoer))
    vertrek_overzicht_list = stationscode(invoer)
    kleine_list = []
    for line in vertrek_overzicht_list[0:20]:
        kleine_list.append(line)
    global vertrek_overzicht_var
    vertrek_overzicht_var.set('\n'.join(kleine_list))
    return toon_reisinfo_frame()


time1 = ''
def stationsklok():
    """Deze functie maakt een werkende klok die blijft refreshen, weergegeven in het 'klok' label"""
    global time1
    # vraag de tijd van lokale pc
    time2 = time.strftime('%H:%M:%S')
    # als de tijd is veranderd, pas de string aan
    if time2 != time1:
        time1 = time2
        klok.config(text=time2)
    # ververst zichzelf elke 200ms
    klok.after(200, stationsklok)


#################### DIT IS HET WELKOMSTFRAME ###################
welkomst_frame = Frame(master=root)
welkomst_frame.pack(fill=BOTH, expand=True)

welkomst_label = Label(master=welkomst_frame,
                       text='Welkom bij NS, u bevindt zich op Utrecht Centraal.',
                       background='DarkGoldenrod1',
                       foreground='midnight blue',
                       font=('Helvetica', 30, 'bold italic'),
                       width=20,
                       height=6)
welkomst_label.pack(fill=BOTH)
button1 = Button(master=welkomst_frame,
                 text='Ik wil naar Amsterdam.',
                 background='midnight blue',
                 fg='DarkGoldenrod1',
                 width=250,
                 height=6,
                 bd=5)
button1.pack()
button2 = Button(master=welkomst_frame,
                 text='Kopen los kaartje.',
                 background="DarkGoldenrod1",
                 fg="midnight blue",
                 width=250,
                 height=6,
                 bd=5)
button2.pack()
button3 = Button(master=welkomst_frame,
                 text='Opladen OV-chipkaart.',
                 background="midnight blue",
                 fg="DarkGoldenrod1",
                 width=250,
                 height=6,
                 bd=5)
button3.pack()
button4 = Button(master=welkomst_frame,
                 text='Ik wil naar het buitenland.',
                 background="DarkGoldenrod1",
                 fg="midnight blue",
                 width=250,
                 height=6,
                 bd=5)
button4.pack()
button5 = Button(welkomst_frame,
                 text='Reisinformatie opvragen.',
                 background="midnight blue",
                 fg="DarkGoldenrod1",
                 width=250,
                 height=6,
                 bd=5,
                 command=default_invoer)
button5.pack()

################### DIT IS HET INVOERFRAME ###################
invoer_frame = Frame(master=root)
invoer_frame.pack(fill=BOTH, expand=True)

invoer_label = Label(invoer_frame,
                     background='DarkGoldenrod1',
                     foreground='midnight blue',
                     width=250,
                     height=6,
                     text='Voer een station in:',
                     font=('Helvetica', 14, 'bold italic'))
invoer_label.pack(fill=BOTH)
gebruiker_invoer = Entry(invoer_frame,
                         background='DarkGoldenrod1',
                         foreground='midnight blue',
                         width=250,
                         font=('Helvetica', 10, 'bold italic'))
gebruiker_invoer.pack()
invoer_button = Button(invoer_frame,
                       background='DarkGoldenrod1',
                       foreground='midnight blue',
                       width=250,
                       height=35,
                       text='Klik hier om vertrektijden op te opvragen',
                       font=('Helvetica', 12, 'bold italic'),
                       command=ingevulde_invoer)
invoer_button.pack(fill=BOTH)

################### DIT IS HET REISINFOFRAME ##################
reisinfo_frame = Frame(master=root)
reisinfo_frame.pack(fill=BOTH, expand=True)

plaatsnaam_label = Label(reisinfo_frame,
                         text='Dit zijn de vertrekkende treinen van station:',
                         bg="DarkGoldenrod1",
                         fg="midnight blue",
                         font=("Helvetica", 15, "bold italic"),
                         width=15)
plaatsnaam_label.pack(side=TOP, fill=BOTH)
plaatsnaam_label_2 = Label(reisinfo_frame,
                           textvariable=gebruiker_invoer_var,
                           bg="DarkGoldenrod1",
                           fg="midnight blue",
                           font=("Helvetica", 30, "bold italic"),
                           width=20)
plaatsnaam_label_2.pack(side=TOP, fill=BOTH)
klok = Label(reisinfo_frame,
             font=('times', 15, 'bold'),
             bg="DarkGoldenrod1")
klok.pack(side=TOP, fill=BOTH, expand=5)
naar_invoer_frame = Button(reisinfo_frame,
                           text="Reis informatie voor ander station",
                           background="midnight blue",
                           foreground="DarkGoldenrod1",
                           width=250,
                           height=6,
                           bd=5,
                           command=toon_invoer_frame)
naar_invoer_frame.pack(side=BOTTOM)
terug_button = Button(reisinfo_frame,
                      text="Terug naar welkomstscherm",
                      background="DarkGoldenrod1",
                      foreground="midnight blue",
                      width=250,
                      height=6,
                      bd=5,
                      command=toon_welkomst_frame)
terug_button.pack(side=BOTTOM)
vertrektijden_label = Label(master=reisinfo_frame,
                            textvariable=vertrek_overzicht_var,
                            background="DarkGoldenrod1",
                            foreground="midnight blue",
                            font=('Helvetica', 12, 'bold italic'),
                            width=80,
                            height=80,)
vertrektijden_label.pack(fill=BOTH)

stationsklok()
toon_welkomst_frame()
mainloop()