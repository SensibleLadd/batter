import json
import requests


user_agent = "WaffleBatter/0.1 +https://github.com/wafflesfm/batter"


class DiscogsAPI(object):

    def __init__(self, user_agent=user_agent):
        self.base_url = 'http://api.discogs.com'
        self.user_agent = user_agent

    def make_request(self, path, **params):
        url = self.base_url + path
        headers = {
            'User-Agent': self.user_agent
        }
        params['per_page'] = 100
        request = requests.get(url, params=params, headers=headers)
        return request.json()

    def search_request(self, query, search_type=None, page=1):
        page += 1
        params = {'q': query}

        if search_type:
            params['type'] = search_type

        search = self.make_request('/database/search', **params)
        yield search['results']

        while page < search['pagination']['pages']:
            params['page'] = page
            yield self.make_request('/database/search', **params)['results']
            page += 1

    def search(self, query, page=1):
        return self.search_request(query, page=page)

    def search_artist(self, query, page=1):
        return self.search_request(query, search_type='artist', page=page)

    def search_release(self, query, page=1):
        return self.search_request(query, search_type='release', page=page)

    def get_artist(self, artist_id):
        return self.make_request('/artists/%s' % artist_id, page=page)

    def get_release(self, release_id):
        return self.make_request('/releases/%s' % release_id)

    def get_releases(self, artist_id, page=1):
        """
        Generator to fetch all releases for given `artist_id`
        ``get_releases(45).next()`` returns a generator for all pages of releases
        takes options page argument for starting page
        """
        page += 1
        releases = self.make_request('/artists/%s/releases' % artist_id)
        yield releases['releases']

        while page < releases['pagination']['pages']:
            params = {'page': page}
            yield self.make_request('/artists/%s/releases' % artist_id, **params)['releases']
            page += 1


if __name__ == '__main__':
    d = DiscogsAPI()
    search = d.search_release('window licker')
    print search.next()[0]['id']