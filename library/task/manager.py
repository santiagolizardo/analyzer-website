
from library.task.html import HtmlAnalyzerTask 
from library.task.domain import DomainAnalyzerTask 
from library.task.twitter import TwitterAccountCheckerTask 
from library.task.robots import RobotsTxtCheckerTask
from library.task.sitemap import SitemapXmlCheckerTask 
from library.task.screenshot import ScreenshotGrabberTask 
from library.task.w3c import W3cValidatorTask
from library.task.alexa import AlexaAnalyzerTask
from library.task.social import FacebookCounterTask
from library.task.search import SearchTask 
from library.task.humans import HumansTxtCheckerTask
from library.task.favicon import FaviconCheckerTask
from library.task.pageRank import PageRankTask 
from library.task.custom404 import Custom404Task

def findAll():
	htmlAnalyzer = HtmlAnalyzerTask()
	domainAnalyzer = DomainAnalyzerTask()
	screenshotGrabber = ScreenshotGrabberTask()
	w3cValidator = W3cValidatorTask()
	robotsChecker = RobotsTxtCheckerTask()
	sitemapChecker = SitemapXmlCheckerTask()
	twitterChecker = TwitterAccountCheckerTask()
	alexaAnalyzer = AlexaAnalyzerTask()

	tasks = (
		screenshotGrabber,
		htmlAnalyzer,
		domainAnalyzer,
		w3cValidator,
		robotsChecker,
		sitemapChecker,
		twitterChecker,
		alexaAnalyzer,
		PageRankTask(),
		FacebookCounterTask(),
		SearchTask(),
		HumansTxtCheckerTask(),
		FaviconCheckerTask(),
		Custom404Task(),
	)

	return tasks

