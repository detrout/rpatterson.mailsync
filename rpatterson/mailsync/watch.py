import sys, subprocess, optparse, logging

logger = logging.getLogger('rpatterson.mailsync')

from rpatterson.mailsync import check

class Watcher(object):

    def __init__(self, maildir, checker):
        args = ['watch_maildirs', '--maildir=%s' % maildir]
        logger.info("Running '%s'" % ' '.join(args))
        self.watcher = subprocess.Popen(args , stdout=subprocess.PIPE)
        self.checker = checker

    # TODO iteration *should* work, but for some reason it blocks
    # def __iter__(self):
    #     for line in self.watcher.stdout:
    #         self.checker(*line.strip().split())
    #         yield line

    def __iter__(self):
        while self.watcher.poll() is None:
            line = self.watcher.stdout.readline()
            if line:
                self.checker(*line.strip().split())
                yield line

def main(args=None):
    parser = optparse.OptionParser()
    options, args = parser.parse_args(args=args)
    maildir, checker = args[:2]
    checker_factory = check.load_checker_factory(checker)
    checker = checker_factory(*args[2:])
    for line in Watcher(maildir=maildir, checker=checker):
        print line,
        sys.stdout.flush()

if __name__ == '__main__':
    main()
