import customtkinter, json, random

from tkinter import messagebox
from pathlib import Path

#setting the theme of the window
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

#getting location of the .py so we can know where the json is
global fileLocation
fileLocation =  str(Path(__file__).resolve().parent)

#setting up the window
app = customtkinter.CTk()
app.geometry("400x240")
app.title("")

#Just refreshes the prompts dictionary
def refreshList():
    global fileLocation
    with open(fileLocation + "\prompts.json") as f:
        x = (json.load(f))
        f.close()
        return x

def generatePrompt():
    promptData = refreshList()

    global stylesDropdown, promptLength, finalPrompt

    prompts = (promptData[stylesDropdown.get()]["Prompts"])

    finaloutput = []

    try:
        for i in range(int(promptLength.get())):
            newprompt = prompts[random.randint(0, len(prompts) -1)]
            if newprompt not in finaloutput:
                finaloutput.append(newprompt)
            else:
                break
        
    except:
        messagebox.showerror("Generation Error", "The value you entered is not a number!")
        return

    finalPrompt.delete(0, len(finalPrompt.get()))
    finalPrompt.insert(0, ", ".join(finaloutput))

#------ Main Widget Frame Start
def createMainMenu():
    mainWidgetsFrame = customtkinter.CTkFrame(master=app, fg_color="transparent")

    styleLabel = customtkinter.CTkLabel(master=mainWidgetsFrame, text="Styles")
    styleLabel.pack()

    global stylesDropdown
    stylesDropdown = customtkinter.CTkOptionMenu(master=mainWidgetsFrame,
    values=(list((refreshList()).keys())))

    stylesDropdown.pack(pady=10)
    stylesDropdown.set((list((refreshList()).keys()))[0])

    global promptLength
    promptLength = customtkinter.CTkEntry(master=mainWidgetsFrame, placeholder_text="Length",width=55)
    promptLength.pack(pady=10)

    global finalPrompt
    finalPrompt = customtkinter.CTkEntry(master=mainWidgetsFrame, placeholder_text="Output")
    finalPrompt.pack(pady=10)

    generateButton = customtkinter.CTkButton(master=mainWidgetsFrame, text="Generate", command=generatePrompt)
    generateButton.pack(pady=10)

    mainWidgetsFrame.pack()
#------ Main Widget Fram End

createMainMenu()

app.mainloop()