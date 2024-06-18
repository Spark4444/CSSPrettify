# Imports
import os
import pyperclip
import re
import tkinter as tk
from tkinter import filedialog
from tkinter import font

# Function to edit the CSS code
def editCss(code, checkState):

    # Modified regular expression pattern to match at-rules
    pattern = r"(@[\w-]+[^{]+{[^{}]*}|@[\w-]+[^{]+\{[\s\S]+?\}\s*\})"

    # Find all at-rules in the CSS code
    atRules = re.findall(pattern, code)

    # Sort the at-rules alphabetically by the at-rule name
    sortedAtRules = sorted(atRules, key=lambda x: re.match(r"@[\w-]+", x).group())

    # Remove found at-rules from the original CSS string
    code = re.sub(pattern, "", code)

    # Regular expression pattern to match element names and their rules, ignoring comments
    pattern = r"([.\w*]+)\s*\{(?:/\*.*?\*/\s*)*([^\}]+)\}"

    # Find all matches of the pattern in the cssContent
    matches = re.findall(pattern, code)

    # Extract element names and rules into separate arrays
    elementArray = [match[0] for match in matches]
    elementRules = [re.sub(r"/\*.*?\*/", "", match[1]).replace("\n", "").split(";")[:-1] for match in matches]
    # Clean up whitespace from the rules
    elementRules = [sorted([rule.replace(" ", "") for rule in rules if rule.replace(" ", "")]) for rules in elementRules]
    elementRules = [[rule.replace(":", ": ") for rule in rules] for rules in elementRules]

    # if the checkBox is checked sort the element names in alphabetical order
    if checkState.get():
        # Zip the two lists together
        zippedLists = zip(elementArray, elementRules)

        # Sort the zipped list by the first element of each tuple
        sortedZippedLists = sorted(zippedLists)

        # Unzip the lists
        elementArray, elementRules = zip(*sortedZippedLists)

    # New CSS structure varaible
    cssStructure = ""

    # Generate the CSS structure for regular rules
    for element, rules in zip(elementArray, elementRules):
        cssStructure += f"{element}{{\n"
        for rule in rules:
            cssStructure += f"    {rule};\n"
        cssStructure += "}\n\n"

    # Append the sorted at-rules to the end of the CSS structure
    for atRule in sortedAtRules:
        cssStructure += f"{atRule}\n\n"

    return cssStructure

# Function for opening CSS files
def openCssFile(checkState, text3, entry2):
    filepath = filedialog.askopenfilename(filetypes=[("CSS Files", "*.css")])
    if filepath:
        with open(filepath, "r") as file:
            # Read and save the new CSS file
            cssContent = file.read()

            # get the CSS structure from the editCss function
            cssStructure = editCss(cssContent, checkState)
            
        # Save the new CSS file in the same directory with an "Edited" added at the end
        newFilename = f"{os.path.splitext(filepath)[0]}Edited.css"
        with open(newFilename, "w") as file:
            file.write(cssStructure)
            text3.config(text="Edited CSS file saved to:")
            text3.place(anchor="s", relx=0.5, rely=0.95)
            entry2.config(state="normal")
            entry2.delete(0, tk.END)
            entry2.insert(0, newFilename)
            entry2.config(state="readonly", cursor="xterm")

# Function for copying the CSS code
def copyToClipboard(entry, checkState, text3, root):
    cssCode = entry.get()

    # get the CSS structure from the editCss function
    cssStructure = editCss(cssCode, checkState)
    pyperclip.copy(cssStructure)
    text3.config(text="Copied your new CSS to clipboard.")
    entry.delete(0, tk.END) 
    root.focus()

# Function to defocus the second entry
def defocus(event, entry, entry2):
    if event.widget != entry:
        entry2.focus() 

# Function to change the text of the entry to nothing if it gets clicked
def onEntryClick(entry, defaultText):
    if entry.get() == defaultText:
        entry.delete(0, tk.END)
        entry.insert(0, "")
        entry.config(fg="white")

# Function to set the entry to deafult text if it loses focus
def onFocusout(entry, defaultText):
    if entry.get() == "":
        entry.insert(0, defaultText)
        entry.config(fg="grey")

def main():
    # Window initalization
    root = tk.Tk()
    root.configure(bg="black")
    root.title("CSS Prettify")
    root.iconbitmap(r"CSSPrettify\dist\main\img\cssIcon.ico")
    root.geometry("500x300")
    root.minsize(500, 300) 
    root.resizable(False, False)

    # Varaibles
    checkState = tk.BooleanVar()
    defaultText = "Copy your CSS here"

    # UI initalization
    customFont = font.Font(family="Helvetica", size=10)
    borderFrame = tk.Frame(root, background="white", bd=1, height=30 , width=115)
    
    text = tk.Label(root, bg="black", fg="white", font=customFont, text="Note that this pretifier removes all comments from your CSS.")
    text.place(anchor="n", relx=0.5)

    openButton = tk.Button(borderFrame, activebackground="white", activeforeground="black", bg="black", command=lambda: openCssFile(checkState, text3, entry2), cursor="hand2", fg="white", font=customFont, highlightthickness=0, relief="flat", text="Select a CSS file")
    borderFrame.place(anchor="center", relx=0.5, rely=0.35)
    openButton.place(anchor="center", relx=0.5, rely=0.45)

    text2 = tk.Label(root, bg="black", fg="white", font=customFont, text="OR")
    text2.place(anchor="center", relx=0.5, rely=0.5)

    entry = tk.Entry(root, bg="black", bd=0, fg="grey", font=customFont, insertbackground="white", justify="center", width=40)
    entry.insert(0, defaultText)
    entry.place(anchor="center", relx=0.5, rely=0.60)

    checkBox = tk.Checkbutton(root, activebackground="black", activeforeground="white", bg="black", cursor="hand2", fg="white", selectcolor="black", text="Sort element names in alphabetical order", variable=checkState)
    checkBox.place(anchor="center", relx=0.5, rely=0.68)

    text3 = tk.Label(root, bg="black", fg="white", font=customFont, text="")
    text3.place(anchor="s", relx=0.5, rely=0.95)

    entry2 = tk.Entry(root, bd=0, cursor="arrow", fg="white", font=customFont, justify="center", readonlybackground="black", state="readonly", width=65)
    entry2.place(anchor="s", relx=0.5, rely=1)

    # Binds
    root.bind("<1>", lambda event: defocus(event, entry, entry2))
    entry.bind("<Return>", lambda event: copyToClipboard(entry, checkState, text3, root))
    entry.bind("<FocusIn>", lambda event: onEntryClick(entry, defaultText))
    entry.bind("<FocusOut>", lambda event: onFocusout(entry, defaultText))

    root.mainloop()

if __name__ == "__main__":
    main()