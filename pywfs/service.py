#!/usr/bin/python3
# -*- coding: UTF-8 -*-


import bs4


class Service:
    def __init__(self, wfsName, mapfilecsv):
        
        # Name for WFS-servicec
        self.wfsName  = wfsName
        
        self.mapfilecsv = mapfilecsv
        
        # Available layer in wfs-service
        self.layers = []
        
        # Pseudo mercator
        DefaultCRS="EPSG:3857"
        
        ## Read in values
        for i, line in enumerate(open(mapfilecsv)):
            row = line.strip().split(";")
            if i == 0:
                header = row
            else:
                
                if row[0]:
                    layer = {}
                    for j, col in enumerate(row):
                        layer[header[j].lower()] = col
                        
                    # Likt for alle lag
                    layer["defaultcrs"] = DefaultCRS
                    
                    self.layers.append(layer)
        
    def returnGetCapabilities(self):
        """
        Ansvering getCapabilities request
        """
        
        # Kun disse kolonnene skal med
        getCapKeys = ["name",
                      "title",
                      "defaultcrs",
                      "abstract",
                      "description",
                      "color",
                      "outlinecolor"]
        
        getCapKeys_up = ["Name",
                         "Title",
                         "DefaultCRS",
                         "Abstract",
                         "Description",
                         "color",
                         "outlinecolor"]
            
        capabilities = bs4.BeautifulSoup(features="xml")
        main = capabilities.new_tag("WFS_Capabilities", version="2.0.0")
            
            
        FeatureTypeList = capabilities.new_tag("FeatureTypeList")
            
        for layer in self.layers:
        
            newLayer = capabilities.new_tag("FeatureType")
            
            for key in layer.keys():
                
                if key in getCapKeys:
                    val = layer[key]
                    
                    # Get uppercase key
                    key_up = getCapKeys_up[getCapKeys.index(key)]
                    
                    tag = capabilities.new_tag(key_up)
                    if type(val) == str:
                        tag.string  = val
                    newLayer.append(tag)

            FeatureTypeList.append(newLayer)
            
        main.append(FeatureTypeList)
        capabilities.append(main)
            
        print("Content-type: text/xml; charset=UTF-8\n")
        print(capabilities)
    
    def returnGetFeature(self):
        
        if "typenames" in self.requestDict:
            layerName  = self.requestDict["typenames"]
        elif "typename" in self.requestDict:
            layerName = self.requestDict["typename"]
        
        
        #"naturopplevelser/geodata"
        
            
        if "outputformat" in self.requestDict:
            outputformat = self.requestDict["outputformat"]
        else:
            outputformat = "gml"
            
        if outputformat == "geojson":
            printMessage = "Content-type: text/json; charset=UTF-8\n"
        else:
            printMessage = "Content-type: text/xml; charset=UTF-8\n"
        
        # 
        csvDir = "/".join(self.mapfilecsv.split("/")[:-1])
        for layer in self.layers:
            if layerName == layer["name"]:
                relAddress = layer["data"]
        
        directory  = "/".join([csvDir, relAddress])
        
        filename = "/".join([directory, layerName])
        file = ".".join([filename, outputformat])
        
        
        #file = open("/var/www/markakartet/wfs/data/naturopplevelser/geodata/eventyrskog.gml","r")
        openfile = open(file,"r")
        
        print(printMessage)
        #print(file)
        for line in openfile:
            print(line)
        
        openfile.close()
        
        
        
        
    def returnDescribeFeatureType(self):
        """
        Answer describe feature type
        """
        delim = ","
        
        if "typenames" in self.requestDict:
            layerName  = self.requestDict["typenames"]
        elif "typename" in self.requestDict:
            layerName = self.requestDict["typename"]
            
        for layer in self.layers:
            if layer["name"] == layerName:
                if "columns" in layer:
                    kolonner = layer["columns"].split(delim)
                    

        ### Start xml document
        soup = bs4.BeautifulSoup(features="xml")
        
        main = soup.new_tag("schema",
                            xmlns = "http://www.w3.org/2001/XMLSchema",
                            elementFormDefault="qualified",
                            version="0.1")
        
        complexType = soup.new_tag("complexType")
        complexType["name"] = layerName + "Type"
        

        #complexType.append(description)
        
        complexContent = soup.new_tag("complexContent")
        extension = soup.new_tag("extension")
        sequence = soup.new_tag("sequence", base="gml:AbstractFeatureType")
        
        # geom element
        element = soup.new_tag("element")
        element["name"] = "geom"
        element["minOccurs"] = "0"
        element["maxOccurs"] = "1"
        element["type"] = "gml:GeometryPropertyType"
        sequence.append(element)
        
        for typeAndName in kolonner:
            
            coltype, colname = typeAndName.split(":")
            
                    
            element = soup.new_tag("element")
            element["minOccurs"] = "0"
            
            element["name"] = colname
            element["type"] = coltype
            
            sequence.append(element)
            
            
        description = soup.new_tag("Description")
        description.string = "Beskrivelse"
        #complexType.append(description)
        #complexContent.append(description)
        #main.append(description)
        extension.append(description)
        
        extension.append(sequence)
        complexContent.append(extension)
        complexType.append(complexContent)
        main.append(complexType)
        
        print("Content-type: text/xml; charset=UTF-8\n")
        print(main)
        
        
    
    
    ###############################
    def response(self, query):
        """
        Analyse the incoming query

        """
        if not query:
            print("Content-type: text/html; charset=UTF-8\n")
            print("Last hjelpeside!")

        self.requestDict = {}
        for kvp in query.split("&"):
            key, value = kvp.split("=")
            self.requestDict[key.lower()] = value
            
        
        
        # If other than WFS is requested
        if "service" in self.requestDict:
            if self.requestDict["service"].lower() != "wfs":
                print("Content-type: text/html; charset=UTF-8\n")
                print("This service only serves WFS-requests.")
                print("Plesase use: service=wfs")
                
        
        # Check if request is valid            
        if "request" in self.requestDict:
            if self.requestDict["request"].lower() == "getcapabilities":
                self.returnGetCapabilities()
            elif self.requestDict["request"].lower() == "getfeature":
                self.returnGetFeature()
            elif self.requestDict["request"].lower() == "describefeaturetype":
                self.returnDescribeFeatureType()
            else:
                print("Content-type: text/html; charset=UTF-8\n")
                print("Unsuported request: {}".format(self.requestDict["request"]))
                print("<br>")
                print("Please use: (request=)")
                print("GetCapabilities, getFeature or describeFeatureType")
                
                
        else: # Ingen request
            print("Content-type: text/html; charset=UTF-8\n")
            print("No request! ")
            
        
        
        
        if False: # verdier
            print("Content-type: text/html; charset=UTF-8")
            print()
            print("Foresporsel: ")
            print(query)
        
            print(self.requestDict)
            
            print("<br><br>")
            print("Kartlag:")
            print(self.layers)
        

            

            
            
