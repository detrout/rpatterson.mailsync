import subprocess, optparse, pkg_resources, logging

logger = logging.getLogger('rpatterson.mailsync')

class Watcher(object):

    def __init__(self, maildir, checker):
        args = ['watch_maildirs', '--maildir=%s' % maildir]
        logger.info("Running '%s'" % ' '.join(args))
        self.watcher = subprocess.Popen(args , stdout=subprocess.PIPE)
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
