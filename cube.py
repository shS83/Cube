import pygame as pg

from OpenGL.GL import (
	GL_COLOR_BUFFER_BIT,
	GL_DEPTH_BUFFER_BIT,
	GL_DEPTH_TEST,
	GL_LINES,
	GL_MODELVIEW,
	GL_PROJECTION,
	glBegin,
	glClear,
	glRotatef,
	glClearColor,
	glColor3f,
	glEnable,
	glEnd,
	glLineWidth,
	glLoadIdentity,
	glMatrixMode,
	glTranslatef,
	glVertex3f,
	glViewport,
)
from OpenGL.GLU import gluPerspective

WIDTH = 960
HEIGHT = 540
FPS = 60

VERTICES = (
    (-1.0, -1.0, -1.0),  # 0
    (1.0, -1.0, -1.0),  # 1
    (1.0, 1.0, -1.0),  # 2
    (-1.0, 1.0, -1.0),  # 3

    (-1.0, -1.0, 1.0),  # 4
    (1.0, -1.0, 1.0),  # 5
    (1.0, 1.0, 1.0),  # 6
    (-1.0, 1.0, 1.0),  # 7
)

EDGES = (
    # Ensimmäinen neliö
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),

    # Toinen neliö
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),

    # Neliöt toisiinsa yhdistävät reunat
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7),
)

def create_window() -> None:
	"""Luo Pygame-ikkunan ja OpenGL-kontekstin."""


	pg.init()
	pg.display.gl_set_attribute(
		pg.GL_CONTEXT_MAJOR_VERSION,
		2,
	)
	pg.display.gl_set_attribute(
		pg.GL_CONTEXT_MINOR_VERSION,
		1,
	)

	# Syvyyspuskuri tarvitaan myöhemmin, kun kuutiolla on täytetyt tahkot.
	pg.display.gl_set_attribute(
		pg.GL_DEPTH_SIZE,
		24,
	)

	flags = pg.OPENGL | pg.DOUBLEBUF

	pg.display.set_mode(
		(WIDTH, HEIGHT),
		flags,
	)

	pg.display.set_caption(
		"Cube — vaihe 1: verteksit ja reunat"
	)

def initialize_opengl() -> None:
	"""Asettaa viewportin, perspektiivin ja OpenGL:n perustilan."""

	# Viewport kertoo OpenGL:lle, mille ikkunan alueelle kuva piirretään.
	glViewport(
		0,
		0,
		WIDTH,
		HEIGHT,
	)

	# Valitaan projektiomatriisi.
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()

	# Perspektiiviprojektio:
	#
	# 60.0          = pystysuuntainen näkökenttä asteina
	# WIDTH/HEIGHT  = kuvasuhde
	# 0.1           = lähin piirrettävä etäisyys
	# 100.0         = kaukaisin piirrettävä etäisyys
	gluPerspective(
		60.0,
		WIDTH / HEIGHT,
		0.1,
		100.0,
	)

	# Palataan model-view-matriisiin. Tähän tulevat myöhemmin
	# kameran ja kappaleiden siirrot sekä pyöritykset.
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

	# Syvyystesti vertaa pikselien etäisyyksiä kameraan.
	glEnable(GL_DEPTH_TEST)

	# Taustaväri: hyvin tumma siniharmaa.
	glClearColor(
		0.02,
		0.025,
		0.04,
		1.0,
	)

	glLineWidth(2.0)


def draw_cube() -> None:
	"""Piirtää kuution 12 reunaa."""

	# Valkoinen, hieman sinertävä viivaväri.
	glColor3f(
		0.75,
		0.85,
		1.0,
	)

	# GL_LINES tulkitsee jokaisen kahden vertexin parin
	# erilliseksi viivaksi.
	glBegin(GL_LINES)

	for start_index, end_index in EDGES:
		start_vertex = VERTICES[start_index]
		end_vertex = VERTICES[end_index]

		glVertex3f(*start_vertex)
		glVertex3f(*end_vertex)

	glEnd()

def main() -> int:
	create_window()
	initialize_opengl()

	clock = pg.time.Clock()
	running = True

	angle_x = 0.0
	angle_y = 0.0

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

		angle_x %= 360.0
		angle_y %= 360.0

		# Pyyhitään edellinen kuva ja vanhat syvyysarvot.
		glClear(
			GL_COLOR_BUFFER_BIT
			| GL_DEPTH_BUFFER_BIT
		)

		# Aloitetaan model-view-matriisi puhtaasta tilasta.
		glLoadIdentity()

		# Kuution keskipiste on (0, 0, 0).
		#
		# Siirrämme sitä viisi yksikköä negatiiviseen Z-suuntaan,
		# jotta se on kameran edessä eikä kameran sisällä.
		glTranslatef(
			0.0,
			0.0,
			-5.0,
		)
		# Pyöritetään kuutiota sen oman origon ympäri.
		glRotatef(
			angle_x,
			1.0,
			0.0,
			0.0,
		)

		glRotatef(
			angle_y,
			0.0,
			1.0,
			0.0,
		)
		draw_cube()

		# OPENGL + DOUBLEBUF -ikkunassa flip vaihtaa valmiin
		# takapuskurin näytettäväksi etupuskuriksi.
		pg.display.flip()

	pg.quit()
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
