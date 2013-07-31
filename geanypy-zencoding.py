from gettext import gettext as _
from gi.repository import Gtk
import geany
import zencoding
from zencoding.utils import caret_placeholder

#~ _key_mod = namedtuple("KeyMod", 'KEY MOD')
#~ 
#~ _actions = { "expand_abbreviation": _key_mod(Gdk.KEY_e, Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.CONTROL_MASK),
	 #~ "expand_abbreviation_with_tab": _key_mod(Gdk.KEY_T, Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.CONTROL_MASK),
	 #~ "match_pair_inward": _key_mod(Gdk.KEY_L, Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.CONTROL_MASK),
	 #~ "match_pair_outward": _key_mod(Gdk.KEY_R, Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.CONTROL_MASK),
	 #~ "wrap_with_abbreviation": _key_mod(Gdk.KEY_q, Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.CONTROL_MASK),
	 #~ "prev_edit_point": _key_mod(Gdk.KEY_p, Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.CONTROL_MASK),
	 #~ "next_edit_point": _key_mod(Gdk.KEY_n, Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.CONTROL_MASK),
	 #~ "insert_formatted_newline": _key_mod(Gdk.KEY_l, Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.CONTROL_MASK),
	 #~ "select_line": _key_mod(Gdk.KEY_s, Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.CONTROL_MASK),
	 #~ "go_to_matching_pair": _key_mod(Gdk.KEY_m, Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.CONTROL_MASK),
	 #~ "merge_lines": _key_mod(Gdk.KEY_b, Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.CONTROL_MASK),
	 #~ "toggle_comment": _key_mod(Gdk.KEY_c, Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.CONTROL_MASK),
	 #~ "split_join_tag": _key_mod(Gdk.KEY_j, Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.CONTROL_MASK),
	 #~ "remove_tag": _key_mod(Gdk.KEY_r, Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.CONTROL_MASK),
	 #~ "increment_number_by_1": _key_mod(0, 0),
	 #~ "increment_number_by_10": _key_mod(0, 0),
	 #~ "increment_number_by_01": _key_mod(0, 0),
	 #~ "decrement_number_by_1": _key_mod(0, 0),
	 #~ "decrement_number_by_10": _key_mod(0, 0),
	 #~ "decrement_number_by_01": _key_mod(0, 0),
	#~ "evaluate_math_expression": _key_mod(0, 0)
    #~ }
actions = ("expand_abbreviation", "expand_abbreviation_with_tab", "match_pair_inward", "match_pair_outward","wrap_with_abbreviation", "prev_edit_point", "next_edit_point", "insert_formatted_newline", "select_line", "go_to_matching_pair", "merge_lines", "toggle_comment", "split_join_tag", "remove_tag", "increment_number_by_1", "increment_number_by_10", "increment_number_by_01", "decrement_number_by_1", "decrement_number_by_10", "decrement_number_by_01", "evaluate_math_expression")

def create_action_label():
    for action in actions:
        if action == "match_pair_outward":
            action = _("Match Tag Outward")
        elif action == "match_pair_inward":
            action = _("Match Tag Inward")
        elif action == "prev_edit_point":
            action = _("Previous Edit Point")
        elif action == "split_join_tag":
            action = _("Split or Join Tag")
        elif action == "increment_number_by_01":
            action = _("Increment Number by 0.1")
        elif action == "decrement_number_by_01":
            action = _("Decrement Number by 0.1")
        else:
            action = _(action.replace("_", " ").title())
        yield action

actions_dict = dict(zip([label for label in create_action_label()], actions))

class ZenEditor(object):

    def __init__(self, document):
        self.document = document
        self.scintilla = self.document.editor.scintilla
        self.active_profile = "xhtml"

    def get_selection_range(self):
        return (self.scintilla.get_selection_start(), self.scintilla.get_selection_end())

    def create_selection(self, start, end):
        self.scintilla.set_selection_start(start)
        self.scintilla.set_selection_end(end)
        
    def get_current_line_range(self):
        line = self.scintilla.get_current_line()
        line_start = self.scintilla.get_position_from_line(line)
        line_end = self.scintilla.get_line_end_position(line)
        return (line_start, line_end)

    def get_caret_pos(self):
        return self.scintilla.get_current_position()
        
    def set_caret_pos(self, pos):
        self.scintilla.set_current_position(pos)

    def get_current_line(self):
        return self.scintilla.get_current_line()
        
    def replace_content(self, text, start=-1, end=-1):
        sel_start, sel_end = self.get_selection_range()
        cur_pos = self.get_caret_pos()
        caret_pos = text.find(caret_placeholder) + cur_pos
        text = text.replace(caret_placeholder, "")
        if sel_start == sel_end:
            self.create_selection(start, end)
        self.scintilla.replace_sel(text)
        self.set_caret_pos(caret_pos)

    def get_content(self):
        return self.scintilla.get_contents(self.scintilla.get_length()+1)

    def get_syntax(self):
        syntax = "html"
        if self.document.file_type.name != 'PHP':
            syntax = self.document.file_type.name.lower()
        return syntax

    def get_profile_name(self):
        return self.active_profile

    def set_profile_name(self, profile):
        self.active_profile = profile

    @staticmethod
    def prompt(title=None):
        if title is None:
            title = _("Enter Abbreviation")
        dialog = Gtk.Dialog(title, geany.main_widgets.window, Gtk.DialogFlags.MODAL or Gtk.DialogFlags.DESTROY_WITH_PARENT, (Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,
             Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))
        dialog.set_default_size(300, -1)
        dialog.set_default_response(Gtk.ResponseType.ACCEPT)
        content_area = dialog.get_content_area()
        entry = Gtk.Entry()
        vbox = Gtk.VBox(False, 0)
        vbox.pack_start(entry, True, True, 0)
        vbox.set_border_width(12)
        content_area.add(vbox)
        vbox.show_all()
        response = dialog.run()
        abbr = None
        if response == Gtk.ResponseType.ACCEPT:
            abbr = entry.get_text()
        dialog.destroy()
        return abbr

    def get_selection(self):
        return self.scintilla.get_selection_contents()

    def get_file_path(self):
        return self.document.file_name

    def init_profiles(self):
        pass

class ZenCoding(geany.Plugin):

    __plugin_name__ = "Zencoding"
    __plugin_version__ = "0.1"
    __plugin_description__ = "Zencoding completely in geanpy."
    __plugin_author__ = "Sagar Chalise <chalisesagar@gmail.com>"

    def __init__(self):
        self.menu_item = Gtk.MenuItem(_("Zen Coding"))
        imenu = Gtk.Menu()
        for label in create_action_label():
            menu_item = Gtk.MenuItem(label)
            menu_item.connect("activate", self.on_action_item_activate, actions_dict[label])
            menu_item.show()
            imenu.append(menu_item)
            try:
                geany.bindings.register_binding("Zen Coding", label, self.on_key_activate, actions_dict[label])
            except AttributeError:
                geany.ui_utils.set_statusbar("GeanyPy was not compiled with keybindings support.")
        self.menu_item.set_submenu(imenu)
        self.menu_item.show()
        geany.main_widgets.tools_menu.append(self.menu_item)
        

    def cleanup(self):
        self.menu_item.destroy()

    @staticmethod
    def run_zencoding_action(action):
        file_types = ('HTML', 'PHP', 'XML', 'CSS')
        cur_file_type = geany.document.get_current().file_type.name
        if cur_file_type in file_types:
            doc = geany.document.get_current()
            zen_editor = ZenEditor(doc)
            zencoding.run_action(action, editor=zen_editor)
        
    def on_action_item_activate(self, data, action_key):
        self.run_zencoding_action(action_key)
        
    def on_key_activate(self, key_id, name):
        self.run_zencoding_action(name)