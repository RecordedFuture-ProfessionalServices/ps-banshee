##################################### TERMS OF USE ###########################################
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
    'delete_sandbox_sample': '.delete',
    'SandboxStats': '.helpers',
    'create_sandbox_profile': '.profiles',
    'delete_sandbox_profile': '.profiles',
    'get_sandbox_profile': '.profiles',
    'list_sandbox_profiles': '.profiles',
    'update_sandbox_profile': '.profiles',
    'fetch_behavioral_reports': '.reports',
    'fetch_overview_report': '.reports',
    'fetch_static_report': '.reports',
    'list_sandbox_samples': '.samples_list',
    'fetch_sandbox_stats': '.stats',
    'print_sandbox_stats': '.stats_output',
    'set_sandbox_sample_profile': '.submit',
    'submit_sandbox_sample': '.submit',
}


def __getattr__(name):
    if name in _LAZY:
        mod = import_module(_LAZY[name], __name__)
        val = getattr(mod, name)
        globals()[name] = val
        return val
    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')


def __dir__():
    return sorted({*globals(), *_LAZY})


__all__ = list(_LAZY)
