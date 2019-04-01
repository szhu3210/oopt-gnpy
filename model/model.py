import matplotlib.pylab as plt
import matplotlib.patches as mpatches


def parse_data_ripple(filename):

    spectrum = {
        'input': {},
        'output': {}
    }

    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if 'existing channels:' in line:
                continue
            for io in ['input', 'output']:
                s = io + '(1%):'
                if io in line:
                    data = line.lstrip(s)
                    if 'wdm' not in filename:
                        key, val = data.lstrip(' {').rstrip('}\n').split(':')
                        spectrum[io][int(key)] = float(val)
                    else:
                        data = data.lstrip(' {').rstrip('}\n')
                        for item in data.split(','):
                            key, val = item.split(':')
                            spectrum[io][int(key)] = float(val)

    # print(spectrum)

    return spectrum


def plot_dict(dicts):

    plt.ylim(17, 23)

    if not isinstance(dicts, list):
        dicts = [dicts]

    for d in dicts:
        lists = sorted(d.items())
        x, y = zip(*lists)
        plt.plot(x, y)

    plt.legend(
        [
            'single channel gain function (experiment)',
            'WDM gain function (experiment)',
            'single channel gain function (prediction)',
            'WDM gain function (prediction)'
        ], loc='upper center')

    plt.rcParams['font.size'] = 13
    plt.xlabel('Channel Index')
    plt.ylabel('Gain [dB]')
    plt.savefig('Kiyo_ripple.pdf', format='pdf')

    plt.show()


def cal_gain(spectrum):

    res = {}

    for ch in spectrum['input']:
        res[ch] = spectrum['output'][ch] - spectrum['input'][ch]

    return res


def get_gain(plot=False, ripple=None):

    # ripple must be a list in the order of single and wdm

    filename = 'single3.txt'
    spectrum1 = parse_data_ripple(filename)

    filename = 'wdm3.txt'
    spectrum2 = parse_data_ripple(filename)

    if ripple:
        spectrum1, spectrum2 = map(parse_data_ripple, ripple)

    gain_single = cal_gain(spectrum1)
    gain_wdm = cal_gain(spectrum2)

    if plot:
        plot_dict([gain_single, gain_wdm])

    return gain_single, gain_wdm


def kiyo_g_model(input_channels, ripple=None):

    # get gain from file
    gs, g = get_gain(plot=False, ripple=ripple)  # gs, g = gain_single, gain_wdm

    # get formula for Kiyo's model
    g_hat = {}
    n = len(input_channels)
    for ch in input_channels:
        g_hat[ch] = g[ch] + 1 / n * sum([gs[ch]-g[ch] for ch in input_channels])

    # print(g_hat)

    return g_hat


def verify_kiyo_model():

    # based on Kiyo's model calculate the gain for single and wdm ripple

    all_channels = [i * 4 for i in range(1, 23)]

    gs, g = get_gain(plot=True)

    g_hat_wdm = kiyo_g_model(input_channels=all_channels)

    L = [kiyo_g_model(input_channels=[ch]) for ch in all_channels]
    g_hat_single = {k: v for d in L for k, v in d.items()}

    plot_dict([gs, g, g_hat_wdm, g_hat_single])


def kiyo_p_model(spectrum_in, ripple=None):

    gain = kiyo_g_model(input_channels=spectrum_in.keys(), ripple=ripple)
    # print(gain)
    spectrum_out = {ch: pwr + gain[ch] for ch, pwr in spectrum_in.items()}

    # print(spectrum_out)

    return spectrum_out


if __name__ == '__main__':

    verify_kiyo_model()

    # based on input get output spectrum
    input_spectrum = {4: -38, 8: -38.2, 12: -38.6, 44: -37.8, 64: -38.1}
    output_spectrum = kiyo_p_model(input_spectrum)
