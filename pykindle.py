#import requests
from bs4 import BeautifulSoup as bs
from mechanize import Browser
from mechanize._mechanize import LinkNotFoundError
import cookielib

def amazon_signin(br, user, password):
    sign_in_url = "https://www.amazon.com/ap/signin?openid.assoc_handle=amzn_kindle&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fkindle.amazon.com%3A443%2Fauthenticate%2Flogin_callback%3Fwctx%3D%252F&pageId=amzn_kindle&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.mode=checkid_setup"
    r = br.open(sign_in_url)
    r.set_data(br.response().read()[144:])
    br.set_response(r)
    br.select_form(name="signIn")
    br['email'] = user
    br["create"] = ["0"]
    br["password"] = password
    br.submit()

def get_highlights(br, books):
    br.open("https://kindle.amazon.com")
    br.follow_link(text_regex="Your Highlights")
    get_highlights_inner(br, books)
    
def get_highlights_inner(br, books):
    for highlighted_books in bs(br.response().read()).find_all(
                                        "div", id="allHighlightedBooks") :
        for book in highlighted_books.find_all("div", class_="bookMain") :
            book_id = book["id"][:book["id"].find("_")]
            books[book_id] = {
                "id": book_id, "title": book.find("a").string, "highlights": [],
                "author": book.find("span", class_ = "author").string.strip()[3:] 
                                 }
        for highlight_div in(highlighted_books.find_all("div", class_="highlightRow")) :
            text = highlight_div.find("span", class_="highlight").string.strip()
            book_id = highlight_div.find("span", class_="asin").string.strip()
            books[book_id]["highlights"].append(text)
    try :
        br.follow_link(br.find_link(text="Next Book"))
        get_highlights_inner(br, books)
    except LinkNotFoundError as _lnfe :
        pass
    
def set_browser_options(br):
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

def main(userid, password):    
    br = Browser()
    br.set_cookiejar(cookielib.LWPCookieJar())
    set_browser_options(br)    
    amazon_signin(br, userid, password)
    books = {}
    get_highlights(br, books)
    dump_books(books)

def html_safe(text): return text.encode('ascii', 'xmlcharrefreplace')

def dump_books(books):    
    with open("kindle_highlights.html","w") as out :
        for id_, book in books.items() :
            out.write('<div class="book" id="{}">\n\t<div class="title">{}</div>\n\t<div class="author">{}</div>' \
                .format(id_, html_safe(book["title"]), html_safe(book["author"])))
            for highlight in book["highlights"] :
                out.write('\t<div class="highlight">{}</div>'.format(html_safe(highlight)))
            out.write('</div>')

if __name__ == "__main__" : 
    import sys
    main(sys.argv[1], sys.argv[2])
