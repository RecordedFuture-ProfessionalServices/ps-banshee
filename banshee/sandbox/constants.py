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

SCORE_BUCKETS = (
    (8, 'malicious'),
    (5, 'suspicious'),
    (3, 'potentially_suspicious'),
    (1, 'clean'),
)

SCORE_COLORS = {
    'malicious': 'red',
    'suspicious': 'dark_orange',
    'potentially_suspicious': 'yellow',
    'clean': 'green',
    'unknown': 'grey50',
}

SCORE_LABELS = {
    'malicious': 'MALICIOUS',
    'suspicious': 'SUSPICIOUS',
    'potentially_suspicious': 'LIKELY BENIGN',
    'clean': 'NO THREAT',
    'unknown': 'UNKNOWN',
}

SCORE_SHORT_LABELS = {
    'malicious': 'malicious (8–10)',
    'suspicious': 'suspicious (5–7)',
    'potentially_suspicious': 'likely benign (3–4)',
    'clean': 'no threat (1–2)',
    'unknown': 'unknown',
}

ARCH_FILE_TAGS = {
    'pe',
    'pe32',
    'pe64',
    'x86',
    'x64',
    'elf',
    'mach-o',
    'apk',
    'dex',
    'office',
    'doc',
    'docx',
    'xls',
    'xlsx',
    'pdf',
    'powershell',
    'vbs',
    'js',
    'jscript',
    'script',
    'bat',
    'cmd',
    'hta',
    'jar',
    'zip',
    'archive',
    'iso',
    'img',
    'lnk',
    'dll',
    'exe',
    'sh',
    'ps1',
    'msi',
    'wsf',
    'vhd',
    'rar',
    'msg',
}

PLATFORM_PACKER_TAGS = {
    'linux',
    'macos',
    'android',
    'windows',
    'upx',
    'packed',
    'obfuscated',
    'armv7',
    'armv8',
    'arm',
    'mips',
    'mipsel',
}

SANDBOX_FRONTEND_URLS = {
    'eu': 'https://sandbox.recordedfuture.com',
    'usa': 'https://us-sandbox.recordedfuture.com',
    'apj': 'https://apj-sandbox.recordedfuture.com',
    'public': 'https://tria.ge',
    'private': 'https://private.tria.ge',
}

INTEL_CARD_BASE = 'https://app.recordedfuture.com/portal/intelligence-card'
INTEL_CARD_TYPE = {
    'IpAddress': 'ip',
    'InternetDomainName': 'idn',
    'URL': 'url',
    'Hash': 'hash',
}

DISPLAY_CAP = 10
MORE_MSG = '  [dim]… and {} more (use JSON output for the full list)[/dim]'
BAR_CHAR = '█'

FAMILY_BADGE_BG = 'magenta'
TAG_BADGE_BG = 'grey23'
EMPTY_BAR_COLOR = 'grey23'

OVERVIEW_WORKERS = 50
SOAR_WORKERS = 10
SOAR_TOP_N = 50
SOAR_MIN_SCORE = 25
BEHAVIORAL_MAX_WORKERS = 10

SAMPLES_PAGE_SIZE = 200  # psengine caps samples_per_page at 200; the API's hard limit
SAMPLES_INITIAL_MAX_RESULTS = 2000

STATIC_WAIT_TIMEOUT = 600
OVERVIEW_WAIT_TIMEOUT = 1800
BEHAVIORAL_WAIT_TIMEOUT = 1800
