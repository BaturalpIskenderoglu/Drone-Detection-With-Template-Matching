import cv2

#this module contains methods for template matching

def match_template(image, threshold):
    """"
    This method takes an 256x256 gray filtered image and apply template matching for 10 different templates
    if there is one match or multiple matches this method returns {"bbox": [x_min,y_min,x_max,y_max], "prediction": 1}
    (bounding box is chosen according to match with highest value)

    if there is no match this method returns {"bbox": [0,0,0,0], "prediction": 0} 
    """

    max_score = threshold
    best_result = {"bbox": [0,0,0,0], "prediction" : 0}
    
    # Check image size
    height, width = image.shape[:2]
    if height != 256 or width != 256:
        print(f"Error: Image must be 256x256 \n Given image shape: {width}x{height}")
        return best_result

    template_paths = ["templates\\1-160-_jpeg_jpg.rf.4X3Q7XtVq16nEh0eNhYf.jpg",
                 "templates\\1-191-_jpeg_jpg.rf.HnscyZH7gEHDLl0n44sm.jpg",
                 "templates\\1-296-_jpeg_jpg.rf.iI8agYkSxagX9ufc4dcD.jpg",
                 "templates\\1-428-_jpeg_jpg.rf.MVIfAhUNqPoMhiUc3c2K.jpg",
                 "templates\\00002_jpg.rf.dhL7R2h7TvmSY1iVGEGk.jpg",
                 "templates\\00003_jpg.rf.2liGlM5tFMA64jQnZS5X.jpg",
                 "templates\\00004_jpg.rf.dPH152PKm6I9idsBre23.jpg",
                 "templates\\00023_jpg.rf.lQOrU8T8V1o0guQbHDaX.jpg",
                 "templates\\00037_jpg.rf.mqCPY5Ty8qt0OvgdRIka.jpg",
                 "templates\\00040_jpg.rf.liTPrzHEZ7TSdazI9QYU.jpg"
                 ]
    
    for template_path in template_paths:
        template = cv2.imread(template_path)

        if template is None:
            print(f"Warning template image could not be read. Template file path: {template_path}")
            continue

        # apply gray filter
        gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        
        # Try for different scales
        scales = [256, 128, 64, 32]
        for scale in scales:
            scaled_template = cv2.resize(gray_template,(scale,scale))
            result = cv2.matchTemplate(image, scaled_template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_location, max_location = cv2.minMaxLoc(result)
            
            if max_val >= threshold:
                # match found
                top_left = max_location
                matching_result = {"bbox": [top_left[0], top_left[1], top_left[0] + scale, top_left[1] + scale], "prediction" : 1}
                
                if max_val >= max_score:
                    # better match found
                    max_score = max_val
                    best_result = matching_result

    return best_result
