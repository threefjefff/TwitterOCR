import sys
import pyocr.builders
import regex


tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)

# The tools are returned in the recommended order of usage
ocrTool = tools[0]
print("Will use tool '%s'" % (ocrTool.get_name()))
langs = ocrTool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))
# Prefer english, otherwise use whatever's available
if 'eng' not in langs:
    lang = langs[0]
else:
    lang = 'eng'
print("Will use lang '%s'" % (lang))

def text_from_image(img):
    """Get the text from a Pillow image"""
    return ocrTool.image_to_string(
        img,
        lang=lang,
        builder=pyocr.builders.TextBuilder()
    )
def twitter_handle(text):
    """Does it contain a @twittername? Then it's a fucking tweet"""
    result = regex.search("(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z_]+[A-Za-z0-9_]+)", text)
    if result is not None:
        return result.group(0)
    else:
        return result

def multiline_cleanup(text):
    """Replace new lines with whitespace, cut down on padding"""
    clean = regex.sub("[\s+|\t|\r\n]", " ", text)
    return regex.match("(?:%s)(.*)" % twitter_handle(clean), clean)