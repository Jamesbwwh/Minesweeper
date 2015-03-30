import gtk
import copy
import random
import Minefield

mineField = []
frameField = []
score = 0
text = ''
gIndex = 0;

def generate(difficulty):

    global mineField

    mineField = Minefield.printMineField(difficulty)

    height = len(mineField)
    width = len(mineField[0])
    ranges = width * height
    mines = random.randint(ranges // 8, ranges // 7)

    print "Difficulty: ", difficulty, "Mines: ", mines, "Height: ", height, "Width: ", width

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

    global score

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

        score += 1

        if str(mineField[i][j]) is '0':
            label = gtk.Label(str( ))
        else:
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

        md = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, "New Game")
        md.format_secondary_text("Create a new Game.")
        response=md.run()
        if response==gtk.RESPONSE_OK:
            md.destroy()
            self.window.destroy()
            gtk.main_quit()

            generate(1)
            main = Minesweeper()

            gtk.main()

    def options_event(self, widget):
        md = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_NONE, "Options")
        md.run()

    def statistics_event(self, widget):
        md = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_NONE, "Statistics")
        md.run()

    def about_event(self, widget):
        about = About()

    def highscore_event(self, widget):
        app_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        app_window.set_size_request(500, 100)
        app_window.set_title("Hall of Fame")

        hbox_b = gtk.VBox(False, 0)
        app_window.add(hbox_b)
        with open("highscore.txt", "r") as ins:
            halloffame = []
            for line in ins:
                label_b = gtk.Label(line)
                label_b.show()
                hbox_b.pack_start(label_b, False, False, 0)

        hbox_b.show()
        app_window.show()


    def button_event(self, widget, event, i, j):
        global score
        if event.button is 1:
            if mineField[i][j] is 9:

                label = gtk.Label(str('X'))
                label.set_size_request(20, 20)
                frame = widget.parent
                frame.remove(widget)
                frame.add(label)
                frame.set_shadow_type(gtk.SHADOW_OUT)
                label.show()

                md = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_YES_NO, "Explosion")
                md.format_secondary_text("You lose !!. Restart?")

                explodeimg = gtk.Image ()
                explodeimg.set_from_file ("mine-explode.png") #load mine explode icon in
                md.set_image(explodeimg)
                md.show_all()

                f = open('highscore.txt','a')
                f.write(text)
                f.write("\t")
                f.write(str(score))
                f.write("\n")
                f.close()

                response=md.run()
                if response==gtk.RESPONSE_YES:
                    score = 0
                    gtk.main_quit()
                    md.destroy()
                    self.window.destroy()
                    generate(1)
                    main = Minesweeper()
                    gtk.main()
                else:
                    md.destroy()
                    self.window.destroy()
                    gtk.main_quit()
                #md.run()

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

    def combo_select_callback(self, widget):

        global g_combo_selected
        global gIndex

        model = widget.get_model()
        gIndex = widget.get_active()
        if gIndex:
            g_combo_selected = model[gIndex][0]
        return



    def responseToDialog(entry, dialog, response):
        dialog.response(response)

    def getUserName(self):

        global text

        global g_combo_selected
        dialog = gtk.MessageDialog(None,gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_QUESTION,gtk.BUTTONS_OK,None)
        combo_box = gtk.combo_box_new_text()
        combo_box.append_text("Easy")
        combo_box.append_text("Medium")
        combo_box.append_text("Hard")
        combo_box.append_text("Really Hard")
        combo_box.connect('changed', self.combo_select_callback)
        combo_box.set_active(0)  # set the default option to be shown
        combo_box.show()
        dialog.add_action_widget(combo_box,0)
        dialog.set_markup('Please enter your <b>username</b>:')
        #create the text input field
        entry = gtk.Entry()
        #allow the user to press enter to do ok
        entry.connect("activate", self.responseToDialog, gtk.RESPONSE_OK)
        #create a horizontal box to pack the entry and a label
        hbox = gtk.HBox()
        hbox.pack_start(gtk.Label("Name:"), False, 5, 5)
        hbox.pack_end(entry)

        #some secondary text
        dialog.format_secondary_markup("This will be used for <i>highscore</i> purposes")
        #add it and show it
        dialog.vbox.pack_end(hbox, True, True, 0)
        dialog.show_all()
        #go go go
        dialog.run()

        text = entry.get_text()
        dialog.destroy()
        # print text

        #base this on a message dialog

    def __init__(self):

        self.getUserName()

        global frameField

        self.builder = gtk.Builder()
        self.builder.add_from_file("minesweeper.glade")
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("Minesweeper")
        vbox = self.builder.get_object("vBox")


        generate(gIndex+1)

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
        # print "Start6.3"

main = Minesweeper()
gtk.main()
#for i in range(len(mineField)):
#    for j in range(len(mineField[i])):
#        print mineField[i][j],
#    print ""
