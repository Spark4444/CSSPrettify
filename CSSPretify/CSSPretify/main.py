import re
import tkinter as tk
from tkinter import filedialog
from tkinter import font
import os

# Function for opening CSS files
def openCssFile(checkState, text2, entry):
    filepath = filedialog.askopenfilename(filetypes=[("CSS Files", "*.css")])
    if filepath:
        with open(filepath, "r") as file:
            # Read and save the new CSS file
            cssContent = file.read()

            # Regular expression pattern to match element names and their rules, ignoring comments
            pattern = r"(\w+)\s*\{(?:/\*.*?\*/\s*)*([^\}]+)\}"

            # Find all matches of the pattern in the cssContent
            matches = re.findall(pattern, cssContent)

            # Extract element names and rules into separate arrays
            elementArray = [match[0] for match in matches]
            elementRules = [re.sub(r"/\*.*?\*/", "", match[1]).replace("\n", "").split(";")[:-1] for match in matches]
            # Clean up whitespace from the rules
            elementRules = [sorted([rule.replace(" ", "") for rule in rules if rule.replace(" ", "")]) for rules in elementRules]
            elementRules = [[rule.replace(":", ": ") for rule in rules] for rules in elementRules]

            # if the checkBox is checked sort the element names in alphabetical order
            print(checkState.get())
            if checkState.get():
                # Zip the two lists together
                zippedLists = zip(elementArray, elementRules)

                # Sort the zipped list by the first element of each tuple
                sortedZippedLists = sorted(zippedLists)

                # Unzip the lists
                elementArray, elementRules = zip(*sortedZippedLists)

            # New CSS structure varaible
            cssStructure = ""

            # Generate the CSS structure
            for element, rules in zip(elementArray, elementRules):
                cssStructure += f"{element}{{\n"
                for rule in rules:
                    cssStructure += f"    {rule};\n"
                cssStructure += "}\n\n"

        # Save the new CSS file in the same directory with an "Edited" added at the end
        newFilename = f"{os.path.splitext(filepath)[0]}Edited.css"
        with open(newFilename, "w") as file:
            file.write(cssStructure)
            text2.config(text="Edited CSS file saved to:")
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, newFilename)
            entry.config(state="readonly", cursor="xterm")

def main():
    # Window initalization
    root = tk.Tk()
    root.configure(bg="black")
    root.title("CSS Pretify")
    root.iconbitmap("img/cssIcon.ico")
    root.geometry("500x300")
    root.minsize(500, 300) 

    # Varaibles
    checkState = tk.BooleanVar()

    # UI initalization
    customFont = font.Font(family="Helvetica", size=10)
    borderFrame = tk.Frame(root, background="white", bd=1, height=30 , width=115)
    
    text = tk.Label(root, bg="black", fg="white", font=customFont, text="Note that this pretifier removes all comments from your CSS.")
    text.place(anchor="n", relx=0.5)

    openButton = tk.Button(borderFrame, activebackground="white", activeforeground="black", bg="black", command=lambda: openCssFile(checkState, text2, entry), cursor="hand2", fg="white", font=customFont, highlightthickness=0, relief="flat", text="Select a CSS file")
    borderFrame.place(relx=0.5, rely=0.5, anchor="center")
    openButton.place(anchor="center", relx=0.5, rely=0.5)

    checkBox = tk.Checkbutton(root, activebackground="black", activeforeground="white", bg="black", cursor="hand2", fg="white", selectcolor="black", text="Sort element names in alphabetical order", variable=checkState)
    checkBox.place(anchor="center", relx=0.5, rely=0.60)

    text2 = tk.Label(root, bg="black", fg="white", font=customFont, text="")
    text2.place(anchor="s", relx=0.5, rely=0.95)

    entry = tk.Entry(root, bd=0, cursor="arrow", fg="white", font=customFont, justify="center", readonlybackground="black", state="readonly", width=100)
    entry.place(anchor="s", relx=0.5, rely=1)

    root.mainloop()

if __name__ == "__main__":
    main()