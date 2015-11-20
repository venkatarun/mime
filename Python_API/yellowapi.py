#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import urllib, urllib2                                                         
import json   
import pyodbc
import  csv,codecs,cStringIO
import time
import sys
reload(sys)
sys.setdefaultencoding("ISO-8859-1")

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=SCS-LT-043\SQLEXPRESS;DATABASE=InsideView;UID=sa;PWD=smartek@123')
cursor = cnxn.cursor()
cursor.execute("SELECT id,[Company Name],[Street],[City],[State],[Zip],[Country] FROM [InsideView].[dbo].[TotalNull] where Status is NULL")
for row in cursor.fetchall():
    Id = row[0]
    CompanyName = ((row[1].encode('utf-8').replace('&','and')).replace("'","")).replace("\\","") 
    StreetAddress1 = row[2].encode('utf-8').replace("'","") 
    City =  row[3].encode('utf-8').replace("'","") 
    State =  row[4].encode('utf-8')
    Zip = row[5]
    Country= row[6].encode('utf-8')
    location = City if City <>'NULL' else Country
    params = {
        'searchloc':location,
        'term':CompanyName,
        'format':'json',
        'key':'qzk7yp2048'
    }
    url = 'http://api2.yp.com/listings/v1/search?' + urllib.urlencode(params)
    print url
    result = urllib2.urlopen(url).read()
     
    data = json.loads(result)
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=SCS-LT-043\SQLEXPRESS;DATABASE=InsideView;UID=sa;PWD=smartek@123')
    cursor = cnxn.cursor()
    if data['searchResult']['searchListings']:
        for x in data['searchResult']['searchListings']['searchListing']:
            businessName= x['businessName'].encode('utf-8').replace("'","''")
            street=x['street'].encode('utf-8').replace("'","''")
            city=x['city'].encode('utf-8').replace("'","''")
            state=x['state'].encode('utf-8').replace("'","''")
            pzip=str(x['zip'])
            row = "INSERT INTO [dbo].[TotalNULLRecords]([Id],[CompanyName],[StreetAddress1],[City],[State],[PostalCode],[Country],[Srch_CompanyName],[Srch_StreetAddress],[Srch_City],[Srch_State],[Srch_PostalCode],[Srch_APIURL],[Created_dt])VALUES('"+Id+"','"+CompanyName+"','"+StreetAddress1+"','"+City+"','"+State+"','"+Zip+"','"+Country+"','"+businessName+"','"+street+"','"+city+"','"+state+"','"+pzip+"','"+url+"',getdate());"
            print row
            cursor.execute(row)
            cnxn.commit()
    else :
        row = "INSERT INTO [dbo].[TotalNULLRecords]([Id],[CompanyName],[StreetAddress1],[City],[State],[PostalCode],[Country],[Srch_CompanyName],[Srch_APIURL],[Created_dt])VALUES('"+Id+"','"+CompanyName+"','"+StreetAddress1+"','"+City+"','"+State+"','"+Zip+"','"+Country+"','no matching records','no matching records',getdate());"
        cursor.execute(row)
        cnxn.commit()
    row = "update  [InsideView].[dbo].[TotalNull] set status='1' where id='"+Id+"';"
    cursor.execute(row)
    cnxn.commit()
#                 row = "INSERT INTO [dbo].[JLLNullSearchResultCityCountryLinkediN]([Id],[CompanyName],[StreetAddress1],[City],[State],[PostalCode],[Country],[Srch_CompanyName],[Srch_APIURL],[Srch_Source],[Created_dt])VALUES('"+Id+"','"+CompanyName+"','"+StreetAddress1+"','"+City+"','"+State+"','"+Zip+"','"+Country+"','"+comp_name+"','"+url+"',4,getdate());"
#           
#                 cursor.execute(row)
#                 cnxn.commit()
#         else:
#                 row = "INSERT INTO [dbo].[JLLNullSearchResultCityCountryLinkediN]([Id],[CompanyName],[StreetAddress1],[City],[State],[PostalCode],[Country],[Srch_CompanyName],[Srch_APIURL],[Srch_Source],[Created_dt])VALUES('"+Id+"','"+CompanyName+"','"+StreetAddress1+"','"+City+"','"+State+"','"+Zip+"','"+Country+"','no matching records','"+url+"',4,getdate());"
#           
#                 cursor.execute(row)
#                 cnxn.commit()
#     except Exception, e:
#         error= str(e)
#         row = "INSERT INTO [dbo].[JLLNullSearchResultCityCountryLinkediN]([Id],[CompanyName],[StreetAddress1],[City],[State],[PostalCode],[Country],[Srch_APIURL],[Srch_Source],[Created_dt],[Error])VALUES('"+Id+"','"+CompanyName+"','"+StreetAddress1+"','"+City+"','"+State+"','"+Zip+"','"+Country+"','"+url+"',2,getdate(),'"+error+"');"
#         print row
#         cursor.execute(row)
#         cnxn.commit()
    time.sleep(5)
cursor.close()
#  