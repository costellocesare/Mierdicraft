from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
#se definen las texturas las provee el tutor#
grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture  = load_texture('assets/dirt_block.png')
sky_texture   = load_texture('assets/skybox.png')
arm_texture   = load_texture('assets/arm_texture.png')
punch_sound   = Audio('assets/punch_sound',loop = False, autoplay = False)
block_pick = 1

window.fps_counter.enabled = False
window.exit_button.visible = False

#se define el block picker con los numeros del 1 al 4

def update():
	global block_pick

	if held_keys['left mouse'] or held_keys['right mouse']:
		hand.active()
	else:
		hand.passive()

	if held_keys['1']: block_pick = 1
	if held_keys['2']: block_pick = 2
	if held_keys['3']: block_pick = 3
	if held_keys['4']: block_pick = 4

#se crean los Voxel tipo botones para generar los bloques dandoles la textura posicion y tamaño que deseamos#
class Voxel(Button):
	def __init__(self, position = (0,0,0), texture = grass_texture):
		super().__init__(
			parent = scene,
			position = position,
			model = 'assets/block',
			origin_y = 0.5,
			texture = texture,
			color = color.color(0,0,random.uniform(0.9,1)),
			scale = 0.5)

#definimos los imputs del mouse y teclado y las respuestas sonoras y cambios de textura segun teclado
	def input(self,key):
		if self.hovered:
			if key == 'left mouse down':
				punch_sound.play()
				if block_pick == 1: voxel = Voxel(position = self.position + mouse.normal, texture = grass_texture)
				if block_pick == 2: voxel = Voxel(position = self.position + mouse.normal, texture = stone_texture)
				if block_pick == 3: voxel = Voxel(position = self.position + mouse.normal, texture = brick_texture)
				if block_pick == 4: voxel = Voxel(position = self.position + mouse.normal, texture = dirt_texture)

#se define que si presionamos boton derecho destruimos el button señalado
			if key == 'right mouse down':
				punch_sound.play()
				destroy(self)


#agregamos el cielo
class Sky(Entity):
	def __init__(self):
		super().__init__(
			parent = scene,
			model = 'sphere',
			texture = sky_texture,
			scale = 150,
			double_sided = True)

#agregamos la entidad Hand para que funcione como la mano del jugador y diciendole parent camera la mantenemos al frente de la camara
class Hand(Entity):
	def __init__(self):
		super().__init__(
			parent = camera.ui,
			model = 'assets/arm',
			texture = arm_texture,
			scale = 0.2,
			rotation = Vec3(150,-10,0),
			position = Vec2(0.4,-0.6))

#declaramos las posiciones para simular el movimiento al hacer click
	def active(self):
		self.position = Vec2(0.3,-0.5)

	def passive(self):
		self.position = Vec2(0.4,-0.6)

#con esto modificamos el tamaño del mapa relacionado a cuantos voxels habra en cada coordenada
for z in range(20):
	for x in range(20):
		voxel = Voxel(position = (x,0,z))

#le decimos al motor que es cada variable
player = FirstPersonController()
sky = Sky()
hand = Hand()


#corremos el juego
app.run()