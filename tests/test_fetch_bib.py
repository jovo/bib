"""Offline tests for bin/fetch-bib's local-clone path. Run: python3 -m unittest discover tests"""
import os
import pathlib
import subprocess
import tempfile
import unittest

FETCH = pathlib.Path(__file__).resolve().parent.parent / 'bin' / 'fetch-bib'


def git(*args, cwd):
    subprocess.run(['git', *args], cwd=cwd, check=True, capture_output=True)


class LocalClone(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.origin = self.tmp / 'origin'
        self.origin.mkdir()
        git('init', '-q', '-b', 'main', cwd=self.origin)
        git('config', 'user.email', 't@t', cwd=self.origin)
        git('config', 'user.name', 't', cwd=self.origin)
        (self.origin / 'references.bib').write_text('@article{A01,}\n')
        git('add', '.', cwd=self.origin)
        git('commit', '-q', '-m', 'one', cwd=self.origin)
        self.clone = self.tmp / 'bib'
        git('clone', '-q', str(self.origin), str(self.clone), cwd=self.tmp)
        self.out = self.tmp / 'build' / 'references.bib'
        self.out.parent.mkdir()

    def run_fetch(self, bib_dir):
        env = {**os.environ, 'BIB_DIR': str(bib_dir)}
        return subprocess.run([str(FETCH), str(self.out)], env=env, capture_output=True, text=True)

    def test_pulls_then_links(self):
        (self.origin / 'references.bib').write_text('@article{A01,}\n@article{B02,}\n')
        git('commit', '-q', '-am', 'two', cwd=self.origin)
        r = self.run_fetch(self.clone)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(os.readlink(self.out), str(self.clone / 'references.bib'))
        self.assertIn('B02', self.out.read_text())

    def test_links_when_pull_fails(self):
        plain = self.tmp / 'plain'
        plain.mkdir()
        (plain / 'references.bib').write_text('@article{C03,}\n')
        r = self.run_fetch(plain)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('could not pull', r.stderr)
        self.assertIn('C03', self.out.read_text())


if __name__ == '__main__':
    unittest.main()
