import curses


class UI(object):
    def __init__(self):
        self.screen = curses.initscr()
        self.screen.keypad(True)
        curses.noecho()
        curses.cbreak()
        curses.start_color()

        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)

        self._start_col = int(float(curses.COLS) / 5)
        self._start_row = int(float(curses.LINES) / 5)
        self.mid_col = int(float(curses.COLS) / 3) - self._start_col
        

    def deinit(self):
        self.screen.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def print(self, row_offset=0, col_offset=0, string="", color=1):
        self.screen.addstr(row_offset+self._start_row,
                           col_offset+self._start_col,
                           string, curses.color_pair(color))


    def scanf(self, row_offset=0, col_offset=0, limit=20):
        return self.screen.getstr(row_offset+self._start_row,
                                  col_offset+self._start_col, limit)


    def move(self, row_offset=0, col_offset=0):
        self.screen.move(row_offset+_start_row, col_offset+_start_col)


    def get_login_info(self, should_alert):
        self.screen.clear()
        self.print(col_offset=self.mid_col, string="Moodle.Nottingham Login", color=1)
        self.print(row_offset=2, string="Username: ", color=4)
        self.print(row_offset=3, string="Password: ", color=4)
        self.print(row_offset=5,
                   string="Login ( Press Enter )\tExit ( Press <C-c> )", color=4)

        if should_alert:
            self.print(row_offset=6, string="Username and password unmatch !", color=3)
        curses.echo()
        username = self.scanf(row_offset=2, col_offset=10)
        curses.noecho()
        password = self.scanf(row_offset=3, col_offset=10)
        
        return username, password


    def show_list(self, data):
        self.screen.clear()
        name = data['name']
        type = data['type']
        position = data['position']
        list = data['list']
        self.print(col_offset=self.mid_col, string="%s's %s Lists:" % (name, type))
        total_rows = min(10, len(list))
        for index in range(total_rows):
            if index == position:
                self.print(row_offset=index+2, col_offset=-2, string="*", color=2)
                self.print(row_offset=index+2,
                           string="%s" % (list[index][0],), color=2)
            else:
                self.print(row_offset=index+2,
                           string="%s" % (list[index][0],), color=5)

        self.screen.move(0,0)
        
    def get_song_name(self):
        self.screen.clear()
        self.print(col_offset=self.mid_col, string="Music Search")
        self.print(row_offset=2, string="Keyword: ", color=4)
        curses.echo()
        keyword = self.scanf(row_offset=2, col_offset=9, limit=50)
        curses.noecho()
        return keyword

    def get_command(self):
        return self.screen.getkey()


