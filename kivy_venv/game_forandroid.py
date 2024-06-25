from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from random import randint


class SnakeGame(Widget):
    def __init__(self, **kwargs):
        super(SnakeGame, self).__init__(**kwargs)
        self.snake_segments = [(0, 0)]
        self.food_position = (randint(0, Window.width - 20), randint(0, Window.height - 20))
        self.direction = 'right'
        self.game_over = False
        self.snake_speed = 0.1
        self.score = 0
        self.update_interval = Clock.schedule_interval(self.update, self.snake_speed)
        self.bind(on_touch_down=self.on_touch_down)

    def on_touch_down(self, touch):
        if self.game_over:
            self.reset_game()
        else:
            if touch.x < Window.width / 2:
                self.direction = 'left' if self.direction != 'right' else self.direction
            else:
                self.direction = 'right' if self.direction != 'left' else self.direction
            if touch.y < Window.height / 2:
                self.direction = 'down' if self.direction != 'up' else self.direction
            else:
                self.direction = 'up' if self.direction != 'down' else self.direction

    def update(self, dt):
        if not self.game_over:
            if self.direction == 'up':
                head = (self.snake_segments[0][0], self.snake_segments[0][1] + 20)
            elif self.direction == 'down':
                head = (self.snake_segments[0][0], self.snake_segments[0][1] - 20)
            elif self.direction == 'left':
                head = (self.snake_segments[0][0] - 20, self.snake_segments[0][1])
            elif self.direction == 'right':
                head = (self.snake_segments[0][0] + 20, self.snake_segments[0][1])

            if head in self.snake_segments[1:] or not (0 <= head[0] < Window.width and 0 <= head[1] < Window.height):
                self.game_over = True
                self.update_interval.cancel()
                self.add_widget(Label(text='Game Over', center=self.center))

            if head == self.food_position:
                self.score += 1
                self.food_position = (randint(0, Window.width - 20), randint(0, Window.height - 20))
            else:
                self.snake_segments.pop()

            self.snake_segments.insert(0, head)

            self.canvas.clear()
            with self.canvas:
                Color(1, 1, 1, 1)
                Rectangle(pos=self.food_position, size=(20, 20))
                Color(0, 1, 0, 1)
                for segment in self.snake_segments:
                    Rectangle(pos=segment, size=(20, 20))

    def reset_game(self):
        self.snake_segments = [(0, 0)]
        self.food_position = (randint(0, Window.width - 20), randint(0, Window.height - 20))
        self.direction = 'right'
        self.game_over = False
        self.score = 0
        self.update_interval = Clock.schedule_interval(self.update, self.snake_speed)

    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(pos=self.pos, size=self.size)


class SnakeApp(App):
    def build(self):
        game = SnakeGame()
        game.reset_game()
        return game


if __name__ == '__main__':
    SnakeApp().run()
