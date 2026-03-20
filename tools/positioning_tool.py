import glob
import json
import os
import sys

import pygame

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

from settings import WIDTH, HEIGHT


class PositioningTool:
    """
    This tools is showing a screenshot of the game with original sprites.
    All the sprites will appear one by one
    Use keys to adjust sprites to original and save in positions files
    """

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()

        bg = pygame.image.load("tools/img/FullScreen.png").convert()

        INCREMENT = 1
        ALL_PREFIX = ["Bird", "Cage", "Nut", "Croco", "Key", "Missed", "Monkey"]

        for prefix in ALL_PREFIX:
            position_file = "positions/" + prefix + "Positions.json"
            all_positions = PositioningTool.get_all_positions(position_file)
            print(all_positions)

            for filepath in glob.iglob("img/sprites/" + prefix + "/*.png"):
                # Filenames are xxx.png thus 7 letters
                spriteName = filepath[-7:-4]
                print(spriteName)
                surface = pygame.image.load(filepath).convert_alpha()
                rect = surface.get_rect()

                if all_positions.get(spriteName) is None:
                    rect.x = WIDTH // 2
                    rect.y = HEIGHT // 2
                else:
                    rect.x = all_positions[spriteName][0]
                    rect.y = all_positions[spriteName][1]

                positioning = True
                while positioning:
                    pygame.event.pump()
                    keys = pygame.key.get_pressed()

                    if keys[pygame.K_RIGHT]:
                        rect.x += INCREMENT
                    if keys[pygame.K_LEFT]:
                        rect.x -= INCREMENT
                    if keys[pygame.K_UP]:
                        rect.y -= INCREMENT
                    if keys[pygame.K_DOWN]:
                        rect.y += INCREMENT
                    if keys[pygame.K_SPACE]:
                        print(rect.x, rect.y)
                        all_positions[spriteName] = (rect.x, rect.y)
                        positioning = False

                    screen.blit(bg, (0, 0))
                    screen.blit(surface, rect)
                    pygame.display.flip()
                    clock.tick(10)

            PositioningTool.write_position_in_file(all_positions, position_file)

        print("End of positionning")
        pygame.quit()

    @staticmethod
    def get_all_positions(json_path):
        if os.path.isfile(json_path):
            with open(json_path, "r") as f:
                return json.load(f)
        return {}

    @staticmethod
    def write_position_in_file(positions, json_path):
        with open(json_path, "w") as f:
            json.dump(positions, f, indent=2, sort_keys=True)


def main():
    PositioningTool().run()


if __name__ == "__main__":
    main()
