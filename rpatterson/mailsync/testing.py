import os, tempfile, subprocess

def makeMaildir(*path):
    subprocess.Popen(['maildirmake', os.path.join(*path)]).wait()

def setUp(test):
    watcher = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        'bin', 'mailsync_watch')
    tmp = tempfile.mkdtemp()
    maildir = os.path.join(tmp, 'Maildir')
    makeMaildir(maildir)
    foo = os.path.join(maildir, '.foo')
    makeMaildir(foo)
    test.globs.update(
        watcher=watcher, tmp=tmp, maildir=maildir, foo=foo)
