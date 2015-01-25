import gtk

class Minesweeper:

    def on_window1_destroy(self, object, data=None):
        gtk.main_quit()

    def on_gtk_quit_activate(self, menuitem, data=None):
        gtk.main_quit()

    def __init__(self):
        self.gladefile = "minesweeper.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("window1")
        self.window.set_title("Minesweeper")
        vbox = self.builder.get_object("vbox1")
        for i in range(10):
            hbox = gtk.HBox()
            vbox.pack_start(hbox, False, False, 0)
            for j in range(10):
                button = gtk.Button(str(i + j))
                button.set_size_request(50, 50)
                hbox.pack_start(button, False, False, 0)
        self.window.show_all()

main = Minesweeper()
gtk.main()
