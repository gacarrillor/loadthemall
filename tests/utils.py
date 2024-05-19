from LoadThemAll.core.LoadConfiguration import LoadConfiguration


def get_configuration() -> LoadConfiguration:
    configuration = LoadConfiguration()
    configuration.base_dir = ""  # Override
    configuration.extension = []  # Override
    configuration.with_gui = False  # Suitable for tests

    configuration.b_groups = False
    configuration.b_search_in_compressed_files = False
    configuration.b_layers_off = False
    configuration.b_not_empty = True
    configuration.b_sort = True
    configuration.b_reverse_sort = False
    configuration.b_case_insensitive = True
    configuration.b_accent_insensitive = False
    configuration.b_styles = False
    configuration.b_search_parent_layer = False
    configuration.b_add_parent_layer_name = False
    configuration.num_layers_to_confirm = 50

    return configuration
