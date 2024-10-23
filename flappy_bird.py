from ursina import *
import random

app = Ursina()
window.size = (1536, 864)
window.force_anti_aliasing = False 
window.render_shadows = False
application.development_mode = False
Sky()

bird = Animation(
    'assets/flappy-bird', 
    scale=(2, 2, 1),
    collider='box',
    position=(0, 0, 0)
)

camera.orthographic = True
camera.fov = 20

pipes = []
pipe_invoke = None

pipe = Entity(
    model='cube',
    color=color.green,
    texture='white_cube',
    position=(20, 10, 0),
    scale=(3, 15, 1),
    enabled=False,
    collider='box'
)

new_game_text = Text(
    text='Neues Spiel!',
    origin=(0, 0),
    scale=0.1,
    enabled=False
)

paused_text = Text(
    text='Spiel pausiert',
    origin=(0, 0),
    scale=0.1,
    enabled=False
)

game_running = False
game_paused = False  # Neue Variable für den Pausenstatus

def resetGame():
    global game_running, pipe_invoke, game_paused
    game_running = False
    game_paused = False
    bird.position = (0, 0, 0)
    bird.y = 0
    
    for p in pipes:
        destroy(p)
    pipes.clear()
    
    if pipe_invoke is not None:
        pipe_invoke.finish()  
        pipe_invoke = None
    new_game_text.enabled = True
    invoke(startGame, delay=2)

def startGame():
    global game_running
    new_game_text.enabled = False
    game_running = True
    createPipes()

def createPipes():
    if not game_running or game_paused:
        return
    newY = random.randint(4, 12)
    newPipe = duplicate(pipe, y=newY, x=20, enabled=True)
    newPipe2 = duplicate(pipe, y=newY-22, x=20, enabled=True)
    pipes.append(newPipe)
    pipes.append(newPipe2)
    global pipe_invoke
    pipe_invoke = invoke(createPipes, delay=2)

def update():
    if not game_running or game_paused:
        return
    bird.y -= 0.1
    bird.y += held_keys['space'] * 0.2
    
    for pipe in pipes[:]:
        pipe.x -= 0.2
        if bird.intersects(pipe).hit:
            resetGame()
            return
        if pipe.x < -20:
            pipes.remove(pipe)
            destroy(pipe)
    
    if bird.y < -10 or bird.y > 10:
        resetGame()

def input(key):
    global game_paused
    if key == 'space' and not game_paused:
        bird.y += 1
    elif key == 'p':
        game_paused = not game_paused
        if game_paused:
            paused_text.enabled = True
            if pipe_invoke is not None:
                pipe_invoke.pause()
        else:
            paused_text.enabled = False
            if pipe_invoke is not None:
                pipe_invoke.resume()

print("Die App läuft jetzt.")
resetGame()
app.run()
print("Das Programm wurde beendet.")
