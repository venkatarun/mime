#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import urllib, urllib2
import json
import pyodbc
import csv, codecs, cStringIO
import time
import sys
import MySQLdb
import difflib

reload(sys)
sys.setdefaultencoding("ISO-8859-1")

class SearchAPI:

    def GoogleSearch(self, location, CompanyName, Id, StreetAddress1, City, State, Zip, Country):
        db = MySQLdb.connect("localhost", "root", "root", "IV")
        cursor = db.cursor()
        query = CompanyName+' '+location
        params = {'query': query,
                  'key': 'AIzaSyCotGU5pfQPN8UmS_PjLp6ixk7MgHuMu1M' }
        url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?' + urllib.urlencode(params)
        result = urllib2.urlopen(url).read()
        data = json.loads(result)
        try:
            if data['status'] == 'OK':
                for company in data['results']:
                    comp_name = (company['name']).encode('utf-8').replace("'", "''")
                    address = (company['formatted_address']).encode('utf-8').replace("'", "''") if company['formatted_address'] is not None else ''

                    placeid = company['place_id']
                    params = {
                        'placeid':        placeid,
                        'key':      'AIzaSyCotGU5pfQPN8UmS_PjLp6ixk7MgHuMu1M'
                    }
                    url_place = 'https://maps.googleapis.com/maps/api/place/details/json?' + urllib.urlencode(params)
                    result = urllib2.urlopen(url_place).read()
                    data = json.loads(result)
                    street_number = ''
                    route = ''
                    city_place = ''
                    state_place = ''
                    country_place = ''
                    postal_code = ''
                    phone_number = ''

                    if 'formatted_phone_number' in data['result']:
                        phone_number = data['result']['formatted_phone_number']

                    for data in data['result']['address_components']:
                        if data['types'] == [u'street_number']:
                            street_number = data['long_name']
                        if data['types'] == [u'route']:
                            route = data['long_name']
                        if data['types'] == [u'locality', u'political']:
                            city_place = data['long_name']
                        if data['types'] == [u'administrative_area_level_1', u'political']:
                            state_place = data['short_name']
                        if data['types'] == [u'country', u'political']:
                            country_place = data['long_name']
                        if data['types'] == [u'postal_code']:
                            postal_code = data['long_name']
                    seq = difflib.SequenceMatcher(a=CompanyName.lower(), b=comp_name.lower())
                    Country = Country.lstrip().rstrip().lower()
                    api_country = country_place.lstrip().rstrip().lower()
                    street_address = street_number+' '+route+' '
                    score = seq.ratio()
                    if Country == api_country and score >= 0.5:
                        print comp_name, street_address, score, Id
                        row = "INSERT INTO austraila_api_New(Id, CompanyName, StreetAddress1, City, State, PostalCode, Country, Srch_CompanyName, Srch_RawAddress, Srch_APIURL, Srch_StreetAddress,Srch_City,Srch_State,Srch_Country,Srch_PostalCode,PhoneNumber) VALUES ('"+str(Id)+"','"+CompanyName+"','"+StreetAddress1+"','"+City+"','"+State+"','"+str(Zip)+"', '"+Country+"','"+comp_name+"','"+address+"','"+url+"','"+street_address+"','"+city_place+"','"+state_place+"','"+str(country_place)+"','"+str(postal_code)+"','"+str(phone_number)+"');"
                        cursor.execute(row)
                        db.commit()
            else:
                return False
            return True
        except Exception, e:
            print e, 'google'
            return False
        except urllib2.HTTPError, err:
            return False
        except urllib2.URLError, e:
            print e.args
            return
        cursor.close()


class DatabaseInsert:
    global the_SearchAPI
    the_SearchAPI = SearchAPI()

    def SQLInsert(self):
        db = MySQLdb.connect("localhost", "root", "root", "IV")
        cursor = db.cursor()
        cursor.execute('SELECT Id, company_name, country, city, State, Postalcode, \
                        Street FROM austraila_data where Status is not NULL')

        for row in cursor.fetchall():
            Id = str(row[0])
            CompanyName = ((row[1].encode('utf-8').replace('&', 'and')).replace("'", "")).replace("\\", "")
            Country = row[2].encode('utf-8')
            City = row[3].encode('utf-8').replace("'", "") if row[3] is not None else ""
            State = row[4].encode('utf-8') if row[4] is not None else ""
            Zip = row[5] if row[5] is not None else ""
            StreetAddress1 = row[6].encode('utf-8').replace("'", "") if row[6] is not None else ""
            if City != 'None' and State != 'None' and Country != 'None':
                location = City+' '+State+' '+Country
            elif City == 'None' and State != 'None' and Country != 'None':
                location = State+' '+Country
            elif City == 'None' and State == 'None' and Country != 'None':
                location = Country
            if City != 'None' and Country != 'None':
                location = City+' '+Country
            elif City == 'None' and Country != 'None':
                location = Country
            # print location, CompanyName, Id
            try:
                result_g = the_SearchAPI.GoogleSearch(location, CompanyName, Id, StreetAddress1, City, State, Zip, Country)
                if not result_g:
                    row = "update austraila_data set status='0' where id='"+Id+"';"
                else:
                    row = "update austraila_data set status='' where id='"+Id+"';"

                cursor.execute(row)
                db.commit()
            except Exception, e:
                print e
            time.sleep(2)

if __name__=='__main__':
    the_dbinsert = DatabaseInsert()
    the_dbinsert.SQLInsert()
