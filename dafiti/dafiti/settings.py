BOT_NAME = "dafiti"

SPIDER_MODULES = ["dafiti.spiders"]
NEWSPIDER_MODULE = "dafiti.spiders"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 10

MAGIC_FIELDS = {
    "timestamp": "$isotime",
    "spider": "$spider:name",
    "url": "$response:url",
}

SPIDER_MIDDLEWARES = {
    "scrapy_magicfields.MagicFieldsMiddleware": 100,
}

GCP_PROJECT_ID = ""
GCP_CREDENTIALS = ""
GCP_STORAGE = ""
GCP_STORAGE_CRAWLER_STATS = ""
ITEM_PIPELINES = {
    "dafiti.pipelines.DiscordMessenger" : 100,
    "dafiti.pipelines.GCSPipeline": 200,
}
DISCORD_WEBHOOK_URL = ""
DISCORD_THUMBNAIL_URL = ""
