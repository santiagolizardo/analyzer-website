
import sys
sys.path.append('library')

import unittest

from html.libraries import findLibrariesInCode

class TestHtmlLibraries(unittest.TestCase):

    def test_no_libraries(self):
        libraries = findLibrariesInCode('')
        self.assertEqual([], libraries)

    def test_library_found(self):
        libraries = findLibrariesInCode('<script src="/bootstrap.min.js"></script>')
        expected_libs = [
	    { 'name': 'Bootstrap', 'pattern': [ r'bootstrap.min.js' ], 'website': 'http://getbootstrap.com/' },
        ]
        self.assertEqual(expected_libs, libraries)

if __name__ == '__main__':
    unittest.main()

