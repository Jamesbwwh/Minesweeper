import Minefield
import quicksort
import gtk
import copy
import thread
import time
import threading
import gobject

mineField = []
frameField = []
mines = 0
flags = 0
name = ''
gIndex = 0
periodic_timer = None
colors = ["#1B1B1B","#2E5894","#00FF00","#FF2800","#062A78","green","green","green","green","red"]

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
        if str(mineField[i][j]) is '0':
            label = gtk.Label()
        else:
            label = gtk.Label(str(mineField[i][j]))
            label.set_markup('<b><span color="%s">%s</span></b>'%((colors[(mineField[i][j])],str(mineField[i][j]))))
        label.set_size_request(20, 20)
        frame.add(label)
        frame.set_shadow_type(gtk.SHADOW_OUT)
        label.show()

class New:
    def quit_event(self, widget):
        self.window.destroy()

    def reset_stats_event(self, widget):
        pass

    def __init__(self):
        self.builder = gtk.glade.XML("new.glade")
        self.window = self.builder.get_widget("messagedialog1")
        self.builder.connect_signals(self)

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
        self.window = self.builder.get_object("window1")
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
        self.window = self.builder.get_object("window1")
        self.window.show_all()

class PeriodicTimer:
    def __init__(self, timeout, builder):
        self.counter = 0
        self.startTimer = True
        self.labela = builder.get_object("lblTime")
        gobject.timeout_add_seconds(timeout, self.ticks)

    def ticks(self):
        self.labela.set_text('Time:' + str(self.counter))
        self.counter += 1
        if self.startTimer:
            return True

    def stop(self):
        self.startTimer = False
        return self.counter

def youWinDialog():
    dialog = gtk.MessageDialog(None,gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_INFO,gtk.BUTTONS_OK,None)
    dialog.set_title("Win")
    dialog.format_secondary_markup("You Win !!!")
    dialog.show_all()
    dialog.run()
    dialog.destroy()

class Minesweeper:
    def quit_event(self, widget):
        self.window.destroy()
        gtk.main_quit()

    def new_game_event(self, widget):
        self.window.destroy()
        gtk.main_quit()
        main = Minesweeper()
        gtk.main()

    def options_event(self, widget):
        options = Options()

    def statistics_event(self, widget):
        statistics = Statistics()

    def about_event(self, widget):
        about = About()

    def highscore_event(self, widget):
        app_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        app_window.set_size_request(500, 100)
        app_window.set_title("Hall of Fame")

        hbox_b = gtk.VBox(False, 0)
        app_window.add(hbox_b)
        halloffame = []
        with open("highscore.txt", "r") as f:
            for line in f:
                data = line.split(",")
                data[1] = int(data[1])
                data[0], data[1] = data[1], data[0]
                halloffame.append(data)
        halloffame = quicksort.QuickSort(halloffame)
        label_b = gtk.Label("%15s,        Time" % "Name")
        label_b.show()
        hbox_b.pack_start(label_b, False, False, 0)
        for entry in halloffame:
            label_b = gtk.Label(entry[1] + ",        " + str(entry[0]))
            label_b.show()
            hbox_b.pack_start(label_b, False, False, 0)
        hbox_b.show()
        app_window.show()

    def button_event(self, widget, event, i, j):
        global mines                                            # Global mines - No. Mines
        global flags                                            # Global flags - No. Mines left
        global colors
        global name

        if event.button is 1:
            if mineField[i][j] is 9:                            # If it is a Mine
                label = gtk.Label(str('X'))                     # Label it as "X"
                label.set_markup('<b><span color="%s">%s</span></b>'%((colors[0],'X')))
                label.set_size_request(20, 20)
                frame = widget.parent
                frame.remove(widget)
                frame.add(label)
                frame.set_shadow_type(gtk.SHADOW_OUT)
                label.show()
                periodic_timer.stop()

                for i in range(len(mineField)):                 # Since lost already due to clicking on mine
                    for j in range(len(mineField)):             # Reveal the entire grid to player
                        if mineField[i][j] is 9:                # if it is a Mine
                            label = gtk.Label(str('Z'))
                            label.set_markup('<b><span color="%s">%s</span></b>'%((colors[9],'Z')))
                        elif mineField[i][j] is 0:              # if empty box
                            label = gtk.Label(str(' '))
                        else:                                   # those number tiles
                            label = gtk.Label(str(mineField[i][j]))
                            label.set_markup('<b><span color="%s">%s</span></b>'%((colors[(mineField[i][j])],str(mineField[i][j]))))


                        # label.set_markup('<span color="red">Z</span>')


                        label.set_size_request(20, 20)
                        frame = frameField[i][j]
                        widget = frame.get_child()
                        if type(widget) is type(gtk.Button()):
                            frame.remove(widget)
                            frame.add(label)
                            frame.set_shadow_type(gtk.SHADOW_OUT)
                            label.show()

                md = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_YES_NO, "Explosion")
                md.set_title("Lose")
                md.format_secondary_text("You lose !!. Restart?")
                explodeimg = gtk.Image()
                explodeimg.set_from_file("mine-explode.png") #load mine explode icon in
                md.set_image(explodeimg)
                md.show_all()

                f = open('highscore.txt','a')               # Update Score to txt
                if not name:
                        name = "anonymous"
                f.write("%s,%s\n" % (name,"-1"))
                f.close()

                response = md.run()
                if response == gtk.RESPONSE_YES:                  # if player want to replay
                    md.destroy()
                    self.new_game_event(None)
                else:                                           # if player do not want to replay
                    md.destroy()

            elif mineField[i][j] is 0:                          # if player click on empty tiles
                map = copy.deepcopy(mineField)
                exploreMineless(map, i, j)

                count = 0
                for i in range(len(mineField)):                 # Check for winning based on no.  of un-open tiles
                    for j in range(len(mineField)):
                        frame = frameField[i][j]
                        if type(frame.get_child()) is type(gtk.Button()):  # Number of un-open tiles left
                            count += 1
                if (count == mines):
                    score = periodic_timer.stop()
                    youWinDialog()
                    f = open('highscore.txt','a')               # Update Score to txt
                    if not name:
                        name = "anonymous"
                    f.write("%s,%s\n" % (name,str(score)))
                    f.close()

            else:
                label = gtk.Label(str(mineField[i][j]))         # if player click on number tiles.
                label.set_markup('<b><span color="%s">%s</span></b>'%((colors[(mineField[i][j])],str(mineField[i][j]))))
                label.set_size_request(20, 20)
                frame = widget.parent
                frame.remove(widget)
                frame.add(label)
                frame.set_shadow_type(gtk.SHADOW_OUT)
                label.show()

                count = 0
                for i in range(len(mineField)):                 # Check for winning based on no.  of un-open tiles
                    for j in range(len(mineField)):
                        frame = frameField[i][j]
                        if type(frame.get_child()) is type(gtk.Button()):  # Number of un-open tiles left
                            count += 1
                if (count == mines):
                    score = periodic_timer.stop()
                    youWinDialog()
                    f = open('highscore.txt','a')               # Update Score to txt
                    if not name:
                        name = "anonymous"
                    f.write("%s,%s\n" % (name,str(score)))
                    f.close()

        elif event.button is 3:                                 # Update of tiles to flag or un-flag it
            if widget.get_label() is "F":
                widget.set_label("")
                flags += 1                                      # Update mine counter accordingly
            else:
                widget.set_label("F")
                flags -= 1                                      # Update mine counter accordingly

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
        global name
        global g_combo_selected

        dialog = gtk.MessageDialog(None,gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_QUESTION,gtk.BUTTONS_OK,None)
        combo_box = gtk.combo_box_new_text()
        combo_box.append_text("Easy")
        combo_box.append_text("Medium")
        combo_box.append_text("Hard")
        combo_box.append_text("Really Hard")
        combo_box.connect('changed', self.combo_select_callback)
        combo_box.set_active(0)                                  # set the default option to be shown
        combo_box.show()
        dialog.add_action_widget(combo_box,0)
        dialog.set_title("Player Name")
        dialog.set_markup('Please enter your <b>username</b>:')
        entry = gtk.Entry()                                      # Create the text input field
        entry.connect("activate", self.responseToDialog, gtk.RESPONSE_OK)# Allow the user to press enter to do ok
        hbox = gtk.HBox()                                        # Create a horizontal box to pack the
                                                                 # entry and a
                                                                                          # label
        hbox.pack_start(gtk.Label("Name:"), False, 5, 5)
        hbox.pack_end(entry)
        dialog.format_secondary_markup("This will be used for <i>highscore</i> purposes")
        dialog.vbox.pack_end(hbox, True, True, 0)                # Add it and show it
        dialog.show_all()
        dialog.run()
        name = entry.get_text()
        dialog.destroy()

    def mineThread(self):
        while(True):
            self.minelabel.set_text('Mines:' + str(mines))
            
    def __init__(self):
        global mineField
        global frameField
        global mines
        global flags
        global periodic_timer
        self.getUserName()

        self.builder = gtk.Builder()
        self.builder.add_from_file("minesweeper.glade")
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("Minesweeper")
        self.minelabel = self.builder.get_object("lblMines")
        vbox = self.builder.get_object("vBox")
        periodic_timer = PeriodicTimer(1, self.builder)
        try:
            thread.start_new_thread(self.mineThread,())
        except:
            print "Error start mine thread"

        mineField, mines = Minefield.generate(gIndex + 1)
        flags = mines
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

main = Minesweeper()
gtk.main()
