import pygame
from display import GraphicsEngine






if __name__ == "__main__":
    # Ima try to document this code but sometimes im just too tired and the comments become... "interesting"
    
    # Inot the gui
    app = GraphicsEngine()
    screen: pygame.Surface = app.getWindow() # Out dated, idk if it still does anything

    app.AddCuboid((0, 0, 0), (10, 3, 4))

    Running = True
    while Running:
        app.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = False
                app.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(app.castRay(pos))

        # Check keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            app.setCameraSpeed(0.05)
        else:
            app.setCameraSpeed(0.005)


