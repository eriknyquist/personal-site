import os
from time import gmtime, strftime

def humanize_bytes(size_bytes, precision=1):
    abbrevs = [
        (1<<20L, 'GB'),
        (1<<10L, 'MB'),
        (1, 'kB')
    ]

    if size_bytes == 0:
        return '0'
    elif size_bytes == 1:
        return '1 kB'

    for factor, suffix in abbrevs:
        if size_bytes >= factor:
            break

    return '%.*f %s' % (precision, float(size_bytes) / factor, suffix)

def run(repo_path, repo, log):
    fifo='/home/ubuntu/poacherfifo'
    try:
        size = repo.size
    except:
        size = 0

    if not os.path.exists(fifo):
        return False

    with open(fifo, 'w') as fh:
        fh.write('%s: %s (%s)\n' % (strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            repo.url, humanize_bytes(size)))

    return False
