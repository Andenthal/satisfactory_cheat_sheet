from Materials import RawMaterials, Part, fields


### Parts sorted roughly by tier and discovery time
# Part cost should be configured as "per minute" as shown in the Constructor/Assembler
# not per-item values (with exceptions as noted)
###

## Raw materials (stuff that comes outta the ground)
_iron_ore = RawMaterials(iron_ore=1)
_coal_ore = RawMaterials(coal=1)
_oil = RawMaterials(oil=1)
_concrete = RawMaterials(concrete=1)
# ingots are calculated per resource, not per minute
# except steel, see below
_iron_ingot = RawMaterials(iron_ore=1)
_copper_ingot = RawMaterials(copper_ore=1)

## T1 copper
wire = Part(inputs=_copper_ingot * 15, output=30)
cable = Part(inputs=wire * 60, output=30)
copper_sheet = Part(inputs=_copper_ingot*20, output=10)

## T1 Iron
iron_plate = Part(inputs=_iron_ingot * 30, output=20)
iron_rod = Part(inputs=_iron_ingot * 15, output=15)

## Iron T2
screw = Part(inputs=iron_rod * 10, output=40)
reinforced_iron_plate = Part(inputs=iron_plate * 30 + screw * 60, output=5)

rotor = Part(inputs=iron_rod * 20 + screw * 100, output=4)
modular_frame = Part(inputs=reinforced_iron_plate * 3 + iron_rod * 15, output=2)
mod_frame = modular_frame

## Steel
steel_ingot = Part(inputs=_iron_ore * 45 + _coal_ore * 45, output=45)
steel_beam = Part(inputs=steel_ingot * 60, output=15)
steel_pipe = Part(inputs=steel_ingot * 30, output=20)

## Mixed/mid-game
stator = Part(inputs=steel_ingot * 15 + wire * 40, output=5)
motor = Part(inputs=rotor * 10 + stator * 10, output=5)
encased_industrial_beam = Part(inputs=steel_beam*24 + _concrete*30, output=6)

## spaceship parts
smart_plating = Part(inputs=reinforced_iron_plate * 2 + rotor * 2, output=2)
#elevator 2500
versatile_frame = Part(inputs=mod_frame * 3 + steel_beam * 30, output=5)
automated_wiring = Part(inputs=stator*2.5 + cable * 50, output=2.5)

# oil
heavy_residue_plastic = Part(inputs=_oil*30, output=10)
heavy_residue_rubber = Part(inputs=_oil*30, output=20)
plastic = Part(inputs=_oil*30, output=20)
rubber = Part(inputs=_oil*30, output=20)

# T5/6  assembler parts
circuit_board = Part(inputs=copper_sheet*15 + plastic*30, output=7.5)
# T5/6 manufacturer parts
#elevator amap (500)
modular_engine = Part(inputs=motor*2 + rubber*15 + smart_plating*2, output=1)
heavy_mod_frame = Part(inputs=mod_frame*10 + steel_pipe*30 + encased_industrial_beam*10 + screw*200, output=2)
computer = Part(inputs=cable*22.5 + plastic*45 + screw*130 + circuit_board*25, output=2.5)
#elevator 1
acu = Part(inputs=automated_wiring*7.5 + circuit_board*5 + heavy_mod_frame*1 + computer*1, output=2)


### helper functions
def how_many_can_i_make(item: Part, **kwargs):
    """
    Attempts to calculate how many buildings can be constructed of item with given mats
    :param item: Part
    :param kwargs: materials E.G. iron_ore=100, copper_ore=100
    :return: str - representation of how many of item can be built with mats provided
    """

    # validate input - ensure that we're only dealing with supported mats.
    avail_mats = locals()['kwargs']
    for m in avail_mats:
        try:
            getattr(RawMaterials, m)
        except AttributeError:
            mats = [x.name for x in fields(RawMaterials)]
            print(f"Unknown material type: '{m}'. Valid material type:{mats}")
            exit()

    # figure out material per item ratios based on user input
    ratios = dict()
    for m in avail_mats:
        try:
            mat = int(avail_mats[m])
        except ValueError:
            print(f"Invalid resource quantity for '{m}': {avail_mats[m]}. Should be a number")
            exit()
        if mat > 0 and getattr(item.inputs, m) > 0:
            ratios[m] = mat / getattr(item.inputs, m)

    min_ratio = int(min(ratios.values()))
    consolidated_mats = RawMaterials()
    for f in fields(consolidated_mats):
        setattr(consolidated_mats, f.name, getattr(item.inputs, f.name) * min_ratio)

    print(f"You can make {min_ratio} of those:\nYou may also need other mats, see full input/output scheme below")
    print(Part(inputs=consolidated_mats, output=item.output * min_ratio))


