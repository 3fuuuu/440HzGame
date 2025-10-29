import pygame
from pygame.locals import *
import sys
import numpy as np
import random
import json
import os

def main():
    pygame.init()
    width, height = 600, 400
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("otoawase")

    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    gray = (180, 180, 180)

    font = pygame.font.SysFont(None, 25)
    big_font = pygame.font.SysFont(None, 100)
    mid_font = pygame.font.SysFont(None, 50)

    saisei_button = pygame.Rect(30, 30, 50, 50)
    saisei_text = font.render("Play", True, black)

    kettei_button = pygame.Rect(100, 30, 50, 50)
    kettei_text = font.render("Enter", True, black)

    retry_button = pygame.Rect(70, 30, 70, 50)
    retry_text = font.render("Retry", True, black)

    slider_x = 100
    slider_y = height // 2
    slider_width = 400
    slider_height = 5
    handle_radius = 10
    handle_x = slider_x + slider_width // 2

    hz_min = random.randint(400, 440)
    hz_max = random.randint(440, 480)

    mousedown = False
    mode = "main"

    pygame.mixer.init(frequency=44100, size=-16, channels=1)

    score_file = "score.json"
    if os.path.exists(score_file):
        try:
            with open(score_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                best_score = data.get("best_score", None)
        except Exception as e:
            print("スコアファイル読み込みエラー:", e)
            best_score = None
    else:
        best_score = None

    retry_count = 0
    new_best = False
    score_file = "score.json"
    scores = []

    if os.path.exists(score_file):
        try:
            with open(score_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    scores = data  
                else:
                    scores = [data]  
        except Exception as e:
            print("スコアファイル読み込みエラー:", e)
            scores = []


    def generate_sin_wave(frequency, duration_ms=500, sample_rate=88200):
        t = np.linspace(0, duration_ms / 1000, int(sample_rate * (duration_ms / 1000)), False)
        wave = 0.5 * np.sin(2 * np.pi * frequency * t)
        wave = (wave * 32767).astype(np.int16)
        return wave.tobytes()

    running = True

    while running:
        screen.fill(black)

        if mode == "main":
            pygame.draw.rect(screen, white, saisei_button)
            screen.blit(saisei_text, (35, 50))

            pygame.draw.rect(screen, white, kettei_button)
            screen.blit(kettei_text, (105, 50))

            pygame.draw.rect(screen, gray, (slider_x, slider_y, slider_width, slider_height))
            pygame.draw.circle(screen, red, (handle_x, slider_y + slider_height // 2), handle_radius)

            ratio = (handle_x - slider_x) / slider_width
            frequency = int(hz_min + ratio * (hz_max - hz_min))

            retry_text_disp = font.render(f"Retries: {retry_count}", True, white)
            screen.blit(retry_text_disp, (width - 150, 30))
            if best_score is not None:
                best_text_disp = font.render(f"Best: {best_score}", True, white)
                screen.blit(best_text_disp, (width - 150, 50))

        elif mode == "win":
            win_text = big_font.render("WIN", True, white)
            screen.blit(win_text, (width // 2 - 80, height // 2 - 45))
            pygame.draw.rect(screen, white, retry_button)
            screen.blit(retry_text, (75, 50))

            score_text = mid_font.render(f"Retries: {retry_count}", True, white)
            screen.blit(score_text, (width // 2 - 90, height // 2 + 60))

            if new_best:
                best_text = mid_font.render("BEST SCORE!", True, red)
                screen.blit(best_text, (width // 2 - 140, height // 2 + 120))

        elif mode == "lose":
            lose_text = big_font.render("LOSE", True, white)
            frequency_text = mid_font.render(f"{frequency} Hz", True, white)
            screen.blit(lose_text, (width // 2 - 80, height // 2 - 45))
            screen.blit(frequency_text, (width // 2 - 80, height // 2 + 30))
            pygame.draw.rect(screen, white, retry_button)
            screen.blit(retry_text, (75, 50))

            score_text = mid_font.render(f"Retries: {retry_count}", True, white)
            screen.blit(score_text, (width // 2 - 90, height // 2 + 100))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if mode == "main":
                if event.type == MOUSEBUTTONDOWN:
                    if saisei_button.collidepoint(event.pos):
                        wave = generate_sin_wave(frequency)
                        sound = pygame.mixer.Sound(buffer=wave)
                        sound.play()
                        print({frequency})

                    elif kettei_button.collidepoint(event.pos):
                        print("決定:", frequency, " Hz")
                        '''if frequency == 440:
                            print("勝")
                            mode = "win"
                            new_best = False
                            if best_score is None or retry_count < best_score:
                                best_score = retry_count
                                new_best = True
                                try:
                                    with open(score_file, "w", encoding="utf-8") as f:
                                        json.dump({"best_score": best_score}, f, ensure_ascii=False, indent=2)
                                    print("ベストスコアを保存しました:", best_score)
                                except Exception as e:
                                    print("スコア保存エラー:", e)
                            else:
                                score = retry_count
                                new_best = False
                                try:
                                    with open(score_file, "w", encoding="utf-8") as f:
                                        json.dump({"score" : score}, f, ensure_ascii=False, indent=2)
                                    print("スコアを保存しました", score)
                                except Exception as e:
                                    print("スコア保存エラー", e)'''
                        if frequency == 440:
                            print("勝")
                            mode = "win"
                            new_best = False

                            score_entry = {"result": "WIN", "score": retry_count}
                            scores.append(score_entry)

                            if best_score is None or retry_count < best_score:
                                best_score = retry_count
                                new_best = True

                                try:
                                    with open(score_file, "w", encoding="utf-8") as f:
                                        json.dump(scores, f, ensure_ascii=False, indent=2)
                                    print("スコアを保存しました:", score_entry)
                                except Exception as e:
                                    print("スコア保存エラー:", e)

                        else:
                            print("敗")
                            mode = "lose"
                            retry_count += 1

                    else:
                        mx, my = event.pos
                        distance = abs(mx - handle_x)
                        if (slider_y - 10) < my < (slider_y + 20) and distance < 20:
                            mousedown = True

                elif event.type == MOUSEBUTTONUP:
                    mousedown = False

                elif event.type == MOUSEMOTION and mousedown:
                    mx, my = event.pos
                    handle_x = max(slider_x, min(mx, slider_x + slider_width))

            elif mode in ["win", "lose"]:
                if event.type == MOUSEBUTTONDOWN:
                    if retry_button.collidepoint(event.pos):
                        print("Retry clicked")
                        mode = "main"
                        mousedown = False
                        handle_x = slider_x + slider_width // 2
                        hz_min = random.randint(380, 420)
                        hz_max = random.randint(440, 480)
                        if mode == "win":
                            retry_count = 0  

if __name__ == "__main__":
    main()
