# Scrapy settings for $project_name project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

project_name = "DublinBusSpider"

BOT_NAME = project_name

SPIDER_MODULES = ['DublinBusSpider.spiders']
NEWSPIDER_MODULE = 'DublinBusSpider.spiders'
RANDOMIZE_DOWNLOAD_DELAY = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = '$project_name (+http://www.yourdomain.com)'
