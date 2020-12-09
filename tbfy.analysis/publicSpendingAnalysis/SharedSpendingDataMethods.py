
'''
Series of methods shared by various analytical approaches
'''


class SharedSpendingDataMethods:

    def __init__(self, conf = None):

        self.conf = conf

    def getAveragedList(self, data, window_size):
        """ Computes moving average using discrete linear convolution of two one dimensional sequences.
        Args:
        -----
                data (pandas.Series): independent variable
                window_size (int): rolling window size

        Returns:
        --------
                ndarray of linear convolution

        References:
        ------------
        [1] Wikipedia, "Convolution", http://en.wikipedia.org/wiki/Convolution.
        [2] API Reference: https://docs.scipy.org/doc/numpy/reference/generated/numpy.convolve.html
        """

        weights = self.conf.numpy.ones(int(window_size)) / float(window_size)
        averagedList = self.conf.numpy.convolve(data, weights, 'same')
        return averagedList.tolist()

    def getExceptionsLocal(self, data, data_av, std_dev):

        """ Helps in exploring the anamolies using stationary standard deviation
          Args:
          -----
              y (pandas.Series): independent variable
              window_size (int): rolling window size
              sigma (int): value for standard deviation

          Returns:
          --------
              a dict (dict of 'standard_deviation': int, 'anomalies_dict': (index: value))
              containing information about the points indentified as anomalies

          """

        residual = list(self.conf.numpy.array(data) - self.conf.numpy.array(data_av))
        stdDev = self.conf.statistics.stdev(residual)

        x = {}
        for index,i_data in enumerate(data):
            if(abs(i_data - data_av[index]) > std_dev * stdDev):
                x[index] = i_data

        return x

    def getBreaksFromData(self, data, treshold, window_size):
        '''
        Function identifies all index-es, where data above specified-in-advance threshold turn into data below certain threshold;
        The turn is identified by the window_size-th consecutive appearance below/under threshold

        :param data: list of transactions
        :param treshold: float, defining two classes of periods
        :param window_size: minimum number of data to switch into another class
        :return: list of breaks
        '''

        isInZerothMode = True if data[0] < treshold else False
        addCandidate2List = True
        curConsecutiveZerothValue = 0
        break_candidate = 0
        atLeastOneSwitchBtwnZeroAndnonZeroHappened = False

        breaks = []
        for index,val in enumerate(data):
            if val < treshold:

                # zero mode
                # zero mode

                if(isInZerothMode == False):

                    # initiate zero mode
                    # initiate zero mode

                    isInZerothMode = True
                    addCandidate2List = False if addCandidate2List == True else True
                    curConsecutiveZerothValue = 0
                    break_candidate = index
                    atLeastOneSwitchBtwnZeroAndnonZeroHappened = True

                # operations in zero mode
                # operations in zero mode

                curConsecutiveZerothValue = curConsecutiveZerothValue + 1
                if(curConsecutiveZerothValue > window_size and addCandidate2List == True):
                    breaks.append(break_candidate)
                    addCandidate2List = False

            else:

                # nonzero mode
                # nonzero mode

                if(isInZerothMode == True):

                    # initiate nonzero mode
                    # initiate nonzero mode

                    isInZerothMode = False
                    addCandidate2List = False if addCandidate2List == True else True
                    curConsecutiveZerothValue = 0
                    break_candidate = index
                    atLeastOneSwitchBtwnZeroAndnonZeroHappened = True

                # operations in zero mode
                # operations in zero mode

                curConsecutiveZerothValue = curConsecutiveZerothValue + 1
                if(curConsecutiveZerothValue > window_size and addCandidate2List == True):
                    breaks.append(break_candidate)
                    addCandidate2List = False


        if len(breaks) == 1 and atLeastOneSwitchBtwnZeroAndnonZeroHappened == False: return []
        else: return breaks

    def getDerivatives(self, data):
        '''
        Function get a list of numbers and returns a list of derivatives 
        
        :param data: 
        :return: 
        '''

        return [y - x for x, y in zip(data[:-1], data[1:])]

    def getMaximumList(self, data, deviation):
        '''
        Function gets a list of data and returns a list of points, identified as maximums on data list

        :param data: list, list of values
        :param deviation: number of points from maximum, that need to obey maximum rule:
            * on the left deviation num of points need to be raising
            * on the right deviation num of points need to be falling
        :return:
        '''

        maxList = []
        leftCondition = 0
        rightCondition = 0
        prevValue = 0.0
        index_candidate = -1
        for index, value in enumerate(data):
            if (prevValue < value):
                # if right condition is not reset, reset all conditions
                if (rightCondition > 0):

                    # is index candidate maximum?
                    if (leftCondition + rightCondition >= 2 * deviation):
                        # print(leftCondition, rightCondition)
                        maxList.append(index_candidate)

                    leftCondition = 0
                    rightCondition = 0

                # increase left condition
                leftCondition = leftCondition + 1

            else:
                # increase right condition only if left condition initiated
                if (leftCondition > 0):
                    rightCondition = rightCondition + 1
                    #  defininf maximum candidate
                    if rightCondition == 1:
                        index_candidate = index - 1
                else:
                    # reset conditions
                    leftCondition = 0
                    rightCondition = 0

            prevValue = value

        # include last maximum
        # include last maximum

        if leftCondition > 0 and rightCondition > 0 and leftCondition + rightCondition >= 2 * deviation:
            if index_candidate not in maxList:
                maxList.append(index_candidate)

        return maxList

    def extractDataFromListMaximums(self, data, dataEntity, window_size, deviation):
        '''
        Function defines maximums on a set of data and defines anomaly range as maximum +/- deviation.
        Function returns all companies (in dataEntity list) within the anomaly ranges.
        Parameter window_size is used to average data.

        Input:
        :param data: list of data for maximum calculations
        :param dataEntity: list of data to return
        :param window_size: int
        :param deviation: int

        Output:
        :param data:
        :param deviation:
        :return: list
        '''

        # get base lists
        # get base lists

        data_av = self.getAveragedList(data, window_size)
        maxList = self.getMaximumList(data_av, deviation)

        # assemble elements from identified maximums
        # assemble elements from identified maximums

        unavailableIndexList = []
        companyDict = {}
        dateEntityLen = len(dataEntity)

        for mx in maxList:
            tmp_left = mx - deviation
            tmp_right = mx + deviation
            if tmp_left < 0:
                tmp_left = 0
            if tmp_right >= len(data_av):
                tmp_right = len(data_av) - 1

            i = tmp_left - 1
            while i <= tmp_right:
                # avoid double count
                # avoid double count
                i = i + 1
                if i in unavailableIndexList:
                    continue
                else:
                    unavailableIndexList.append(i)

                if i < dateEntityLen:
                    for maticna in dataEntity[i]:
                        if maticna in companyDict:
                            companyDict[maticna] = companyDict[maticna] + dataEntity[i][maticna]
                        else:
                            companyDict[maticna] = dataEntity[i][maticna]

        return maxList, sorted(companyDict.items(), key=lambda kv: kv[1], reverse=True)


