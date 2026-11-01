from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import random

class GokulActionGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=15, **kwargs)
        
        self.score = 0
        self.hp = 100
        self.ammo = 7
        self.enemy_pos = 0
        self.enemy_dist = 5
        self.game_event = None
        
        self.lbl_hud = Label(
            text=f"Score: {self.score}  |  HP: {self.hp}  |  Ammo: {self.ammo}/7",
            font_size='22sp',
            size_hint_y=0.15
        )
        self.add_widget(self.lbl_hud)

        self.lbl_status = Label(
            text="Game Ready! Tap Start.",
            font_size='20sp',
            size_hint_y=0.2
        )
        self.add_widget(self.lbl_status)

        fire_box = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.35)
        
        self.btn_left = Button(text="FIRE LEFT\n(डावीकडे)", font_size='18sp')
        self.btn_left.bind(on_press=lambda x: self.fire(-1))
        fire_box.add_widget(self.btn_left)

        self.btn_center = Button(text="FIRE CENTER\n(समोर)", font_size='18sp')
        self.btn_center.bind(on_press=lambda x: self.fire(0))
        fire_box.add_widget(self.btn_center)

        self.btn_right = Button(text="FIRE RIGHT\n(उजवीकडे)", font_size='18sp')
        self.btn_right.bind(on_press=lambda x: self.fire(1))
        fire_box.add_widget(self.btn_right)

        self.add_widget(fire_box)

        act_box = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.15)
        
        self.btn_reload = Button(text="RELOAD (रिलोड)", font_size='18sp')
        self.btn_reload.bind(on_press=lambda x: self.reload_gun())
        act_box.add_widget(self.btn_reload)

        self.btn_start = Button(text="START GAME", font_size='18sp', background_color=(0, 0.8, 0.2, 1))
        self.btn_start.bind(on_press=lambda x: self.start_game())
        act_box.add_widget(self.btn_start)

        self.add_widget(act_box)

    def start_game(self):
        self.score = 0
        self.hp = 100
        self.ammo = 7
        self.update_hud()
        self.lbl_status.text = "Battle Started! Listen carefully!"
        self.spawn_enemy()
        if self.game_event:
            self.game_event.cancel()
        self.game_event = Clock.schedule_interval(self.game_tick, 1.5)

    def spawn_enemy(self):
        self.enemy_pos = random.choice([-1, 0, 1])
        self.enemy_dist = 5
        pos_str = "LEFT" if self.enemy_pos == -1 else ("RIGHT" if self.enemy_pos == 1 else "CENTER")
        self.lbl_status.text = f"Enemy Footsteps: {pos_str}!"

    def game_tick(self, dt):
        self.enemy_dist -= 1
        if self.enemy_dist <= 0:
            self.hp -= 25
            self.update_hud()
            if self.hp <= 0:
                self.game_over()
            else:
                self.lbl_status.text = "Enemy Attacked! Enemy respawned!"
                self.spawn_enemy()

    def fire(self, direction):
        if self.ammo <= 0:
            self.lbl_status.text = "No Ammo! Tap RELOAD!"
            return

        self.ammo -= 1
        self.update_hud()

        if direction == self.enemy_pos:
            self.score += 10
            self.update_hud()
            self.lbl_status.text = "Target Hit! Enemy Down!"
            self.spawn_enemy()
        else:
            self.lbl_status.text = "Shot Missed!"

    def reload_gun(self):
        self.ammo = 7
        self.update_hud()
        self.lbl_status.text = "Reloaded! Ready to fire!"

    def update_hud(self):
        self.lbl_hud.text = f"Score: {self.score}  |  HP: {self.hp}  |  Ammo: {self.ammo}/7"

    def game_over(self):
        if self.game_event:
            self.game_event.cancel()
        self.lbl_status.text = f"Game Over! Final Score: {self.score}"

class GokulActionApp(App):
    def build(self):
        return GokulActionGame()

if __name__ == '__main__':
    GokulActionApp().run()

