# Import du module pygame
import pygame

# Import du module aléatoire
import random

# Initialisation de la fonction pour la musique
pygame.mixer.init()
       
# Initialisation de pygame
pygame.init()

# Import pygame.locals pour les touches
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_SPACE,
)

# Vitesse des ennemis
enemy_timer = 1000

# Definition de la classe Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("C:/Users/coco/Desktop/Jeu_python/vaisseau1.png")
        self.rect = self.surf.get_rect()
        self.rect.y = 268

    # Definition des mouvements du joueur
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

    # Faire en sorte que le joueur reste sur l'ecran
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Definition de la classe Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("C:/Users/coco/Desktop/Jeu_python/meteor16px.png")
        # La position de départ est generee de maniere aleatoire ainsi que la vitesse
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(1, 3)

    # Definition du mouvement des ennemis
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Definition de la classe Cloud (pour le fond d'ecran)
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("C:/Users/coco/Desktop/Jeu_python/galaxie64px.png").convert()
        # Rend le fond de mon "rec" transparent
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # Met mon rec aux dimensions souhaitées
        self.surf = pygame.transform.scale(self.surf, (128, 128))
        # Met mon rec en transparence
        self.surf.set_alpha(20)
        # Definition de la position aléatoire de base
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # Mouvement des "nuages"
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


# Creation de la classe Projectile
class Projectile(pygame.sprite.Sprite):
    def __init__(self):
        super(Projectile, self).__init__()
        self.surf = pygame.image.load("C:/Users/coco/Desktop/Jeu_python/diamond.png").convert()
        self.rect = self.surf.get_rect()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.velocity = 10
        # Definition de la position aléatoire de base
        self.rect = self.surf.get_rect(
            center=(player.rect.x+32, player.rect.y+16)
        )

    # Mouvement des "projectile"
    def update(self):
        self.rect.move_ip(self.velocity, 0)
        if self.rect.right > SCREEN_WIDTH:
            self.kill()

# Definition de la taille de l'ecran
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Titre du jeu
pygame.display.set_caption("Les Maitres de l'espace")

# Creation de l'objet "ecran" avec ses dimensions
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Import de l'image pour le fond d'ecran et son redimentionnement
background = pygame.image.load ("C:/Users/coco/Desktop/Jeu_python/background.jpg")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Import de l'image game over et son redimentionnement
end_screen = pygame.image.load("C:/Users/coco/Desktop/Jeu_python/52107.png").convert()
end_screen = pygame.transform.scale(end_screen, (400, 300))

# Import de l'image de vainqueur et son redimentionnement
win_screen = pygame.image.load("C:/Users/coco/Desktop/Jeu_python/youwin.png").convert()
win_screen = pygame.transform.scale(win_screen, (400, 300))

# Import de l'image smiley 
smiley_screen = pygame.image.load("C:/Users/coco/Desktop/Jeu_python/smiley.png")

# Charge et joue une musique de fond
pygame.mixer.music.load("C:/Users/coco/Desktop/Jeu_python/iam.mp3")
pygame.mixer.music.play(loops=-1)

# Charge les sons du jeu
collision_sound = pygame.mixer.Sound("C:/Users/coco/Desktop/Jeu_python/explosion.wav")
laser_sound = pygame.mixer.Sound("C:/Users/coco/Desktop/Jeu_python/laser.wav")
fin_sound = pygame.mixer.Sound("C:/Users/coco/Desktop/Jeu_python/fin.wav")
victory = pygame.mixer.Sound("C:/Users/coco/Desktop/Jeu_python/victory.wav")
victory2 = pygame.mixer.Sound("C:/Users/coco/Desktop/Jeu_python/victory2.wav")
rire = pygame.mixer.Sound("C:/Users/coco/Desktop/Jeu_python/rire.wav")


# Configuration de l'horloge pour un débit d'images décent
clock = pygame.time.Clock()

# Creation d'un evenement pour l'ajout des enemies et des nuages
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 400)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Variable joueur à partir de la classe Player
player = Player()

# Variables concernant le score et son affichage
score = 0 
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

# Creation de groupes de sprites
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


# Definition d'une variable de jeu
running = True

# Depart de la boucle de jeu
while running:
    # Départ de la liste des evenements
    for event in pygame.event.get():
        # Pour les evenements concernant les touches
        if event.type == KEYDOWN:
            # Si on appuie sur la touche echap, on sort du jeu
            if event.key == K_ESCAPE:
                running = False
            # Si on appuie sur la touche espace, on lance un projectile et on joue la musique adequate
            if event.key == K_SPACE:
                projectile = Projectile()
                projectiles.add(projectile)
                all_sprites.add(projectile)
                laser_sound.play()

        # Si on appuie sur quitter, on quitte le jeu
        elif event.type == QUIT:
            running = False

        # Ajout d'un nouvel ennemi
        elif event.type == ADDENEMY:
            # Cree un nouvel ennemi et l'ajoute au groupe de sprites
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

         # Ajout d'un nouveau nuage
        elif event.type == ADDCLOUD:
            # Cree un nouveau nuage et l'ajoute au groupe de sprites
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)    

    if score >= 20:
        for enemy in enemies:
            projectile.surf = pygame.image.load("C:/Users/coco/Desktop/Jeu_python/diamond.png")
            new_enemy.surf = pygame.image.load("C:/Users/coco/Desktop/Jeu_python/meteor2.png")
            new_enemy.surf.set_colorkey((0, 0, 0))
            new_enemy.speed = random.randint(3, 5)

    if score >= 40:
        for enemy in enemies:
            projectile.surf = pygame.image.load("C:/Users/coco/Desktop/Jeu_python/laser.png")
            new_enemy.surf = pygame.image.load("C:/Users/coco/Desktop/Jeu_python/alien35px.png")
            new_enemy.surf.set_colorkey((0, 0, 0))
            new_enemy.speed = random.randint(5, 7)

    if score >= 60:
        for enemy in enemies:
            projectile.surf = pygame.image.load("C:/Users/coco/Desktop/Jeu_python/laser.png")
            new_enemy.surf = pygame.image.load("C:/Users/coco/Desktop/Jeu_python/alien40px.png")
            new_enemy.surf.set_colorkey((0, 0, 0))
            new_enemy.speed = random.randint(7, 9)

    if score >= 80:
        for enemy in enemies:
            projectile.surf = pygame.image.load("C:/Users/coco/Desktop/Jeu_python/fire_ball.png")
            new_enemy.surf = pygame.image.load("C:/Users/coco/Desktop/Jeu_python/alien.png")
            new_enemy.surf.set_colorkey((0, 0, 0))
            new_enemy.speed = random.randint(9, 10)  
    
    if score == 100:
        pygame.time.delay(1000)
        pygame.mixer.music.stop()
        pygame.time.delay(500)  
        player.kill()
        screen.blit(win_screen, (200, 150))
        victory.play()    
        pygame.time.delay(4000)
        victory2.play()
        pygame.display.flip()
        pygame.time.delay(4000)
        running = False


    # Pour les touches enfoncees
    pressed_keys = pygame.key.get_pressed()

    # Met a jour le joueur et les touches
    player.update(pressed_keys)

    # Met a jour la position des ennemis et des nuages
    enemies.update()
    clouds.update()
    projectiles.update()

    # Affiche l'arriere plan 
    screen.blit(background,(0,0))

    # Affiche le score
    score_surface = myfont.render('Score: '+  str(int(score)), False, (255, 255, 255))
    screen.blit(score_surface,(0,0))

    # Affiche les sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Si un des ennemis rentre en collision avec le joueur
    if pygame.sprite.spritecollideany(player, enemies):
        fin_sound.play()
        player.kill()
        pygame.time.delay(1000)
        pygame.mixer.music.stop()
        pygame.time.delay(2000)
        screen.blit(end_screen, (200, 150))
        pygame.display.flip()
        pygame.time.delay(1000) 
        rire.play()
        screen.blit(smiley_screen, (368, 15))
        pygame.display.flip()
        pygame.time.delay(4000) 
        # Arrete la boucle de jeu
        running = False

    # Si un projectile atteint un ennemi
    for projectile in pygame.sprite.groupcollide(projectiles, enemies, True, True):
        # On ajoute 1 au score
        score += 1
        # on joue la musique collision
        collision_sound.play()
    
    # Met a jour l'affichage
    pygame.display.flip()

    # Taux de 40 images par secondes
    clock.tick(40)

# Arrete les musiques
pygame.mixer.music.stop()
pygame.mixer.quit()