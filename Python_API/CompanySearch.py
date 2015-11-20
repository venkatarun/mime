#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import urllib, urllib2
import json
import pyodbc
import csv, codecs
import time
import sys
import MySQLdb
import difflib

reload(sys)
sys.setdefaultencoding("ISO-8859-1")


class SearchAPI:

    def GoogleSearch(self, location, CompanyName, Id, StreetAddress1, City,
                     State, Zip, Country):
        # cnxn = pyodbc.connect('DRIVER={SQL Server};
        # SERVER=SCS-LT-043\SQLEXPRESS;DATABASE=InsideView;UID=sa;
        # PWD=smartek@123')
        # cursor = cnxn.cursor()
        db=MySQLdb.connect("localhost", "root", "root", "IV")
        cursor=db.cursor()
        query = CompanyName+' '+location
        params = {
            'query':        query,
            'key':     'AIzaSyCotGU5pfQPN8UmS_PjLp6ixk7MgHuMu1M'
            # 'AIzaSyDelp0LWIZaeBRwKDYdFADnMJF6GLFTQRE'
                }
        url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?' + urllib.urlencode(params)
        result = urllib2.urlopen(url).read()
        data = json.loads(result)
        print data
        try:
            if data['status'] == 'OK':
                for company in data['results']:
                    comp_name=(company['name']).encode('utf-8').replace("'", "''")
                    address=(company['formatted_address']).encode('utf-8').replace("'", "''") if company['formatted_address'] is not None else ''
                    api_country = address.rsplit(',', 1)[1].lstrip().rstrip()
                    Country = Country.lstrip().rstrip()
                    # row = "INSERT INTO [dbo].[Data]([Id],[CompanyName],[StreetAddress1],[City],[State],[PostalCode],[Country],[Srch_CompanyName],[Srch_RawAddress],[Srch_APIURL],[Srch_Source],[Created_dt])VALUES('"+Id+"','"+CompanyName+"','"+StreetAddress1+ data['subpremise']+','"+City+"','"+State+"','"+Zip+"','"+Country+"','"+comp_name+"','"+address+"','"+url+"',1,getdate());"
                    seq = difflib.SequenceMatcher(a=CompanyName.lower(), b=comp_name.lower())
                    if seq.ratio() >= 0.5 and api_country.lower() == Country.lower():
                        print " ------- "
                        print "API Company Name --> " + comp_name
                        print "API Address --> " + address
                        print " ------- "
                        print "Input Company Name --> " + CompanyName
                        print "Input Address --> " + StreetAddress1
                        print " ------- "
                        row = "INSERT INTO austraila_api (Id, CompanyName, StreetAddress1, City, State, PostalCode, Country, Srch_CompanyName, Srch_RawAddress, Srch_APIURL, Srch_Source) VALUES ('"+str(Id)+"', '"+CompanyName+"', '"+StreetAddress1+"', '"+City+"', '"+State+"', '"+str(Zip)+"', '"+Country+"', '"+comp_name+"', '"+address+"', '"+url+"', '1');"
                        cursor.execute(row)
                        db.commit()
            else:
                return False
            return True
        except Exception as e:
            print e, 'google'
            return False
        except urllib2.HTTPError as err:
            return False
        except urllib2.URLError as e:
            print e.args
            return
        # cursor.close()


class DatabaseInsert:
    global the_SearchAPI
    the_SearchAPI=SearchAPI()

    def SQLInsert(self):
        # cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=SCS-LT-043\SQLEXPRESS;DATABASE=InsideView;UID=sa;PWD=smartek@123')
        # cursor = cnxn.cursor()
        # cursor.execute("SELECT id,[Company Name],[Street],[City],[State],[Zip],[Country] FROM [InsideView].[dbo].[log] where Status is NULL")
        db=MySQLdb.connect("localhost", "root", "root", "IV")
        cursor=db.cursor()
        cursor.execute('SELECT Id, company_name, country, City, State, Postalcode, \
                        Street FROM austraila_data')
        for row in cursor.fetchall():
            print row
            Id=row[0]
            inputCompanyName=((row[1].encode('utf-8').replace('&', 'and')).replace("'", "")).replace("\\", "")
            Country=row[2].encode('utf-8')
            City=row[3].encode('utf-8').replace("'", "") if row[3] is not None else ""
            State=row[4].encode('utf-8') if row[4] is not None else ""
            Zip=row[5] if row[5] is not None else ""
            StreetAddress1=row[6].encode('utf-8').replace("'", "") if row[6] is not None else ""
            # location = City if City <>'NULL' else Country
            if State != 'None':
                location=State + "+"
            if City != 'None':
                location += City + "+"
            location += Country
            print location
            try:
                result_g=the_SearchAPI.GoogleSearch(location, inputCompanyName,\
                                                    Id, StreetAddress1, City,\
                                                    State, Zip, Country)
                # result_y=the_SearchAPI.YahooQueryLanguage(location, CompanyName, Id, StreetAddress1, City, State, Zip, Country)
                # result_f=the_SearchAPI.Facebook(CompanyName, Id, StreetAddress1, City, State, Zip, Country)
                # if result_g==False and  result_y==False and  result_f==False:
                #     cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=SCS-LT-043\SQLEXPRESS;DATABASE=InsideView;UID=sa;PWD=smartek@123')
                #     cursor = cnxn.cursor()
                #     row = "INSERT INTO [dbo].[Data]([Id],[CompanyName],[StreetAddress1],[City],[State],[PostalCode],[Country],[Srch_CompanyName],[Srch_APIURL],[Created_dt])VALUES('"+Id+"','"+CompanyName+"','"+StreetAddress1+"','"+City+"','"+State+"','"+Zip+"','"+Country+"','no matching records','no matching records',getdate());"
                #     cursor.execute(row)
                #     cnxn.commit()
                #     row = "update  [InsideView].[dbo].[log] set status='0' where id='"+Id+"';"
                #     cursor.execute(row)
                #     cnxn.commit()
                #     cursor.close()
            except Exception as e:
                print e
            time.sleep(5)


if __name__ == '__main__':
    the_dbinsert = DatabaseInsert()
    the_dbinsert.SQLInsert()
