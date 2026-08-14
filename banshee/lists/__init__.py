#################################### TERMS OF USE ###########################################
# The following code is provided for demonstration purpose only, and should not be used      #
# without independent verification. Recorded Future makes no representations or warranties,  #
# express, implied, statutory, or otherwise, regarding any aspect of this code or of the     #
# information it may retrieve, and provides it both strictly “as-is” and without assuming    #
# responsibility for any information it may retrieve. Recorded Future shall not be liable    #
# for, and you assume all risk of using, the foregoing. By using this code, Customer         #
# represents that it is solely responsible for having all necessary licenses, permissions,   #
# rights, and/or consents to connect to third party APIs, and that it is solely responsible  #
# for having all necessary licenses, permissions, rights, and/or consents to any data        #
# accessed from any third party API.                                                         #
##############################################################################################

from importlib import import_module

_LAZY = {
    'add_entity': '.list_add',
    'bulk_add_entities': '.list_bulk_add',
    'bulk_remove_entities': '.list_bulk_remove',
    'clear_list': '.list_clear',
    'copy_list': '.list_copy',
    'create_list': '.list_create',
    'fetch_entities': '.list_entities',
    'fetch_entries': '.list_entries',
    'fetch_list_info': '.list_info',
    'remove_entity': '.list_remove',
    'search_lists': '.list_search',
    'fetch_list_status': '.list_status',
}


def __getattr__(name):
    if name in _LAZY:
        mod = import_module(_LAZY[name], __name__)
        val = getattr(mod, name)
        globals()[name] = val
        return val
    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')


__all__ = list(_LAZY)
