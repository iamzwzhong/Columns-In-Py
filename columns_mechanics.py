from collections import deque

class ColumnsField():
    
    def __init__(self,rows:int,columns:int):
        self._score = 0
        self._field = []
        self._next_faller = deque([])
        self._faller_exists = False
        self._faller_state = 'None'
        self._time_freeze = False
        self._match_found = False
        for row in range(rows):
            self._field.append([])
            for col in range(columns):
                self._field[-1].append(' ')
        self._matching = set()

    def update(self)->None:
        """Handles the passage of time"""
        if self._faller_state != 'None' and self._match_found == False:
            if not self._time_freeze:
                for row in range(len(self._faller_rows)):
                    if self._faller_rows[row] >= 0:
                        self._field[self._faller_rows[row]][self._faller_column] = self._faller[row]
            elif self._time_freeze:
                for row in range(len(self._faller_rows)):
                    if self._faller_rows[row] >= 0:
                        self._field[self._faller_rows[row]][self._faller_column] = self._faller[row]
                self._time_freeze = False
        elif self._faller_state == 'Frozen':
            self._faller_state = 'None'
            self._match_found = False
        else:
            self._match_found = False

    def destroy_jewels(self)->None:
        """Destroys matching jewels"""
        if len(self._matching) != 0:
            for rowIndex in range(len(self._field)):
                for colIndex in range(len(self._field[0])):
                    if (rowIndex,colIndex) in self._matching:
                        self._field[rowIndex][colIndex] = ' '
                        self._score += 100
            self._matching = set()
            self.jewel_fall()
            self._match_found = True

    def jewel_fall(self)->None:
        """Makes all the jewels fall to the lowest possible location"""
        new_field = []
        for i in range(len(self._field[0])):
            new_field.append(self._gets_new_fallen_columns(i))
        maxCol = len(new_field[0])
        for row in new_field:
            rowLength = len(row)
            if rowLength > maxCol:
                maxCol = rowLength
        new_new_field = []
        for colIndex in range(maxCol):
            new_new_field.append([])
            for row in new_field:
                if colIndex < len(row):
                    new_new_field[colIndex].append(row[colIndex])
        self._field = new_new_field

    def check_matching(self)->None:
        """Checks if there is any matching to be found and updates a set of (row,column) tuples that contain matching values"""
        matching = []
        for rowIndex in range(len(self._field)):
            for colIndex in range(len(self._field[0])):
                if self._horizontal_matching(rowIndex,colIndex) != None:
                    matching += self._horizontal_matching(rowIndex,colIndex)
                if self._vertical_matching(rowIndex,colIndex) != None:
                    matching += self._vertical_matching(rowIndex,colIndex)
                if self._diagonal_matching(rowIndex,colIndex) != None:
                    matching += self._diagonal_matching(rowIndex,colIndex)
        self._matching = set(matching)

    def _horizontal_matching(self,row:int,column:int)->[(int)]:
        """Checks if there is any horizontal matching and returns the indexes that are part of it"""
        matching_indexes = []
        if column - 1 < 0 or column + 2 > len(self._field[0]):
            return None
        elif self._field[row][column] == self._field[row][column-1] == self._field[row][column+1] and self._field[row][column] != ' ':
            matching_indexes = [(row,column),(row,column-1),(row,column+1)]
        return matching_indexes

    def _vertical_matching(self,row:int,column:int)->{(int)}:
        """Checks if there is any vertical matching and returns the indexes that are part of it"""
        matching_indexes = []
        if row - 1 < 0 or row + 2 > len(self._field):
            return None
        elif self._field[row][column] == self._field[row+1][column] == self._field[row-1][column] and self._field[row][column] != ' ':
            matching_indexes = [(row,column),(row+1,column),(row-1,column)]
        return matching_indexes

    def _diagonal_matching(self,row:int,column:int)->{(int)}:
        """Checks if there is any diagonal matching and returns the indexes that are part of it"""
        matching_indexes = []
        if row - 1 < 0 or row + 2 > len(self._field) or column - 1 < 0 or column + 2 > len(self._field[0]):
            return None
        elif self._field[row][column] == self._field[row+1][column-1] == self._field[row-1][column+1] and self._field[row][column] != ' ':
            matching_indexes = [(row+1,column-1),(row,column),(row-1,column+1)]
        elif self._field[row][column] == self._field[row-1][column-1] == self._field[row+1][column+1] and self._field[row][column] != ' ':
            matching_indexes = [(row,column),(row-1,column-1),(row+1,column+1)]
        return matching_indexes
    
    def _gets_new_fallen_columns(self,column:int)->list:
        """Gets all of the nonempty values in a column and puts it into a list"""
        nonempty = []
        empty = []
        for row in range(len(self._field)):
            if self._field[row][column] != ' ':
                nonempty.append(self._field[row][column])
            else:
                empty.append(' ')
        return empty + nonempty                
        
    
    def drop(self)->None:
        """Drops every value in the faller down a row"""
        try:
            if self._check_valid_fall():
                for row in range(len(self._faller_rows)):
                    self._faller_rows[row] += 1
        except InvalidMoveError:
            if self.check_game_over():
                raise GameOverError()

    def hard_drop(self)->None:
        """Drops the full faller onto the nearest available space"""
        for i in range(1,len(self._field)):
            if self._field[-i][self._faller_column] == ' ':
                open_spot = -i
                break
        l = len(self._field)
        new_faller_rows = [l+open_spot-2,l+open_spot-1,l+open_spot]
        self.clear_old_faller()
        self._faller_rows = new_faller_rows
            
            

    def clear_old_faller(self)->None:
        """Clears old faller remnants on the board"""
        for row in range(len(self._faller_rows)):
            if self._faller_rows[row] >= 0:
                self._field[self._faller_rows[row]][self._faller_column] = ' '

    def make_faller(self,column:int,faller:[str]):
        """Creates a faller"""
        self._faller = faller
        self._faller_exists = True
        self._faller_column = column - 1
        self._faller_rows = [-2,-1,0]
        if self._field[0][self._faller_column] == ' ' and self._field[1][self._faller_column] != ' ':
            self._faller_state = 'Landed'
        elif self._field[0][self._faller_column] != ' ':
            raise GameOverError()
        else:
            self._faller_state = 'Falling'

    def check_game_over(self)->bool:
        """Checks if the game is over due to the faller not being completely visible"""
        for row in self._faller_rows:
            if row < 0:
                return True

    def _check_valid_fall(self)->bool:
        """Returns True if the faller can continue to drop"""
        if self._faller_rows[-1] + 1 < len(self._field):
            if self._field[self._faller_rows[-1] + 1][self._faller_column] == ' ':
                if self._faller_rows[-1] + 2 == len(self._field):
                    if self._time_freeze == False:
                        self._faller_state = 'Landed'
                elif self._field[self._faller_rows[-1] + 2][self._faller_column] != ' ':
                    self._faller_state = 'Landed'
                return True
            elif self._faller_state == 'Falling':
                self._faller_state = 'Landed'
            elif self._faller_state == 'Landed':
                self._faller_state = 'Frozen'
                self._faller_exists = False
        elif self._faller_state == 'Falling':
            self._faller_state = 'Landed'
        else:
            self._faller_state = 'Frozen'
            self._faller_exists = False

    def move_faller(self,move:str)->None:
        """Moves the faller left or right"""
        try:
            if self._faller_exists == True:
                self.clear_old_faller()
                self._faller_state = 'Falling'
                if move == '>':
                    if self._faller_column > len(self._field[0]) - 2:
                        raise InvalidMoveError()
                    for row in self._faller_rows:
                        if row >= 0:
                            if self._field[row][self._faller_column + 1] != ' ':
                                raise InvalidMoveError()
                    else:
                        self._faller_column += 1
                        self._time_freeze = True
                        self._check_valid_fall()
                elif move == '<':
                    if self._faller_column - 1 < 0:
                        raise InvalidMoveError()
                    for row in self._faller_rows:
                        if row >= 0:
                            if self._field[row][self._faller_column - 1] != ' ':
                                raise InvalidMoveError()
                    else:
                        self._faller_column -= 1
                        self._time_freeze = True
                        self._check_valid_fall()
        except InvalidMoveError:
            self._time_freeze = True
            self._check_valid_fall()

    def rotate_faller(self)->None:
        """Rotates the faller where the bottom goes to the top everything goes down"""
        if self._faller_exists == True:
            self.clear_old_faller()
            self._faller = self._faller[-1:] + self._faller[:-1]
            self._time_freeze = True
        
def make_columns_field(rows:int,columns:int)->ColumnsField:
    """Makes a new columns field"""
    return ColumnsField(rows,columns)

class GameOverError(Exception):
    """Raised whenever an attempt is made to make a move after the game is already over"""
    pass

class InvalidMoveError(Exception):
    """Raised whenever an invalid move is made"""
    pass


