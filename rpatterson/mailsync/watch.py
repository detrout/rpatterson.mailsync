import os, sys, signal, subprocess, optparse, logging

logger = logging.getLogger('rpatterson.mailsync')

from rpatterson.mailsync import check

class Watcher(object):

    def __init__(self, maildir=None,
                 checker=check.EmacsclientChecker()):
        args = ['watch_maildirs']
        if maildir is not None:
            args.append('--maildir=%s' % maildir)
        logger.info("Running '%s'" % ' '.join(args))
        self.watcher = subprocess.Popen(
            args , stdin=subprocess.PIPE, stdout=subprocess.PIPE)
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
                folders = line.strip().split()
                logger.info("Running '%s'" % ' '.join(
                    self.checker.getArgs(*folders)))
                out, err = self.checker(*folders)
                if out:
                    logger.info('Checker output: %s' % out)
                if err:
                    logger.error('Checker error: %s' % err)
                yield line

    def __del__(self):
        """Ensure the watcher process is always killed on exit"""
        if self.watcher.poll() is None:
            os.kill(self.watcher.pid, signal.SIGTERM)
            self.watcher.wait()

    def printLines(self):
        for line in self:
            print line,
            sys.stdout.flush()

def main(args=None):
    parser = optparse.OptionParser()
    options, args = parser.parse_args(args=args)
    maildir, checker = args[:2]
    checker_factory = check.load_checker_factory(checker)
    checker = checker_factory(*args[2:])
    Watcher(maildir=maildir, checker=checker).printLines()

def gnus_main(args=None):
    parser = optparse.OptionParser()
    options, args = parser.parse_args(args=args)
    Watcher().printLines()

if __name__ == '__main__':
    main()
