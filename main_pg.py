from livewires import games, color
import random
import datetime

games.init(screen_width=600, screen_height=450, fps=50)


class Lesya_Ukrainka(games.Sprite):

    image = games.load_image('img/LU.png')

    def __init__(self, game, x, y):
        super(Lesya_Ukrainka, self).__init__(image=Lesya_Ukrainka.image, x=x, y=y)
        self.game = game
        terra_lst = []
        for _ in range(3):
            t = Terra()
            games.screen.add(t)
            terra_lst.append(t)
        self.terra_lst = terra_lst
        self.stone = Stone(game=self, x=games.screen.width - 60, y=games.screen.height - 60)
        games.screen.add(self.stone)
        self.cf = 0
        self.time_of_waiting = 0

    def update(self):
        if self.time_of_waiting > 0:
            self.time_of_waiting -= 1

        if games.keyboard.is_pressed(games.K_UP):
            self.y -= 2
        if games.keyboard.is_pressed(games.K_DOWN):
            self.y += 2
        if games.keyboard.is_pressed(games.K_LEFT):
            self.x -= 2
        if games.keyboard.is_pressed(games.K_RIGHT):
            self.x += 2

        if games.keyboard.is_pressed(games.K_SPACE) and self.time_of_waiting == 0:
            water = Water(self.x, self.y)
            games.screen.add(water)
            self.time_of_waiting = 40

        if self.x < 30:
            self.x = 30
        if self.x > (games.screen.width - 150):
            self.x = games.screen.width - 150
        if self.y > (games.screen.height - 50):
            self.y = games.screen.height - 50
        if self.y < (games.screen.height/2):
            self.y = games.screen.height/2

        cf = 0
        for i in self.terra_lst:
            cf += i.count
        self.cf = cf

        self.stone.y = games.screen.height - 60 - 25*cf


class Stone(games.Sprite):

    image = games.load_image('img/stone.png')

    def __init__(self, game, x, y):
        super(Stone, self).__init__(image=Stone.image, x=x, y=y)
        self.game = game
        self.timestart = datetime.datetime.now()
        self.timestop = 0

    def update(self):

        if (games.screen.height - 210) < self.y <= (games.screen.height - 135):
            background = games.load_image('img/background_2.jpg', transparent=False)
            games.screen.background = background
        if (games.screen.height - 285) < self.y <= (games.screen.height - 210):
            background = games.load_image('img/background_3.jpg', transparent=False)
            games.screen.background = background
        if (games.screen.height - 360) < self.y <= (games.screen.height - 285):
            background = games.load_image('img/background_4.jpg', transparent=False)
            games.screen.background = background
        if (games.screen.height - 435) < self.y <= (games.screen.height - 360):
            background = games.load_image('img/background_5.jpg', transparent=False)
            games.screen.background = background
        if self.y < (games.screen.height - 435):
            background = games.load_image('img/background_6.jpg', transparent=False)
            games.screen.background = background

        if self.y <= 70:
            self.timestop = datetime.datetime.now()
            time = (self.timestop - self.timestart).seconds
            timetext = 'Ваш результат: ' + str(time) + 'секунд'
            if time <= 17:
                text = 'Вы - Мавка'
            elif 17 < time <= 32:
                text = 'Вы - Лукаш'
            else:
                text = 'Вы - Килина'
            message_end_1 = games.Message(value='Конец игры', size=50, color=color.brown,
                                          x=games.screen.width / 2, y=games.screen.height/4,
                                          lifetime=2*games.screen.fps, after_death=games.screen.quit)
            message_end_2 = games.Message(value=timetext, size=50, color=color.brown,
                                          x=games.screen.width / 2, y=games.screen.height/3,
                                          lifetime=2 * games.screen.fps, after_death=games.screen.quit)
            message_end_3 = games.Message(value=text, size=50, color=color.brown,
                                          x=games.screen.width / 2, y=games.screen.height*5/12,
                                          lifetime=2 * games.screen.fps, after_death=games.screen.quit)
            games.screen.add(message_end_1)
            games.screen.add(message_end_2)
            games.screen.add(message_end_3)


class Water(games.Sprite):

    image = games.load_image('img/water.png')
    speed = 2

    def __init__(self, x, y):
        super(Water, self).__init__(image=Water.image, x=x, y=y, dx=0, dy=Water.speed)

    def update(self):
        if self.x < 0 or self.x > games.screen.width:
            self.destroy()
        if self.y < 0 or self.y > games.screen.height:
            self.destroy()


class Terra(games.Sprite):

    image = games.load_image('img/terra.png')

    def __init__(self):
        super(Terra, self).__init__(image=Terra.image,
                                    x=random.randint(0, games.screen.width - 80),
                                    y=random.randint(games.screen.height*2/3, games.screen.height),
                                    dx=random.choice([-2, -1, 1, 2]),
                                    dy=random.choice([-2, -1, 1, 2]))
        self.count = 0

    def update(self):
        if self.x < 0:
            self.x = games.screen.width - 80
        if self.x > (games.screen.width - 80):
            self.x = 0
        if self.y < (games.screen.height*2/3):
            self.y = games.screen.height
        if self.y > games.screen.height:
            self.y = games.screen.height*2/3

        for water in self.overlapping_sprites:
            if type(water) == Water:
                self.count += 1
                new_flower = Flower(self.x, self.y)
                games.screen.add(new_flower)
                water.destroy()


class Flower(games.Sprite):
    image = games.load_image('img/flower.png')

    def __init__(self, x, y):
        super(Flower, self).__init__(image=Flower.image, x=x, y=y,)


class Game:

    def __init__(self):
        games.music.load('music/1.mp3')
        games.music.play(-1)
        self.LU = Lesya_Ukrainka(game=self, x=(games.screen.width / 2) + 30, y=(games.screen.height / 2) + 70)
        games.screen.add(self.LU)

    def playing(self):
        message_start = games.Message(value='Lesya Ukrainka`s world', size=50, color=color.brown,
                                      x=games.screen.width / 2, y=games.screen.height / 2.5,
                                      lifetime=2*games.screen.fps)
        games.screen.add(message_start)
        background = games.load_image('img/background_1.jpg', transparent=False)
        games.screen.background = background
        games.screen.mainloop()


def main():
    Lesya_Ukrainka_s_world = Game()
    Lesya_Ukrainka_s_world.playing()


if __name__ == main():
    main()
