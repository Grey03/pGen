import customtkinter

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("400x240")
app.title("")

test = ("Kristofer")

label = customtkinter.CTkLabel(master=app, text=test)
label.pack()

app.mainloop()