"""Offline tests for bin/addref. Run: python3 -m unittest discover tests"""
import importlib.machinery
import importlib.util
import pathlib
import unittest

path = pathlib.Path(__file__).resolve().parent.parent / 'bin' / 'addref'
loader = importlib.machinery.SourceFileLoader('addref', str(path))
spec = importlib.util.spec_from_loader('addref', loader)
addref = importlib.util.module_from_spec(spec)
loader.exec_module(addref)


class DoiFromText(unittest.TestCase):
    cases = {
        '10.1146/annurev.neuro.31.060407.125606': '10.1146/annurev.neuro.31.060407.125606',
        'https://doi.org/10.1523/JNEUROSCI.23-23-08432.2003': '10.1523/jneurosci.23-23-08432.2003',
        'doi:10.1038/nature12345.': '10.1038/nature12345',
        'https://www.annualreviews.org/doi/10.1146/annurev.neuro.31.060407.125606':
            '10.1146/annurev.neuro.31.060407.125606',
        'https://onlinelibrary.wiley.com/doi/full/10.1002/syn.20316': '10.1002/syn.20316',
        'https://www.biorxiv.org/content/10.1101/2021.02.15.431238v1.full.pdf': '10.1101/2021.02.15.431238',
        'https://arxiv.org/abs/1606.08415v3': '10.48550/arxiv.1606.08415',
        'https://arxiv.org/pdf/2005.11401': '10.48550/arxiv.2005.11401',
        'https://link.springer.com/article/10.3758%2FBF03327224': '10.3758/bf03327224',
        'https://example.com/paper': None,
    }

    def test_cases(self):
        for text, want in self.cases.items():
            with self.subTest(text=text):
                self.assertEqual(addref.doi_from_text(text), want)


class DoiFromHtml(unittest.TestCase):
    def test_citation_doi_meta(self):
        page = '<head><meta name="citation_doi" content="10.1016/j.nlm.2004.06.005"></head>'
        self.assertEqual(addref.doi_from_html(page), '10.1016/j.nlm.2004.06.005')

    def test_dc_identifier_with_prefix(self):
        page = '<meta name="dc.identifier" content="doi:10.1126/science.7414331" />'
        self.assertEqual(addref.doi_from_html(page), '10.1126/science.7414331')

    def test_no_meta(self):
        self.assertIsNone(addref.doi_from_html('<html><body>no doi here</body></html>'))


class PubmedPattern(unittest.TestCase):
    def test_urls_and_prefix(self):
        for text in ['https://pubmed.ncbi.nlm.nih.gov/17510549/', 'https://www.ncbi.nlm.nih.gov/pubmed/17510549',
                     'PMID: 17510549']:
            with self.subTest(text=text):
                self.assertEqual(addref.PUBMED_RE.search(text).group(1), '17510549')


class LibraryDois(unittest.TestCase):
    bib = (
        '@article{Squire04,\n  title = {Memory Systems},\n  doi = {10.1016/J.NLM.2004.06.005},\n}\n\n'
        '@online{OtherOtherf,\n  title = {A Web Page},\n  url = {https://example.com},\n}\n\n'
        '@article{Cisek22,\n  doi = {https://doi.org/10.1098/rstb.2020.0522},\n}\n')

    def test_maps_doi_to_key(self):
        got = addref.library_dois(self.bib)
        self.assertEqual(got, {'10.1016/j.nlm.2004.06.005': 'Squire04', '10.1098/rstb.2020.0522': 'Cisek22'})


if __name__ == '__main__':
    unittest.main()
