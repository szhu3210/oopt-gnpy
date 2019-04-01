import matplotlib.pylab as plt

from os import listdir
from os.path import isfile, join

import json
import collections

import model


def parse_data(filename, corner_case=False, ripple=None, threshold=None):

    input = []
    output = []
    craig = []
    kiyo = []

    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            """
            input:{12: -40.10000003046137 16: -39.5000000601424 68: -38.60000019952784 80: -36.29999993363326 }
            """
            # print(line)
            if 'input:' in line:
                input_spectrum = dict()
                input_line = line.lstrip('input:{').rstrip(' }\n').split()
                while input_line:
                    input_spectrum[int(input_line[-2].rstrip(':'))] = float(input_line[-1])
                    input_line.pop()
                    input_line.pop()
                # print(input_spectrum)
                # print(model.kiyo_p_model(input_spectrum))
                input.append(input_spectrum)
                kiyo.append(model.kiyo_p_model(input_spectrum, ripple=ripple))
            if 'output true:' in line:
                output.append({int(line.split(':')[-2]): float(line.split(':')[-1])})
            if 'output predicted:' in line:
                craig.append({int(line.split(':')[-2]): float(line.split(':')[-1])})
    print(input[:10])
    print(output[:10])
    print(craig[:10])
    print(kiyo[:10])

    error = collections.defaultdict(list)
    for i in range(len(output)):
        if threshold is not None and input[i][list(output[i].keys())[0]] < threshold:
            continue
        craig_error = list(craig[i].values())[0] - list(output[i].values())[0]
        kiyo_error = kiyo[i][list(craig[i].keys())[0]] - list(output[i].values())[0]
        if corner_case:
            if len(input[i]) < 3:
                error['craig'].append(craig_error)
                error['kiyo'].append(kiyo_error)
                # error['craig'].append(abs(craig_error))
                # error['kiyo'].append(abs(kiyo_error))
        else:
            error['craig'].append(craig_error)
            error['kiyo'].append(kiyo_error)

    print(error)
    save(error, "error_%s%s" % (filename, "_corner" if corner_case else ""))
    return error


def get_errors(condition):

    # get all file names
    path = 'data'
    files = [path + '/' + f for f in listdir(path) if isfile(join(path, f))]

    errors = []

    # use kiyo's model and get output
    for file in files:

        print(condition)
        print(file)
        print()

        if not all([c in file for c in condition]):
            continue

        print(file)
        samples = parse_data_power(file)

        # get the error of outputs
        for sample in samples:
            input_exp = sample['input']
            output_kiyo = kiyo_p_model(input_exp)
            output_exp = sample['output']
            error = {}
            for key in output_kiyo:
                error[key] = output_kiyo[key] - output_exp[key]
                errors.append(error[key])

    return errors


def save_modeled_data(condition):

    # get all file names
    path = 'data'
    files = [path + '/' + f for f in listdir(path) if isfile(join(path, f))]

    # use kiyo's model and get output
    for file in files:

        print(condition)
        print(file)
        print()

        if not all([c in file for c in condition]):
            continue

        print(file)
        samples = parse_data_power(file)

        data = []
        # get the error of outputs
        for sample in samples:
            record = dict()
            record['input'] = sample['input']
            record['output'] = sample['output']
            record['kiyo'] = kiyo_p_model(record['input'])
            data.append(record)

        save(data, 'data_for_wmo_' + str(condition))


def plot_error(errors):

    # get params of errors
    length = len(errors)
    x = [float(i) / length for i in range(length)]
    y = sorted(errors)
    plt.plot(x, y)


def save(error, filename):

    with open(filename, 'w') as f:
        f.write(json.dumps(error))


def load_error(filename):

    with open(filename, 'r') as f:
        res = json.loads(f.read())

    return res


def read_error_from_data_and_save():

    error = {}
    for e in [3, 6, 9]:
        error[e] = get_errors(['tilt=3', 'fluctuation_abs=%d' % e])
    save(error, 'error')


def save_for_wmo():

    for e in [3, 6, 9]:
        save_modeled_data(['tilt=3', 'fluctuation_abs=%d' % e])


def parse_error():
    pass


def plot_hist_error():

    # histtypes = ['bar', 'barstacked', 'step', 'stepfilled']
    histtypes = ['stepfilled']

    variation = {
        0: 3,
        1: 6,
        2: 9
    }

    plt.figure(figsize=(10, 10))

    for i in range(3):
        for j in range(2):

            filename = 'outputs_%ddb.txt' % variation[i]
            corner_case = bool(j)
            # error = parse_data(filename, corner_case=corner_case)
            error = load_error("error_%s%s" % (filename, "_corner" if corner_case else ""))

            for histtype in histtypes:
                plt.rcParams['font.size'] = 20
                plt.subplot(3, 2, i * 2 + j + 1)
                p1 = plt.hist([error['craig'], error['kiyo']], bins=33 if histtype == 'bar' else 65, histtype=histtype, normed=True, alpha=0.8)
                legends = ['ML', 'ana.']
                plt.legend(legends if histtype == 'bar' else legends[::-1])
                plt.xlabel('Error [dB]\n(%s)' % chr(ord('a')+i*2+j))
                plt.ylabel('NFD')
                plt.xlim(-1.5, +2.0)
                plt.ylim(0, +5.0)
                plt.text(-1.2, 3.5, '+/- %d dB\n%s' % (variation[i], 'corner' if corner_case else ''),
                         horizontalalignment='left',
                         verticalalignment='center',
                         # transform=ax1.transAxes,
                         color='#1d8450',
                         alpha=0.95)
                # plt.caption()
                # break

    plt.tight_layout(pad=0.1)
    plt.savefig('error_dist_comparison.pdf', format='pdf')
    plt.show()


def plot_hist_error_v2():

    # histtypes = ['bar', 'barstacked', 'step', 'stepfilled']
    histtypes = ['stepfilled']

    variation = {
        0: 14,
        1: 22,
        # 2: 9
    }

    plt.figure(figsize=(10, 4))

    for i in range(2):
        for j in range(1):

            filename = 'outputs_9db_%ddb.txt' % variation[i]
            corner_case = bool(j)
            # error = parse_data(filename, corner_case=corner_case, ripple=["single_%ddb.txt" % variation[i], "wdm_%ddb.txt" % variation[i]])
            error = load_error("error_%s%s" % (filename, "_corner" if corner_case else ""))

            for histtype in histtypes:
                plt.rcParams['font.size'] = 20
                plt.subplot(1, 2, i + 1)
                p1 = plt.hist([error['craig'], error['kiyo']], bins=33 if histtype == 'bar' else 65, histtype=histtype, normed=True, alpha=0.8)
                legends = ['ML', 'ana.']
                plt.legend(legends if histtype == 'bar' else legends[::-1])
                plt.xlabel('Error [dB]\n(%s)' % chr(ord('a')+i))
                plt.ylabel('NFD')
                plt.xlim(-1.5, +1.5)
                plt.ylim(0, +3.0)
                plt.text(-0.8, 2.4, 'Gain = %d dB' % (variation[i]),
                         horizontalalignment='center',
                         verticalalignment='center',
                         # transform=ax1.transAxes,
                         color='#1d8450',
                         alpha=0.95)
                # plt.caption()
                # break

            for model in ['craig', 'kiyo']:
                l = len(error[model])
                cls = collections.defaultdict(int)

                for err in error[model]:
                    for r in [0.1 * i for i in range(21)]:
                        if abs(err) <= r:
                            cls[r] += 1

                for r in cls:
                    cls[r] /= l

                # plot_dict(cls)
                # print(cls)

                for r in [0.2, 0.5, 1.0]:
                    print('ratio of error (%5s, %d%s) within %.1f dB: %.4f' %
                          (model, variation[i], ', corner' if bool(j) else '', r, cls[r]))

                mse_err = (sum([x ** 2 for x in error[model]]) / len(error[model])) ** 0.5
                print('MSE of error (%5s, %d%s): %.4f' %
                    (model, variation[i], ', corner' if bool(j) else '', mse_err))


            print()


    plt.tight_layout(pad=0.1)
    plt.savefig('error_dist_comparison.pdf', format='pdf')
    plt.show()


def plot_hist_error_v3():

    # histtypes = ['bar', 'barstacked', 'step', 'stepfilled']
    histtypes = ['stepfilled']

    variation = {
        0: 40,
        1: 35,
        2: 30
    }

    plt.figure(figsize=(5, 9))

    for i in range(3):
        for j in range(1):

            filename = 'outputs_9db_18db_noise%d.txt' % variation[i]
            corner_case = bool(j)
            error = parse_data(filename, corner_case=corner_case, ripple=["single_18db.txt", "wdm_18db.txt"], threshold=-variation[i]+5-20)
            # error = load_error("error_%s%s" % (filename, "_corner" if corner_case else ""))

            for histtype in histtypes:
                plt.rcParams['font.size'] = 20
                plt.subplot(3, 1, i + 1)
                p1 = plt.hist([error['craig'], error['kiyo']], bins=33 if histtype == 'bar' else 65, histtype=histtype, normed=True, alpha=0.8)
                legends = ['ML', 'ana.']
                plt.legend(legends if histtype == 'bar' else legends[::-1])
                plt.xlabel('Error [dB] (+/- %d dB%s)\n(%s)' % (variation[i], ', corner' if corner_case else '', chr(ord('a')+i)))
                plt.ylabel('NFD')
                plt.xlim(-1.5, +2.0)
                # plt.caption()
                # break

            for model in ['craig', 'kiyo']:
                l = len(error[model])
                cls = collections.defaultdict(int)

                for err in error[model]:
                    for r in [0.1 * i for i in range(21)]:
                        if abs(err) <= r:
                            cls[r] += 1

                for r in cls:
                    cls[r] /= l

                # plot_dict(cls)
                # print(cls)

                for r in [0.2, 0.5, 1.0]:
                    print('ratio of error (%5s, %d%s) within %.1f dB: %.4f' %
                          (model, variation[i], ', corner' if bool(j) else '', r, cls[r]))

                mse_err = (sum([x ** 2 for x in error[model]]) / len(error[model])) ** 0.5
                print('MSE of error (%5s, %d%s): %.4f' %
                    (model, variation[i], ', corner' if bool(j) else '', mse_err))

            print()


    plt.tight_layout(pad=0.1)
    plt.savefig('error_dist_comparison.pdf', format='pdf')
    plt.show()


def cal_error_ratio_v2():

    variation = {
        0: 3,
        1: 6,
        2: 9
    }

    for i in range(3):
        for j in range(2):

            filename = 'outputs_%ddb.txt' % variation[i]
            corner_case = bool(j)
            # error = parse_data(filename, corner_case=corner_case)
            error = load_error("error_%s%s" % (filename, "_corner" if corner_case else ""))
            # print(error)

            for model in ['craig', 'kiyo']:
                l = len(error[model])
                cls = collections.defaultdict(int)

                for err in error[model]:
                    for r in [0.1 * i for i in range(21)]:
                        if abs(err) <= r:
                            cls[r] += 1

                for r in cls:
                    cls[r] /= l

                # plot_dict(cls)
                # print(cls)

                for r in [0.2, 0.5, 1.0]:
                    print('ratio of error (%5s, %d%s) within %.1f dB: %.4f' %
                          (model, variation[i], ', corner' if bool(j) else '', r, cls[r]))

            print()


def cal_error_ratio():

    error_3 = load_error('error_3')
    error_6 = load_error('error_6')

    for error_list in [error_3, error_6]:
        l = len(error_list)
        cls = collections.defaultdict(int)

        for err in error_list:
            for r in [0.1 * i for i in range(21)]:
                if abs(err) <= r:
                    cls[r] += 1

        for r in cls:
            cls[r] /= l

        # plot_dict(cls)
        # print(cls)

        for r in [0.1 * i for i in range(21)]:
            print('ratio of error within %.1f dB: %.4f' % (r, cls[r]))


if __name__ == '__main__':

    # aux
    # read_error_from_data_and_save()
    # save_for_wmo()
    # parse_data('outputs_3db.txt')

    # plots
    # plot_hist_error()  # error dist. with diff. variation/dynamic range
    plot_hist_error_v2()  # error dist. with diff. gain value
    # plot_hist_error_v3()  # error dist. with diff. noise level
