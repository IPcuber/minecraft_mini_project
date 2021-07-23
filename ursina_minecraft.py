from ursina import *
from ursina.camera import Camera
from ursina.prefabs.first_person_controller import FirstPersonController
import time
import multiprocessing
import random

app = Ursina()
grass_texture = load_texture('grass_block.png')
stone_texture = load_texture('stone_block.png')
brick_texture = load_texture('brick_block.png')
dirt_texture = load_texture('dirt_block.png')
punch_sound = Audio('punch_sound', loop = False, autoplay = False)
passive_music = Audio('passive_music.mp3', loop = True, autoplay = False)
block_pick = 1

passive_music.play()
window.fps_counter.enabled = False
window.exit_button.visible = False



class Hotbar(Entity):
    def __init__(self, position = (0,0,0)):
        super().__init__(
            parent = camera.ui,
            model = 'quad',
            texture = 'hotbar.png',
            position = position,
            scale = 0.09)

class Item(Entity):
    def __init__(self, position = (0,0,0), texture = None):
        super().__init__(
            parent = camera.ui,
            model = 'quad',
            texture = texture,
            position = position,
            scale = 0.07)

def update():
    global block_pick

    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()

    if held_keys['1']: 
        highlight.position = (-0.11,-0.4,0)
        block_pick = 1

    if held_keys['2']:
        highlight.position = (-0.02,-0.4,0)
        block_pick = 2

    if held_keys['3']: 
        highlight.position = (0.07,-0.4,0)
        block_pick = 3
    
    if held_keys['4']: 
        highlight.position = (0.16,-0.4,0)
        block_pick = 4

class Voxel(Button):
    def __init__(self, position = (0,0,0), texture = grass_texture):
        super().__init__(
            parent = scene,
            position = position,
            model = 'block.obj',
            origin_y = 0.5,
            texture = texture,
            color = color.white,
            highlight_color = color.white,
            scale = 0.5)

    
    def input(self,key):
        if self.hovered:
            if key == 'right mouse down':
                punch_sound.play()
                if block_pick == 1:
                    voxel = Voxel(position = self.position + mouse.normal, texture = grass_texture)
                if block_pick == 2:
                    voxel = Voxel(position = self.position + mouse.normal, texture = stone_texture)
                if block_pick == 3:
                    voxel = Voxel(position = self.position + mouse.normal, texture = brick_texture)
                if block_pick == 4:
                    voxel = Voxel(position = self.position + mouse.normal, texture = dirt_texture)

            if key == 'left mouse down':
                punch_sound.play()
                destroy(self)

class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = 'sphere',
            texture = 'skybox.png',
            scale = 300,
            double_sided = True)

class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'arm.obj',
            texture = 'arm_texture.png',
            scale = 0.2,
            rotation = Vec3(150, -10, 0),
            position = Vec2(0.8,-0.6))

    def active(self):
        self.position = Vec2(0.3,-0.5)
    
    def passive(self):
        self.position = Vec2(0.8,-0.6)


for x in range(16):
    for z in range(16):
        for y in range(15):
            voxel = Voxel((x,y,z))






sky = Sky()
hand = Hand()

x = -0.2
for i in range(4):
    x += .09
    hotbar = Hotbar((x,-0.4,0))

x = -0.2
for i in range(4):
    if i == 0:
        texture = 'grass.png'
    elif i == 1:
        texture = 'Stone.png'
    elif i == 2:
        texture = 'Brick.png'
    else:
        texture = 'dirt.png'
    x += .09
    item = Item((x,-0.4,0), texture)

highlight = Entity(model = 'quad', color = color.rgba(255,255,255,120), parent = camera.ui, scale = 0.08, position = (-0.11,-0.4,0))

player = FirstPersonController()
player.x = 8
player.z = 8
player.y = 18
if player.y == -10:
    player.y = 10

app.run()

#if __name__ == '__main__':
    #for i in range(20):
        #p = multiprocessing.Process(target=multiprocessing_func, args=(i,))
    #p.start()
    #p.join()
