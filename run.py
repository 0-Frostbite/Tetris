from data import *
    
events = [["Menu()","Instruct()","Quit()","Level()","Game_Over()"],
["Menu.run(Run)","Instruct.run(Run)","Quit.run(Run)","Level.run(Run,key)","Game_Over.run(Run)"]]

event_code , event_run = 0 , -1

fps=pygame.time.Clock()

class main():

    button_press = pygame.mixer.Sound(path.join('assets','button.wav'))
    button_press.set_volume(0.2)
    
    while True:
        if event_run!=event_code:
            event_run=event_code
            Run=eval(events[0][event_run])
            box=list(Run.buttons.values())
            box_code=list(Run.buttons.keys()) 

        key = 0

        for event in pygame.event.get(): 
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONUP and event.dict.get('button')==1:
                for button in box:
                    if button.collidepoint(pygame.mouse.get_pos()):
                        button_press.play()
                        event_code=box_code[box.index(button)]
            elif event.type == KEYDOWN:
                key=event.dict.get('key')

        code=eval(events[1][event_run])

        pygame.display.update()

        fps.tick(5)
        FPS=fps.get_fps()
        pygame.display.set_caption(str(FPS))

        if type(code)==int:
            event_code=code

if __name__ == '__main__':
    exec = main()