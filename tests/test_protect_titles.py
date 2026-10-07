"""Tests for bin/protect-titles. Run: python3 -m unittest discover tests"""
import importlib.machinery
import importlib.util
import pathlib
import unittest

path = pathlib.Path(__file__).resolve().parent.parent / 'bin' / 'protect-titles'
loader = importlib.machinery.SourceFileLoader('protect_titles', str(path))
spec = importlib.util.spec_from_loader('protect_titles', loader)
pt = importlib.util.module_from_spec(spec)
loader.exec_module(pt)


class Protect(unittest.TestCase):
    def test_wraps_bare_title(self):
        self.assertEqual(pt.protect('  title = {Model Training Anatomy},'),
                         '  title = {{Model Training Anatomy}},')

    def test_wraps_title_with_inner_braces(self):
        self.assertEqual(pt.protect('  title = {Reverse Optical Probing ({{ROPING}})},'),
                         '  title = {{Reverse Optical Probing ({{ROPING}})}},')

    def test_leaves_wrapped_title(self):
        line = '  journaltitle = {{Neuron}},'
        self.assertEqual(pt.protect(line), line)

    def test_inner_groups_are_not_a_full_wrap(self):
        self.assertEqual(pt.protect('  title = {{A} and {B}}'), '  title = {{{A} and {B}}}')

    def test_other_fields_untouched(self):
        line = '  author = {Cisek, Paul},'
        self.assertEqual(pt.protect(line), line)

    def test_idempotent(self):
        text = '@article{X,\n  title = {Foo Bar},\n  booktitle = {Proc. {{ICLR}}},\n}\n'
        once = pt.protect(text)
        self.assertEqual(pt.protect(once), once)


if __name__ == '__main__':
    unittest.main()
