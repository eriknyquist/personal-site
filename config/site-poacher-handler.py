import os

from time import gmtime, strftime

FIFO='/home/ubuntu/poacherfifo'

def write_to_fifo(data):
    try:
        fd = os.open(FIFO, os.O_CREAT | os.O_WRONLY | os.O_NONBLOCK)
        os.write(fd, data)
        os.close(fd)
    except OSError as ex:
        pass


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
    try:
        size = repo.size
    except:
        size = 0

    if not os.path.exists(FIFO):
        return False

    write_to_fifo('%s: %s (%s)\n' % (strftime("%Y-%m-%d %H:%M:%S", gmtime()),
        repo.url, humanize_bytes(repo.size)))

    return False
