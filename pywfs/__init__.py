
# Import new service object
from pywfs.service import service
# When loaded it is assumed that the directory is above

if __name__ == "__main__":
    #a = pywfs.service("hei")
    a = service("hei")
    print(a)