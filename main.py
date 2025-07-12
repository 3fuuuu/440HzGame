import pygame
from pygame.locals import *
import sys
import numpy as np
import random

def main():
    pygame.init()
    width, height = 600, 400
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("otoawase")

    # 色
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    gray = (180, 180, 180)

    font = pygame.font.SysFont(None, 25)

    # ボタン
    saisei_button = pygame.Rect(30, 30, 50, 50)
    saisei_text = font.render("Play", True, black)

    kettei_button = pygame.Rect(100, 30, 50, 50)
    kettei_text = font.render("Enter", True, black)

    # スライダー
    slider_x = 100
    slider_y = height // 2
    slider_width = 400
    slider_height = 5
    handle_radius = 10
    handle_x = slider_x + slider_width // 2

    # 周波数範囲
    hz_min = random.randint(380, 420)
    hz_max = random.randint(440, 480)

    mousedown = False
    mode = "main"  # 状態管理：main, win, lose

    pygame.mixer.init(frequency=44100, size=-16, channels=1)

    # サイン波を生成する関数
    def generate_sin_wave(frequency, duration_ms=500, sample_rate=88200): #44100だと1オクターブ上になったため2倍にした
        t = np.linspace(0, duration_ms / 1000, int(sample_rate * (duration_ms / 1000)), False)
        wave = 0.5 * np.sin(2 * np.pi * frequency * t)  # サイン波
        wave = (wave * 32767).astype(np.int16)  # 16ビット整数に変換
        return wave.tobytes()

    running = True

    while running:
        screen.fill(black)

        if mode == "main":
            # ボタン描画
            pygame.draw.rect(screen, white, saisei_button)
            screen.blit(saisei_text, (35, 50))

            pygame.draw.rect(screen, white, kettei_button)
            screen.blit(kettei_text, (105, 50))

            # スライダー描画
            pygame.draw.rect(screen, gray, (slider_x, slider_y, slider_width, slider_height))
            pygame.draw.circle(screen, red, (handle_x, slider_y + slider_height // 2), handle_radius)

            # 周波数計算
            ratio = (handle_x - slider_x) / slider_width
            frequency = int(hz_min + ratio * (hz_max - hz_min))


        elif mode == "win":
            win_text = pygame.font.SysFont(None, 100).render("WIN", True, white)
            screen.blit(win_text, (width // 2 - 80, height // 2 - 45))
            

        elif mode == "lose":
            lose_text = pygame.font.SysFont(None, 100).render("LOSE", True, white)
            frequency_text = pygame.font.SysFont(None, 50).render(f"{frequency} Hz", True, white)
            screen.blit(lose_text, (width // 2 - 80, height // 2 - 45))
            screen.blit(frequency_text, (width // 2 - 80, height // 2  + 30))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if mode == "main":
                if event.type == MOUSEBUTTONDOWN:
                    if saisei_button.collidepoint(event.pos):
                        print("再生")
                        wave = generate_sin_wave(frequency)
                        sound = pygame.mixer.Sound(buffer=wave)
                        sound.play()
                        
                    elif kettei_button.collidepoint(event.pos):
                        print("決定:", frequency, " Hz")
                        if frequency == 440:
                            print("勝")
                            mode = "win"
                        else:
                            print("敗")
                            mode = "lose"
                    else:
                        mx, my = event.pos
                        distance = abs(mx - handle_x)
                        if (slider_y - 10) < my < (slider_y + 20) and distance < 20:
                            mousedown = True

                elif event.type == MOUSEBUTTONUP:
                    mousedown = False

                elif event.type == MOUSEMOTION and mousedown:
                    mx, my = event.pos
                    handle_x = max(slider_x, min(mx, slider_x + slider_width))  # 範囲制限

if __name__ == "__main__":
    main()
