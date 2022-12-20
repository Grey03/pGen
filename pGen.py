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
app.title("pGen")
app.iconbitmap(fileLocation + "\pGenLogo.ico")

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
        if (int(promptLength.get()) <= len(prompts)):
            while len(finaloutput) < (int(promptLength.get())):
                newprompt = prompts[random.randint(0, len(prompts) -1)]
                if newprompt not in finaloutput:
                    finaloutput.append(newprompt)
        else:
            messagebox.showerror("Generation Error", "The value you entered is too large! You can only generate " + str(len(prompts)) + " or less!")
        
    except:
        messagebox.showerror("Generation Error", "The value you entered is not a number!")
        return

    finalPrompt.delete("0.0", "end")
    finalPrompt.insert("end", ", ".join(finaloutput))

def promptMenu():
    def refreshDropdown():
        global promptStyleDropdown, stylesDropdown

        promptStyleDropdown.configure(values=(list((refreshList()).keys())))
        promptStyleDropdown.set((list((refreshList()).keys()))[0])

        stylesDropdown.configure(values=(list((refreshList()).keys())))
        stylesDropdown.set((list((refreshList()).keys()))[0])

    def refreshTextBox(*args):
        global promptTextBox, styleName, promptStyleDropdown
        promptData = refreshList()
        prompts = promptData[promptStyleDropdown.get()]["Prompts"]

        promptTextBox.delete("0.0","end")

        for i in range(len(prompts)):
            promptTextBox.insert("end", str(prompts[i] + "\n"))

        styleName.delete(0,"end")
        styleName.insert(0,promptStyleDropdown.get())

    def savePrompt():
        global promptTextBox, styleName, fileLocation

        toJson = (list((promptTextBox.get("1.0", "end")).split("\n")))
        
        while ("") in toJson:
            toJson.remove("")

        promptData = refreshList()

        promptData[styleName.get()] = promptData.pop(promptStyleDropdown.get())
        promptData[styleName.get()].update({"Prompts": toJson})

        with open(fileLocation + "\prompts.json", "w") as f:
            json.dump(promptData, f, indent=4)
            f.close()

        refreshDropdown()
        refreshTextBox()

        messagebox.showinfo(title="Save", message="Successfully Saved!")

    def deleteStyle():
        global fileLocation, promptStyleDropdown
        promptData = refreshList()
        promptData.pop(promptStyleDropdown.get())

        with open(fileLocation + "\prompts.json", "w") as f:
            json.dump(promptData, f, indent=4)
            f.close()

        refreshDropdown()
        refreshTextBox()
    
    def startDelete():
        global promptStyleDropdown
        answer = messagebox.askyesno(title="Delete Style", message=("Are you sure you want to delete " + promptStyleDropdown.get() + " style?"))
        if (answer):
            deleteStyle()

    def newStyle():
        global fileLocation
        promptData = refreshList()
        newName = "New Style"
        x = 0
        while (newName + str(x)) in promptData:
            x+=1
        newName = newName + (str(x))
        finalData = {newName: { "Prompts": ["Word1", "Word2", "Word3"]}}
        promptData.update(finalData)
        with open(fileLocation + "\prompts.json", "w") as f:
            json.dump(promptData, f, indent=4)
            f.close()

        refreshDropdown()
        refreshTextBox()

        messagebox.showinfo(title="New Style", message="New style successfully created!")
                  
    menu = customtkinter.CTkToplevel()
    menu.title("Prompts Editor")
    menu.iconbitmap(fileLocation + "\pGenLogo.ico")
    upperFrame = customtkinter.CTkFrame(master = menu)

    global promptStyleDropdown
    promptStyleDropdown = customtkinter.CTkOptionMenu(master=upperFrame,
    values=(list((refreshList()).keys())), command=refreshTextBox)

    promptStyleDropdown.pack(side="left", padx=3)
    promptStyleDropdown.set((list((refreshList()).keys()))[0])

    newStyleButton = customtkinter.CTkButton(master=upperFrame, text="New Style", command=newStyle)
    newStyleButton.pack(side="right", padx=3)

    upperFrame.pack(pady=5)

    global styleName
    styleName = customtkinter.CTkEntry(master=menu, placeholder_text="Style Name")
    styleName.pack(pady=5)

    global promptTextBox
    promptTextBox = customtkinter.CTkTextbox(master=menu, activate_scrollbars=True)
    promptTextBox.pack(pady=5)

    refreshTextBox()

    saveButton = customtkinter.CTkButton(master=menu, text="Save", command=savePrompt, width=100)
    saveButton.pack(pady=5)

    deleteButton = customtkinter.CTkButton(master=menu, text="Delete", command=startDelete, width=50, fg_color="red", hover_color="#b41400")
    deleteButton.pack(pady=10)

#------ Main Widget Frame Start
def createMainMenu():
    mainWidgetsFrame = customtkinter.CTkFrame(master=app, fg_color="transparent")

    styleFrame = customtkinter.CTkFrame(master=mainWidgetsFrame, fg_color="transparent")

    styleFont = customtkinter.CTkFont(family="greyFont", size=24, weight="bold", underline=True)

    styleLabel = customtkinter.CTkLabel(master=styleFrame, text="Styles", font=styleFont)
    styleLabel.pack(pady=5)

    global stylesDropdown
    stylesDropdown = customtkinter.CTkOptionMenu(master=styleFrame,
    values=(list((refreshList()).keys())), height=30)
    stylesDropdown.pack()

    stylesDropdown.set((list((refreshList()).keys()))[0])

    styleFrame.pack(pady=5)


    lengthSettingsFrame = customtkinter.CTkFrame(master=mainWidgetsFrame, fg_color="transparent")

    global promptLength
    promptLength = customtkinter.CTkEntry(master=lengthSettingsFrame, placeholder_text="Length",width=55)
    promptLength.pack(side="left", padx=2)

    promptEditorButton = customtkinter.CTkButton(master=lengthSettingsFrame, text="Editor", command=promptMenu, width=50)
    promptEditorButton.pack(side="left", padx=2)

    lengthSettingsFrame.pack(pady=5)


    generateButton = customtkinter.CTkButton(master=mainWidgetsFrame, text="Generate", command=generatePrompt, height=45)
    generateButton.pack()

    mainWidgetsFrame.pack(side="left", padx=10)

    #------ Main Widget Frame End

    finalPromptFrame = customtkinter.CTkFrame(master=app, fg_color="transparent")

    finalPromptFont = customtkinter.CTkFont(family="greyFont", size=16, weight="bold")

    finalPromptLabel = customtkinter.CTkLabel(master=finalPromptFrame,text="Output:", font=finalPromptFont)
    finalPromptLabel.pack()
    global finalPrompt
    finalPrompt = customtkinter.CTkTextbox(master=finalPromptFrame, activate_scrollbars=True, height=150, width=250)
    finalPrompt.pack()

    finalPromptFrame.pack(side="left", pady=10,padx=10)
    

createMainMenu()

app.mainloop()