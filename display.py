import time

import pygame as pg
import moderngl as mgl
import math
import sys
from model import *
from camera import Camera, FOV
from light import Light
from mesh import Mesh
from scene import Scene

import picker_util
from threading import Thread

class Vector:
    def __init__(self, xyz):
        self.x, self.y, self.z = xyz

    def __add__(self, other):
        return Vector([self.x + other.x , self.y + other.y, self.z + other.z])

    def __sub__(self, other):
        return Vector([self.x - other.x , self.y - other.y, self.z - other.z])

class GraphicsEngine:
    def __init__(self, win_size=(1600, 900)):
        # init pygame modules
        pg.init()
        # window size
        self.WIN_SIZE = win_size
        # set opengl attr
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        # create opengl context
        self.Screen = pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        # mouse settings
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        # detect and use existing opengl context
        self.ctx = mgl.create_context()
        # self.ctx.front_face = 'cw'
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)
        # create an object to help track time
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0
        # light
        self.light = Light(position=(10, 30, 50))
        # camera
        self.camera = Camera(self)
        # mesh
        self.mesh = Mesh(self)
        # scene
        self.scene = Scene(self)

        # Recursion Depth
        sys.setrecursionlimit(2001)

    def getWindow(self):
        return self.Screen

    def setCameraSpeed(self, x):
        self.camera.SPEED = x

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.mesh.destroy()
                pg.quit()
                sys.exit()

    def render(self):
        # clear framebuffer
        self.ctx.clear(color=(1, 1, 1))
        # render scene
        self.scene.render()
        # swap buffers
        pg.display.flip()

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001
    def AddCuboid(self, pos, size):
        self.scene.AddCube(pos, size)
        self.scene.render()


    def castRay(self, coord="center"):
        # Get Camera Pos
        xyz = Vector(self.camera.position)

        if coord == "center":
            coord = (self.WIN_SIZE[0] // 2, self.WIN_SIZE[1] // 2)

        # Calculate the pitch we should fire the ray (+The angle the camera is facing)
        Pitch = self.camera.pitch
        AngleOfScreenPitch = (FOV / self.WIN_SIZE[1]) * coord[1]
        # Adjust for negatives
        AngleOfScreenPitch -= self.WIN_SIZE[1] / 2
        Pitch += AngleOfScreenPitch

        # Calculate the yaw
        Yaw = self.camera.yaw
        AngleOfScreenYaw = (FOV / self.WIN_SIZE[0]) * coord[0]
        # Adjust for negatives
        AngleOfScreenYaw -= self.WIN_SIZE[0] / 2
        Yaw += AngleOfScreenYaw

        # Figure out delta values
        x = math.cos(Pitch)
        delta_x = (math.cos(Yaw) * x ) * 0.5
        delta_y = (math.sin(Pitch) ) * 0.5
        delta_z = (math.sin(Yaw) * x ) * 0.5
        delta_xyz = Vector([delta_x, delta_y, delta_z])

        # March
        print(self.scene.objects)  # this line makes it work and IDK why. maybe to-do with threading

        hitObject = self.March(xyz, delta_xyz, self.scene.objects, Timeout=1500)
        return hitObject

    def March(self, xyz, delta_xyz, objects, Timeout=100):
        Timeout -= 1

        if Timeout <= 0:
            return [None]

        # Get New Pos
        new_xyz = xyz - delta_xyz
        Points = glm.vec3(new_xyz.x, new_xyz.y, new_xyz.z)

        # Check for collisions
        for Object in objects:
            if Object.vao_name == "cube":
                # Get all 8 vertices From: Object.pos, Object.scale, Object.rot
                modelMatrix = Object.m_model
                vertexData = picker_util.CUBE_get_vertices()
                transformedVertexData = [modelMatrix @ vertex for vertex in vertexData]

                maxDistance = 0
                for vertex in transformedVertexData:
                    maxDistance = max(glm.distance(vertex, Points), maxDistance)

                maxSizeForCube = glm.distance(modelMatrix @ (-1, -1, -1), modelMatrix @ (1, 1, 1))

                if maxSizeForCube > maxDistance:
                    return [Object, new_xyz]




            else:
                raise Warning("Invalid Object Found While Marching...")

        self.March(new_xyz, delta_xyz, objects, Timeout)

    def exit(self):
        self.EXIT = True

    def update(self):
        self.get_time()
        self.check_events()
        self.camera.update()
        self.render()
        self.delta_time = self.clock.tick(60)


