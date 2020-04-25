from python_console_menu import AbstractMenu, MenuItem


class MecanumMenu(AbstractMenu):
    show_hidden_menu = False

    def __init__(self):
        super().__init__("Welcome to the test menu.")

    def initialise(self):
        self.add_menu_item(MenuItem(0, "Exit menu").set_as_exit_option())
        self.add_menu_item(MenuItem(1, "Forward", print("move forward")))
        self.add_menu_item(MenuItem(2, "Backward", lambda: print("move backward")))


demoMenu = MecanumMenu()
demoMenu.display()
