from tkinter import *

import tkinter as tk

class CurrencyConverter:
    def __init__(self):
        window = Tk()    
        window.title("currency converter")
        window.configure(bg= "yellow")
        Label(window,font="Helvectica 12 bold ",bg = "yellow",text = "amount to convert").grid(row=1,column=1)
        Label(window,font="Helvectica 12 bold ",bg = "yellow",text = "amount to convert").grid(row=1,column=1)
        Label(window,font="Helvectica 12 bold ",bg = "yellow",text = "amount to convert").grid(row=1,column=1)

        self.amounttoConverterVar = StringVar()
        Entry(window,textvariable = self.amounttoConverterVar,justify = RIGHT).grid(row=1,column=2)

        self.conversionRateVar =StringVar()
        Entry(window,textvariable = self.conversionRateVar,justify = RIGHT).grid(row=2,column=2)

        self.convertedAmountvariable =StringVar()
        lblconvertedAmount = Label(window,font="Helvectica 12 bold",bg="yellow",textvariable=self.convertedAmountvariable).grid(row=3,column=2,sticky=E)


        btconvertedAmount = Button(window,text="convert",font="Helvectica 12 bold",bg="blue",fg='white',command=self.convertedAmount).grid(row=4,column=2,sticky=E)
        vtdelete_all = Button(window,text="clear",font="Helvectica 12 bold",bg='red',fg='white',command=self.delete_all).grid(row=4,column=6,padx=25,pady=25,sticky=E)
        window.mainloop()

    def convertedAmount(self):
        amt= float(self.conversionRateVar.get())
        convertedAmountvariable = float(self.amounttoConverterVar.get())*amt
        self.convertedAmountvariable.set(format(convertedAmountvariable,'10.2f'))

# function to clr inputsset 
    def delete_all(self):
        self.amounttoConverterVar.set("")
        self.conversionRateVar.set("")
        self.convertedAmountvariable.set("")


CurrencyConverter()        








