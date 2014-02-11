from apiclient import APIClient

class RTApi(APIClient):
  API_FILE = '.rottentomatoes_api_key'
  API_KEY = open(API_FILE).read().rstrip()
  BASE_URL = 'http://api.rottentomatoes.com/api/public/v1.0/'

  def search(self,path,params):
    params['apikey'] = self.API_KEY
    return self.call(path, **params)

  def movie(self,name):
    return self.search('movies.json', {'q': name, 'page_limit':'1'})

if __name__ == '__main__':
  rt = RTApi()
  print rt.movie('Ronin')
