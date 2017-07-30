import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import numpy as np
from scipy import stats


class data_pre:
    def __init__(self, filename):
        file_txt = open(filename)
        self.lines = file_txt.readlines()
        file_txt.close()

    def build_feature_vector(self):
        # feature_vector = [[0.0] * 9] * len(self.lines)
        feature_vector = []
        trace_num = 0
        trace_total_num = len(self.lines)
        while trace_num < trace_total_num:
            # Data analyse
            trace = self.lines[trace_num].split()[1].split(';')

            if len(trace) > 5:
                x = [0] * (len(trace) - 1)
                y = [0] * (len(trace) - 1)
                t = [0] * (len(trace) - 1)
            else:
                print trace
                print trace_num
                self.lines.pop(trace_num)
                trace_total_num = trace_total_num - 1
                continue

            for i in range(len(trace) - 1):
                x[i] = float(trace[i].split(',')[0])
                y[i] = float(trace[i].split(',')[1])
                t[i] = float(trace[i].split(',')[2])

            ele_num = 1
            len_num = len(x) - 1
            while ele_num <= len_num:
                if t[ele_num] <= t[ele_num - 1]:
                    x.pop(ele_num)
                    y.pop(ele_num)
                    t.pop(ele_num)
                    ele_num = ele_num - 1
                    len_num = len_num - 1
                ele_num = ele_num + 1

            # Calculate the displacement, velocity and acceleration
            d = [0] * (len(x) - 1)
            d_x = [0] * (len(x) - 1)
            d_y = [0] * (len(x) - 1)

            v = [0] * (len(x) - 1)
            v_x = [0] * (len(x) - 1)
            v_y = [0] * (len(x) - 1)

            a = [0] * (len(x) - 1)
            a_x = [0] * (len(x) - 1)
            a_y = [0] * (len(x) - 1)

            for j in range(1, len(x) - 1):
                d_x[j] = round((x[j] - x[j - 1]),4)
                d_y[j] = round((y[j] - y[j - 1]), 4)
                d[j] = round(math.sqrt(d_x[j] ** 2 + d_y[j] ** 2), 4)
                v_x[j] = round((x[j] - x[j - 1]) / (t[j] - t[j - 1]) if t[j] - t[j - 1] != 0 else -1, 4)
                v_y[j] = round((y[j] - y[j - 1]) / (t[j] - t[j - 1]) if t[j] - t[j - 1] != 0 else -1, 4)
                v[j] = round(math.sqrt(v_x[j] ** 2 + v_y[j] ** 2), 4)
                a_x[j] = round((v_x[j] - v_x[j - 1]) / (t[j] - t[j - 1]) if t[j] - t[j - 1] != 0 else -1, 4)
                a_y[j] = round((v_y[j] - v_y[j - 1]) / (t[j] - t[j - 1]) if t[j] - t[j - 1] != 0 else -1, 4)
                a[j] = round(math.sqrt(a_x[j] ** 2 + a_y[j] ** 2), 4)

                # Filter
                # v_ave = [-100] * len(v)
                # v_ave[0] = (v[0] + v[1] + v[2]) / 3
                # v_ave[1] = (v[0] + v[1] + v[2] + v[3]) / 4
                # v_ave[-1] = (v[-1] + v[-2] + v[-3]) / 3
                # v_ave[-2] = (v[-1] + v[-2] + v[-3] + v[-4]) / 4
                # for dot_num in range(2, len(v) - 2):
                #     v_ave[dot_num] = (v[dot_num - 2] + v[dot_num - 1] + v[dot_num] + v[dot_num + 1] + v[dot_num + 2]) / 5

                v_x_ave = [-100] * len(v_x)
                v_x_ave[0] = round((v_x[0] + v_x[1] + v_x[2]) / 3, 4)
                v_x_ave[1] = round((v_x[0] + v_x[1] + v_x[2] + v_x[3]) / 4, 4)
                v_x_ave[-1] = round((v_x[-1] + v_x[-2] + v_x[-3]) / 3 ,4)
                v_x_ave[-2] = round((v_x[-1] + v_x[-2] + v_x[-3] + v_x[-4]) / 4, 4)
                for dot_num in range(2, len(v_x) - 2):
                    v_x_ave[dot_num] = round((v_x[dot_num - 2] + v_x[dot_num - 1] + v_x[dot_num] + v_x[dot_num + 1] + v_x[
                        dot_num + 2]) / 5, 4)

                v_y_ave = [-100] * len(v_y)
                v_y_ave[0] = round((v_y[0] + v_y[1] + v_y[2]) / 3, 4)
                v_y_ave[1] = round((v_y[0] + v_y[1] + v_y[2] + v_y[3]) / 4, 4)
                v_y_ave[-1] = round((v_y[-1] + v_y[-2] + v_y[-3]) / 3, 4)
                v_y_ave[-2] = round((v_y[-1] + v_y[-2] + v_y[-3] + v_y[-4]) / 4, 4)
                for dot_num in range(2, len(v_y) - 2):
                    v_y_ave[dot_num] = round((v_y[dot_num - 2] + v_y[dot_num - 1] + v_y[dot_num] + v_y[dot_num + 1] + v_y[
                        dot_num + 2]) / 5, 4)

                a_x_ave = [-100] * len(a_x)
                a_x_ave[0] = round((a_x[0] + a_x[1] + a_x[2]) / 3, 4)
                a_x_ave[1] = round((a_x[0] + a_x[1] + a_x[2] + a_x[3]) / 4, 4)
                a_x_ave[-1] = round((a_x[-1] + a_x[-2] + a_x[-3]) / 3, 4)
                a_x_ave[-2] = round((a_x[-1] + a_x[-2] + a_x[-3] + a_x[-4]) / 4, 4)
                for dot_num in range(2, len(a_x) - 2):
                    a_x_ave[dot_num] = round((a_x[dot_num - 2] + a_x[dot_num - 1] + a_x[dot_num] + a_x[dot_num + 1] + a_x[
                        dot_num + 2]) / 5, 4)

                a_y_ave = [-100] * len(a_y)
                a_y_ave[0] = round((a_y[0] + a_y[1] + a_y[2]) / 3, 4)
                a_y_ave[1] = round((a_y[0] + a_y[1] + a_y[2] + a_y[3]) / 4, 4)
                a_y_ave[-1] = round((a_y[-1] + a_y[-2] + a_y[-3]) / 3, 4)
                a_y_ave[-2] = round((a_y[-1] + a_y[-2] + a_y[-3] + a_y[-4]) / 4, 4)
                for dot_num in range(2, len(a_y) - 2):
                    a_y_ave[dot_num] = round((a_y[dot_num - 2] + a_y[dot_num - 1] + a_y[dot_num] + a_y[dot_num + 1] + a_y[
                        dot_num + 2]) / 5, 4)

            def kurtosis_pre(raw_list):
                raw_list_num = 0
                raw_list_total_num = len(raw_list)
                while raw_list_num < raw_list_total_num:
                    if raw_list[raw_list_num] == 0:
                        raw_list.remove(0)
                        raw_list_total_num = raw_list_total_num - 1
                    raw_list_num = raw_list_num + 1
                    list_pre = map(abs, raw_list)
                return list_pre

            v_y_ave_ka = round(stats.kurtosis(kurtosis_pre(v_y_ave)),4)

            def list_count(raw_list):
                count_dict = {}
                for lc_ele in raw_list:
                    count_dict[lc_ele] = raw_list.count(lc_ele)
                return count_dict

            y_distribute_ratio = round(float(len(list_count(y)))/float(len(y)),4)
            list_count_values = list_count(y).values()
            list_count_values_ka = round(stats.kurtosis(list_count_values), 4)

            # feature_vector.append([int(self.lines[trace_num].split()[3]), [max(v_x_ave), min(v_x_ave), max(v_y_ave), min(v_y_ave),
            #                        max(a_x_ave), min(a_x_ave), max(a_y_ave), min(a_y_ave),
            #                        v_y_ave_ka, y_distribute_ratio, list_count_values_ka]])
            # maxy_index = y.index(max(y))
            # miny_index = y.index(min(y))
            # maxy_index_ratio = abs(v[maxy_index]) / max(map(abs, v))
            # print 'index:',miny_index
            # print 'len:',len(v)
            # miny_index_ratio = abs(v[miny_index]) / max(map(abs, v))
            feature_vector.append(
                [int(self.lines[trace_num].split()[3]), [max(v_x_ave), min(v_x_ave), max(v_y_ave), min(v_y_ave),
                                                         max(a_x_ave), 30*min(a_x_ave), max(a_y_ave), min(a_y_ave)
                                                         ]])

            trace_num = trace_num + 1

        return feature_vector

    def plot_no(self, trace_num):
        trace = self.lines[trace_num].split()[1].split(';')
        x = [0] * (len(trace) - 1)
        y = [0] * (len(trace) - 1)
        t = [0] * (len(trace) - 1)
        d = [0] * (len(trace) - 1)
        d_x = [0] * (len(trace) - 1)
        d_y = [0] * (len(trace) - 1)
        v = [0] * (len(trace) - 1)
        v_x = [0] * (len(trace) - 1)
        v_y = [0] * (len(trace) - 1)
        a = [0] * (len(trace) - 1)
        a_x = [0] * (len(trace) - 1)
        a_y = [0] * (len(trace) - 1)

        for i in range(len(trace) - 1):
            x[i] = float(trace[i].split(',')[0])
            y[i] = float(trace[i].split(',')[1])
            t[i] = float(trace[i].split(',')[2])

        for j in range(1, len(trace) - 1):
            d_x[j] = round((x[j] - x[j - 1]), 4)
            d_y[j] = round((y[j] - y[j - 1]), 4)
            d[j] = round(math.sqrt(d_x[j] ** 2 + d_y[j] ** 2), 4)
            v_x[j] = round((x[j] - x[j - 1]) / (t[j] - t[j - 1]) if t[j] - t[j - 1] != 0 else -1, 4)
            v_y[j] = round((y[j] - y[j - 1]) / (t[j] - t[j - 1]) if t[j] - t[j - 1] != 0 else -1, 4)
            v[j] = round(math.sqrt(v_x[j] ** 2 + v_y[j] ** 2), 4)
            a_x[j] = round((v_x[j] - v_x[j - 1]) / (t[j] - t[j - 1]) if t[j] - t[j - 1] != 0 else -1, 4)
            a_y[j] = round((v_y[j] - v_y[j - 1]) / (t[j] - t[j - 1]) if t[j] - t[j - 1] != 0 else -1, 4)
            a[j] = round(math.sqrt(a_x[j] ** 2 + a_y[j] ** 2), 4)

        # Filter
        v_ave = [-100]*len(v)
        v_ave[0] = (v[0] + v[1] + v[2]) / 3
        v_ave[1] = (v[0] + v[1] + v[2] + v[3]) / 4
        v_ave[-1] = (v[-1] + v[-2] + v[-3]) / 3
        v_ave[-2] = (v[-1] + v[-2] + v[-3]+ v[-4]) / 4
        for dot_num in range(2,len(v)-2):
            v_ave[dot_num] = (v[dot_num-2]+v[dot_num-1]+v[dot_num]+v[dot_num+1]+v[dot_num+2])/5

        v_x_ave = [-100] * len(v_x)
        v_x_ave[0] = (v_x[0] + v_x[1] + v_x[2]) / 3
        v_x_ave[1] = (v_x[0] + v_x[1] + v_x[2] + v_x[3]) / 4
        v_x_ave[-1] = (v_x[-1] + v_x[-2] + v_x[-3]) / 3
        v_x_ave[-2] = (v_x[-1] + v_x[-2] + v_x[-3] + v_x[-4]) / 4
        for dot_num in range(2, len(v_x) - 2):
            v_x_ave[dot_num] = (v_x[dot_num - 2] + v_x[dot_num - 1] + v_x[dot_num] + v_x[dot_num + 1] + v_x[dot_num + 2]) / 5

        v_y_ave = [-100] * len(v_y)
        v_y_ave[0] = (v_y[0] + v_y[1] + v_y[2]) / 3
        v_y_ave[1] = (v_y[0] + v_y[1] + v_y[2] + v_y[3]) / 4
        v_y_ave[-1] = (v_y[-1] + v_y[-2] + v_y[-3]) / 3
        v_y_ave[-2] = (v_y[-1] + v_y[-2] + v_y[-3] + v_y[-4]) / 4
        for dot_num in range(2, len(v_y) - 2):
            v_y_ave[dot_num] = (v_y[dot_num - 2] + v_y[dot_num - 1] + v_y[dot_num] + v_y[dot_num + 1] + v_y[dot_num + 2]) / 5



        # Scatter the figure
        fig = plt.figure(figsize=(40,18))
        ax = fig.add_subplot(231, projection='3d')
        ax.set_title('The trace %d label %s' % (trace_num, self.lines[trace_num].split()[3]))
        ax.scatter(x, y, v_x_ave)
        ax = fig.add_subplot(232, projection='3d')
        ax.scatter(x, y, v_y_ave)
        ax = fig.add_subplot(233, projection='3d')
        ax.scatter(x, y, v_ave)
        hist_v_x = plt.subplot(234)
        hist_v_x.hist(v_x_ave, 10, normed=1, histtype='bar', facecolor='yellow', alpha=0.75)

        hist_v_y = plt.subplot(235)
        hist_v_y.hist(v_y_ave,10,normed = 1,histtype='bar',facecolor='green',alpha=0.75)


        print 'x:', x
        print 'y:', y
        print 'v_x:', v_x
        plt.show()

    #

