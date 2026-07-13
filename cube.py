import pygame as pg

from OpenGL.GL import (
	GL_COLOR_BUFFER_BIT,
	GL_DEPTH_BUFFER_BIT,
	GL_DEPTH_TEST,
	GL_DOUBLEBUFFER,
	GL_LINES,
	GL_LESS,
	GL_MODELVIEW,
	GL_POLYGON_OFFSET_FILL,
	GL_PROJECTION,
	GL_QUADS,
	glBegin,
	glClear,
	glClearColor,
	glColor3f,
	glDepthFunc,
	glDisable,
	glEnable,
	glEnd,
	glLineWidth,
	glLoadIdentity,
	glMatrixMode,
	glPolygonOffset,
	glRotatef,
	glTranslatef,
	glVertex3f,
	glViewport,
	GL_LINEAR,
	GL_RGBA,
	GL_TEXTURE_2D,
	GL_TEXTURE_MAG_FILTER,
	GL_TEXTURE_MIN_FILTER,
	GL_UNSIGNED_BYTE,
	glBindTexture,
	glGenTextures,
	glTexCoord2f,
	glTexImage2D,
	glTexParameteri,
)
from OpenGL.GLU import gluPerspective


WIDTH = 960
HEIGHT = 540
FPS = 60


VERTICES = (
	(-1.0, -1.0, -1.0),  # 0
	(1.0, -1.0, -1.0),   # 1
	(1.0, 1.0, -1.0),    # 2
	(-1.0, 1.0, -1.0),   # 3
	(-1.0, -1.0, 1.0),   # 4
	(1.0, -1.0, 1.0),    # 5
	(1.0, 1.0, 1.0),     # 6
	(-1.0, 1.0, 1.0),    # 7
)


EDGES = (
	(0, 1),
	(1, 2),
	(2, 3),
	(3, 0),

	(4, 5),
	(5, 6),
	(6, 7),
	(7, 4),

	(0, 4),
	(1, 5),
	(2, 6),
	(3, 7),
)


FACES = (
	(4, 5, 6, 7),  # Etutahko
	(1, 0, 3, 2),  # Takatakho
	(0, 4, 7, 3),  # Vasen tahko
	(5, 1, 2, 6),  # Oikea tahko
	(3, 7, 6, 2),  # Ylätahko
	(0, 1, 5, 4),  # Alataho
)


FACE_COLORS = (
	(0.85, 0.15, 0.20),  # Punainen
	(0.15, 0.75, 0.25),  # Vihreä
	(0.15, 0.35, 0.90),  # Sininen
	(0.90, 0.75, 0.15),  # Keltainen
	(0.70, 0.20, 0.85),  # Violetti
	(0.15, 0.80, 0.85),  # Syaani
)

TEXTURE_COORDS = (
	(0.0, 0.0),  # Vasen alakulma
	(1.0, 0.0),  # Oikea alakulma
	(1.0, 1.0),  # Oikea yläkulma
	(0.0, 1.0),  # Vasen yläkulma
)

def create_window():
	pg.init()

	pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, 24)
	pg.display.set_caption("OpenGL Cube")

	return pg.display.set_mode(
		(WIDTH, HEIGHT),
		pg.OPENGL | pg.DOUBLEBUF,
	)


def initialize_opengl():
	glViewport(0, 0, WIDTH, HEIGHT)

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()

	gluPerspective(
		60.0,
		WIDTH / HEIGHT,
		0.1,
		100.0,
	)

	glMatrixMode(GL_MODELVIEW)

	glEnable(GL_DEPTH_TEST)
	glDepthFunc(GL_LESS)

	glClearColor(0.03, 0.03, 0.05, 1.0)

def load_texture(filename):
	image = pg.image.load(filename).convert_alpha()

	width, height = image.get_size()

	# True kääntää kuvan pystysuunnassa, koska pygame ja OpenGL
	# käyttävät eri kohtaa kuvan koordinaatiston alkupisteenä.
	image_data = pg.image.tostring(image, "RGBA", True)

	texture_id = glGenTextures(1)

	glBindTexture(GL_TEXTURE_2D, texture_id)

	glTexParameteri(
		GL_TEXTURE_2D,
		GL_TEXTURE_MIN_FILTER,
		GL_LINEAR,
	)

	glTexParameteri(
		GL_TEXTURE_2D,
		GL_TEXTURE_MAG_FILTER,
		GL_LINEAR,
	)

	glTexImage2D(
		GL_TEXTURE_2D,
		0,
		GL_RGBA,
		width,
		height,
		0,
		GL_RGBA,
		GL_UNSIGNED_BYTE,
		image_data,
	)

	glBindTexture(GL_TEXTURE_2D, 0)

	return texture_id

def draw_faces(texture_id):
	glEnable(GL_POLYGON_OFFSET_FILL)
	glPolygonOffset(1.0, 1.0)

	glEnable(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D, texture_id)

	# Valkoinen säilyttää tekstuurin alkuperäiset värit.
	# Muut värit värjäisivät tekstuurin.
	glColor3f(1.0, 1.0, 1.0)

	glBegin(GL_QUADS)

	for face in FACES:
		for vertex_index, texture_coord in zip(
			face,
			TEXTURE_COORDS,
		):
			glTexCoord2f(*texture_coord)
			glVertex3f(*VERTICES[vertex_index])

	glEnd()

	glBindTexture(GL_TEXTURE_2D, 0)
	glDisable(GL_TEXTURE_2D)

	glDisable(GL_POLYGON_OFFSET_FILL)


def draw_edges():
	glColor3f(1.0, 1.0, 1.0)
	glLineWidth(2.0)

	glBegin(GL_LINES)

	for start_index, end_index in EDGES:
		glVertex3f(*VERTICES[start_index])
		glVertex3f(*VERTICES[end_index])

	glEnd()


def draw_cube(texture_id):
	draw_faces(texture_id)
	draw_edges()


def main():
	create_window()
	initialize_opengl()

	texture_id = load_texture("face.png")

	clock = pg.time.Clock()

	angle_x = 0.0
	angle_y = 0.0

	running = True

	while running:
		dt = clock.tick(FPS) / 1000.0

		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False

			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					running = False

		angle_x += 25.0 * dt
		angle_y += 40.0 * dt

		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		glLoadIdentity()
		glTranslatef(0.0, 0.0, -5.0)

		glRotatef(angle_x, 1.0, 0.0, 0.0)
		glRotatef(angle_y, 0.0, 1.0, 0.0)

		draw_cube(texture_id)

		pg.display.flip()

	pg.quit()


if __name__ == "__main__":
	main()