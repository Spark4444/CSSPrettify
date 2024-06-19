# CSS Prettify

This app sorts `CSS` code in alphabetical order to make it look pretty.
After choosing the `CSS` code using the button or copying it into entry, it will edit it and save it into the same directory with `Edited` added to the file name or copy it into your clipboard. If you don't need the `CSSPretify.py` file you can delete it after downloading the project, it's not needed for the `CSSPretify.exe` to work.
Also i can't fix it, but this prettiefier removes all comments from your `CSS` after editing it.

## Instalation

1. Press the blue button `<> Code`
2. Hover over the `Download Zip` button and click it to download the zip version of this repository

### &nbsp;&nbsp;&nbsp;Or

Use the git clone command to copy it onto your computer
```
bash git clone https://github.com/Spark4444/CSSPrettify
```

## Usage examples

After choosing the `CSS` code file this is how the app will edit it

#### CSS code before:
```
alement{
    color: blue;
    background: yellow;
}
element2{
    color:yellow;
    background:blue;
}
.blement3{
    /*comment*/
    display: inline;
    color:yellow;
    background:blue;
}

element4{color:yellow;/*comment*/background:blue;}
```

#### CSS code after:
```
alement{
    background: yellow;
    color: blue;
}

element2{
    background: blue;
    color: yellow;
}

.blement3{
    background: blue;
    color: yellow;
    display: inline;
}

element4{
    background: blue;
    color: yellow;
}
```

## Usage

* To open the app, open the `CSSPretify.exe` executable located in `CSSPretify/dist/main/`
* `Checkbox Sort element names in alphabetical order` sorts all the element names in alphabetical order if checked, like this:

#### before:
```
br{
    ...
}

div{
    ...
}

a{
    ...
}
```
#### After:
```
a{
    ...
}

b{
    ...
}

div{
    ...
}
```


## Current state of this project
**Finished**
