import operator
from dataclasses import dataclass, field, fields, astuple


# Mostly keeps track of how much raw Materials a thing uses, and raw materials themselves (ore, etc)
@dataclass
class RawMaterials:
    iron_ore: int = field(default=0)
    copper_ore: int = field(default=0)
    coal: int = field(default=0)
    oil: int = field(default=0)
    concrete: int = field(default=0)

    # We're allowing raw materials to be used in maths, this helps support the Parts class
    # addition and multiplication only, no division, or subtraction
    def __mul__(self, other):
        other_list = (other for x in fields(self))
        return RawMaterials(*(operator.mul(*pair) for pair in zip(self, other_list)))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, other):
        if isinstance(other, RawMaterials):
            return RawMaterials(*(operator.add(*pair) for pair in zip(self, other)))
        elif isinstance(other, Part):
            return RawMaterials(*(operator.add(*pair) for pair in zip(self, other.inputs)))

    def __radd__(self, other):
        return self.__add__(other)

    def __iter__(self):
        return iter(astuple(self))


# a Part is any product crafted in a constructor/assembler/etc
@dataclass
class Part:
    inputs: RawMaterials
    output: float = field(default=1.0)

    def __repr__(self):
        """Only show relevant materials, disregard the rest"""
        # also very sightly tweak standard repr output
        mats = ''
        outputs = ''
        for m in fields(self.inputs):
            if getattr(self.inputs, m.name):
                mats += f'{m.name}={getattr(self.inputs, m.name)} '
        if getattr(self, 'output'):
            outputs += f' | output={self.output}'
        return f'inputs={mats.strip()}{outputs}'

    def __mul__(self, other):
        cost_per = self.cost_per_unit()
        mul_tuple = [other for x in fields(self.inputs)]
        new_mats = RawMaterials(*(operator.mul(*pair) for pair in zip(cost_per, mul_tuple)))
        return new_mats

    def __rmul__(self, other):
        return self.__mul__(other)

    # we can also add parts together and get the sum of their mats
    def __add__(self, other):
        if isinstance(other, RawMaterials):
            for s, o in zip(fields(self.inputs), fields(other)):
                o_val = getattr(other, o.name)
                s_val = getattr(self.inputs, s.name)
                setattr(self.inputs, s.name, s_val+o_val)
        elif isinstance(other, Part):
            for s, o in zip(fields(self.inputs), fields(other.inputs)):
                o_val = getattr(other.inputs, o.name)
                s_val = getattr(self.inputs, s.name)
                setattr(self.inputs, s.name, s_val+o_val)

        # When parts are added together, we ignore their outputs, we only care about inputs
        # Set output to zero as it's less confusing to the user (but still not ideal)
        setattr(self, 'output', 0)
        return self

    def __radd__(self, other):
        return self.__add__(other)

    def __iter__(self):
        return iter(astuple(self))

    def cost_per_unit(self):
        """Returns a RawMaterials object representing cost per unit"""
        cost_per = RawMaterials()
        for m in fields(self.inputs):
            mat_cost = getattr(self.inputs, m.name) / self.output
            setattr(cost_per, m.name, mat_cost)

        return cost_per

    def __get_condensed_materials_dict(self):
        """Returns a dict of only the materials that are used for this part"""
        mats = dict()
        for m in fields(self.inputs):
            if getattr(self.inputs, m.name):
                mats[m.name] = getattr(self.inputs, m.name)
        return mats

    def multiply(self, quantity):
        """convenience function, use if you want to know how many resources X constructors/assemblers consume"""
        new_mats = RawMaterials()
        for m in fields(self.inputs):
            setattr(new_mats, m.name, getattr(self.inputs, m.name) * quantity)
        return Part(inputs=new_mats, output=self.output*quantity)

    def turbo(self, turbo):
        """To help facilitate the emulation of adding power shards to machines. turbo=# of power shards"""
        turbo = 1.0 + (turbo*.5)
        new_mats = RawMaterials()
        for m in fields(self.inputs):
            setattr(new_mats, m.name, getattr(self.inputs, m.name) * turbo)
        return Part(inputs=new_mats, output=self.output*turbo)
