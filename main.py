import math
import os
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color, Line, Ellipse, PushMatrix, PopMatrix, Rotate

# 强制全屏和横屏
Window.fullscreen = 'auto'
Window.orientation = 'landscape'

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

class GameCanvas(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        bg_path = os.path.join(BASE_PATH, '233c.png')
        car_path = os.path.join(BASE_PATH, 'car2.png')
        self.bg_texture = Image(source=bg_path).texture
        self.car_texture = Image(source=car_path).texture
        
        # ★ 尺寸减小 1.5 倍 (从 270x135 改回 180x90)
        self.car_w = 180
        self.car_h = 90
        self.car_x = Window.width / 2
        self.car_y = Window.height / 2
        self.car_angle = 90.0  
        # ★ 手柄距离适当拉近 (从 150 改为 110)
        self.handle_dist = 110 
        
        self.is_dragging = False
        self.is_rotating = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.last_angle = 0.0

        Window.bind(on_resize=self.on_resize)
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def on_resize(self, window, width, height):
        self.car_x = max(100, min(self.car_x, width - 100))
        self.car_y = max(50, min(self.car_y, height - 50))
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            Rectangle(texture=self.bg_texture, pos=(0, 0), size=(Window.width, Window.height))
            
            PushMatrix()
            Rotate(angle=self.car_angle, origin=(self.car_x, self.car_y))
            Rectangle(
                texture=self.car_texture,
                pos=(self.car_x - self.car_w / 2, self.car_y - self.car_h / 2),
                size=(self.car_w, self.car_h)
            )
            PopMatrix()
            
            rad = math.radians(self.car_angle)
            handle_x = self.car_x + math.cos(rad) * self.handle_dist
            handle_y = self.car_y + math.sin(rad) * self.handle_dist
            
            Color(0, 1, 0, 1) 
            Line(points=[self.car_x, self.car_y, handle_x, handle_y], width=2)
            
            Color(0, 1, 0, 1)
            Ellipse(pos=(handle_x - 25, handle_y - 25), size=(50, 50))
            Color(1, 1, 1, 1)
            Line(circle=(handle_x, handle_y, 25), width=2)

    def on_touch_down(self, touch):
        rad = math.radians(self.car_angle)
        handle_x = self.car_x + math.cos(rad) * self.handle_dist
        handle_y = self.car_y + math.sin(rad) * self.handle_dist

        # 手柄点击判定
        if math.hypot(touch.x - handle_x, touch.y - handle_y) <= 60: 
            self.is_rotating = True
            self.last_angle = math.atan2(touch.y - self.car_y, touch.x - self.car_x)
            return True
            
        # 车身点击判定（使用动态的车宽）
        if math.hypot(touch.x - self.car_x, touch.y - self.car_y) < (self.car_w / 2 + 20):
            self.is_dragging = True
            self.drag_offset_x = self.car_x - touch.x
            self.drag_offset_y = self.car_y - touch.y
            return True

        return False

    def on_touch_move(self, touch):
        if self.is_dragging:
            self.car_x = touch.x + self.drag_offset_x
            self.car_y = touch.y + self.drag_offset_y
            self.car_x = max(100, min(self.car_x, Window.width - 100))
            self.car_y = max(50, min(self.car_y, Window.height - 50))
            self.update_canvas()
            return True

        elif self.is_rotating:
            current_angle = math.atan2(touch.y - self.car_y, touch.x - self.car_x)
            delta = current_angle - self.last_angle
            if delta > math.pi: delta -= 2 * math.pi
            elif delta < -math.pi: delta += 2 * math.pi
            self.car_angle += math.degrees(delta * 0.1) 
            self.last_angle = current_angle
            self.update_canvas()
            return True
        return False

    def on_touch_up(self, touch):
        self.is_dragging = False
        self.is_rotating = False
        return False


class MainGame(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_canvas = GameCanvas()
        self.add_widget(self.game_canvas)
        
        # 退出按钮（使用英文 EXIT 防止手机乱码）
        self.quit_btn = Button(
            text="EXIT", 
            size_hint=(None, None), 
            size=(100, 50),
            pos_hint={'right': 0.95, 'top': 0.95},
            background_color=(0.95, 0.26, 0.21, 1), 
            font_size='18sp',
            bold=True
        )
        self.quit_btn.bind(on_release=self.quit_app)
        self.add_widget(self.quit_btn)

    def quit_app(self, instance):
        App.get_running_app().stop()

    def on_touch_down(self, touch):
        if self.quit_btn.collide_point(*touch.pos):
            return super().on_touch_down(touch)
        if self.game_canvas.on_touch_down(touch):
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.game_canvas.on_touch_move(touch):
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        self.game_canvas.on_touch_up(touch)
        return super().on_touch_up(touch)


class MyApp(App):
    def build(self):
        return MainGame()

if __name__ == '__main__':
    MyApp().run()
