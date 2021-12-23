
class LoadConfiguration:
    """ Load Them All configuration object """
    def __init__(self):
        # Vector/Raster tab
        self.base_dir = ''
        self.extension = ''

        # Configuration tab
        self.b_groups = False
        self.b_layers_off = False
        self.b_not_empty = True
        self.b_sort = True
        self.b_reverse_sort = False
        self.b_case_insensitive = True
        self.b_accent_insensitive = False
        self.b_styles = False
        self.b_search_parent_layer = False
        self.b_add_parent_layer_name = True
        self.num_layers_to_confirm = 50
