import pygame, sys, random, pickle
# Hàm
def draw_floor():
  screen.blit(floor,(floor_x_pos,650))
  screen.blit(floor,(floor_x_pos+432,650))
def create_pipe():
  random_pipe_pos = random.choice(pipe_height)
  bottom_pipe = pipe_surface.get_rect(midtop=(500,random_pipe_pos))
  top_pipe = pipe_surface.get_rect(midtop=(500,random_pipe_pos - 750))
  return bottom_pipe, top_pipe
def move_pipe(pipes):
  for pipe in pipes:
    pipe.centerx -=4
  return pipes
def draw_pipe(pipes):
  for pipe in pipes:
    if pipe.bottom >= 600:
      screen.blit(pipe_surface, pipe)
    else:
      flip_pipe = pygame.transform.flip(pipe_surface, False, True)
      screen.blit(flip_pipe, pipe)
def check_collision(pipes):
  for pipe in pipes:
    if bird_rect.colliderect(pipe):
      hit_sound.play()
      return False
  if bird_rect.bottom <= -75 or bird_rect.bottom >= 650:
    hit_sound.play()
    return False
  return True
def rotate_bird(bird):
  new_bird = pygame.transform.rotozoom(bird, -bird_movement*3,1)
  return new_bird
def bird_animation():
  new_bird = bird_list[bird_index]
  new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
  return new_bird, new_bird_rect 
def score_display(game_state):
  if game_state == 'main game':
    score_surface = game_font.render(str(int(score)),True, (255, 255, 255))
    score_rect = score_surface.get_rect(center = (216, 100))
    screen.blit(score_surface, score_rect)
  if game_state == 'game over':
    score_surface = game_font.render(f'Score: {int(score)}',True, (255, 255, 255))
    score_rect = score_surface.get_rect(center = (216, 100))
    screen.blit(score_surface, score_rect)
    high_score_surface = game_font.render(f'High Score: {int(high_score)}',True, (255, 255, 255))
    high_score_rect = high_score_surface.get_rect(center = (216, 620))
    screen.blit(high_score_surface, high_score_rect)
def update_score(score, high_score):
  if score > high_score:
    high_score = score
    with open('highscore.dat', 'wb') as file:
      pickle.dump(high_score, file)
  return high_score
def incscore(pipes, score):
  for pipe in pipes:
    if pipe.top < 0 and pipe.right > 64:
      if pipe.right  < bird_rect.left: 
        point_sound.play()
        score+=1
  return score
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
# Path maker pyinstaller
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
	print('running in a PyInstaller bundle')
	path = sys._MEIPASS + '/'
else:
	print('running in a normal Python process')
	path = ''

screen = pygame.display.set_mode((432,768))
pygame.display.set_caption('Flappy Bird')
Icon = pygame.image.load(path + 'assets/yellowbird-upflap.png')
pygame.display.set_icon(Icon)
clock = pygame.time.Clock()
game_font = pygame.font.Font(path + 'assets/font/04B_19.ttf',35)

# Biến
sound_check = 0
pipe_height = [300, 350, 400, 450,  500]
gravity = 0.25
bird_movement = 0
game_active = True
game_start = True
score = 0
high_score = 0

try:
  with open('highscore.dat', 'rb') as file:
    high_score = pickle.load(file)
except:
  high_score = 0

bg = pygame.image.load(path + "assets/background-night.png").convert()
bg = pygame.transform.scale2x(bg)

floor = pygame.image.load(path + "assets/floor.png").convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

bird_down = pygame.transform.scale2x(pygame.image.load(path + 'assets/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load(path + 'assets/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load(path + 'assets/yellowbird-upflap.png').convert_alpha())
bird_list= [bird_down,bird_mid,bird_up]
bird_index = 0
bird = bird_list[bird_index]
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 200)
bird_rect = bird.get_rect(center = (100,384))

pipe_surface = pygame.image.load(path + "assets/pipe-green.png").convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)

game_over_surface = pygame.transform.scale2x(pygame.image.load(path + 'assets/gameover.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = ( 216, 384))

game_start_surface = pygame.transform.scale2x(pygame.image.load(path + 'assets/message.png').convert_alpha())
game_start_rect = game_start_surface.get_rect(center = ( 216, 384))
# Sound
flap_sound = pygame.mixer.Sound(path + 'sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound(path + 'sound/sfx_hit.wav')
point_sound = pygame.mixer.Sound(path + 'sound/sfx_point.wav')
running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE and game_start == True:
        game_start = False
        pipe_list.clear()
      if event.key == pygame.K_SPACE:
        bird_movement = 0
        bird_movement = -7
        flap_sound.play()
      if event.key == pygame.K_SPACE and game_active == False:
        score = 0
        game_active = True
        pipe_list.clear()
        bird_rect.center = (100, 384)
        sound_check = 0
    if event.type == spawnpipe:
      pipe_list.extend(create_pipe())
    if event.type == birdflap:
      if bird_index < 2:
        bird_index += 1
      else:
        bird_index = 0 
      bird, bird_rect = bird_animation()
  screen.blit(bg,(0,0))
  if game_start:
    screen.blit(game_start_surface, game_start_rect)
  else:
    if game_active:
      bird_movement += gravity
      rotated_bird = rotate_bird(bird)
      bird_rect.centery += bird_movement
      game_active = check_collision(pipe_list)
      screen.blit(rotated_bird,bird_rect)
      pipe_list = move_pipe(pipe_list)
      draw_pipe(pipe_list)
      score = incscore(pipe_list, score)
      for pipe in pipe_list:
        if pipe.right<0:
          del pipe_list[0]
      score_display('main game')
    else:
      screen.blit(game_over_surface, game_over_rect)
      high_score = update_score(score, high_score)
      score_display('game over')
  floor_x_pos -=1
  draw_floor()
  if floor_x_pos <= -432:
    floor_x_pos = 0
  pygame.display.update()
  clock.tick(120)