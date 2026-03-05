# Application configuration defaults

# Flask settings
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
FLASK_DEBUG = False

# Generator settings
DEFAULT_CHECK_PERIOD = "24x7"
DEFAULT_NOTIFICATION_INTERVAL = 30
DEFAULT_MAX_CHECK_ATTEMPTS = 5

# Nagios defaults
NAGIOS_CHECK_COMMANDS = [
    "check-host-alive",
    "check_ping",
    "check_http",
    "check_ssh",
    "check_disk",
    "check_load",
    "check_procs",
    "check_swap",
    "check_tcp",
    "check_udp",
    "check_dns",
    "check_ftp",
    "check_smtp",
    "check_pop",
    "check_imap",
    "check_nt",
    "check_nrpe",
]

NAGIOS_TIME_PERIODS = [
    "24x7",
    "workhours",
    "nonworkhours",
    "never",
]

NAGIOS_NOTIFICATION_OPTIONS_SERVICE = "w,u,c,r"
NAGIOS_NOTIFICATION_OPTIONS_HOST = "d,u,r"
