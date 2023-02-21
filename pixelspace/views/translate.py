from colormath.color_objects import LabColor, sRGBColor, AdobeRGBColor
from colormath.color_conversions import convert_color




def RGBConvert(light, axisA, axisB):
    lab = LabColor(light, axisA, axisB)
    #print(lab)
    try:
        rgb = convert_color(lab, AdobeRGBColor)
        print(rgb)
        return True
    except:
        return False

def sRGBConvert(light, axisA, axisB):
    lab = LabColor(light, axisA, axisB)
    #print(lab)
    try:
        srgb = convert_color(lab, sRGBColor)
        print(srgb)
        return True
    except:
        return False


def main():
    #lab = LabColor(0.903, 16.296, -2.22)
    light = -10000
    axisA = 100000
    axisB = 10000000
    print(RGBConvert(light, axisA, axisB))
    print(sRGBConvert(light, axisA, axisB))


main()