"""Module containing global variables for use in news_retrieval_service"""

EXCEPTION_CAUSING_URLS = [
    "https://www.newsweek.com/",
    "https://www.forbes.com",
    "https://www.malaysiasun.com/",
]

GDELT_LATEST_UPDATE_URL = "http://data.gdeltproject.org/gdeltv2/lastupdate.txt"

GDELT_MASTER_LIST_URL = "http://data.gdeltproject.org/gdeltv2/masterfilelist.txt"

GDELT_COLUMNS = [
    "GlobalEventID",
    "Day",
    "MonthYear",
    "Year",
    "FractionDate",
    "Actor1Code",
    "Actor1Name",
    "Actor1CountryCode",
    "Actor1KnownGroupCode",
    "Actor1EthnicCode",
    "Actor1Religion1Code",
    "Actor1Religion2Code",
    "Actor1Type1Code",
    "Actor1Type2Code",
    "Actor1Type3Code",
    "Actor2Code",
    "Actor2Name",
    "Actor2CountryCode",
    "Actor2KnownGroupCode",
    "Actor2EthnicCode",
    "Actor2Religion1Code",
    "Actor2Religion2Code",
    "Actor2Type1Code",
    "Actor2Type2Code",
    "Actor2Type3Code",
    "IsRootEvent",
    "EventCode",
    "EventBaseCode",
    "EventRootCode",
    "QuadClass",
    "GoldsteinScale",
    "NumMentions",
    "NumSources",
    "NumArticles",
    "AvgTone",
    "Actor1Geo_Type",
    "Actor1Geo_Fullname",
    "Actor1Geo_CountryCode",
    "Actor1Geo_ADM1Code",
    "Actor1Geo_ADM2Code",
    "Actor1Geo_Lat",
    "Actor1Geo_Long",
    "Actor1Geo_FeatureID",
    "Actor2Geo_Type",
    "Actor2Geo_Fullname",
    "Actor2Geo_CountryCode",
    "Actor2Geo_ADM1Code",
    "Actor2Geo_ADM2Code",
    "Actor2Geo_Lat",
    "Actor2Geo_Long",
    "Actor2Geo_FeatureID",
    "Action2Geo_Type",
    "Action2Geo_Fullname",
    "Action2Geo_CountryCode",
    "Action2Geo_ADM1Code",
    "Action2Geo_ADM2Code",
    "Action2Geo_Lat",
    "Action2Geo_Long",
    "Action2Geo_FeatureID",
    "DATEADDED",
    "SOURCEURL",
]
