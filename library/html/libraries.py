
import re

known_libraries = [
    {
        'name': 'Google Tag Manager',
        'pattern': [ r'googletagmanager.com' ],
        'website': 'https://www.google.co.uk/analytics/tag-manager/' },
    {
        'name': 'Google Analytics',
        'pattern': [ r'google-analytics.com', r'/ga.js' ],
        'website': 'https://www.google.com/analytics/' },
    { 'name': 'React',
        'pattern': [ r'react.js' ],
        'website': 'https://facebook.github.io/react/' },
    { 'name': 'Vue',
        'pattern': [ r'vue.js' ],
        'website': 'http://vuejs.org/' },
    { 'name': 'Optimizely Statistics',
        'pattern': [ r'optimizely.com' ],
        'website': 'https://www.optimizely.com/statistics/' },
    { 'name': 'jQuery',
        'pattern': [ r'jquery' ],
        'website': 'https://jquery.com/' },
    { 'name': 'Bootstrap',
        'pattern': [ r'bootstrap.min.js' ],
        'website': 'http://getbootstrap.com/' },
    { 'name': 'Normalize.css',
        'pattern': [ r'normalize.css' ],
        'website': 'https://necolas.github.io/normalize.css/' },
    { 'name': 'Modernizr',
        'pattern': [ r'modernizr' ],
        'website': 'https://modernizr.com/' },
]

def findLibrariesInCode(code):
    libraries = []
    for library in known_libraries:
        for pattern in library['pattern']:
            if re.search(pattern, code, re.MULTILINE | re.IGNORECASE):
                libraries.append(library)
    return libraries

