import pygame


class Mine(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        sheet = pygame.image.load("sprites/Mines.png")
        self.sprites = []
        for row in range(3):
            self.sprites.append(sheet.subsurface((row * 30, 0), (30, 30)))
        explosion_sheet = pygame.image.load("sprites/explosion.png")
        self.explosion_sprites = []
        for col in range(2):
            for row in range(4):
                self.explosion_sprites.append(explosion_sheet.subsurface((row * 200, col * 200), (200, 200)))

        self.image = self.sprites[0]
        self.rect = self.image.get_rect(center=pos)
        self.life_timer = 0
        self.exploded = False

    def collisions(self, players, walls):
        for sprite in players:
            dis = ((self.rect.centerx - sprite.rect.centerx)**2 + (self.rect.centery - sprite.rect.centery)**2)**.5
            if dis < 40:
                self.explode(players, walls)
            for bullet in sprite.bullets.sprites():
                diss = ((self.rect.centerx - bullet.rect.centerx)**2 + (self.rect.centery - bullet.rect.centery)**2)**.5
                if diss < 15:
                    self.explode(players, walls)
                    bullet.kill()

    def explode(self, players, walls):
        self.exploded = True
        pos = self.rect.center
        self.image = self.explosion_sprites[0]
        self.rect = self.image.get_rect(center=pos)
        self.life_timer = 0
        for sprite in players:
            dis = ((self.rect.centerx - sprite.rect.centerx)**2 + (self.rect.centery - sprite.rect.centery)**2)**.5
            if dis < 125:
                sprite.die()
        for sprite in walls:
            dis = ((self.rect.centerx - sprite.rect.centerx)**2 + (self.rect.centery - sprite.rect.centery)**2)**.5
            if dis < 200 and sprite.is_breakable:
                sprite.kill()

    def update(self, time_passed, players, walls):
        self.life_timer += time_passed
        if not self.exploded:
            if self.life_timer < 1000:
                pass
            elif self.life_timer < 23000:
                self.image = self.sprites[1]
                self.collisions(players, walls)
            elif self.life_timer < 26000:
                if (self.life_timer % 300) < 150:
                    self.image = self.sprites[2]
                else:
                    self.image = self.sprites[1]
                self.collisions(players, walls)
            else:
                self.explode(players, walls)
        else:
            index = self.life_timer//40
            if index == 7:
                self.kill()
            self.image = self.explosion_sprites[self.life_timer//40]





