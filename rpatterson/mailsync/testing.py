import os, signal, tempfile, subprocess, shutil

class PrintingChecker(object):

    def __call__(self, *folders):
        print 'printChecker: '+' '.join(folders)

def makeMaildir(*path):
    subprocess.Popen(['maildirmake', os.path.join(*path)]).wait()

def setUp(test):
    watcher_script = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        'bin', 'mailsync_watch')
    tmp = tempfile.mkdtemp()
    maildir = os.path.join(tmp, 'Maildir')
    makeMaildir(maildir)
    foo = os.path.join(maildir, '.foo')
    makeMaildir(foo)
    test.globs.update(
        watcher_script=watcher_script, tmp=tmp, maildir=maildir, foo=foo)

def tearDown(test):
    shutil.rmtree(test.globs['tmp'])
