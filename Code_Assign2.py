import arcpy as ap
#set arcpy to 'ap' to save typing as you write code

#to allow to overwrite data
ap.env.overwriteOutput = True

#Create new geodatabase
workingGDB = ap.management.CreateFileGDB(r"E:\School\Geog428\Assign2", "WorkingAssign2.gdb")
print("Created new file geodatabase...")

#set workspace
gdb = r"E:\School\Geog428\Assign2\WorkingAssign2.gdb"
ap.env.workspace = gdb
print("Workspace set...")
print("Starting Program...")


#Create Layers
ap.MakeFeatureLayer_management(r"E:\School\Geog428\Assign2\Data\Crime\Victoria_Crime.shp", "Crimes")
ap.MakeFeatureLayer_management(r"E:\School\Geog428\Assign2\Data\Parks\Parks.shp", 'Parks')
ap.MakeFeatureLayer_management(r"E:\School\Geog428\Assign2\Data\Neighbourhood Boundary\Neighbourhood_Boundaries.shp", 'Neighbourhoods')
ap.MakeFeatureLayer_management(r"E:\School\Geog428\Assign2\Data\Schools\Schools.shp", 'Schools')
print("Import Data and Create Feature Layers Complete...")

#
#
#
#
#Question 1: How many incidents of any type occurred within all parks in the city?
print("\nStarting Question 1...")

#Intersect crime and parks
ap.analysis.Intersect(['Crimes', 'Parks'], "crime_in_parks_intersect", "ALL", None, "INPUT")
print("Intersect Complete...")

#assign variable for crime within parks
crimeParks = "crime_in_parks_intersect"

#count the number of crimes in parks
countCrimesQ1 = ap.management.GetCount(crimeParks)
print("There were", str(countCrimesQ1), "crimes that occur within parks in Victoria.")

#
#
#
#
#Question 2: In 2016, how many property crime incidents occurred within 500m of parks in the Oaklands, Fernwood, and North/South Jubilee neighbourhoods?
print("\nStarting Question 2...")

#assign variable to buffer size, neighbourhoods
bufferSize = "500 Meters"
neighbourhood = "Neighbourh = 'Oaklands' Or Neighbourh = 'Fernwood' Or Neighbourh = 'North Jubilee' Or Neighbourh = 'South Jubilee'"
print("Variables assigned...")

#assign crime year and type
crimeYear = 2016
crimeType = 'Property Crime'
#Assign variable to crime selection
crimeYearType = "(incident_d LIKE '%%%s%%'" %crimeYear + ") And (parent_inc LIKE '%%%s%%'" %crimeType + ")"
print("Crime SQL =", crimeYearType)

#select property crimes in 2016
ap.analysis.Select('Crimes', "property_crime2016", crimeYearType)
propertyCrime = "property_crime2016"
print("Crimes selected...")

#select Oaklands, Fernwood, and North/South Jubilee neighbourhoods
ap.analysis.Select('Neighbourhoods', "neighbourh_OakFernNSJubilee", neighbourhood)
nhood_OakFernNSJubilee = "neighbourh_OakFernNSJubilee"
print("Neighbourhoods selected...")

#Intersect parks and neighbourhoods
ap.analysis.Intersect(['Parks', nhood_OakFernNSJubilee], "parks_in_neighbourhood_OakFernNSJubilee_intersect", "ALL", None, "INPUT")
nhoodParks = "parks_in_neighbourhood_OakFernNSJubilee_intersect"
print("Intersect Parks in Neighbourhood Complete...")

#buffer parks
ap.analysis.Buffer(nhoodParks, "parksBuff500m", bufferSize, "FULL", "ROUND", "ALL", None, "PLANAR")
buffParks500 = "parksBuff500m"
print("Parks Buffered...")

#intersect 2016 property crime with buffer parks
ap.analysis.Intersect([propertyCrime, buffParks500], "Property_crime_500m_parks", "ALL", None, "INPUT")
parks500PropertyCrime = "Property_crime_500m_parks"

#count the number of crimes within 500m of parks in Oaklands, Fernwood, and North/South Jubilee neighbourhoods
countCrimesQ2 = ap.management.GetCount(parks500PropertyCrime)
print("There were", str(countCrimesQ2), "crimes that occur within 500m of parks in Oaklands, Fernwood, and North/South Jubilee neighbourhoods in 2016.")

#
#
#
#
#Question 3: In 2017, how many drug and liquor and disorder incidents occurred within 500 meters of schools in all neighbourhoods except Victoria West?
print("\nStarting Question 3...")

#assign variables to crime year, buffer size, crime type, neighbourhoods
bufferSize = "500 Meters"
neighbourhood = "Neighbourh <> 'Victoria West'"
print("Variables assigned...")

#assign crime year and type
crimeYear = 2017
crimeType1 = 'Drugs'
crimeType2 = 'Liquor'
crimeType3 = 'Disorder'
#Assign variable to crime selection
crimeYearType = "(incident_d LIKE '%%%s%%'" %crimeYear + ") And (parent_inc LIKE '%%%s%%'" %crimeType1 + " Or parent_inc LIKE '%%%s%%'" %crimeType2 + " Or parent_inc LIKE '%%%s%%'" %crimeType3 + ")"
print("Crime SQL =", crimeYearType)

#select drug, liquor and disorder crimes in 2017
ap.analysis.Select('Crimes', "drug_liq_disorder_crime2017", crimeYearType)
drugLiqDisCrime2017 = "drug_liq_disorder_crime2017"
print("Crimes in 2017 selected...")

#select all neighbourhoods except Victoria West
ap.analysis.Select('Neighbourhoods', "neighbourh_Not_Vic_West", neighbourhood)
nhood_NotVicWest = "neighbourh_Not_Vic_West"
print("Neighbourhoods selected...")

#Intersect buffered schools and neighbourhoods
ap.analysis.Intersect(['Schools', nhood_NotVicWest], "School_in_neighbourhood_Not_VicWest_intersect", "ALL", None, "INPUT")
nhoodSchools = "School_in_neighbourhood_Not_VicWest_intersect"
print("Intersect Buffered Schools in Neighbourhood Complete...")

#buffer schools
ap.analysis.Buffer(nhoodSchools, "schoolBuff500m", bufferSize, "FULL", "ROUND", "ALL", None, "PLANAR")
buffSchool500 = "schoolBuff500m"
print("Schools Buffered...")

#intersect 2017 drug, liquor and disorder crime with buffer Schools
ap.analysis.Intersect([drugLiqDisCrime2017, buffSchool500], "drug_liq_disorder_crime_500m_school", "ALL", None, "INPUT")
school500DrugLiqDisorderCrime = "drug_liq_disorder_crime_500m_school"

#count the number of crimes within 500m schools in all neighbourhoods except Victoria West
countCrimesQ3 = ap.management.GetCount(school500DrugLiqDisorderCrime)
print("There were", str(countCrimesQ3), "crimes that occur within 500m of schools in all neighbourhoods except Victoria West in 2017.")

#
#
#
#
#Question 4: In 2017, how many property crime incidents occurred within 100 meters of parks in the Oaklands, Fernwood, and North/South Jubilee neighbourhoods?

print("\nStarting Question 4...")

#assign variable to buffer size, neighbourhoods
bufferSize = "100 Meters"
neighbourhood = "Neighbourh = 'Oaklands' Or Neighbourh = 'Fernwood' Or Neighbourh = 'North Jubilee' Or Neighbourh = 'South Jubilee'"
print("Variables assigned...")

#assign crime year and type
crimeYear = 2017
crimeType = 'Property Crime'
#Assign variable to crime selection
crimeYearType = "(incident_d LIKE '%%%s%%'" %crimeYear + ") And (parent_inc LIKE '%%%s%%'" %crimeType + ")"
print("Crime SQL =", crimeYearType)

#select property crimes in 2017
ap.analysis.Select('Crimes', "property_crime2017", crimeYearType)
propertyCrime = "property_crime2017"
print("Crimes selected...")


#select Oaklands, Fernwood, and North/South Jubilee neighbourhoods (from Question 2)
nhood_OakFernNSJubilee = "neighbourh_OakFernNSJubilee"
print("Neighbourhoods selected...")


#Intersect parks and neighbourhoods
ap.analysis.Intersect(['Parks', nhood_OakFernNSJubilee], "parks_in_neighbourhood_OakFernNSJubilee_intersect", "ALL", None, "INPUT")
nhoodParks = "parks_in_neighbourhood_OakFernNSJubilee_intersect"
print("Intersect Parks in Neighbourhood Complete...")

#buffer parks
ap.analysis.Buffer(nhoodParks, "parksBuff100m", bufferSize, "FULL", "ROUND", "ALL", None, "PLANAR")
buffParks100 = "parksBuff100m"
print("Parks Buffered...")

#intersect 2017 property crime with buffer parks
ap.analysis.Intersect([propertyCrime, buffParks100], "Property_crime_100m_parks", "ALL", None, "INPUT")
parks100PropertyCrime = "Property_crime_100m_parks"

#count the number of crimes within 100m of parks in Oaklands, Fernwood, and North/South Jubilee neighbourhoods
countCrimesQ4 = ap.management.GetCount(parks100PropertyCrime)
print("There were", str(countCrimesQ4), "crimes that occur within 100m of parks in Oaklands, Fernwood, and North/South Jubilee neighbourhoods in 2016.")

#
#
#
#
#Question 5: In 2015, how many drug and liquor and disorder incidents occurred within 100 meters of schools in all neighbourhoods except Victoria West?
print("\nStarting Question 5...")

#assign variables to crime year, buffer size, crime type, neighbourhoods
bufferSize = "100 Meters"
neighbourhood = "Neighbourh <> 'Victoria West'"
print("Variables assigned...")

#assign crime year and type
crimeYear = 2015
crimeType1 = 'Drugs'
crimeType2 = 'Liquor'
crimeType3 = 'Disorder'
#Assign variable to crime selection
crimeYearType = "(incident_d LIKE '%%%s%%'" %crimeYear + ") And (parent_inc LIKE '%%%s%%'" %crimeType1 + " Or parent_inc LIKE '%%%s%%'" %crimeType2 + " Or parent_inc LIKE '%%%s%%'" %crimeType3 + ")"
print("Crime SQL =", crimeYearType)

#select drug, liquor and disorder crimes in 2015
ap.analysis.Select('Crimes', "drug_liq_disorder_crime2015", crimeYearType)
drugLiqDisCrime2015 = "drug_liq_disorder_crime2015"
print("Crimes in 2015 selected...")

#select all neighbourhoods except Victoria West (from Question 3)
nhood_NotVicWest = "neighbourh_Not_Vic_West"
print("Neighbourhoods selected...")

#Intersect schools and neighbourhoods
ap.analysis.Intersect(['Schools', nhood_NotVicWest], "parks_in_neighbourhood_Not_VicWest_intersect", "ALL", None, "INPUT")
nhoodSchool = "parks_in_neighbourhood_Not_VicWest_intersect"
print("Intersect Schools in Neighbourhood Complete...")

#buffer schools
ap.analysis.Buffer(nhoodSchool, "schoolBuff100m", bufferSize, "FULL", "ROUND", "ALL", None, "PLANAR")
buffSchool100 = "schoolBuff100m"
print("Schools Buffered...")

#intersect 2015 drug, liquor and disorder crime with buffer schools
ap.analysis.Intersect([drugLiqDisCrime2015, buffSchool100], "drug_liq_disorder_crime_100m_school", "ALL", None, "INPUT")
school100DrugLiqDisorderCrime = "drug_liq_disorder_crime_100m_school"

#count the number of crimes within 100m of schools in all neighbourhoods except Victoria West

countCrimesQ5 = ap.management.GetCount(school100DrugLiqDisorderCrime)
print("There were", str(countCrimesQ5), "crimes that occur within 100m of schools in all neighbourhoods except Victoria West in 2015.")

#
#
#
#
#Question 6: Iteration
import numpy as np
import pandas as pd

crimeTypes = ['Robbery', 'Assault', 'Property Crime', 'Theft', 'Theft from Vehicle']
dayCounter = [None] * 7 #gives array with 7 elements with nothing inside it
maxDays = [[None] * 3] * len(crimeTypes) #len takes the number of values in the crimeType array to make that many arrays for maxDays
print("Created arrays...")

#For each crime type
for i in (np.arange(len(crimeTypes))):
    crime = crimeTypes[i]
    print('\n\nStarting ' + crime + " crimes...")
    
    # For each day
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for j in (np.arange(len(days))):
        day = days[j]
        print('\n\nStarting ' + day + ' ' + crime + " crimes...")
        
        #Select and count crimes
        crime = crimeTypes[i]
        day = days[j]
        
        whereExpr = "(day_of_wee LIKE '%s'" %day + ") And (parent_inc = '%s'" %crime + ")"
        ap.management.SelectLayerByAttribute("Crimes", "NEW_SELECTION", whereExpr)
        countCrimes = ap.management.GetCount('Crimes')
        dayCounter[j] = int(countCrimes[0])
        print("There were", countCrimes[0], crime, "crimes on", day)
        
    #Find max crime
    maxCrime = np.amax(dayCounter)

    #get max day
    maxCrimeDay = days[np.where(dayCounter == np.amax(dayCounter))[0][0]]

    #populate maxDays with crime and day of the highest crime
    maxDays[i] = [crime, maxCrimeDay, maxCrime]
    print("\nThe highest crime count was", maxDays[i][0], "crimes on", maxDays[i][1], "with", maxDays[i][2], "crimes reported.")


#put results into a csv file
dataframe = pd.DataFrame.from_records(maxDays)
dataframe.to_csv(r"E:\School\Geog428\Assign2\LoopResults.csv", index = False)
print("CSV file created...")

print("\n\nMax crime day for each crime type:", maxDays)
print("\nDone Program!")
