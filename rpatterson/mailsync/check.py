import subprocess, pkg_resources

class Checker(object):

    def getArgs(self, *folders):
        raise NotImplementedError

    def __call__(self, *folders):
        args = self.getArgs(*folders)
        process = subprocess.Popen(
            args , stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        return process.communicate()

class EmacsclientChecker(Checker):

    def __init__(self, elisp_func='mailsync/gnus-check'):
        self.elisp_func = elisp_func

    def getArgs(self, *folders):
        folders = ' '.join(
            ('"%s"' % folder for folder in folders))
        return ['emacsclient', '--eval',
                '(%s (quote (%s)))' % (self.elisp_func, folders)]

class SSHChecker(Checker):

    def __init__(self, host, checker=EmacsclientChecker(),
                 checker_args=()):
        self.host = host
        self.checker = checker

    def getArgs(self, *folders):
        command = ["'%s'" % arg
                   for arg in self.checker.getArgs(*folders)]
        return ["ssh", self.host] + command

def load_checker_factory(checker):
    return pkg_resources.EntryPoint.parse(
        'checker = %s' % checker).load(require=False)
