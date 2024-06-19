# Imports
import os
import pyperclip
import re
import tkinter as tk
from tkinter import filedialog, font
from tkinterdnd2 import DND_FILES, TkinterDnD

# Function to edit the CSS code
def editCss(code, checkState):
    # Remove all comments from CSS
    cleanedCss = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)

    # Modified regular expression pattern to match at-rules
    pattern = r"(@[\w-]+[^{]+{[^{}]*}|@[\w-]+[^{]+\{[\s\S]+?\}\s*\})"

    # Find all at-rules in the CSS code
    atRules = re.findall(pattern, cleanedCss)

    # Sort the at-rules alphabetically by the at-rule name
    sortedAtRules = sorted(atRules, key=lambda x: re.match(r"@[\w-]+", x).group())

    # Remove found at-rules from the original CSS string
    cleanedCss = re.sub(pattern, "", cleanedCss)



    #RULES SELECTION    
    # Regular expresion to select anything inside { }
    curlyBracketsPattern = r"\{([^}]+)\}"

    # Find all matches of the pattern in the CSS code
    matches = re.findall(curlyBracketsPattern, cleanedCss)

    # Initialize an empty list to store the rules
    rules = []

    # Process each match
    for match in matches:
        # Split the match by semicolon to separate ruleName and ruleParameter
        parts = match.split(";")
        for part in parts:
            # Split each part by colon to get ruleName and ruleParameter
            ruleParts = part.split(":")
            if len(ruleParts) == 2:
                ruleName, ruleParameter = ruleParts
                # Remove any leading/trailing spaces
                ruleName = ruleName.strip()
                ruleParameter = ruleParameter.strip()
                # Append the rule as a list [ruleName, ruleParameter] to the "rules" list
                rules.append([ruleName, ruleParameter+";"])

    # Sort rules names in alphabetical order
    sortedRules = sorted(rules, key=lambda x: x[0])


    #NAME SELECTION 
    # Initialize an empty list to store the element names
    elementNames = []

    # Other varaibles
    insideBraces = False
    currentWord = ""

    # Select all the content outside of the curly braces
    for char in cleanedCss:
        if char == "{":
            insideBraces = True
        elif char == "}":
            insideBraces = False
            if currentWord:
                # Append the element name [elementName] to the "elementNames" list while removing any leading/trailing spaces
                elementNames.append(currentWord.strip())
            currentWord = ""
        elif not insideBraces:
            currentWord += char

    if checkState.get():
        elementNames = sorted(elementNames)

    print(elementNames)
    print(rules)

    # New CSS structure variable
    # cssStructure = []

    # Generate the CSS structure for regular rules
    # cssStructure = ""
    # for element, rules in zip(elementArray, elementRules):
    #     cssStructure += f"{element} {{\n"
    #     for rule in rules:
    #         rule_name, rule_value = rule.split(":")
    #         cssStructure += f"    {rule_name.strip()}: {rule_value.strip()};\n"
    #     cssStructure += "}\n\n"

    # Append the sorted at-rules to the end of the CSS structure
    # for atRule in sortedAtRules:
    #     cssStructure += f"{atRule}\n\n"

    # return cssStructure

# Function for opening a CSS files and then editing it
def openCssFile(checkState, text3, entry2):
    filePath = filedialog.askopenfilename(filetypes=[("CSS Files", "*.css")])
    if filePath:
        with open(filePath, "r") as file:
            # Read and save the new CSS file
            cssContent = file.read()

            # get the new CSS structure from the editCss function
            cssStructure = editCss(cssContent, checkState)
            
        # Save the new CSS file in the same directory with an "Edited" added at the end
        newFilename = f"{os.path.splitext(filePath)[0]}Edited.css"
        with open(newFilename, "w") as file:
            # file.write(cssStructure)
            text3.config(text="Edited CSS file saved to:")
            text3.place(anchor="s", relx=0.5, rely=0.95)
            entry2.config(state="normal")
            entry2.delete(0, tk.END)
            entry2.insert(0, newFilename)
            entry2.config(state="readonly", cursor="xterm")
            text3.place(anchor="s", relx=0.5, rely=0.95)
            entry2.place(anchor="s", relx=0.5, rely=1)

# Function for editing CSS from an entry and then copying it into clipboard
def copyCssToClipboard(checkState, entry, entry2, event, root, text3):
    cssCode = entry.get()

    # get the new CSS structure from the editCss function
    cssStructure = editCss(cssCode, checkState)

    # Copy the new CSS into clipboard
    pyperclip.copy(cssStructure)

    # Set the text3 to display that you"ve copied the new CSS text
    text3.config(text="Copied your new CSS to clipboard.")
    text3.place(anchor="s", relx=0.5, rely=1)
    entry2.config(state="normal")
    entry2.delete(0, tk.END)
    entry2.config(state="readonly", cursor="arrow")
    entry2.place(anchor="s", relx=0.5, rely=0.92)
    entry.delete(0, tk.END) 
    root.focus()

# Function for editing a CSS file by dropping it
def dropCss(checkState, entry2, event, text3, text4):
    # Assuming only one file is dropped, get the file path
    filePath = event.data.replace("{", "").replace("}", "").strip()
    text4.place_forget() 
    
    # Open and read the file content
    with open(filePath, "r") as file:
        # Read and save the new CSS file
        cssContent = file.read()

        # get the new CSS structure from the editCss function
        cssStructure = editCss(cssContent, checkState)
        
    # Save the new CSS file in the same directory with an "Edited" added at the end
    newFilename = f"{os.path.splitext(filePath)[0]}Edited.css"
    with open(newFilename, "w") as file:
        file.write(cssStructure)
        text3.config(text="Edited CSS file saved to:")
        text3.place(anchor="s", relx=0.5, rely=0.95)
        entry2.config(state="normal")
        entry2.delete(0, tk.END)
        entry2.insert(0, newFilename)
        entry2.config(state="readonly", cursor="xterm")
        text3.place(anchor="s", relx=0.5, rely=0.95)
        entry2.place(anchor="s", relx=0.5, rely=1)

# Function to defocus the second entry if another element is being clicked
def defocusEntry2(entry, entry2, event):
    if event.widget != entry:
        entry2.focus() 

# Function to change the text of the entry to nothing
def entryDefaultON(defaultText, entry, event):
    if entry.get() == defaultText:
        entry.delete(0, tk.END)
        entry.insert(0, "")
        entry.config(fg="white")

# Function to set the entry to default text
def entryDefaultOFF(defaultText, entry, event):
    if entry.get() == "":
        entry.insert(0, defaultText)
        entry.config(fg="grey")

# Function to show text4
def showText4(event, text4):
    text4.place(relwidth=1, relheight=1)

# Function to hide text4
def hideText4(event, text4):
    text4.place_forget() 

def main():
    # Window initalization
    root = TkinterDnD.Tk()
    root.configure(bg="black")
    root.title("CSS Prettify")
    # root.iconbitmap(r"dist\CSSPrettify\img\cssIcon.ico")
    root.geometry("500x300")
    root.minsize(500, 300) 
    root.resizable(False, False)

    # Varaibles
    checkState = tk.BooleanVar()
    defaultText = "Copy your CSS here"

    # UI initalization
    normalFont = font.Font(family="Helvetica", size=10)
    bigFont = font.Font(family="Helvetica", size=40)
    borderFrame = tk.Frame(root, background="white", bd=1, height=30 , width=115)
    
    text = tk.Label(root, bg="black", fg="white", font=normalFont, text="Note that this prettifier removes all comments from your CSS.\n (You can drop your files and it will work too)")
    text.place(anchor="n", relx=0.5)

    openButton = tk.Button(borderFrame, activebackground="white", activeforeground="black", bg="black", command=lambda: openCssFile(checkState, text3, entry2), cursor="hand2", fg="white", font=normalFont, highlightthickness=0, relief="flat", text="Select a CSS file")
    borderFrame.place(anchor="center", relx=0.5, rely=0.35)
    openButton.place(anchor="center", relx=0.5, rely=0.45)

    text2 = tk.Label(root, bg="black", fg="white", font=normalFont, text="OR")
    text2.place(anchor="center", relx=0.5, rely=0.5)

    entry = tk.Entry(root, bg="black", bd=0, fg="grey", font=normalFont, insertbackground="white", justify="center", width=40)
    entry.insert(0, defaultText)
    entry.place(anchor="center", relx=0.5, rely=0.60)

    checkBox = tk.Checkbutton(root, activebackground="black", activeforeground="white", bg="black", cursor="hand2", fg="white", selectcolor="black", text="Sort element names in alphabetical order", variable=checkState)
    checkBox.place(anchor="center", relx=0.5, rely=0.68)

    text3 = tk.Label(root, bg="black", fg="white", font=normalFont, text="")

    entry2 = tk.Entry(root, bd=0, cursor="arrow", fg="white", font=normalFont, justify="center", readonlybackground="black", state="readonly", width=65)
    entry2.place(anchor="s", relx=0.5, rely=1)

    text4 = tk.Label(root, bg="black", fg="white", font=bigFont, text="Drop your file here")

    # Binds
    entry.bind("<FocusIn>", lambda event: entryDefaultON(defaultText, entry, event))
    entry.bind("<FocusOut>", lambda event: entryDefaultOFF(defaultText, entry, event))
    entry.bind("<Return>", lambda event: copyCssToClipboard(checkState, entry, entry2, event, root, text3))
    root.bind("<1>", lambda event: defocusEntry2(entry, entry2, event))
    root.dnd_bind("<<Drop>>", lambda event: dropCss(checkState, entry2, event, text3, text4))
    root.dnd_bind("<<DropEnter>>", lambda event: showText4(event, text4))
    root.dnd_bind("<<DropLeave>>", lambda event: hideText4(event, text4))
    root.drop_target_register(DND_FILES)

    root.mainloop()

if __name__ == "__main__":
    main()