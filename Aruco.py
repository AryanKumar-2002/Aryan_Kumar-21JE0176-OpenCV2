import cv2 as cv, numpy as np
import Squares as sq

__markerSources = [
           cv.imread("assets/1.jpg"),
           cv.imread("assets/2.jpg"),
           cv.imread("assets/3.jpg"),
           cv.imread("assets/4.jpg")]

testMode = (0,0,0,0,1)

__dictionaries = {
    "(5*5, 50)"   : cv.aruco.DICT_5X5_50,
	"(5*5, 100)"  : cv.aruco.DICT_5X5_100,
	"(5*5, 250)"  : cv.aruco.DICT_5X5_250,
	"(5*5, 1000)" : cv.aruco.DICT_5X5_1000,
    
	# "(4*4, 50)"  : cv.aruco.DICT_4X4_50,
	# "(4*4, 100)"  : cv.aruco.DICT_4X4_100,
	# "(4*4, 250)"  : cv.aruco.DICT_4X4_250,
	# "(4*4, 1000)"  : cv.aruco.DICT_4X4_1000,

	# "(6*6, 50)"  : cv.aruco.DICT_6X6_50,
	# "(6*6, 100)"  : cv.aruco.DICT_6X6_100,
	# "(6*6, 250)"  : cv.aruco.DICT_6X6_250,
	# "(6*6, 1000)"  : cv.aruco.DICT_6X6_1000,

	# "(7*7, 50)"  : cv.aruco.DICT_7X7_50,
	# "(7*7, 100)"  : cv.aruco.DICT_7X7_100,
	# "(7*7, 250)"  : cv.aruco.DICT_7X7_250,
	# "(7*7, 1000)"  : cv.aruco.DICT_7X7_1000,
}

def setMarkerSources(markerSources):
    global __markerSources
    __markerSources = markerSources

def getMarkerSources():
    return __markerSources.copy()

def getMarkersInfo(allMarkerSources = getMarkerSources()):
    allMarkers = {}
    allMarkersId = {}

    for i in range(len(allMarkerSources)):
        frameMarkers = []
        frameMarkersId = []

        for dName in __dictionaries:
            dictionary = cv.aruco.Dictionary_get(__dictionaries[dName])
            parameters = cv.aruco.DetectorParameters_create()
            squares, ids, _ = cv.aruco.detectMarkers(allMarkerSources[i], dictionary, parameters = parameters)
            try: ids.copy()
            except AttributeError: 
                frameMarkers.append([])
                continue

            for j in range(len(squares)):
                marker = []
                frameMarkersId.append(ids[j][0])

                for k in range(4):
                    coordinate = int(tuple(squares[j].tolist()[0][k])[0]), int(tuple(squares[j].tolist()[0][k])[1])
                    marker.append(coordinate)

                frameMarkers.append(marker)
            break

        allMarkers[i+1] = frameMarkers
        allMarkersId[i+1] = frameMarkersId
    return allMarkers, allMarkersId

def rotate(image, angle, centre):
    height, width = image.shape[:2]
    rotationMatrix = cv.getRotationMatrix2D(center = centre, angle = angle, scale=1)
    rotatedImage = cv.warpAffine (src= image, M= rotationMatrix, dsize= (width,height))
    return rotatedImage

def crop(image, corner1, corner2):
    x1 = corner1[0]
    y1 = corner1[1]

    x2 = corner2[0]
    y2 = corner2[1]

    crop = image[y2:y1, x1:x2]
    return crop

def addPadding(image):
    oldHeight, oldWidth, channels = image.shape

    newHeight = int(1.45 * oldHeight)
    newWidth = int(1.45 * oldWidth)
    paddedImage = np.full((newHeight,newWidth, channels), (0,0,0), dtype=np.uint8)

    centreY = (newHeight - oldWidth) // 2
    centreX = (newWidth - oldWidth) // 2

    paddedImage[centreY: centreY + oldHeight, centreX: centreX + oldWidth] = image
    return paddedImage

def test1():
    allMarkerSources = getMarkerSources()
    allMarkerSources.append(cv.imread("assets/CVtask.jpg"))
    allMarkers = {}
    allMarkersId = {}

    for i in range(len(allMarkerSources)):
        frameMarkers = []
        frameMarkersId = []
        print("Marker source no.:", i+1)

        for dName in __dictionaries:
            dictionary = cv.aruco.Dictionary_get(__dictionaries[dName])
            print("    Looking for appropriate dictionary in ", dName + ", i.e.", dictionary)
            parameters = cv.aruco.DetectorParameters_create()
            squares, ids, a = cv.aruco.detectMarkers(allMarkerSources[i], dictionary, parameters = parameters)
            try: ids.copy()
            except AttributeError:
                print("    Unsuccessful :(\n")
                continue

            print("    Success!!")
            print("    Uff, finally now!! Getting the coordinates of markers in this image.\n")

            for j in range(len(squares)):
                frameMarkersId.append(ids[j][0])
                marker = []
                print("    Marker", j+1, ":")

                for k in range(4):
                    coordinate = int(tuple(squares[j].tolist()[0][k])[0]), int(tuple(squares[j].tolist()[0][k])[1])
                    print("        ", str(chr(ord("a") + k)), ": ", coordinate)
                    marker.append(coordinate)
                
                frameMarkers.append(marker)
                print()
            break

        allMarkers[i+1] = frameMarkers
        allMarkersId[i+1] = frameMarkersId
    print("Marker coordinates list:", allMarkers, "\n")
    print("Marker IDs list:", allMarkersId, "\n")
if testMode[0]: test1()

def test2():
    s = getMarkerSources()
    #s.append(cv.imread("assets/images/CVtask.jpg"))
    allMarkers, allIds = getMarkersInfo(s)
    labeledSources = s

    for i in range(len(allMarkers)):
        for j in range(len(allMarkers[i+1])):
            for coordinate in allMarkers[i+1][j]:
                cv.drawContours(labeledSources[i], np.array(coordinate).reshape((-1,1,2)).astype(np.int32), -1, (255,0,0), 10)

    cv.imshow("Marker source 1", labeledSources[0])
    cv.imshow("Marker source 2", labeledSources[1])
    cv.imshow("Marker source 3", labeledSources[2])
    cv.imshow("Marker source 4", labeledSources[3])
    # cv.imshow("Marker source 5", labeledSources[4])
    if cv.waitKey(0) == ord ("q"): cv.destroyAllWindows()
if testMode[1]: test2()

def test3():
    image = cv.imread("assets/1.jpg")
    markers,_ = getMarkersInfo([image])
    marker = markers[1][0]

    centre = sq.getCentreSquare(marker)
    angle = sq.getAngleSquare(marker)

    rotated = rotate(image, angle, centre)

    cv.imshow ("Original", image)
    cv.imshow ("Rotated", rotated)
    if cv.waitKey(0) == ord ("q"): cv.destroyAllWindows()
if testMode[2]: test3()

def test4():
    image = cv.imread("assets/1.jpg")
    markers,_ = getMarkersInfo([image])
    marker = markers[1][0]

    centre = sq.getCentreSquare(marker)
    angle = sq.getAngleSquare(marker)
    rotated = rotate(image, angle, centre)

    rotatedMarkers,_ = getMarkersInfo([rotated])
    rotatedMarker = rotatedMarkers[1][0]
    cropped = crop(rotated, rotatedMarker[0], rotatedMarker[2])

    cv.imshow ("Original", image)
    cv.imshow ("Rotated and Cropped", cropped)
    if cv.waitKey(0) == ord ("q"): cv.destroyAllWindows()
if testMode[3]: test4()

def test5():
    image = cv.imread("assets/1.jpg")
    paddedImage = addPadding(image)

    cv.imshow ("Original", image)
    cv.imshow ("Padded Image", paddedImage)
    if cv.waitKey(0) == ord ("q"): cv.destroyAllWindows()
if testMode[4]: test5()