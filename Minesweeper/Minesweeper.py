import gtk
import copy
import random
import Minefield

mineField = []
frameField = []

def generate(difficulty):
    global mineField
    mineField = Minefield.printMineField(difficulty)
    height = len(mineField)
    width = len(mineField[0])
    ranges = width * height
    mines = random.randint(ranges // 8, ranges // 7)
    ranges -= 1
    for mine in range(mines):
        while(True):
            placeMine = random.randint(0, ranges)
            x = placeMine // width
            y = placeMine % width
            if mineField[x][y] != 9:
                mineField[x][y] = 9
                if x - 1 >= 0: #Top
                    if y - 1 >= 0: #Top-Left
                        if mineField[x - 1][y - 1] != 9:
                            mineField[x - 1][y - 1] += 1
                    if mineField[x - 1][y] != 9:
                        mineField[x - 1][y] += 1
                    if y + 1 < width: #Top-Right
                        if mineField[x - 1][y + 1] != 9:
                            mineField[x - 1][y + 1] += 1
                if y - 1 >= 0: #Left
                    if mineField[x][y - 1] != 9:
                        mineField[x][y - 1] += 1
                if y + 1 < width: #Right
                    if mineField[x][y + 1] != 9:
                        mineField[x][y + 1] += 1
                if x + 1 < width: #Bottom
                    if y - 1 >= 0: #Bottom-Left
                        if mineField[x + 1][y - 1] != 9:
                            mineField[x + 1][y - 1] += 1
                    if mineField[x + 1][y] != 9:
                        mineField[x + 1][y] += 1
                    if y + 1 < width: #Bottom-Right
                        if mineField[x + 1][y + 1] != 9:
                            mineField[x + 1][y + 1] += 1
                break

def exploreMineless(world,i,j):
    N = len(world)
    M = len(world[0])
    if i < 0 or j < 0 or i >= N or j >= M:
        return
    if world[i][j] is 0:
        world[i][j] = 9
        exploreMineless(world,i - 1,j - 1) #top-left
        exploreMineless(world,i - 1,j) #top
        exploreMineless(world,i - 1,j + 1) #top-right
        exploreMineless(world,i,j - 1) #left
        exploreMineless(world,i,j + 1) #right
        exploreMineless(world,i + 1,j - 1) #bottom-left
        exploreMineless(world,i + 1,j) #bottom
        exploreMineless(world,i + 1,j + 1) #bottom-right
    frame = frameField[i][j]
    widget = frame.get_child()
    if type(widget) is type(gtk.Button()):
        frame.remove(widget)
        label = gtk.Label(str(mineField[i][j]))
        label.set_size_request(20, 20)
        frame.add(label)
        frame.set_shadow_type(gtk.SHADOW_OUT)
        label.show()

class About:
    def quit_event(self, widget):
        self.window.destroy()

    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("about.glade")
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("aboutMinesweeper")
        self.window.show_all()

class Options:
    def quit_event(self, widget):
        self.window.destroy()

    def ok_event(self, widget):
        pass

    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("options.glade")
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("Options")
        self.window.show_all()

class Statistics:
    def quit_event(self, widget):
        self.window.destroy()

    def reset_stats_event(self, widget):
        pass

    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("statistics.glade")
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("Statistics")
        self.window.show_all()

class Minesweeper:
    def quit_event(self, widget):
        self.window.destroy()
        gtk.main_quit()

    def new_game_event(self, widget):
        md = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_NONE, "New Game")
        md.run()

    def options_event(self, widget):
        md = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_NONE, "Options")
        md.run()

    def statistics_event(self, widget):
        md = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_NONE, "Statistics")
        md.run()

    def about_event(self, widget):
        md = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_NONE, "About")
        md.run()

    def button_event(self, widget, event, i, j):
        if event.button is 1:
            if mineField[i][j] is 9:
                md = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_NONE, "Explosion")
                md.run()
            elif mineField[i][j] is 0:
                map = copy.deepcopy(mineField)
                exploreMineless(map, i, j)
                pass
            else:
                label = gtk.Label(str(mineField[i][j]))
                label.set_size_request(20, 20)
                frame = widget.parent
                frame.remove(widget)
                frame.add(label)
                frame.set_shadow_type(gtk.SHADOW_OUT)
                label.show()
        elif event.button is 3:
            if widget.get_label() == "F":
                widget.set_label("")
            else:
                widget.set_label("F")

    def __init__(self):
        global frameField
        self.builder = gtk.Builder()
        self.builder.add_from_file("minesweeper.glade")
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("Minesweeper")
        vbox = self.builder.get_object("vBox")
        frameField = [[None] * len(mineField) for i in xrange(len(mineField[0]))]
        for i in range(len(mineField)):
            hbox = gtk.HBox()
            vbox.pack_start(hbox, False, False, 0)
            for j in range(len(mineField[0])):
                button = gtk.Button()
                button.connect("button_press_event", self.button_event, i, j)
                button.set_size_request(20, 20)
                frame = gtk.Frame()
                frame.add(button)
                frame.set_shadow_type(gtk.SHADOW_NONE)
                frameField[i][j] = frame
                hbox.pack_start(frame, False, False, 0)
        self.window.show_all()

generate(1)
main = Minesweeper()
gtk.main()
#for i in range(len(mineField)):
#    for j in range(len(mineField[i])):
#        print mineField[i][j],
#    print ""
