import cv2


def findSquares(contours):
    squares = []
    for cnt in contours:
        epsilon = 0.1 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        if len(approx) == 4:
            area = cv2.contourArea(approx)
            if area > 1000:
                print(area)
                squares.append(approx)
    return squares


def cropIfNeeded(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray = cv2.adaptiveThreshold(
    #     gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    # )
    _, gray = cv2.threshold(gray, 125, 255, cv2.THRESH_BINARY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    edged = cv2.Canny(gray, 50, 150)

    contours, _ = cv2.findContours(
        edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)

        image_area = image.shape[0] * image.shape[1]
        contour_area = w * h
        coverage_ratio = contour_area / image_area

        if coverage_ratio > 0.3:
            cropped_image = image[y + 5 : y + h - 5, x + 5 : x + w - 5]
            return cropped_image

    return image


def showImage(image):
    cv2.namedWindow("Test", cv2.WINDOW_NORMAL)
    cv2.imshow("Test", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def imagePreprocess(path):
    image = cv2.imread(path)

    image = cv2.resize(image, (960, 1280))
    showImage(image)
    # cv2.imwrite("C:\\Users\\Asus\\Pictures\\Screenshots\\output.jpg", image)

    image = cropIfNeeded(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # _, blackNwhite = cv2.threshold(gray, 125, 255, cv2.THRESH_BINARY)
    # blur = cv2.GaussianBlur(blackNwhite, (5, 5), 0)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blur, 50, 150)
    contours, _ = cv2.findContours(
        edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    return image, blur, contours


def detectSquares(image_path):
    image, blur, contours = imagePreprocess(image_path)

    squares = findSquares(contours)

    print(f"Number of squares detected: {len(squares)}")

    for i, square in enumerate(squares):
        print(f"Square {i+1} coordinates:")
        for point in square:
            print(f"x: {point[0][0]}, y: {point[0][1]}")

    for square in squares:
        for point in square:
            cv2.circle(image, tuple(point[0]), 12, (0, 0, 255), -1)

    showImage(blur)
    showImage(image)


detectSquares("C:\\Users\\Asus\\Downloads\\test.jpg")
