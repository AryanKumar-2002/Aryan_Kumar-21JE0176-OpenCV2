import cv2 as cv
from cv2 import imshow
import Masking as mask, Squares as sq, Aruco as aruco

image = mask.getImage()

temp = sq.getSquares()

squares = [temp[1][0], temp[2][0], temp[3][0]]
sizeOfSquares = [sq.getLenSquare(squares[0]), sq.getLenSquare(squares[1]), sq.getLenSquare(squares[2])]
angleOfSquares = [sq.getAngleSquare(squares[0]), sq.getAngleSquare(squares[1]), sq.getAngleSquare(squares[2])]

temp = aruco.getMarkerSources()
markers = [temp[0], temp[1], temp[2]]
temp,_ = aruco.getMarkersInfo(markers)
cofMarkers = [temp[1][0], temp[2][0], temp[3][0]]

for i in range(len(squares)): 

    centre = sq.getCentreSquare(cofMarkers[i])
    angle = sq.getAngleSquare(cofMarkers[i])
    rotated = aruco.rotate(markers[i], angle, centre)

    rotatedMarkers,_ = aruco.getMarkersInfo([rotated])
    rotatedMarker = rotatedMarkers[1][0]
    cropped = aruco.crop(rotated, rotatedMarker[0], rotatedMarker[2])

    resized = cv.resize(cropped, (sizeOfSquares[i],sizeOfSquares[i]))

    angle2 = angleOfSquares[i]
    padded = aruco.addPadding(resized, (90 - angle2))

    centre2 = aruco.getCentreImage(padded)
    rerotated = aruco.rotate(padded, -angle2, centre2)

    x_offset = int(sq.getCentreSquare(squares[i])[0] - sizeOfSquares[i]/2)
    y_offset = int(sq.getCentreSquare(squares[i])[1] - sizeOfSquares[i]/2)

    x_end = x_offset + rerotated.shape[1]
    y_end = y_offset + rerotated.shape[0]

    image[y_offset:y_end, x_offset:x_end] = rerotated

    # cv.imshow("Original", markers[i])
    # mask.showImage()
    # cv.imshow ("Rotated, cropped, resized, padded, rerotated, pasted", image)
    # if cv.waitKey(0) == ord("q"): cv.destroyAllWindows()

mask.showImage()
cv.imshow("Final.jpg", image)
if cv.waitKey(0) == ord("q"): cv.destroyAllWindows()
# cv.imwrite("Final.jpg", image)