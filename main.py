from tkinter import *
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import cv2
import math
import os

class Enhance_Image:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1375x880")
        self.root.title("Image Enhancer")
        self.image_path = None
        
        title = Label(self.root, text="Image Enhancer", font=('Arial', 30, 'bold'), pady=2, bd=12, bg="#8A8A8A", fg="Black", relief=GROOVE)
        title.pack(fill=X)
        
        self.LoadImg_Frame = LabelFrame(self.root, text="Load Image", font=('Arial', 15, 'bold'), bd=10, fg="Black", bg="grey")
        self.LoadImg_Frame.place(x=0, y=75, width=625, height=705)
        
        self.Option_Frame = LabelFrame(self.LoadImg_Frame, text="Options", font=('Arial', 15, 'bold'), bd=10, fg="Black", bg="grey")
        self.Option_Frame.place(x=0, y=570, width=605, height=100)
        
        self.load_button = Button(self.Option_Frame, text="Load Image", command=self.load_image, bg="#13B10F", bd=2, fg="black", pady=15, width=12, font='arial 13 bold')
        self.load_button.pack(side=LEFT,padx=4)
        
        self.Enhance_Button = Button(self.Option_Frame, text="Enhance Image",command=self.Enhance_Image, state=DISABLED,  bg="red", bd=2, fg="black", pady=15, width=20, font='arial 13 bold')
        self.Enhance_Button.pack(side=LEFT,padx=4)
        
        self.reset = Button(self.Option_Frame, text="Reset", command=self.ResetWindow,  bg="red",fg="black", pady=15, width=12, font='arial 13 bold')
        self.reset.pack(side=RIGHT,padx=60)
        
        self.Generated_Frame = LabelFrame(self.root, text="Output", font=('Arial', 15, 'bold'), bd=10, fg="Black", bg="grey")
        self.Generated_Frame.place(x=625, y=75, width=750, height=705)
        
        self.Bit_Frame = LabelFrame(self.root, text="Parameters", font=('arial', 14, 'bold'), bd=10, bg="grey")
        self.Bit_Frame.place(x=0, y=780, relwidth=1, height=100)
        
        self.Final_Image = []
        
        E_Lb = Label(self.Bit_Frame, text="E=", font=('arial', 16, 'bold'), bg="grey", fg="black")
        E_Lb.grid(row=0, column=0, padx=2, pady=10, sticky='W')
        self.ERes = Entry(self.Bit_Frame, width=10,  font=('arial', 16, 'bold'), bd=5, relief=GROOVE)
        self.ERes.grid(row=0, column=1, padx=0, pady=10)

        
        self.K_List = []
        
        Ci = 1
        for i in range(2,5):
            K_Lb = Label(self.Bit_Frame, text="K" + str(Ci), font=('arial', 16, 'bold'), bg="grey", fg="black")
            K_Lb.grid(row=0, column=2*i-2, padx=10, pady=0, sticky='W')
            K = Entry(self.Bit_Frame, width=10, font=('arial', 16, 'bold'), bd=5, relief=GROOVE)
            K.grid(row=0, column=2*i-1, padx=10, pady=0)
            self.K_List.append(K)
            Ci += 1
        
        self.LoadVal_Btn = Button(self.Bit_Frame, text="Load Values", command=self.load_values,  bg="green",fg="black", pady=15, width=10, font='arial 13 bold')
        self.LoadVal_Btn.grid(row=0,column=8,padx=10)
    
    def load_values(self):
         
        self.K0 = float(self.K_List[0].get())
        self.K1 = float(self.K_List[1].get())
        self.K2 = float(self.K_List[2].get())
        self.E = float(self.ERes.get())

        if((self.K0 is not None) and ( self.K1 is not None) and (self.K2 is not None) and (self.E is not None)):
            self.Enhance_Button.config(state=NORMAL)
        else:
            self.Enhance_Button.config(state=DISABLED)
        
    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])     
        if self.image_path:
            self.Original_image = Image.open(self.image_path).convert("L")
            self.Original_image = self.Original_image.resize((550, 550))
            self.photo = ImageTk.PhotoImage(self.Original_image)
            self.image_display = Label(self.LoadImg_Frame)
            self.image_display.pack()
            self.image_display.config(image=self.photo)
    
    
    def Get_Global_Deviation(self, mean_intensity):
        self.ReadyDv_List = []
        height, width =  self.Image_BitList.shape[:2]
        sum_sq_diff = 0
        
        for r in range(width):
            for c in range(height):
                intensity = self.Image_BitList[r][c]
                # print(intensity)
                sq_diff = (intensity - mean_intensity) ** 2
                sum_sq_diff += sq_diff

        variance = sum_sq_diff / (height * width)
        std_dev = math.sqrt(variance)
        print(f"Global Standard deviation: {std_dev}")
        print("\n")
        return std_dev
    
        
    def Get_Global_Mean(self):
        self.Image_BitList = np.array(self.Original_image)
        self.AvgInt_List = []
        
        height, width =  self.Image_BitList.shape[:2]
        sum_intensity = 0
        
        for r in range(width):
            for c in range(height):
                intensity =  self.Image_BitList[r][c]
                sum_intensity += intensity

        mean_intensity = sum_intensity / (height * width)
        print(f"Global Mean Intensity: {mean_intensity}")
        return mean_intensity

    def ResetWindow(self):
        root.destroy()
        os.system('main.py')

    
if __name__ == "__main__":
    root = Tk()
    app = Enhance_Image(root)
    root.mainloop()