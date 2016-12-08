import multiprocessing

backlog = 2048

proc_name = 'tippy'
bind = 'unix:/var/run/{0}.sock'.format(proc_name)

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
max_requests = 0
timeout = 30
keepalive = 2
debug = False
spew = False

logfile = '/var/log/tippy.log'
loglevel = 'info'
logconfig = None

