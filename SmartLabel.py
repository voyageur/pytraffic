## PyTraffic -- A python simulation of the game Rush Hour invented by
## Nob Yoshigahara and commercialized by Binary Arts Corporation.
##
## Copyright (C) 2001-2005 Michel Van den Bergh <michel.vandenbergh@uhasselt.be>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; see the file COPYING.
## If not, write to the Free Software Foundation, Inc.,
## 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
##


from gi.repository import Gtk, Gdk, Pango

class SmartLabel(Gtk.EventBox):
    def __init__(self, text=""):
        Gtk.EventBox.__init__(self)
        self.label = Gtk.Label(label=text)
        self.add(self.label)
        # GTK3: get font metrics via Pango context (get_font is deprecated)
        font_desc = self.label.get_pango_context().get_font_description()
        font_metrics = self.label.get_pango_context().get_metrics(font_desc)
        self.approximate_char_width = font_metrics.get_approximate_char_width()
        self._css_provider = Gtk.CssProvider()
        self.get_style_context().add_provider(self._css_provider,
                                              Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def modify_bg(self, color):
        # GTK3: use CSS for background color instead of deprecated modify_bg
        if isinstance(color, Gdk.RGBA):
            rgba = color
        elif isinstance(color, Gdk.Color):
            rgba = Gdk.RGBA(color.red / 65535.0,
                            color.green / 65535.0,
                            color.blue / 65535.0, 1.0)
        else:
            rgba = Gdk.RGBA()
            rgba.parse(str(color))
        css = "* { background-color: rgba(%d,%d,%d,%f); }" % (
            int(rgba.red * 255),
            int(rgba.green * 255),
            int(rgba.blue * 255),
            rgba.alpha)
        self._css_provider.load_from_data(css.encode())

    def reset_bg(self):
        self._css_provider.load_from_data(b"")

    def set_char_width(self, n):
        self.set_size_request(n * self.approximate_char_width // Pango.SCALE, -1)

    def set_anchor(self, s=''):
        if s == 'e':
            self.label.set_halign(Gtk.Align.END)
        elif s == 'w':
            self.label.set_halign(Gtk.Align.START)
        else:
            self.label.set_halign(Gtk.Align.CENTER)

    def set_text(self, text):
        self.label.set_text(text)

    def set_sensitive(self, gtk_boolean):
        self.label.set_sensitive(gtk_boolean)
