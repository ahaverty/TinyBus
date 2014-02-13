from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector



class DublinBusSpider(Spider):
    name="dublinbusspider"
    allowed_domains=['http://www.dublinbus.ie/']

    def __init__(self, stop_number=None, *args, **kwargs):
        super(DublinBusSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://www.dublinbus.ie/en/RTPI/Sources-of-Real-Time-Information/?searchtype=view&searchquery=%s' % stop_number]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        page_elmnt = "//table[@id='rtpi-results']"

        realtime_table = hxs.select(page_elmnt).extract()
        print(realtime_table)

        Html_file= open("bustimes.html","w")
        Html_file.write("<html><body>")
        for item in realtime_table:
            Html_file.write("%s\n" % item)
        Html_file.write("</body></html>")
        Html_file.close()

