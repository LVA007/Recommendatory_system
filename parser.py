from html.parser import HTMLParser
from urllib.request import quote, urlopen

links = dict()
queue = dict()

class ParserArticleText(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_body_text_tag = False
        self.body_text = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            attrs = dict(attrs)
            flag = 1
            for elem in attrs:
                if elem != ' ' and not (elem >= 'a' and elem <= 'z') and not (elem >= 'A' and elem <= 'Z'):
                    flag = 0
            if flag:
                self.in_body_text_tag = True

    def handle_endtag(self, tag):
        if self.in_body_text_tag and tag == 'p':
            self.in_body_text_tag = False

    def handle_data(self, data):
        if self.in_body_text_tag:
            self.body_text += data + ' '

    def parse(self, page):
        self.feed(page)
        return self.body_text

class ParserArticleTitle(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_title_tag = False
        self.title_text = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.in_title_tag = True

    def handle_endtag(self, tag):
        if self.in_title_tag and tag == 'title':
            self.in_title_tag = False

    def handle_data(self, data):
        if self.in_title_tag:
            self.title_text = data

    def parse(self, page):
        self.feed(page)
        return self.title_text

PHYS_ROOT = 'http://phys.org/news/'

def load(name):
    with urlopen(PHYS_ROOT + name) as file:
        page = str(file.read(), encoding='utf-8')
        index = -1
        string = '<h4 class'
        other = '.html'
        while True:
            index = page.find(string, index + 1, len(page))
            if index == -1:
                break
            another = page.find(other, index + 1, len(page))
            link = page[index + 49 : another + 5]
            if link not in links:
                links[link] = 0
                queue[link] = 0
        file = open(str(name + '.txt'), 'w')
        file.write(page)
        file.close()
    return page

def get_title_text(page):
    return ParserArticleTitle().parse(page)

def get_body_text(page):
    return ParserArticleText().parse(page)

def add_links(page):
    ParserArticleLinks().parse(page)

def get_data(page):
    return page[21 : 25] + page[26 : 28]

def main():
    links['2016-02-values-important-scientists.html'] = 0
    queue['2016-02-values-important-scientists.html'] = 0
    while True:
        new_links = dict()
        for elem in queue:
            new_links[elem] = 0
        queue.clear()
        for link in new_links:
            page = load(link)
            file = open(str(get_title_text(page) + '.txt'), 'w')
            file.write(get_body_text(page))
            file.close()

if __name__ == '__main__':
    main()