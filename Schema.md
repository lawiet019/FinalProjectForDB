- Entrance(__EntranceId__,Name,lon.lat,line,url)
- EntranceId -> every other attribute
- lon,lat -> every other attribute
According to the FD above, we can conclude that keys can be (EntranceId) or (lon,lat). Since all the leftside are superkeys so that we can create schema
```
Entrance1(__EntranceId__,Name,line,url,lon,lat)
Entrance2(__lon__,__lat__,Name,line,url,EntranceId)
```

- WIFI(__wifiID__,borough,type,location,latitude,longitude,city SSID,activated,NTA,NTAcode,bin,bbl)
- wifiId -> every other attribute
- lat,lon -> every other attribute
- NTAcode ->NTA

According to the FD above, we can conclude that keys can be (wifiID) or (lon,lat). The third FD doesnot follow the BCNF so we break it into R3,R4.

R3 = (NTAcode,NTA)

R4 = (NTAcode,borough,type,location,latitude,longitude,city SSID,activated,NTA,NTAcode)

 BCNF Decomposition cannot apply to  the R3  by  and R4 is covered by R1,R2
so the schema will be
```
WIFI1(__wifiID__,borough,type,location,latitude,longitude,city SSID,activated,NTA,NTAcode)
WIFI2(__NTAcode__,NTA)
WIFI3(__latitude__,__longitude__,wifiID,borough,type,location,city SSID,activated,NTA,NTAcode)

```


-  Restuarant(__CAMIS__,__inspectionDate__,__violationCode__,DBA,boro,building,street,phone,cuisine,Zipcode,BIN,BBL,NTAcode,lat,lon,grade,violationdescription)
- CAMIS,inspectionDate,violationCode -> violationdescription,grade
- lat,lon,inspectionDate,violationCode -> violationdescription,grade
- CAMIS ->DBA,boro,building,street,phone,cuisine,Zipcode,BIN,BBL,NTAcode,lat,lon
- lat,lon -> DBA,boro,building,street,phone,cuisine,Zipcode,BIN,BBL,NTAcode,CAMIS
According to the FD above, we can conclude that keys can be (CAMIS,inspectionDate,violationCode) or (lat,lon,inspectionDate,violationCode)
by Decomposition we can get the the new schema
```
rest1(__CAMIS__,__inspectionDate__,__violationCode__, violationdescription,grade)
rest2(__CAMIS__,DBA,boro,building,street,phone,cuisine,Zipcode,BIN,BBL,NTAcode,lat,lon)
rest3(__lat__,__lon__,__inspectionDate__,__violationCode__ ,violationdescription,grade)
rest4(__lat__,__lon__,DBA,boro,building,street,phone,cuisine,Zipcode,BIN,BBL,NTAcode,CAMIS)

```
- LPC(__LPC__,lat,lon,borough,block,lot,address,BBL,LPC_name,URLreport)
- loc ->every other attribute
- lon,lat -> every other attribute
According to the FD above, we can conclude that keys can be (LPC) or (lon,lat). Since all the leftside are superkeys so that we can create schema
```
LPC1(__LPC__,lat,lon,borough,block,lot,address,BBL,LPC_name,URLreport)
LPC2(__lat__,__lon__,LPC,borough,block,lot,address,BBL,LPC_name,URLreport)
```


Note: Since some FD may means nothing in practial, we may delete some schema. For example Entrance1 and Entrance2, we may just keep Entrance1. So the schema left will be :
```
Entrance1(__EntranceId__,Name,line,url,lon,lat)
rest1(__CAMIS__,__inspectionDate__,__violationCode__, violationdescription,grade)
rest2(__CAMIS__,DBA,boro,building,street,phone,cuisine,Zipcode,BIN,BBL,NTAcode,lat,lon)
WIFI1(__wifiID__,borough,type,location,latitude,longitude,city SSID,activated,NTA,NTAcode,bin,bbl)
WIFI2(__NTAcode__,NTA)

LPC1(__LPC__,lat,lon,borough,block,lot,address,BBL,LPC_name,URLreport)
```
