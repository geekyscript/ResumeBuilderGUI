from tkinter import Tk,Entry,Label,Button,messagebox;from reportlab.pdfgen import canvas
def g():
    n,a=e1.get(),e2.get()
    if not n or not a.isdigit():messagebox.showerror("Error","Enter valid");return
    fn=f"{n.replace(' ','_')}.pdf";c=canvas.Canvas(fn);c.drawString(100,750,f"Name: {n}");c.drawString(100,730,f"Age: {a}");c.save();messagebox.showinfo("Done",f"{fn} created")
r=Tk();Label(r,text="Name").pack();e1=Entry(r);e1.pack();Label(r,text="Age").pack();e2=Entry(r);e2.pack();Button(r,text="Gen PDF",command=g).pack();r.mainloop()
