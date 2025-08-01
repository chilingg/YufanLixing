import os

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

_namespaceList = dict()

def svgParse(path):
    global _namespaceList
    _namespaceList = dict([node for _, node in ET.iterparse(path, events=['start-ns'])])
    for k, v in _namespaceList.items():
        ET.register_namespace(k, v)
    
    return ET.parse(path)

FONT_VARSION = "1.0"
CHAR_WIDTH = 1000
GLYPHS_DIR = 'glyph'
SYMBOLS_DIR = 'symbol'

def generateFont():
    import fontforge
    font = fontforge.open("config.sfd")
    font.version = FONT_VARSION
    font.createChar(32).width = int(CHAR_WIDTH/4) #空格
    
    errorList = {}
    charList = []

    with open(GLYPHS_DIR + '/char_list.txt', 'r', encoding='UTF-8') as f:
        charList = f.read().splitlines()

    num = len(charList)
    count = 0
    for i in range(num):
        char = charList[i]
        code = ord(char)
        width = CHAR_WIDTH
        filePath = '%s/%s.svg' % (GLYPHS_DIR, char)
        count += 1

        print("(%d/%d)%s: import glyph '%s' %d" % (count, num, font.fontname, char, code))
        
        try:
            glyph = font.createChar(code)
            glyph.importOutlines(filePath)
            glyph.width = width
        except Exception as e:
            errorList[char] = e
            print(char, e)

    symTargets = os.listdir(SYMBOLS_DIR)
    symList = []
    num = len(symTargets)
    symCount = 0
    for filename in symTargets:
        filePath = '%s/%s' % (SYMBOLS_DIR, filename)
        if(filename[-4:] == '.svg'):
            if(filename[:-4].isdecimal()):
                n = int(filename[:-4])
                char = chr(n)
                code = n
                width = int(float(svgParse(filePath).getroot().attrib['viewBox'].split()[2]))
            else:
                continue

            symList.append(char)
            symCount += 1
            print("(%d/%d)%s: import symbol glyph '%s' %d from %s" % (symCount, num, font.fontname, char, code, filename))
            
            try:
                glyph = font.createChar(code)
                glyph.importOutlines(filePath)
                glyph.width = width
            except Exception as e:
                errorList[filename] = e
                print(filename, e)
    
    font.selection.all()
    font.removeOverlap()

    if len(errorList):
        print("\n%d glyphs with errors!" % len(errorList))
        for name, e in errorList.items():
            print(name, e)
    
    with open('char_list.txt', 'w') as f:
        f.write(''.join(symList))
        f.write('\n')
        f.write(''.join(charList))

    print("\n%s: The Font has %d glyphs" % (font.fontname, count + symCount - len(errorList)))
    print("Generate font file in %s\n" % (font.fontname + ".otf"))
    
    font.generate(font.fontname + ".otf")
    font.save(font.fontname + ".sfd")
    font.close()

if __name__ == '__main__':
    generateFont()