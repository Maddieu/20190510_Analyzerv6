import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


def readolddata(self, backgrounddata, workingdirectorypath, datafoldername, analysisfolderpath, progressbarfolder,
                  datalengthlimit, parentdirectorypath):
    filelist = []
    bgsubstrdatalist = []
    summedmassspec = []
    for file in os.listdir(workingdirectorypath):
        filelist.append(file)
    for element in range(1, filelist.__len__() - 1):
        bgsubstrdatalist.append([])

        with open(datafoldername + '_' + str(element).zfill(3) + '.dat', 'r', encoding="cp1252") as file:

        #with open(datafoldername + '_' + str(element).zfill(3) + '.dat', 'r', encoding="cp1252") as file:
            #print('open file: ', datafoldername + '_' + str(element).zfill(3) + '.dat of insgesamt',
            #      filelist.__len__() - 2)
            #print('readrawdatav2, element:', element, '\t\ttotal number of files:', filelist.__len__() - 2)
            progressbarfolder.setValue(round(element / (filelist.__len__() - 2) * 100))

            #
            #                               Updates the Progress Bar.
            #                                       Does this slow down the program?
            #                                       Or cause a crash?
            #

            qApp.processEvents()

            i = 0
            j = 0

            for n, line in enumerate(file):

                # print('File Nr.:', element, 'from:', filelist.__len__()-2, '/// line:', i)
                i = i + 1
                #print(n, line)

                    ## read Number of Gigasamples:
                if n == 1:
                    timebase = float(line.split()[0])
                    #print('\ttimebase:\t', timebase)



                if n > 5:
                    bgsubstracteddatapoint = (int(line.replace('\n', "")) - int(backgrounddata[j]))
                    bgsubstrdatalist[element - 1].append(str(bgsubstracteddatapoint))
                    if element == 1:
                        summedmassspec.append(0)
                    summedmassspec[j] = summedmassspec[j] + bgsubstracteddatapoint
                    j = j + 1
                if i > datalengthlimit:
                    break

    return bgsubstrdatalist, summedmassspec, timebase



#
#       for the mono file we're doing some cheating
#           we 'normally' read in the data
#           then, we find out the energy-set and photocurrent column
#           and we will just return a 'cheated' monofilecontent list-list
#              with all zeros but columns 3 and 5
#              which correspond to the new columns of energy and photocurrent in the new monofiles



def readoldmonofile(self, workingdirectorypath, datafoldername, parentdirectorypath):
    print('## reading old mono file ##')
    os.chdir(workingdirectorypath)

    with open(datafoldername + '_Mono.txt', 'r', encoding="cp1252") as file:

        monofilecontent = []
        i = 0
        print('readoldmono_test0')

        for n, elementline in enumerate(file):
            if n > 3:
                monofilecontent.append([])
                for elementdata in elementline.split('\t'):
                    monofilecontent[i].append(elementdata)
                i = i + 1

    print('readoldmono_test1')

    monofilecontent_photocurrent = []
    monofilecontent_photonenergy = []
    for energy, content in enumerate(monofilecontent):
        monofilecontent_photocurrent.append(monofilecontent[energy][-1])
        monofilecontent_photonenergy.append(monofilecontent[energy][1])
    print('readoldmono_test2')

    for energyindex in range(monofilecontent_photocurrent.__len__()):
        monofilecontent[energyindex] = [0, 0, 0, monofilecontent_photonenergy[energyindex], 0, monofilecontent_photocurrent[energyindex]]
    print('readoldmono_test3')

    for energyelement in monofilecontent:
        pass
        #print(energyelement)

    return monofilecontent

# 3 and 5


def readoldbackground(self, workingdirectorypath, datafoldername, analysisfolderpath, parentdirectorypath):

    os.chdir(workingdirectorypath)



    backgrounddata = []


    #print('test_201904091146_1')
    #print(datafoldername)
    with open(datafoldername + '_Untergrund.dat', 'r', encoding="cp1252") as file:
        for n, line in enumerate(file):
            if n > 5:
                backgrounddata.append(line.replace('\n', ""))



    return backgrounddata