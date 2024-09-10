# ai_pong.py
import gym
from gym import spaces
import numpy as np
import pygame
from stable_baselines3 import PPO

# Importer les classes du jeu Pong
from pong import Paddle, Ball, SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE

# Création de l'environnement personnalisé pour l'IA
class PongEnv(gym.Env):
    def __init__(self):
        super(PongEnv, self).__init__()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        # Définition des actions (monter ou descendre)
        self.action_space = spaces.Discrete(3)  # 0: rien, 1: monter, 2: descendre
        self.observation_space = spaces.Box(low=0, high=255, shape=(SCREEN_HEIGHT, SCREEN_WIDTH, 3), dtype=np.uint8)

        self.player = Paddle(10)
        self.opponent = Paddle(SCREEN_WIDTH - 20)
        self.ball = Ball()

        # Système de score
        self.player_score = 0
        self.opponent_score = 0

    def reset(self):
        self.player = Paddle(10)
        self.opponent = Paddle(SCREEN_WIDTH - 20)
        self.ball = Ball()
        self.player_score = 0
        self.opponent_score = 0
        obs = self.get_observation()
        return obs

    def step(self, action):
        # Mouvement du joueur selon l'action
        if action == 1:
            self.player.move(-10)
        elif action == 2:
            self.player.move(10)

        # Mouvement de la balle et de l'adversaire
        self.ball.move()
        if self.ball.rect.centery < self.opponent.rect.centery:
            self.opponent.move(-7)
        else:
            self.opponent.move(7)

        # Vérification des collisions et scores
        reward = 0
        if self.player.rect.colliderect(self.ball.rect):
            self.ball.speed_x *= -1
            reward = 8  # Récompense positive pour toucher la balle
        if self.opponent.rect.colliderect(self.ball.rect):
            self.ball.speed_x *= -1

        # Mise à jour du score
        if self.ball.rect.left <= 0:
            self.opponent_score += 1
            self.ball.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.ball.speed_x = -self.ball.speed_x
            reward = -10  # Pénalité pour manquer la balle
        elif self.ball.rect.right >= SCREEN_WIDTH:
            self.player_score += 1
            self.ball.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.ball.speed_x = -self.ball.speed_x
            reward = 10  # Récompense pour marquer un point

        # Vérification de fin de partie
        done = False
        if self.opponent_score >= 10 or self.player_score >= 10:
            done = True

        obs = self.get_observation()
        return obs, reward, done, {}

    def get_observation(self):
        # Capture l'état actuel de l'écran comme observation
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, WHITE, self.player.rect)
        pygame.draw.rect(self.screen, WHITE, self.opponent.rect)
        pygame.draw.ellipse(self.screen, WHITE, self.ball.rect)
        pygame.draw.aaline(self.screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

        pygame.display.flip()
        self.clock.tick(60)

        obs = np.array(pygame.surfarray.array3d(pygame.display.get_surface()))
        return np.flip(np.rot90(obs, 3), axis=0)

    def render(self, mode='human'):
        pass

    def close(self):
        pygame.quit()

# Entraînement de l'IA
env = PongEnv()
model = PPO('CnnPolicy', env, verbose=1)
model.learn(total_timesteps=5000)  # Ajuste le nombre de timesteps pour un meilleur apprentissage

# Teste l'IA
obs = env.reset()
while True:
    action, _ = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    env.render()
    if done:
        obs = env.reset()