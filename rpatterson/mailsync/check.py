import logging, subprocess, pkg_resources

logger = logging.getLogger('rpatterson.mailsync')

class Checker(object):

    def getArgs(self, *folders):
        raise NotImplementedError

    def __call__(self, *folders):
        args = self.getArgs(*folders)
        logger.info("Running '%s'" % ' '.join(args))
        process = subprocess.Popen(
            args , stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        out, err = process.communicate()
        if out:
            logger.info('Checker output: %s' % out)
        if err:
            logger.error('Checker error: %s' % err)

class EmacsclientChecker(Checker):

    def __init__(self, elisp_func='mailsync/gnus-check'):
        self.elisp_func = elisp_func

    def getArgs(self, *folders):
        folders = ' '.join(
            ('"%s"' % folder for folder in folders))
        return ['emacsclient', '--eval',
                '(%s (quote (%s)))' % (self.elisp_func, folders)]

class SSHChecker(Checker):

    def __init__(self, host, checker, *checker_args):
        self.host = host
        self.checker = load_checker_factory(checker)(*checker_args)

    def getArgs(self, *folders):
        return ["ssh", self.host,
                "'%s'" % self.checker.getArgs(*folders)]

def load_checker_factory(checker):
    return pkg_resources.EntryPoint.parse(
        'checker = %s' % checker).load(require=False)
