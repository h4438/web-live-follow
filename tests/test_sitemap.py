import sys
sys.path.append("./")

from sitemap import *

def explore_sitemap():
    url = 'https://reviewedu.net/'
    name = 'ReviewEdu'
    site = explore_sitemap(url, name)
    assert(site.name == name)
    assert(len(site.sitemap) > len(url))
    assert(len(site.robots) > len(url))
    assert(len(site.pages) > 10)


def test_compare_sitemaps():
    a = ['a', 'b', 'c', 'e']
    b = ['a', 'c', 'd', 'b']
    c = set()
    c.add('e')
    c.add('d')
    dff = compare_sitemaps(a, b)
    assert(len(dff) == 2)
    assert(set(dff) == c)
