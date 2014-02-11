#!/usr/bin/env python
from apiclient import RateLimiter
from rotten_tomatoes import RTApi
import freebase as fb

lock = RateLimiter(max_messages=10, every_seconds=60)
rt = RTApi(rate_limit_lock=lock)

actors = fb.all_actors()
actors = actors[0:1]
for actor in actors:
  movies = fb.movies(actor['name'])
  #movies = movies[0:1]
  for movie in movies:
    rt_result = rt.movie(movie['name'])
    print rt_result
    print "%(name)s\t" % actor,
    print "%(name)s\t" % movie,
    if len(rt_result['movies']) > 0:
      rt_movie = rt_result['movies'][0]
      rt_rating = rt_movie['ratings']
      print "%(year)s\t" % rt_movie,
      print "%(audience_score)s" % rt_rating


