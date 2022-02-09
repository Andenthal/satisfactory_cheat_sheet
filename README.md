# Ande's Satisfactory Helper Tool

## Install
Put these files on your machine.

## Usage
See `satisfactory.py` for more examples. 

Generally speaking each part (Iron Plate, Iron Rod, etc) is defined as the sum of its inputs, combined with how many
items are crafted as the output, on a per-minute basis (based on being crafted in an automated building). Basically an 
item is a {Constructor/Assembler/Manufacturer} making that item at 100% capacity.

I'm essentially trying to answer questions like, "I have X iron ore, how many of Y (automated building) can I make with that."

Just print out the item to see its inputs and outputs.
```console_example
>>> import recipes
>>> print(reinforced_iron_plate) 
inputs=iron_ore=60.0 | output=5
```

Basic maths can be done on multiple parts, to figure out their combined cost
```basic_maths
>>> print(reinforced_iron_plate + modular_frame)
inputs=iron_ore=111.0
```
Notice that the `iron_ore` input for each type has been added together. Also notice that there is no output, the tool
isn't smart enough to calculate dissimilar output quantities and display them elegantly. 
