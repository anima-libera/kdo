
from random import randint, random, choice
from math import sqrt, cos, sin, tau
import tkinter as tk

while True:

	window = tk.Tk()
	window.title("Kdo")
	window["bg"] = "#000000"
	canvas = tk.Canvas(window, bg = "#ffffff", heigh = 800, width = 800, cursor = "tcross")
	canvas.grid(row = 1, column = 1)
	running = True
	began = False
	died = False

	def dist(ca, cb):
		return sqrt((ca[0]-cb[0])**2 + (ca[1]-cb[1])**2)

	def edgebouce(obj, vfactor, dielist, j):
		for i in range(2):
			if obj[i] < 0:
				if dielist != None:
					dielist.append(j)
				else:
					obj[i+2] = abs(obj[i+2])
					obj[i] = 0
					obj[i+2] *= vfactor
			elif obj[i] > 800:
				if dielist != None:
					dielist.append(j)
				else:
					obj[i+2] = -abs(obj[i+2])
					obj[i] = 800
					obj[i+2] *= vfactor

	cursorxy = [400, 900]

	ship = [400, 400, 0, 0]
	shipshapes = [
		canvas.create_oval(ship[0]-2, ship[1]-2, ship[0]+2, ship[1]+2, width = 6),
		canvas.create_arc(ship[0]-10, ship[1]-10, ship[0]+10, ship[1]+10,
			style = tk.ARC, width = 5)]
	shiparc = 0
	dist_shipcur = dist(cursorxy, ship)

	score = 0
	defeat = True
	endcause = ""

	shoot_color = "#ff0000"
	super_shoots = 5

	insp_quotes = [
		"L'espoir fait vivre!",
		"Courage!",
		"Bonne chance!",
		"On sait que c'est dur, mais c'est pas une raison d'abandonner!",
		"Encore un effort!",
		"v(^^)> La prochiane fois c'est la bone! <(^^)v",
		"Enocre!",
		"Abandonner, c'est moins bien que ne pas abandonner!",
		"Plus ça rate, plus ya de chances que ça marche!",
		"(^^)!",
		"Conditions de la vicoire: (score >= 250) et (plus d'ennemis).",
		"Penser au clic droit!!!",
		"Lire les messages de morts, y a des infos dedans ^^.",
		"Si on a qu'une vie, c'est pour rendre le jeu plus long, pas plus dur "
			"(même si ça le rend plus dur)...",
		"Les ennemis ont une backstory tellement triste que personne n'oserait "
			"les affronter en connaissance de cause",
		"L'univers est carré et mesure 800 pixel de côté.",
		"Avant de ganger, le fond changera de couleur par deux fois.",
		"Garder les clics droits pour quand c'est noir ptet.",
		"Aller! Encore une!",
		"Bwahaha ki c ki a encor perdu xdddd lool xptdr mdr lel xxdd!",
		"Y a pas moyen de mettre en pause ? Nan. Ok..."
	]

	def die(cause):
		global running, defeat, endcause, died
		defeat = True
		endcause = cause
		running = False
		died = True
		poof_effect(*ship[:2], -1, 200)
		canvas.delete(shipshapes[0])
		canvas.delete(shipshapes[1])
		print()
		print()
		print("Fin de partie: C'est une défaite")
		print("Cause de la défaite: << {} >>".format(endcause))
		print("Score: {}".format(score))
		print(choice(insp_quotes))

	def ship_update():
		global dist_shipcur, shiparc
		dist_shipcur = dist(cursorxy, ship)
		if dist_shipcur < 15:
			die("le vaisseau a touché le curseur")
		for i in range(2):
			ship[i+2] += (cursorxy[i]-ship[i])/(dist_shipcur+1)
		for i in range(2):
			ship[i] += ship[i+2]*0.4
		edgebouce(ship, 0.6, None, 0)
		canvas.coords(shipshapes[0], ship[0]-2, ship[1]-2, ship[0]+2, ship[1]+2)
		canvas.coords(shipshapes[1], ship[0]-10, ship[1]-10, ship[0]+10, ship[1]+10)
		shiparc = shiparc+6000/(dist_shipcur+1)+0.3
		canvas.itemconfigure(shipshapes[1], start = shiparc, extent = 180)

	shots, shots_del = [], []

	def click(event):
		global began, died
		if began and not died:
			shoot_at(event.x, event.y)

	def rightclick(event):
		global began, died, super_shoots
		if began and not died and super_shoots > 0:
			super_shoots -= 1
			x, y = event.x, event.y
			for i in range(30):
				a = random()*tau
				r = random()*40
				shoot_at(x+r*cos(a), y+r*sin(a))

	def shoot_at(x, y):
		global shots
		v = [((x, y)[i]-ship[i])/(0.0004*dist_shipcur**2+1) for i in range(2)]
		shots.append([
			*ship[:2], *v,
			canvas.create_line(*ship[:2], ship[0]+v[0]*3, ship[1]+v[1]*3,
				width = 4, fill = shoot_color),
			20,
		])

	def shots_update():
		for i in range(len(shots)):
			shots[i][5] -= 1
			for j in range(2):
				shots[i][j] += shots[i][j+2]
			canvas.coords(shots[i][4], shots[i][0], shots[i][1],
				shots[i][0]+3*shots[i][2], shots[i][1]+3*shots[i][3])
			edgebouce(shots[i], 0, shots_del, i)
		shots_del.sort()
		for i in range(len(shots_del)):
			if shots_del[::-1][i] < len(shots):
				canvas.delete(shots[shots_del[::-1][i]][4])
				shots.pop(shots_del[::-1][i])
		shots_del.clear()

	def collision_shot_ship_test():
		for i in range(len(shots)):
			if shots[i][5] < 0 and dist(shots[i][:2], ship) < 12:
				die("le vaisseau a touché un de ses propres tirs")

	enemies, enemies_del = [], []

	color_per_type = [
		"#0000ff",
		"#ff00ff",
		"#ffffff",
		"#ffff00",
		"#ffff00",
		"#004444",
		"#ff0000",
	]
	rpt = [
		7,
		7,
		7,
		7,
		5,
		9,
		9,
	]

	def spawn_enemy(x, y, vx, vy, type, *args):
		enemies.append([
			x, y, vx, vy,
			canvas.create_oval(x-rpt[type], y-rpt[type], x+rpt[type], y+rpt[type],
				width = 0, fill = color_per_type[type]),
			type, *args
		])

	def enemies_update():
		for i in range(len(enemies)):
			type = enemies[i][5]
			if type == 4:
				for j in range(2):
					enemies[i][j] += enemies[i][j+2]
					enemies[i][j+2] += random()*0.05
					if abs(enemies[i][j+2]) > 8:
						enemies[i][j+2] *= 0.95
				edgebouce(enemies[i], 1, None, 0)
			elif type == 5:
				d = dist(cursorxy, enemies[i])
				for j in range(2):
					enemies[i][j+2] += (cursorxy[j]-enemies[i][j])/(d+1)
				for j in range(2):
					enemies[i][j] += enemies[i][j+2]*0.4
				edgebouce(enemies[i], 0.6, None, 0)
			elif type == 6:
				d = dist(ship, enemies[i])
				for j in range(2):
					enemies[i][j+2] += (ship[j]-enemies[i][j])/(d+1)
				for j in range(2):
					enemies[i][j] += enemies[i][j+2]*0.4
				edgebouce(enemies[i], 0.6, None, 0)
			else:
				for j in range(2):
					enemies[i][j] += enemies[i][j+2]
				edgebouce(enemies[i], 1, None, 0)
			canvas.coords(enemies[i][4],
				enemies[i][0]-rpt[type], enemies[i][1]-rpt[type],
				enemies[i][0]+rpt[type], enemies[i][1]+rpt[type])
		enemies_del.sort()
		for i in range(len(enemies_del)):
			if enemies_del[::-1][i] < len(enemies):
				if enemies[enemies_del[::-1][i]][5] == 3:
					spawn_spawner(*enemies[enemies_del[::-1][i]][:2], 3)
				canvas.delete(enemies[enemies_del[::-1][i]][4])
				enemies.pop(enemies_del[::-1][i])
		enemies_del.clear()

	def collision_shot_enemy_test():
		global score
		for i in range(len(shots)):
			for j in range(len(enemies)):
				if dist(shots[i][:2], enemies[j][:2]) < 13:
					shots_del.append(i)
					enemies_del.append(j)
					poof_effect(*enemies[j][:2], enemies[j][5], 14)
					score += 1
					break

	def collision_shot_enemy_ship():
		for i in range(len(enemies)):
			if dist(enemies[i][:2], ship) < 17:
				die("le vaisseau a touché un ennemi")

	spawners, spawners_del = [], []

	def spawnerfunctiontype0(x, y):
		angle = random()*tau
		spawn_enemy(x, y, 1*cos(angle), 1*sin(angle), 0)
		spawn_enemy(x, y, 1*cos(angle+tau/3), 1*sin(angle+tau/3), 0)
		spawn_enemy(x, y, 1*cos(angle+2*tau/3), 1*sin(angle+2*tau/3), 0)

	def spawnerfunctiontype1(x, y):
		angle = random()*tau
		spawn_enemy(x, y, 3.5*cos(angle), 3.5*sin(angle), 1)
		spawn_enemy(x, y, 3.5*cos(angle+tau/2), 3.5*sin(angle+tau/2), 1)

	def spawnerfunctiontype2(x, y):
		angle = random()*tau
		for i in range(34):
			a = (i/34)*tau
			v = random()*0.9+0.1
			spawn_enemy(x, y, v*cos(angle+a), v*sin(angle+a), 2+int(i==20))

	def spawnerfunctiontype3(x, y):
		angle = random()*tau
		for i in range(11):
			a = (i/11)*tau
			spawn_enemy(x, y, 5*cos(angle+a), 5*sin(angle+a), 4)

	def spawnerfunctiontype5(x, y):
		angle = random()*tau
		spawn_enemy(x, y, 10*cos(angle), 10*sin(angle), 5)
		spawn_enemy(x, y, 10*cos(angle+tau/3), 10*sin(angle+tau/3), 5)
		spawn_enemy(x, y, 10*cos(angle+2*tau/3), 10*sin(angle+2*tau/3), 5)

	def spawnerfunctiontype6(x, y):
		angle = random()*tau
		spawn_enemy(x, y, 10*cos(angle), 10*sin(angle), 6)
		spawn_enemy(x, y, 10*cos(angle+tau/3), 10*sin(angle+tau/3), 6)
		spawn_enemy(x, y, 10*cos(angle+2*tau/3), 10*sin(angle+2*tau/3), 6)

	spawnfunction_per_type = [
		spawnerfunctiontype0,
		spawnerfunctiontype1,
		spawnerfunctiontype2,
		spawnerfunctiontype3,
		None,
		spawnerfunctiontype5,
		spawnerfunctiontype6,
	]

	def spawn_spawner(x, y, type):
		spawners.append([x, y, type, 150,
			canvas.create_arc(x-10, y-10, x+10, y+10,
				style = tk.ARC, width = 10, outline = color_per_type[type])
		])

	def spawners_update():
		for i in range(len(spawners)):
			spawners[i][3] -= 1
			canvas.itemconfigure(spawners[i][4],
				start = (100/(spawners[i][3]+2))*(160-spawners[i][3]),
				extent = 180)
			if spawners[i][3] < 0:
				spawnfunction_per_type[spawners[i][2]](spawners[i][0], spawners[i][1])
				spawners_del.append(i)
		spawners_del.sort()
		for i in range(len(spawners_del)):
			if spawners_del[::-1][i] < len(spawners):
				canvas.delete(spawners[spawners_del[::-1][i]][4])
				spawners.pop(spawners_del[::-1][i])
		spawners_del.clear()

	phase = 0

	def phasefunction0():
		global phase
		if len(enemies) < 6 and len(spawners) == 0 and randint(1, 150) == 1:
			spawn_spawner(randint(0, 800), randint(0, 800), 0)
		if score > 13:
			for i in range(6):
				spawn_spawner(randint(0, 800), randint(0, 800), 1)
			phase = 1

	def phasefunction1():
		global phase
		if len(enemies) < 5:
			phase = 2

	def phasefunction2():
		global phase
		if len(enemies) < 15 and len(spawners) < 2:
			spawn_spawner(randint(0, 800), randint(0, 800), choice((0, 1, 1)))
		if score > 60:
			phase = 3

	def phasefunction3():
		global phase, shoot_color
		if len(enemies) == 0:
			phase = 4
			shoot_color = "#ffffff"
			canvas.itemconfigure(shipshapes[0], outline = "#ffffff")
			canvas.itemconfigure(shipshapes[1], outline = "#ffffff")
			canvas["bg"] = "#000000"
			for i in range(3):
				spawn_spawner(randint(0, 800), randint(0, 800), 2)

	def phasefunction4():
		global phase, shoot_color
		if len(spawners) == 0 and len(enemies) == 0:
			phase = 5
			shoot_color = "#ff0000"
			canvas.itemconfigure(shipshapes[0], outline = "#000000")
			canvas.itemconfigure(shipshapes[1], outline = "#000000")
			canvas["bg"] = "#ffff00"

	vicory_bangs = 7

	def phasefunction5():
		global phase, running, defeat, vicory_bangs
		if score >= 250:
			if len(spawners) == 0 and len(enemies) == 0:
				defeat = False
				if vicory_bangs > 0:
					if randint(1, 20) == 1:
						vicory_bangs -= 1
						poof_effect(randint(0, 800), randint(0, 800), -1, 50)
				else:
					defeat = False
					running = False
		if len(spawners) == 0 and len(enemies) < 5 and randint(1, 50) == 1:
			spawn_spawner(randint(0, 800), randint(0, 800), choice((0, 1, 5, 6)))

	phasefunctions = [
		phasefunction0,
		phasefunction1,
		phasefunction2,
		phasefunction3,
		phasefunction4,
		phasefunction5,
	]

	particles, particles_del = [], []

	def spawn_particle(x, y, vx, vy, time, type):
		color = (color_per_type[type] if type != -1 else "#ff0000")
		particles.append([
			x, y, vx, vy,
			canvas.create_oval(x-3, y-3, x+3, y+3, width = 0, fill = color),
			time, type
		])

	def poof_effect(x, y, type, magnitude):
		for i in range(magnitude + randint(0, 10)):
			v = 8*random()+0.3
			a = random()*tau
			spawn_particle(x, y, v*cos(a), v*sin(a), randint(30, 100), type)

	def particles_update():
		for i in range(len(particles)):
			particles[i][5] -= 1
			if particles[i][5] < 0:
				particles_del.append(i)
			for j in range(2):
				particles[i][j] += particles[i][j+2]
			if particles[i][6] == -1:
				canvas.itemconfigure(particles[i][4], fill = choice(("#ff0000", "#0000ff")))
			r = int((particles[i][5]+5)/20)+1
			canvas.coords(particles[i][4],
				particles[i][0]-r, particles[i][1]-r, particles[i][0]+r, particles[i][1]+r)
		particles_del.sort()
		for i in range(len(particles_del)):
			if particles_del[::-1][i] < len(particles):
				canvas.delete(particles[particles_del[::-1][i]][4])
				particles.pop(particles_del[::-1][i])
		particles_del.clear()

	def loop():
		global running, died
		if running:
			ship_update()
		shots_update()
		enemies_update()
		spawners_update()
		if running:
			collision_shot_ship_test()
		collision_shot_enemy_test()
		if running:
			collision_shot_enemy_ship()
		particles_update()
		phasefunctions[phase]()
		if running or len(particles) > 0:
			window.after(20, loop)
		else:
			died = False
			window.destroy()

	def cursorxy_update(event):
		global cursorxy, began
		cursorxy[0], cursorxy[1] = event.x, event.y
		began = True

	canvas.bind('<Motion>', cursorxy_update)
	canvas.bind('<Button-1>', click)
	canvas.bind('<Button-3>', rightclick)
	window.after(20, loop)
	window.mainloop()

	if not defeat:
		print("Fin de partie: C'est un succès !!!")
		print("Bien joué !! ")
		print("Score: {}".format(score))
		break

	if running or died:
		print()
		print()
		print("A bientôt !")
		break
