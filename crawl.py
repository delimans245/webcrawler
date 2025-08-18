from urllib.parse import urlparse

def normalize_url(url):
    '''
    Normalize a URL by:
    - Removing the protocol (https:/http:)
    - Checking for match in characters regardless of upper/lower case
    - Normalize regardless of whether it has ONE ending slash or not
    - Removing query parameters and fragments
    '''

    #parse the url
    generalUrl = urlparse(url)

    #getting the path name of the url
    pathName = generalUrl.path

    #convert to lowercase in all cases
    result = (generalUrl.netloc + pathName).lower()

    #stripping any trailing slashes(/)
    if (result[len(result) - 1] == "/"):
        return result[:-1]
    return result