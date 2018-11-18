import requests
import json
from json2table import convert
import webbrowser

top10Virus = "https://worldmap3.f-secure.com/api/top10"
streamURL = "https://worldmap3.f-secure.com/api/stream"
detectionsAfterMatch = {}


def responseGenerator(URL):
    response = requests.get(URL)  # Get the response
    return response.json()


def changeKeyName(json, newKeyName, oldKeyName):  # Edit Json Key Name
    json[newKeyName] = json.pop(oldKeyName)


def matchDetections(firstList, secondList):
    global detectionsAfterMatch
    index = 0
    for val1 in secondList["detections"]:
        for val2 in firstList["Detections"]:
            if val1["name"] == val2["name"]:
                detectionsAfterMatch[index] = val1
                index = index + 1
    return detectionsAfterMatch


topTenData = responseGenerator(top10Virus)
streamURLData = responseGenerator(streamURL)

changeKeyName(topTenData, "Time Of The Report Generated", "response_generated")
changeKeyName(topTenData, "Polling Interval", "polling_interval")
changeKeyName(topTenData, "Detections", "detections")

# Table HTML Config
build_direction = "LEFT_TO_RIGHT"
table_attributes = {"style": "width:50%", "class": "table table-striped", "border": 3}
matched_Table_Attributes = {"class": "table table-striped", "border": 1}
topTenHTML = convert(topTenData, build_direction=build_direction, table_attributes=table_attributes)
matchedAsJson = json.dumps(matchDetections(topTenData, streamURLData))
loadedJson = json.loads(matchedAsJson)
matchedHTML = convert(loadedJson, build_direction=build_direction, table_attributes=matched_Table_Attributes)
HTMLFile = open("TopTenVirus.html", "w")
HTMLFile.write("<h3>Top Ten Detections:</h3>")
HTMLFile.write(topTenHTML)  # Save the top ten results to HTML Page
HTMLFile.write("</br></br>")
HTMLFile.write("<h3>Matched Detections With Info.</h3>")
HTMLFile.write(matchedHTML)  # Save the matched results to HTML Page
webbrowser.open('TopTenVirus.html')  # Open the HTML Page
