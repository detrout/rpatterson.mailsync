"""Watch a given Maildir and returning change notifications optionally
checking changed folders before returning the notification"""

import os, sys, signal, subprocess, optparse, logging

from rpatterson.mailsync import parse, check

logging.basicConfig()
logger = logging.getLogger('rpatterson.mailsync')

parser = optparse.OptionParser(description=__doc__)
parser.set_defaults(checker=check.EmacsclientChecker)
parser.add_option(
    '-m', '--maildir', metavar='DIR', help=
    'Override the setting of the $MAILDIR environment variable (or '
    '~/Maildir if $MAILDIR is not defined) with DIR.')
parser.add_option(
    '-c', '--checker', type="string", action='callback',
    callback=check.get_checker, metavar='ENTRYPOINT', help=
    'Check folder using the checker at the stuptools ENTRYPOINT when '
    'folders are modified')
parse.add_options(parser, check.parser, 'Checkers')

class Watcher(object):
    __doc__ = __doc__

    def __init__(self, maildir=parser.defaults['maildir'],
                 checker=check.EmacsclientChecker(), **kw):
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
                self.check(line)
                yield line

    def __del__(self):
        """Ensure the watcher process is always killed on exit"""
        if self.watcher.poll() is None:
            os.kill(self.watcher.pid, signal.SIGTERM)
            self.watcher.wait()

    def check(self, line):
        folders = line.strip().split()
        logger.info("Running '%s'" % ' '.join(
            self.checker.getArgs(*folders)))
        out, err = self.checker(*folders)
        if out:
            logger.info('Checker output: %s' % out)
        if err:
            logger.error('Checker error: %s' % err)
                
    def printLines(self):
        for line in self:
            print line,
            sys.stdout.flush()

def main(args=None):
    options, args = parser.parse_args(args=args)
    options.checker = options.checker(**options.__dict__)
    Watcher(**options.__dict__).printLines()

gnus_parser = optparse.OptionParser(description=Watcher.__doc__)
gnus_parser.add_option(parser.get_option('--maildir'))
parse.add_options(gnus_parser, check.EmacsclientChecker.parser,
                  'Emacsclient Checker') 

def gnus_main(args=None):
    options, args = gnus_parser.parse_args(args=args)
    options.checker = check.EmacsclientChecker(**options.__dict__)
    Watcher(**options.__dict__).printLines()

if __name__ == '__main__':
    main()
