#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import boto3
import json
import decimal

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

#Update the movies in a json file
def updateMovie(file):
       dynamodb = boto3.resource('dynamodb',region_name='us-west-2', endpoint_url="https://dynamodb.us-west-2.amazonaws.com")
       table = dynamodb.Table('Movies')
       print('updating table: ' + table.name + 'from file: ' + file)
       with open(file) as json_file:
            for line in json_file:
                        movie = json.loads(line, parse_float = decimal.Decimal)
                        name = movie['name'][0]
                        movie_id = movie['movieid']
                        year = movie['year']
                        score = movie['score']
                        classification = movie['classification']
                        url = movie['url']
                        actor = movie['actor']
                        director = movie['director']
                        
                        print ("Adding movie: ", name)
                        
                        response = table.put_item(
                               Item = {
                                       'name': name,
                                       'movie_id': movie_id,
                                       'year': year,
                                       'score': score,
                                       'classification': classification,
                                       'url': url,
                                       'actor': actor,
                                       'director': director 
                               }
                        )
        
                        print("PutItem succeeded:")
                        print(json.dumps(response, indent=4, cls=DecimalEncoder)) 
      
       print("Done update movie table")
     


if __name__ == '__main__':
    updateMovie("doubanUpdateMovie.json")
