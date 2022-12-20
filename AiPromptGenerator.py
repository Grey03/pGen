import customtkinter,json

from pathlib import Path

#setting the theme of the window
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

#getting location of the .py so we can know where the json is
global fileLocation
fileLocation =  str(Path(__file__).resolve().parent)

global prompts
prompts = {}

#setting up the window
app = customtkinter.CTk()
app.geometry("400x240")
app.title("")

#Just refreshes the prompts dictionary
def reloadList():
    global fileLocation
    with open(fileLocation + "\prompts.json") as f:
        x = (json.load(f))
        f.close()
        return x

prompts = reloadList()

def generatePrompt(jsonFile, style, promptLenth):
    print ('Temp')


#------ Main Widget Frame Start
mainWidgetsFrame = customtkinter.CTkFrame(master=app, fg_color="transparent")

styleLabel = customtkinter.CTkLabel(master=mainWidgetsFrame, text="Style")
styleLabel.pack()

stylesDropdown = customtkinter.CTkOptionMenu(master=mainWidgetsFrame,
values=["Style 1", "Style 2"])

stylesDropdown.pack(pady=10)
stylesDropdown.set("Style 1")

promptLength = customtkinter.CTkEntry(master=mainWidgetsFrame, placeholder_text="Prompt Length")
promptLength.pack(pady=10)

#finalPrompt = customtkinter.CTkLabel(master=mainWidgetsFrame, text="Temporary")
#finalPrompt.pack(pady=10)

finalPrompt = customtkinter.CTkEntry(master=mainWidgetsFrame, placeholder_text="Output")
finalPrompt.pack(pady=10)

generateButton = customtkinter.CTkButton(master=mainWidgetsFrame, text="Generate")
generateButton.pack(pady=10)

mainWidgetsFrame.pack()
#------ Main Widget Fram End

app.mainloop()