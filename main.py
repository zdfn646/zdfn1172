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
        
        # 1. 加载图片纹理
        bg_path = os.path.join(BASE_PATH, '233c.png')
        car_path = os.path.join(BASE_PATH, 'car2.png')
        self.bg_texture = Image(source=bg_path).texture
        self.car_texture = Image(source=car_path).texture
        
        # ★ 修改点 1：车身适当放大 (从 180x90 改为 220x110)
        self.car_w = 220
        self.car_h = 110
        
        self.car_x = Window.width / 2
        self.car_y = Window.height / 2
        self.car_angle = 90.0  # 初始角度：90度朝上
        
        # 配合车身放大，连接杆距离稍微拉长
        self.handle_dist = 130 
        
        self.is_dragging = False
        self.is_rotating = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.last_angle = 0.0

        Window.bind(on_resize=self.on_resize)
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def on_resize(self, window, width, height):
        # 限制车不要跑出屏幕边界
        self.car_x = max(80, min(self.car_x, width - 80))
        self.car_y = max(50, min(self.car_y, height - 50))
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            # 1. 画背景
            Rectangle(texture=self.bg_texture, pos=(0, 0), size=(Window.width, Window.height))
            
            # 2. 画车身
            PushMatrix()
            Rotate(angle=self.car_angle, origin=(self.car_x, self.car_y))
            Rectangle(
                texture=self.car_texture,
                pos=(self.car_x - self.car_w / 2, self.car_y - self.car_h / 2),
                size=(self.car_w, self.car_h)
            )
            PopMatrix()
            
            # 3. 计算手柄位置
            rad = math.radians(self.car_angle)
            handle_x = self.car_x + math.cos(rad) * self.handle_dist
            handle_y = self.car_y + math.sin(rad) * self.handle_dist
            
            # 4. 画连接线
            Color(0, 1, 0, 1) 
            Line(points=[self.car_x, self.car_y, handle_x, handle_y], width=2)
            
            # 5. 画旋转手柄
            Color(0, 1, 0, 1)
            Ellipse(pos=(handle_x - 25, handle_y - 25), size=(50, 50))
            Color(1, 1, 1, 1)
            Line(circle=(handle_x, handle_y, 25), width=2)

    def on_touch_down(self, touch):
        rad = math.radians(self.car_angle)
        handle_x = self.car_x + math.cos(rad) * self.handle_dist
        handle_y = self.car_y + math.sin(rad) * self.handle_dist

        # 判断点手柄（触摸范围放宽到 60 像素，防误触）
        if math.hypot(touch.x - handle_x, touch.y - handle_y) <= 60: 
            self.is_rotating = True
            self.last_angle = math.atan2(touch.y - self.car_y, touch.x - self.car_x)
            return True
            
        # 判断点车身
        if math.hypot(touch.x - self.car_x, touch.y - self.car_y) < (self.car_w / 2 + 25):
            self.is_dragging = True
            self.drag_offset_x = self.car_x - touch.x
            self.drag_offset_y = self.car_y - touch.y
            return True

        return False

    def on_touch_move(self, touch):
        if self.is_dragging:
            # 拖拽位置
            self.car_x = touch.x + self.drag_offset_x
            self.car_y = touch.y + self.drag_offset_y
            
            # 边界限制
            self.car_x = max(80, min(self.car_x, Window.width - 80))
            self.car_y = max(50, min(self.car_y, Window.height - 50))
            
            self.update_canvas()
            return True

        elif self.is_rotating:
            # 增量角度计算
            current_angle = math.atan2(touch.y - self.car_y, touch.x - self.car_x)
            delta = current_angle - self.last_angle
            
            if delta > math.pi: delta -= 2 * math.pi
            elif delta < -math.pi: delta += 2 * math.pi
            
            # ★ 修改点 2：旋转幅度再加 2 倍 (从 0.2 改为 0.4)
            self.car_angle += math.degrees(delta * 0.4) 
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
        
        # 退出按钮
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
        # Kivy 原生退出，瞬间秒退，不转圈
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
