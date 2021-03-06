from scrapy.utils.project import get_project_settings
import os
from scrapy.crawler import CrawlerRunner
from dafiti.spiders import DafitiAdidasSpider
from scrapy.utils.log import configure_logging
from config import settings
from typer import Typer
from twisted.internet import reactor


app = Typer()

@app.command()
def start_crawl(brand: str = ""):
    if brand not in settings.get("store.brands"):
        raise ValueError(f"{brand} is not a valid store.")
    crawl_settings = get_project_settings()
    settings_module_path = os.environ.get("SCRAPY_ENV", "dafiti.settings")
    crawl_settings.setmodule(settings_module_path)
    configure_logging(crawl_settings)
    runner = CrawlerRunner(crawl_settings)
    d = runner.crawl(DafitiAdidasSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run() 


if __name__ == "__main__":
    app()
