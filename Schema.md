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

R4 = (NTAcode,borough,type,location,latitude,longitude,city SSID,activated,NTA,NTAcode,bin,bbl)

 BCNF Decomposition cannot apply to  the R3  by  and R4 is covered by R1,R2
so the schema will be
```
WIFI1(__wifiID__,borough,type,location,latitude,longitude,city SSID,activated,NTA,NTAcode,bin,bbl)
WIFI2(__NTAcode__,NTA)
WIFI3(__latitude__,__longitude__,wifiID,borough,type,location,city SSID,activated,NTA,NTAcode,bin,bbl)

```


-  Restuarant(__CAMIS__,DBA,boro,building,street,phone,cuisine,Zipcode,BIN,BBL,NTAcode,lat,lon,grade)
- CAMIS -> every other attribute
- lat,lon -> every other attribute
According to the FD above, we can conclude that keys can be (CAMIS) or (lon,lat). Since all the leftside are superkeys so that we can create schema
```
Restuarant1(__CAMIS__,DBA,boro,building,street,phone,cuisine,Zipcode,BIN,BBL,NTAcode,lat,lon,grade)
Restuarant2(__lon__,__lat__,CAMIS,DBA,boro,building,street,phone,cuisine,Zipcode,BIN,BBL,NTAcode,grade)
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
Restuarant1(__CAMIS__,DBA,boro,building,street,phone,cuisine,Zipcode,BIN,BBL,NTAcode,lat,lon,grade)
WIFI1(__wifiID__,borough,type,location,latitude,longitude,city SSID,activated,NTA,NTAcode,bin,bbl)
WIFI2(__NTAcode__,NTA)
Restuarant1(__CAMIS__,DBA,boro,building,street,phone,cuisine,Zipcode,BIN,BBL,NTAcode,lat,lon,grade)
LPC1(__LPC__,lat,lon,borough,block,lot,address,BBL,LPC_name,URLreport)
```
