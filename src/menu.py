# RetroProbe - Retro Game/Computer Controller Probe & Tester
#
# Copyright (C) 2026, Ian Michael Dunmore
#
# License: https://github.com/idunmore/retroprobe/blob/master/LICENSE

# Built On:
#
# Adafruit CircuitPython 10.1.4 on 2026-03-09; Raspberry Pi Pico with rp2040
# (w/ 16MB flash memory)

# Standard Modules

# Circuit Python & Adafruit Modules
import board
import busio
import digitalio
import adafruit_ssd1306
import adafruit_framebuf

# Menu Constants
MENU_LINES = 5
MENU_WINDOW = 4

# Classes

class MenuBase:
    """Abstract base for all menu elements."""
    def __init__(self, display_name):
        self._display_name = display_name

    @property
    def display_name(self):
        return self._display_name

class MenuItem(MenuBase):
    """A selectable command/option that invokes a function."""
    def __init__(self, display_name, action):
        super().__init__(display_name)
        self._action = action

    def execute(self):
        self._action()

class Menu(MenuBase):
    """A navigable list of MenuItems and nested Menus."""

    # A Menu becomes a sub-menu simply by being added to another Menu.

    # Display is a 5-slot window: w/ up to 4 real entries plus a <More...> or
    # <Top...> navigation sentinel.  If more than 4 entries total, selecting
    # <More...> advances the window by 4; <Top...> resets to entry 0.
    def __init__(self, display_name):
        super().__init__(display_name)
        self._entries = []
        self._window_start = 0
        self._window_cursor = 0

    def add(self, entry):
        """Append an entry and return self for chaining."""
        self._entries.append(entry)
        return self
    
    def _visible(self):
        """Return the items for the current 5-slot display window."""
        n = len(self._entries)
        if n <= MENU_LINES:
            return list(self._entries)
        page = self._entries[self._window_start : self._window_start + MENU_WINDOW]
        at_end = self._window_start + MENU_WINDOW >= n
        return page + ['<Top...>' if at_end else '<More...>']

    @property
    def current(self):
        """The highlighted real entry, or None when on a sentinel."""
        visible = self._visible()
        if not visible:
            return None
        item = visible[self._window_cursor]
        return None if isinstance(item, str) else item

    def next(self):
        """Advance the cursor within the visible window, wrapping around."""
        visible = self._visible()
        if visible:
            self._window_cursor = (self._window_cursor + 1) % len(visible)

    def select(self):
        """
        Action the currently highlighted item.
        - <More...>: slide the window forward 4 entries.
        - <Top...>:  reset the window to the first entry.
        - Menu:      return it (caller pushes it onto the stack).
        - MenuItem:  execute its action.
        """
        visible = self._visible()
        if not visible:
            return None
        item = visible[self._window_cursor]
        if item == '<More...>':
            self._window_start += MENU_WINDOW
            self._window_cursor = 0
            return None
        if item == '<Top...>':
            self._window_start = 0
            self._window_cursor = 0
            return None
        if isinstance(item, Menu):
            return item
        if isinstance(item, MenuItem):
            item.execute()
        return None

    # --- display -----------------------------------------------------------

    def _item_label(self, item):
        """Return the display string for one visible item."""
        if isinstance(item, str):
            return item
        if isinstance(item, Menu):
            return f"[{item.display_name}]"
        return item.display_name

    def show(self, screen):
        """Render the current window."""
        screen.fill(0)
        screen.text(self._display_name[:25], 0, 1, 1)
        screen.hline(0, 12, 128, 1)
        for i, item in enumerate(self._visible()):
            cursor = chr(16) if i == self._window_cursor else " "
            line = f"{cursor}{self._item_label(item)}"
            screen.text(line[:25], 0, 7 + (i+1) * 10, 1)
        screen.show()


class MenuSystem:
    """Run the Menu System as a Controller."""
    def __init__(self, root, screen, button_select, button_next, quittable=False):
        self._screen = screen
        self._button_select = button_select
        self._button_next = button_next
        self._stack = [root]
        self._running = False
        self._inject_navigation(root, is_root=True, add_quit=quittable)

    # Helper Methods

    def _back(self):
        if len(self._stack) > 1:
            self._stack.pop()

    def _quit(self):
        self._running = False

    def _inject_navigation(self, menu, *, is_root, add_quit=False):
        """Depth-first: add <Back...> to every nested Menu, optionally <Quit> to the root."""
        for entry in menu._entries:
            if isinstance(entry, Menu):
                self._inject_navigation(entry, is_root=False)

        if is_root:
            if add_quit:
                menu.add(MenuItem("<Quit>", self._quit))
        else:
            menu.add(MenuItem("<Back...>", self._back))

    # Public Interface

    @property
    def current_menu(self):
        return self._stack[-1]

    def next(self):
        self.current_menu.next()

    def select(self):
        submenu = self.current_menu.select()
        if submenu is not None:
            self._stack.append(submenu)

    def show(self):
        self.current_menu.show(self._screen)

    def run(self):
        """Start the MenuSystem"""        
        self._running = True

        while self._running:
            self.show()
            if not self._button_next.value:
                self.next()
            if not self._button_select.value:
                self.select()

                