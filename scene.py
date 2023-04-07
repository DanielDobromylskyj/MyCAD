from model import *


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()

    def add_object(self, obj):
        self.objects.append(obj)


    def AddCube(self, xyz, size, Rot=(0, 0, 0)):
        self.add_object(
            Cube(self.app,
                 pos=xyz,
                 scale=size,
                 rot=Rot)
        )

    def AddCylinder(self, xyz, radius, height, Rot=(0, 0, 0)):
        self.add_object(
            Cylinder(self.app,
                 pos=xyz,
                 scale=(radius, height),
                 rot=Rot)
        )


    def load(self):
        """        app = self.app
        add = self.add_object

        n, s = 30, 3
        for x in range(-n, n, s):
            for z in range(-n, n, s):
                add(Cube(app, pos=(x, -s, z)))"""
        pass


    def render(self):
        for obj in self.objects:
            obj.render()