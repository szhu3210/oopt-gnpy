
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.ticker import FuncFormatter
import os
import re
import csv


def getTestFiles():
    fileList = []
    try:
        print(os.getcwd() + "/test/old_testing")
        files = [f for f in os.listdir(os.getcwd() + "/test/old_testing")]
        wantedLogFiles = [filename for filename in files if filename.startswith("TestPar")]
        # wantedLogFiles = [file for file in wantedLogFiles if file.replace(config_file, "")]
        if len(wantedLogFiles) != 0:
            # numIdentifier = 1
            for i in range(0,len(wantedLogFiles)):
                file = "./test/" + wantedLogFiles[i]
                # if(i % 5 == 0):
                #     fileList.append(wantedLogFiles[i:i + 5])
                print("\"" + file + "\", ")
    except:
        # There was an exception
        print("exception opening a file - log file")
    # return fileList


def plot_to_percent(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    s = str(100 * y)

    # The percent symbol needs escaping in latex
    return s + '%'

# Currently writes results to a csv file specified by name
def plot_to_matrix(tr2, tr4, tr6, tr8, tr1, trmse, trmae):

    with open("./alltraing.csv", 'a') as myfile:
        wr = csv.writer(myfile, delimiter =",", quoting=csv.QUOTE_ALL)
        #listbreak = [x*2 for x in range(0, 50)]
        #wr.writerow(listbreak)
        wr.writerow(tr2)
        wr.writerow(tr4)
        wr.writerow(tr6)
        wr.writerow(tr8)
        wr.writerow(tr1)
        wr.writerow(trmse)
        wr.writerow(trmae)

# Plots a 2 dimensional graph depending on the percentages and iteration number
def plotGraph(val2, val4, val6, val8, val1, title):
    plt.plot(val2)
    plt.plot(val4)
    plt.plot(val6)
    plt.plot(val8)
    plt.plot(val1)
    plt.suptitle(title, fontsize=20)

    # Set the right Y axis format, limit labels and convert to percentages.
    plt.ylabel('Accuracy percentage')
    plt.locator_params(numticks=12)


    # Create the formatter using the function to_percent. This multiplies all the
    # default labels by 100, making them all percentages
    formatter = FuncFormatter(plot_to_percent)

    # Set the formatter
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.show()
    plt.savefig(title + ".png")
    print("Did plot" + title)
    plt.close()



# Recieves a list of files strings and averages the results for each list
# Defined for multiple files, in our case 5.
def averageResults(stringTofind):
    # Collect all files to average by their name (looks for a specific string)
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    files = [filename for filename in files if filename.find(stringTofind) != -1]
    print(len(files))
    # Set temporary lists to work on
    testdb = []
    # val2 = []
    # val4 = []
    # val6 = []
    # val8 = []
    # val1 = []
    tr2 = []
    tr4 = []
    tr6 = []
    tr8 = []
    tr1 = []
    # mseVal = []
    # maeVal = []
    mseTr = []
    maeTr = []
    mseTest = []
    maeTest = []
    list_length = len(files)

    # Sum each file into arrays
    for file in files:
        [testdbcur, testMseCur, testMaeCur, tr2cur, tr4cur, tr6cur, tr8cur, tr1cur, trMseCur, trMaeCur] = CropFile(file)
        testdb.append(testdbcur)
        mseTest.append(testMseCur)
        maeTest.append(testMaeCur)
        # val2.append(val2cur)
        # val4.append(val4cur)
        # val6.append(val6cur)
        # val8.append(val8cur)
        # val1.append(val1cur)
        tr2.append(tr2cur)
        tr4.append(tr4cur)
        tr6.append(tr6cur)
        tr8.append(tr8cur)
        tr1.append(tr1cur)
        # mseVal.append(valMseCur)
        # maeVal.append(valMaeCur)
        mseTr.append(trMseCur)
        maeTr.append(trMaeCur)

    # Arrange final lists, sum up and perform average.
    testdb = np.array(testdb).astype(np.float)
    mseTest = np.array(mseTest).astype(np.float)
    maeTest = np.array(maeTest).astype(np.float)
    # val2 = np.array(val2).astype(np.float)
    # val4 = np.array(val4).astype(np.float)
    # val6 = np.array(val6).astype(np.float)
    # val1 = np.array(val1).astype(np.float)
    # val8 = np.array(val8).astype(np.float)
    tr2 = np.array(tr2).astype(np.float)
    tr4 = np.array(tr4).astype(np.float)
    tr6 = np.array(tr6).astype(np.float)
    tr8 = np.array(tr8).astype(np.float)
    tr1 = np.array(tr1).astype(np.float)
    # mseVal = np.array(mseVal).astype(np.float)
    # maeVal = np.array(maeVal).astype(np.float)
    mseTr = np.array(mseTr).astype(np.float)
    maeTr = np.array(maeTr).astype(np.float)
    finaldb = [listValue / list_length for listValue in testdb.sum(axis=0)]
    # finalval2 = [listValue / list_length for listValue in val2.sum(axis=0)]
    # finalval4 = [listValue / list_length for listValue in val4.sum(axis=0)]
    # finalval6 = [listValue / list_length for listValue in val6.sum(axis=0)]
    # finalval8 = [listValue / list_length for listValue in val8.sum(axis=0)]
    # finalval1 = [listValue / list_length for listValue in val1.sum(axis=0)]
    finaltr2 = [listValue / list_length for listValue in tr2.sum(axis=0)]
    finaltr4 = [listValue / list_length for listValue in tr4.sum(axis=0)]
    finaltr6 = [listValue / list_length for listValue in tr6.sum(axis=0)]
    finaltr8 = [listValue / list_length for listValue in tr8.sum(axis=0)]
    finaltr1 = [listValue / list_length for listValue in tr1.sum(axis=0)]
    # finalmseval = [listValue / list_length for listValue in mseVal.sum(axis=0)]
    # finalmaeval = [listValue / list_length for listValue in maeVal.sum(axis=0)]
    finalmsetr = [listValue / list_length for listValue in mseTr.sum(axis=0)]
    finalmaetr = [listValue / list_length for listValue in maeTr.sum(axis=0)]
    finalmsetest = [listValue / list_length for listValue in mseTest.sum(axis=0)]
    finalmaetest = [listValue / list_length for listValue in maeTest.sum(axis=0)]


    return [finaldb, finalmsetest, finalmaetest, finaltr2, finaltr4, finaltr6, finaltr8, finaltr1, finalmsetr, finalmaetr]


def CropFile(file):
    '''

        Validation: Percent of non zero Power predictions within .2,.4,.6 dB
        0.21735626007522837
        0.39024717893605587
        0.5080601826974744
        0.5836915636754433
        0.6265448683503493
        Number of Test Cases 0 Power

    :param file:
    :return:
    '''
    inputfile = open(file)
    # valdb2 = []
    # valdb4 = []
    # valdb6 = []
    # valdb8 = []
    # valdb1 = []
    trdb2 = []
    trdb4 = []
    trdb6 = []
    trdb8 = []
    trdb1 = []
    trmse = []
    trmae = []
    testmse = []
    testmae = []
    testdb = []
    #valPattern = re.compile("Validation: .* dB")
    trPattern = re.compile("Training: .* dB")
    trMsePattern = re.compile(".*Training MSE dB:.*")
    testPattern = re.compile("Test: .* dB")
    testMsePattern = re.compile(".*TEST MSE dB:.*")
    valCounter = 0
    testCounter = 0
    trCounter = 0
    trMseCounter = 0
    testMseCounter = 0
    # Run over the file, looks for patterns and insert into arrays
    for i, line in enumerate(inputfile):

        for match in re.finditer(trMsePattern, line):
            trMseCounter = 2
        line = line.replace("\n", "")
        if (trMseCounter == 2):
            trmse.append(line.replace("  +Training MSE dB: ",""))
            trMseCounter -= 1
        elif (trMseCounter == 1):
            trmae.append(line.replace("  +Training MAE dB: ",""))
            trMseCounter -= 1

        for match in re.finditer(trPattern, line):
            trCounter = 6
        line = line.replace("\n", "")
        if(trCounter == 6):
            trCounter -= 1
        elif(trCounter == 5):
            trdb2.append(line)
            trCounter -= 1
        elif (trCounter == 4):
            trdb4.append(line)
            trCounter -= 1
        elif (trCounter == 3):
            trdb6.append(line)
            trCounter -= 1
        elif (trCounter == 2):
            trdb8.append(line)
            trCounter -= 1
        elif (trCounter == 1):
            trdb1.append(line)
            trCounter -= 1
        for match in re.finditer(testPattern, line):
            testCounter = 6
            # print('Found on line %s: %s' % (i + 1, match.groups()))
        if(testCounter == 6):
            testCounter -= 1
        elif(testCounter != 0):
            testdb.append(line)
            testCounter -= 1
        for match in re.finditer(testMsePattern, line):
            testMseCounter = 2
        line = line.replace("\n", "")
        if (testMseCounter == 2):
            testmse.append(line.replace("  +TEST MSE dB: ",""))
            testMseCounter -= 1
        elif (testMseCounter == 1):
            testmae.append(line.replace("  +TEST MAE dB: ",""))
            testMseCounter -= 1
    print("Those are the values:")
    # for i in range(0, len(valdb2)):
    #     print('0.2: {}, 0.4: {}, 0.6: {}, 0.8: {}, 1:{}'.format(valdb2[i], valdb4[i], valdb6[i], valdb8[i], valdb1[i]))
    # print("Those are test results: ")
    for i in range(0, len(testdb)):
        print("Test: %s" % testdb[i])

    return [testdb, testmse, testmae, trdb2, trdb4, trdb6, trdb8, trdb1, trmse, trmae ]

def PlotFileGraph(file):
    inputfile = open(file)
    my_text = inputfile.readlines()

# This method is to parse a 90 channels.
def ParseDataFile(file):
    # file='sameroute_3short.txt'

    inputfile = open(file)
    my_text = inputfile.readlines()
    input_vector_all = []
    new_channel_all = []
    out_power_all = []
    on_channels_all = []
    counter = 0
    counter_all = []
    set_number = 0

    for line in my_text:
        # line_split=line.split("initial_channelpower_dict")
        # print(line_split)
        '''
        existing channels: (40, 72)

        added channel #: 88

        before adding new channel: {40: -18.3, 72: -19.0}

        after adding new channel: {40: -18.4, 72: -19.0}

        '''
        counter += 1
        if line.find("before adding") != -1:
            set_number += 1
            # print("")
            init = [0] * 90
            on_channels = [0] * 90
            new_string = re.sub('[^0-9:,.-]', '', line)
            new_string = new_string.replace(":", " ")
            new_string = new_string.replace(",", " ")
            list = new_string.split()
            for i in range(0, len(list), 2):
                init[int(list[i]) - 1] = pow(10, float(list[i + 1]) / 10)
                on_channels[int(list[i]) - 1] = 1

        if line.find("after adding") != -1:
            out_power = [0] * 90
            on_channels = [0] * 90
            new_string = re.sub('[^0-9:,.-]', '', line)
            new_string = new_string.replace(":", " ")
            new_string = new_string.replace(",", " ")
            list = new_string.split()
            for i in range(0, len(list), 2):
                out_power[int(list[i]) - 1] = pow(10, float(list[i + 1]) / 10)
                on_channels[int(list[i]) - 1] = 1

            on_channels_all.append(np.array(on_channels))
            input_vector_all.append(np.array(init))
            out_power_all.append(np.array(out_power))
            # output_excursions_all.append(np.array(output))
            counter_all.append(set_number)

    on_channels_all = np.asarray(on_channels_all)
    input_vector_all = np.asarray(input_vector_all)
    out_power_all = np.asarray(out_power_all)
    # output_excursions_all=np.asarray(output_excursions_all)
    counter_all = np.asarray(counter_all)
    return [counter_all, on_channels_all, input_vector_all, out_power_all]

# This method is parsing each channel inputs/outputs to a seperated dictionaries
# return value is the counter of inputs, inputDictionary, outputDictionary
def ParseDataFileSingleChannel(file):
    inputfile = open(file)
    my_text = inputfile.readlines()
    counter = 0
    counter_all = []
    set_number = 0
    currentChannel = -1
    inputsDict = dict()
    outputsDict = dict()

    for line in my_text:

        counter += 1
        # Set the current channel to parse
        if line.find("added channel") != -1:
            new_string = re.sub('\D', '', line)
            currentChannel = int(new_string)
            if not currentChannel in inputsDict:
                # create a new array in this slot
                inputsDict[currentChannel] = []
            if not currentChannel in outputsDict:
                # create a new array in this slot
                outputsDict[currentChannel] = []

        if line.find("input") != -1:
            in_power = [0] * 90
            on_channels = [0] * 90
            outputEntry = [0] * 1
            new_string = re.sub('[^0-9:,.-]', '', line)
            new_string = new_string.replace(":", " ")
            new_string = new_string.replace(",", " ")
            list = new_string.split()

            # convert to decimals and insert channel to each dictionary
            for i in range(1, len(list), 2): # 56:-18.2, 80:-17.9, 60:-18.0, 4:-20.7, |28|:-18.4
                set_number += 1
                listChan = int(list[i])
                if not listChan in inputsDict:
                    # create a new array in this slot
                    inputsDict[listChan] = []
                if not listChan in outputsDict:
                    # create a new array in this slot
                    outputsDict[listChan] = []

                # out_power[listChan - 1] = pow(10, float(list[i + 1]) / 10)
                in_power[listChan - 1] = pow(10, float(list[i + 1]) / 10)
                on_channels[listChan - 1] = 1

        if line.find("output") != -1:
            out_power = [0] * 90
            on_channels = [0] * 90
            outputEntry = [0] * 1
            new_string = re.sub('[^0-9:,.-]', '', line)
            new_string = new_string.replace(":", " ")
            new_string = new_string.replace(",", " ")
            list = new_string.split()

            # convert to decimals and insert channel to each dictionary
            for i in range(1, len(list), 2): # 56:-18.2, 80:-17.9, 60:-18.0, 4:-20.7, |28|:-18.4
                set_number += 1
                listChan = int(list[i])
                if not listChan in inputsDict:
                    # create a new array in this slot
                    inputsDict[listChan] = []
                if not listChan in outputsDict:
                    # create a new array in this slot
                    outputsDict[listChan] = []

                # out_power[listChan - 1] = pow(10, float(list[i + 1]) / 10)
                #out_power[listChan - 1] = pow(10, float(-18) / 10)
                #on_channels[listChan - 1] = 1

            for i in range(1, len(list), 2):
                listChan = int(list[i])
                inputsDict[listChan].append(np.array(in_power)) #vector of 90 input powers
                outputEntry[0] = pow(10, float(list[i + 1]) / 10)
                outputsDict[listChan].append(np.array(outputEntry)) # 1 output power for that channel
                counter_all.append(set_number)
            currentChannel = -1

    # Sum arrays together for each channel and return values.
    for key in inputsDict.keys():
        inputsDict[key] = np.asarray(inputsDict[key])
        outputsDict[key] = np.asarray(outputsDict[key])
    counter_all = np.asarray(counter_all)

    return [counter_all, inputsDict, outputsDict ]

def averageResults_val(stringTofind):
    # Collect all files to average by their name (looks for a specific string)
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    files = [filename for filename in files if filename.find(stringTofind) != -1]
    print(len(files))
    # Set temporary lists to work on
    testdb = []
    val2 = []
    val4 = []
    val6 = []
    val8 = []
    val1 = []
    tr2 = []
    tr4 = []
    tr6 = []
    tr8 = []
    tr1 = []
    mseVal = []
    maeVal = []
    mseTr = []
    maeTr = []
    list_length = len(files)

    # Sum each file into arrays
    for file in files:
        [val2cur, val4cur, val6cur, val8cur, val1cur, valMseCur, valMaeCur] = CropFile_val(file)
        #testdb.append(testdbcur)
        val2.append(val2cur)
        val4.append(val4cur)
        val6.append(val6cur)
        val8.append(val8cur)
        val1.append(val1cur)
        #tr2.append(tr2cur)
        #tr4.append(tr4cur)
        #tr6.append(tr6cur)
        #tr8.append(tr8cur)
        #tr1.append(tr1cur)
        mseVal.append(valMseCur)
        maeVal.append(valMaeCur)
        #mseTr.append(trMseCur)
        #maeTr.append(trMaeCur)

    # Arrange final lists, sum up and perform average.
    #testdb = np.array(testdb).astype(np.float)
    val2 = np.array(val2).astype(np.float)
    val4 = np.array(val4).astype(np.float)
    val6 = np.array(val6).astype(np.float)
    val1 = np.array(val1).astype(np.float)
    val8 = np.array(val8).astype(np.float)
    #tr2 = np.array(tr2).astype(np.float)
    #tr4 = np.array(tr4).astype(np.float)
    #tr6 = np.array(tr6).astype(np.float)
    #tr8 = np.array(tr8).astype(np.float)
    #tr1 = np.array(tr1).astype(np.float)
    mseVal = np.array(mseVal).astype(np.float)
    maeVal = np.array(maeVal).astype(np.float)
    #mseTr = np.array(mseTr).astype(np.float)
    #maeTr = np.array(maeTr).astype(np.float)
    #finaldb = [listValue / list_length for listValue in testdb.sum(axis=0)]
    finalval2 = [listValue / list_length for listValue in val2.sum(axis=0)]
    finalval4 = [listValue / list_length for listValue in val4.sum(axis=0)]
    finalval6 = [listValue / list_length for listValue in val6.sum(axis=0)]
    finalval8 = [listValue / list_length for listValue in val8.sum(axis=0)]
    finalval1 = [listValue / list_length for listValue in val1.sum(axis=0)]
    #finaltr2 = [listValue / list_length for listValue in tr2.sum(axis=0)]
    #finaltr4 = [listValue / list_length for listValue in tr4.sum(axis=0)]
    #finaltr6 = [listValue / list_length for listValue in tr6.sum(axis=0)]
    #finaltr8 = [listValue / list_length for listValue in tr8.sum(axis=0)]
    #finaltr1 = [listValue / list_length for listValue in tr1.sum(axis=0)]
    finalmseval = [listValue / list_length for listValue in mseVal.sum(axis=0)]
    finalmaeval = [listValue / list_length for listValue in maeVal.sum(axis=0)]
    #finalmsetr = [listValue / list_length for listValue in mseTr.sum(axis=0)]
    #finalmaetr = [listValue / list_length for listValue in maeTr.sum(axis=0)]


    return [finalval2, finalval4, finalval6, finalval8, finalval1, finalmseval, finalmaeval]


def CropFile_val(file):
    '''

        Validation: Percent of non zero Power predictions within .2,.4,.6 dB
        0.21735626007522837
        0.39024717893605587
        0.5080601826974744
        0.5836915636754433
        0.6265448683503493
        Number of Test Cases 0 Power

    :param file:
    :return:
    '''
    inputfile = open(file)
    # valdb2 = []
    # valdb4 = []
    # valdb6 = []
    # valdb8 = []
    # valdb1 = []
    trdb2 = []
    trdb4 = []
    trdb6 = []
    trdb8 = []
    trdb1 = []
    trmse = []
    trmae = []
    testdb = []
    valPattern = re.compile("Validation: .* dB")
    #trPattern = re.compile("Validation: .* dB")
    valMsePattern = re.compile(".*Validation MSE dB:.*")
    #testPattern = re.compile("Test: .* dB")
    valCounter = 0
    testCounter = 0
    trCounter = 0
    trMseCounter = 0
    # Run over the file, looks for patterns and insert into arrays
    for i, line in enumerate(inputfile):

        for match in re.finditer(valMsePattern, line):
            trMseCounter = 2
        line = line.replace("\n", "")
        if (trMseCounter == 2):
            trmse.append(line.replace("  +Validation MSE dB: ",""))
            trMseCounter -= 1
        elif (trMseCounter == 1):
            trmae.append(line.replace("  +Validation MAE dB: ",""))
            trMseCounter -= 1

        for match in re.finditer(valPattern, line):
            trCounter = 6
        line = line.replace("\n", "")
        if(trCounter == 6):
            trCounter -= 1
        elif(trCounter == 5):
            trdb2.append(line)
            trCounter -= 1
        elif (trCounter == 4):
            trdb4.append(line)
            trCounter -= 1
        elif (trCounter == 3):
            trdb6.append(line)
            trCounter -= 1
        elif (trCounter == 2):
            trdb8.append(line)
            trCounter -= 1
        elif (trCounter == 1):
            trdb1.append(line)
            trCounter -= 1
    print("Those are the values:")

    return [trdb2, trdb4, trdb6, trdb8, trdb1, trmse, trmae]

def plot_to_matrix_Val(val2, val4, val6, val8, val1, valmse, valmae):

    with open("./all_Val.csv", 'a') as myfile:
        wr = csv.writer(myfile, delimiter =",", quoting=csv.QUOTE_ALL)
        #listbreak = [x*2 for x in range(0, 50)]
        #wr.writerow(listbreak)
        wr.writerow(val2)
        wr.writerow(val4)
        wr.writerow(val6)
        wr.writerow(val8)
        wr.writerow(val1)
        wr.writerow(valmse)
        wr.writerow(valmae)

def plot_to_matrix_test(testdb, testmse, testmae):

    with open("./all_test.csv", 'a') as myfile:
        wr = csv.writer(myfile, delimiter =",", quoting=csv.QUOTE_ALL)
        #listbreak = [x*2 for x in range(0, 50)]
        #wr.writerow(listbreak)
        wr.writerow(testdb+testmse+testmae)
        #wr.writerow(testdb[1])
        #wr.writerow(testdb[2])
        #wr.writerow(testdb[3])
        #wr.writerow(testdb[4])
        #wr.writerow(testmse)
        #wr.writerow(testmae)

