from settings import *
import scrapelib
import time
import re
from BeautifulSoup import BeautifulSoup
from soupselect import select

class NextbusPredictor(object):
	"""Tracks Nextbus arrival times"""
	def __init__(self, routes):
		super(NextbusPredictor, self).__init__()
		self.routes = map(lambda x: str(x), routes)
		self.predictions = {}
		self.last_refresh = {}
		self.scraper = scrapelib.Scraper(requests_per_minute=10, follow_robots=False)
		for r in self.routes:
			self.predictions[r] = None
			self.last_refresh[r] = None
			self.refresh(r)
	
	def _extract_prediction(self, html):
		if '<p class="predictHead"><span id=\'i18n_en\'>No prediction</span><br/>' in html:
			return None
		else:
			soup = BeautifulSoup(html)			
			minutes = re.sub(r'&nbsp;','', re.sub(r'<[^>]*>','',(str(select(soup, '.predictionNumberForFirstPred')[0])), flags=re.MULTILINE|re.DOTALL))
			return int(minutes.strip())


	def refresh(self, route):
		"""Force a refresh of a specific route"""
		route = str(route)

		url = NEXTBUS_URLS.get(str(route), False)
		if not url:
			return

		html = self.scraper.urlopen(url)

		self.predictions[route] = self._extract_prediction(html)
		self.last_refresh[route] = time.time()

	def refresh_if_necessary(self):
		"""Only refresh prediction times intermittently -- don't hammer"""
		for r in self.routes:
			if self.predictions[r] is None:
				if (time.time() - self.last_refresh[r]) > TIMEOUT:
					self.refresh(r)
			else:
				# if we have a prediction, refresh if we're halfway or more to
				# the expected arrival time
				if (time.time() - self.last_refresh[r]) > (self.predictions[r] * 30):
					self.refresh(r)
		
	def get_closest_arrival(self):
		"""Return the (route, arrival) pair that's happening soonest"""
		soonest_time = 9999
		soonest_found = False
		soonest_route = None
		for r in self.routes:
			p = self.predictions.get(r, None)
			if p is not None:
				if p<soonest_time:
					soonest_time = p
					soonest_route = r
					soonest_found = True

		if soonest_found:
			return (soonest_route, soonest_time)
		else:
			return False


if __name__ == '__main__':
	main()