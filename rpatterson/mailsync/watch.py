import subprocess, optparse, pkg_resources, tempfile

class Watcher(object):

    def __init__(self, maildir, checker):
        self.watcher = subprocess.Popen(
            ['watch_maildirs', '--maildir=%s' % maildir],
            stdout=subprocess.PIPE)
        self.checker = checker

    def __iter__(self):
        while self.watcher.poll() is None:
            line = self.watcher.stdout.readline()
            if line:
                self.checker(*line.strip().split())
                yield line

def main(args=None):
    parser = optparse.OptionParser()
    options, args = parser.parse_args(args=args)
    maildir, checker = args
    checker = pkg_resources.EntryPoint.parse(
        'checker = %s' % checker).load(require=False)
    for line in Watcher(maildir=maildir, checker=checker):
        print line,

if __name__ == '__main__':
    main()
