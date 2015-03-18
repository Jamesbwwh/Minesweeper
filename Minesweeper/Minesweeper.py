import gtk
import random
import Minefield

mineField = []

def generate(difficulty):
    global mineField
    mineField = Minefield.printMineField(difficulty)
    height = len(mineField)
    width = len(mineField[0])
    ranges = width * height
    mines = random.randint(ranges // 4, ranges // 3)
    ranges -= 1
    for mine in range(mines):
        while(True):
            placeMine = random.randint(0, ranges)
            x = placeMine // width
            y = placeMine % width
            if mineField[x][y] != 9:
                mineField[x][y] = 9
                if x - 1 >= 0:
                    if y - 1 >= 0:
                        if mineField[x - 1][y - 1] != 9:
                            mineField[x - 1][y - 1] += 1
                    if mineField[x - 1][y] != 9:
                        mineField[x - 1][y] += 1
                    if y + 1 < width:
                        if mineField[x - 1][y + 1] != 9:
                            mineField[x - 1][y + 1] += 1
                if y - 1 >= 0:
                    if mineField[x][y - 1] != 9:
                        mineField[x][y - 1] += 1
                if y + 1 < width:
                    if mineField[x][y + 1] != 9:
                        mineField[x][y + 1] += 1
                if x + 1 < width:
                    if y - 1 >= 0:
                        if mineField[x + 1][y - 1] != 9:
                            mineField[x + 1][y - 1] += 1
                    if mineField[x + 1][y] != 9:
                        mineField[x + 1][y] += 1
                    if y + 1 < width:
                        if mineField[x + 1][y + 1] != 9:
                            mineField[x + 1][y + 1] += 1
                break

class Minesweeper:
    def quit_event(self, widget):
        self.window.destroy()

    def new_game_event(self, widget):
        md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE, "New Game")
        md.run()

    def options_event(self, widget):
        md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE, "Options")
        md.run()

    def statistics_event(self, widget):
        md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE, "Statistics")
        md.run()

    def about_event(self, widget):
        md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE, "About")
        md.run()

    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("minesweeper.glade")
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("Minesweeper")
        vbox = self.builder.get_object("vBox")
        for i in range(len(mineField)):
            hbox = gtk.HBox()
            vbox.pack_start(hbox, False, False, 0)
            for j in range(len(mineField[0])):
                button = gtk.Button(str(mineField[i][j]))
                button.set_size_request(20, 20)
                hbox.pack_start(button, False, False, 0)
        self.window.show_all()

generate(1)
main = Minesweeper()
gtk.main()
#for i in range(len(mineField)):
#    for j in range(len(mineField[i])):
#        print mineField[i][j],
#    print ""
