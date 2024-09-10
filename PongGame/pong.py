# pong.py
import pygame
import random

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
BALL_SIZE = 20
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fenêtre de jeu
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# Classe pour la raquette (joueur ou bot)
class Paddle:
    def __init__(self, x):
        self.rect = pygame.Rect(x, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 10

    def move(self, y):
        self.rect.y += y
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Classe pour la balle
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
        self.speed_x = random.choice((5, -5))
        self.speed_y = random.choice((5, -5))

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Collision avec le haut et le bas
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y *= -1

        # Réinitialise la balle si elle sort à gauche ou à droite
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.speed_x *= -1

# Fonction principale
def main():
    clock = pygame.time.Clock()
    player = Paddle(10)
    opponent = Paddle(SCREEN_WIDTH - 20)
    ball = Ball()

    player_score = 0
    opponent_score = 0
    font = pygame.font.SysFont(None, 55)

    def draw_score():
        player_text = font.render(f"{player_score}", True, WHITE)
        opponent_text = font.render(f"{opponent_score}", True, WHITE)
        screen.blit(player_text, (SCREEN_WIDTH // 4, 20))
        screen.blit(opponent_text, (3 * SCREEN_WIDTH // 4, 20))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Commandes du joueur
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.move(-10)
        if keys[pygame.K_s]:
            player.move(10)

        # Mouvement du bot (difficulté moyenne)
        if ball.rect.centery < opponent.rect.centery:
            opponent.move(-7)
        else:
            opponent.move(7)

        # Mouvement de la balle
        ball.move()

        # Collisions
        if player.rect.colliderect(ball.rect):
            ball.speed_x *= -1
        if opponent.rect.colliderect(ball.rect):
            ball.speed_x *= -1

        # Mise à jour du score
        if ball.rect.left <= 0:
            opponent_score += 1
            ball.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            ball.speed_x = -ball.speed_x
        elif ball.rect.right >= SCREEN_WIDTH:
            player_score += 1
            ball.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            ball.speed_x = -ball.speed_x

        # Dessine le terrain
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, player.rect)
        pygame.draw.rect(screen, WHITE, opponent.rect)
        pygame.draw.ellipse(screen, WHITE, ball.rect)
        pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))
        draw_score()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()