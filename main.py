import flet as ft
import math
import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# ================= 兼容新旧版本 Flet 的垫片 =================
def get_border_all(width, color):
    try:
        return ft.Border.all(width, color)
    except AttributeError:
        return ft.border.all(width, color)

def get_padding_symmetric(h, v):
    try:
        return ft.Padding.symmetric(horizontal=h, vertical=v)
    except AttributeError:
        return ft.padding.symmetric(horizontal=h, vertical=v)

def get_alignment_center():
    try:
        return ft.Alignment(0, 0)
    except AttributeError:
        return ft.alignment.center

def get_local_pos(e):
    x = getattr(e, "local_x", None)
    if x is not None:
        return x, getattr(e, "local_y", 0.0)
        
    if hasattr(e, "local_position") and e.local_position is not None:
        pos = e.local_position
        dx = getattr(pos, "dx", getattr(pos, "x", 0.0))
        dy = getattr(pos, "dy", getattr(pos, "y", 0.0))
        return dx, dy
        
    if hasattr(e, "local_delta") and e.local_delta is not None:
        delta = e.local_delta
        dx = getattr(delta, "dx", getattr(delta, "x", 0.0))
        dy = getattr(delta, "dy", getattr(delta, "y", 0.0))
        return dx, dy
        
    return 0.0, 0.0
# ============================================================

def main(page: ft.Page):
    page.title = "曲线行驶模拟"
    page.padding = 0
    page.spacing = 0

    # 窗口设置
    try:
        page.window.orientation = ft.Orientation.LANDSCAPE
        page.window.full_screen = False 
        page.window.width = 900
        page.window.height = 600
        page.window.min_width = 600
        page.window.min_height = 400
    except:
        pass

    state = {
        "car_x": 300.0,
        "car_y": 500.0,
        "angle_rad": math.pi / 2,
        "is_dragging": False,
        "is_rotating": False,
        "drag_offset_x": 0.0,
        "drag_offset_y": 0.0,
        "last_angle": 0.0
    }

    HANDLE_RADIUS = 20
    HANDLE_DISTANCE = 90

    bg_img = ft.Image(src="233c.png", fit="cover", width=2000, height=2000)
    car_img = ft.Image(src="car2.png", width=210, height=100, fit="contain")

    car_container = ft.Container(
        content=car_img,
        width=210,
        height=100,
        rotate=ft.Rotate(angle=0),
        alignment=get_alignment_center(),
    )

    handle_container = ft.Container(
        width=HANDLE_RADIUS * 2,
        height=HANDLE_RADIUS * 2,
        bgcolor="#4CAF50",
        border=get_border_all(2, "#FFFFFF"),
        border_radius=HANDLE_RADIUS,
    )

    # ================= 窗口控制逻辑 =================
    def minimize_window(e):
        try:
            page.window.minimized = True
            page.update()
        except:
            pass

    def toggle_maximize(e):
        try:
            if getattr(page.window, "full_screen", False):
                page.window.full_screen = False
                page.update()
                return
            
            page.window.maximized = not getattr(page.window, "maximized", False)
            page.update()
        except:
            pass

    # ================= 退出逻辑 =================
    def close_dialog(dlg):
        dlg.open = False
        page.update()

    def really_close(e):
        page.controls.clear()
        page.bgcolor = ft.Colors.BLACK
        page.add(ft.Container(
            content=ft.Text("程序已安全退出", color="white", size=24),
            alignment=ft.Alignment(0, 0),
            expand=True
        ))
        page.update()
        try:
            page.window.destroy()
        except:
            try: page.window.close()
            except:
                try: page.window_close()
                except: pass

    def show_exit_dialog(e):
        dlg = ft.AlertDialog(
            title=ft.Text("确认退出"),
            content=ft.Text("您确定要退出曲线行驶模拟吗？"),
            actions=[
                ft.TextButton("取消", on_click=lambda _: close_dialog(dlg)),
                ft.TextButton("确定退出", on_click=really_close, style=ft.ButtonStyle(color=ft.Colors.RED)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    # ================= 顶部悬浮控制栏 =================
    def make_btn(text, color, on_click):
        return ft.Container(
            content=ft.Text(text, color="#FFFFFF", weight="bold", size=16),
            bgcolor=color,
            padding=get_padding_symmetric(12, 6),
            border_radius=8,
            on_click=on_click,
            # ★ 彻底移除 margin，改用 Row 的 spacing 控制间隔
        )

    top_controls = ft.Container(
        content=ft.Row([
            make_btn("➖", "#607D8B", minimize_window),
            make_btn("🔲", "#FF9800", toggle_maximize),
            make_btn("❌", "#F44336", show_exit_dialog),
        ], alignment=ft.MainAxisAlignment.END, spacing=10), # ★ 这里加上 spacing=10
        top=30,
        right=30,
    )
    # ====================================================

    def update_ui():
        cx, cy = state["car_x"], state["car_y"]
        rad = state["angle_rad"]

        car_container.left = cx - 105
        car_container.top = cy - 50
        car_container.rotate.angle = -math.degrees(rad)

        handle_x = cx + math.cos(rad) * HANDLE_DISTANCE
        handle_y = cy - math.sin(rad) * HANDLE_DISTANCE
        handle_container.left = handle_x - HANDLE_RADIUS
        handle_container.top = handle_y - HANDLE_RADIUS

        page.update()

    def on_resize(e=None):
        if state["car_x"] == 300.0 and state["car_y"] == 500.0:
            state["car_x"] = page.width / 2 if page.width else 400
            state["car_y"] = page.height / 2 if page.height else 600
            update_ui()

    page.on_resize = on_resize

    def on_pan_start(e: ft.DragStartEvent):
        fx, fy = get_local_pos(e)
        cx, cy = state["car_x"], state["car_y"]
        
        handle_x = cx + math.cos(state["angle_rad"]) * HANDLE_DISTANCE
        handle_y = cy - math.sin(state["angle_rad"]) * HANDLE_DISTANCE

        if math.hypot(fx - handle_x, fy - handle_y) <= HANDLE_RADIUS + 20:
            state["is_rotating"] = True
            state["last_angle"] = math.atan2(cy - fy, fx - cx)
            return
            
        if math.hypot(fx - cx, fy - cy) < 100:
            state["is_dragging"] = True
            state["drag_offset_x"] = cx - fx
            state["drag_offset_y"] = cy - fy

    def on_pan_update(e: ft.DragUpdateEvent):
        fx, fy = get_local_pos(e)
        cx, cy = state["car_x"], state["car_y"]

        if state["is_dragging"]:
            state["car_x"] = fx + state["drag_offset_x"]
            state["car_y"] = fy + state["drag_offset_y"]
            update_ui()

        elif state["is_rotating"]:
            current_angle = math.atan2(cy - fy, fx - cx)
            delta_angle = current_angle - state["last_angle"]
            
            if delta_angle > math.pi:
                delta_angle -= 2 * math.pi
            elif delta_angle < -math.pi:
                delta_angle += 2 * math.pi
                
            state["angle_rad"] += delta_angle * 0.1
            state["last_angle"] = current_angle
            update_ui()

    def on_pan_end(e: ft.DragEndEvent):
        state["is_dragging"] = False
        state["is_rotating"] = False

    gesture_layer = ft.GestureDetector(
        on_pan_start=on_pan_start,
        on_pan_update=on_pan_update,
        on_pan_end=on_pan_end,
        content=ft.Container(bgcolor="transparent", expand=True),
        drag_interval=10,
    )

    page.add(
        ft.Stack(
            controls=[
                ft.Container(content=bg_img, expand=True),
                car_container,
                handle_container,
                gesture_layer,
                top_controls
            ],
            expand=True
        )
    )
    
    on_resize()

if __name__ == "__main__":
    try:
        ft.run(main)
    except AttributeError:
        ft.app(target=main)