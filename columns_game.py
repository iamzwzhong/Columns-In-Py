import columns_mechanics
import pygame
import random

#Constants representing game setup
_FRAME_RATE = 30
_COLUMNS_ROWS = 13
_COLUMNS_COLUMNS = 6
_GRID_MARGIN = 2

#Constants representing colors
RED = 'R'
BLUE = 'B'
YELLOW = 'Y'
ORANGE = 'O'
GREEN = 'G'
MAGENTA = 'M'
CYAN = 'C'

#dictionary linking color to its hexcode
colors = {
            RED:(255,0,0),
            BLUE:(0,0,255),
            YELLOW:(255,255,0),
            ORANGE:(255,165,0),
            GREEN:(0,255,0),
            MAGENTA:(255,0,255),
            CYAN:(0,255,255)
        }

class ColumnsGame:
    def __init__(self):
        self._state = columns_mechanics.ColumnsField(_COLUMNS_ROWS,_COLUMNS_COLUMNS)
        self._running = True
        self._WINDOWS_HEIGHT = _COLUMNS_ROWS * 40
        self._WINDOWS_WIDTH = _COLUMNS_COLUMNS * 40
    
    def run(self)->None:
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("bgm.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)
        pygame.display.set_caption("Columns Remake")
        try:
            clock = pygame.time.Clock()

            self._create_surface((self._WINDOWS_WIDTH+200,self._WINDOWS_HEIGHT))
            
            draw_delay = 0

            while self._running:                
                clock.tick(_FRAME_RATE)
                self._handle_events()

                if draw_delay == 10:
                    draw_delay = 0
                    self._run_game()
                self._draw_frame()
                draw_delay += 1
                
        except columns_mechanics.GameOverError:
            self._stop_running()
        finally:
            pygame.quit()

    def _run_game(self)->None:
        if not self._state._faller_exists:
            faller = []
            jewels = list(colors.keys())
            for number in range(3):
                faller.append(random.choice(jewels))
            self._state.make_faller(random.randint(1,_COLUMNS_COLUMNS),faller)
        else:
            self._state.clear_old_faller()
            self._state.drop()
            self._state.update()
            self._state.check_matching()
            if self._state._faller_state in ['None','Frozen']:
                self._state.destroy_jewels()
                while self._state._match_found:
                    self._state.update()
                    self._state.check_matching()
                    self._state.destroy_jewels()
            

    def _create_surface(self,size:(int,int))->None:
        self._surface = pygame.display.set_mode(size,pygame.RESIZABLE)

    def _handle_events(self)->None:
        for event in pygame.event.get():
            self._handle_event(event)

    def _handle_event(self,event)->None:
        if event.type == pygame.QUIT:
            self._stop_running()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self._state.move_faller('<')
            elif event.key == pygame.K_RIGHT:
                self._state.move_faller('>')
            elif event.key == pygame.K_SPACE:
                self._state.rotate_faller()

    def _stop_running(self)->None:
        self._running = False

    def _draw_frame(self)->None:
        self._surface.fill(pygame.Color(0,0,0))
        self._draw_grid()
        self._draw_scoring()
        pygame.display.flip()
        if self._state._faller_state == 'Landed':
            self._draw_landing_faller()
            pygame.display.flip()

    def _draw_grid(self)->None:

        _GRID_WIDTH = self._get_grid_width()
        _GRID_HEIGHT = self._get_grid_height()
        
        for row in range(_COLUMNS_ROWS):
            for column in range(_COLUMNS_COLUMNS):
                if self._state._field[row][column] in colors:
                    color = colors[self._state._field[row][column]]
                else:
                    color = (128,128,128)
                
                pygame.draw.rect(self._surface,color,
                                 [(_GRID_MARGIN + _GRID_WIDTH) * column + _GRID_MARGIN,
                                  (_GRID_MARGIN + _GRID_HEIGHT) * row + _GRID_MARGIN,
                                  _GRID_WIDTH, _GRID_HEIGHT])

    def _draw_scoring(self)->None:
        font = pygame.font.Font('anton.ttf',32)
        text = font.render('Score: ', True, (0,255,0),(0,0,128))
        textRect = text.get_rect()
        textRect.center = (self._WINDOWS_WIDTH+100, self._WINDOWS_HEIGHT/2)
        self._surface.blit(text,textRect)
                    
    def _draw_landing_faller(self)->None:

        _GRID_WIDTH = self._get_grid_width()
        _GRID_HEIGHT = self._get_grid_height()
        
        for row in range(_COLUMNS_ROWS):
            for column in range(_COLUMNS_COLUMNS):
                if row in self._state._faller_rows and column == self._state._faller_column:
                    pygame.draw.rect(self._surface,(255,255,255),
                         [(_GRID_MARGIN + _GRID_WIDTH) * column + _GRID_MARGIN,
                          (_GRID_MARGIN + _GRID_HEIGHT) * row + _GRID_MARGIN,
                          _GRID_WIDTH, _GRID_HEIGHT])
                
    def _get_grid_height(self)->float:
        return 0.965 * (self._WINDOWS_HEIGHT / _COLUMNS_ROWS)        

    def _get_grid_width(self)->float:
        return 0.965 * (self._WINDOWS_WIDTH / _COLUMNS_COLUMNS)
                

if __name__ == '__main__':
    ColumnsGame().run()

    

    
