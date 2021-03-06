#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 12:32:04 2017

@author: briantaylor
"""
import numpy as np
from numpy import polyfit, polyval, mean
from utilities import lin2db, db2lin, itufs, freq2wavelength
import matplotlib.pyplot as plt
from scipy.constants import h


def noise_profile(nf, gain, ffs, df):
    """ noise_profile(nf, gain, ffs, df) computes amplifier ase

    :param nf: Noise figure in dB
    :param gain: Actual gain calculated for the EDFA in dB units
    :param ffs: A numpy array of frequencies
    :param df: the reference bw in THz
    :type nf: numpy.ndarray
    :type gain: numpy.ndarray
    :type ffs: numpy.ndarray
    :type df: float
    :return: the asepower in dBm
    :rtype: numpy.ndarray

    ASE POWER USING PER CHANNEL GAIN PROFILE
    INPUTS:
    NF_dB - Noise figure in dB, vector of length number of channels or
            spectral slices
    G_dB  - Actual gain calculated for the EDFA, vector of length number of
            channels or spectral slices
    ffs     - Center frequency grid of the channels or spectral slices in THz,
            vector of length number of channels or spectral slices
    dF    - width of each channel or spectral slice in THz,
            vector of length number of channels or spectral slices
    OUTPUT:
        ase_dBm - ase in dBm per channel or spectral slice
    NOTE: the output is the total ASE in the channel or spectral slice. For
    50GHz channels the ASE BW is effectively 0.4nm. To get to noise power in
    0.1nm, subtract 6dB.

    ONSR is usually quoted as channel power divided by
    the ASE power in 0.1nm RBW, regardless of the width of the actual
    channel.  This is a historical convention from the days when optical
    signals were much smaller (155Mbps, 2.5Gbps, ... 10Gbps) than the
    resolution of the OSAs that were used to measure spectral power which
    were set to 0.1nm resolution for convenience.  Moving forward into
    flexible grid and high baud rate signals, it may be convenient to begin
    quoting power spectral density in the same BW for both signal and ASE,
    e.g. 12.5GHz."""

    h_mWThz = 1e-3 * h * (1e14)**2
    nf_lin = db2lin(nf)
    g_lin = db2lin(gain)
    ase = h_mWThz * df * ffs * (nf_lin * g_lin - 1)
    asedb = lin2db(ase)

    return asedb


def gain_profile(dfg, dgt, Pin, gp, gtp):
    """
    :param dfg: design flat gain
    :param dgt: design gain tilt
    :param Pin: channing input power profile
    :param gp: Average gain setpoint in dB units
    :param gtp: gain tilt setting
    :type dfg: numpy.ndarray
    :type dgt: numpy.ndarray
    :type Pin: numpy.ndarray
    :type gp: float
    :type gtp: float
    :return: gain profile in dBm
    :rtype: numpy.ndarray

    AMPLIFICATION USING INPUT PROFILE
    INPUTS:
        DFG - vector of length number of channels or spectral slices
        DGT - vector of length number of channels or spectral slices
        Pin - input powers vector of length number of channels or
        spectral slices
        Gp  - provisioned gain length 1
        GTp - provisioned tilt length 1

    OUTPUT:
        amp gain per channel or spectral slice
    NOTE: there is no checking done for violations of the total output power
        capability of the amp.
        Ported from Matlab version written by David Boerges at Ciena.
    Based on:
        R. di Muro, "The Er3+ fiber gain coefficient derived from a dynamic
        gain
        tilt technique", Journal of Lightwave Technology, Vol. 18, Iss. 3,
        Pp. 343-347, 2000.
    """
    err_tolerance = 1.0e-11
    simple_opt = True

    # TODO make all values linear unit and convert to dB units as needed within
    # this function.
    nchan = list(range(len(Pin)))

    # TODO find a way to use these or lose them.  Primarily we should have a
    # way to determine if exceeding the gain or output power of the amp
    tot_in_power_db = lin2db(np.sum(db2lin(Pin)))
    avg_gain_db = lin2db(mean(db2lin(dfg)))

    # Linear fit to get the
    p = polyfit(nchan, dgt, 1)
    dgt_slope = p[0]

    # Calculate the target slope-  Currently assumes equal spaced channels
    # TODO make it so that supports arbitrary channel spacing.
    targ_slope = gtp / (len(nchan) - 1)

    # 1st estimate of DGT scaling
    dgts1 = targ_slope / dgt_slope

    # when simple_opt is true code makes 2 attempts to compute gain and
    # the internal voa value.  This is currently here to provide direct
    # comparison with original Matlab code.  Will be removed.
    # TODO replace with loop

    if simple_opt:

        # 1st estimate of Er gain & voa loss
        g1st = dfg + dgt * dgts1
        voa = lin2db(mean(db2lin(g1st))) - gp

        # 2nd estimate of Amp ch gain using the channel input profile
        g2nd = g1st - voa
        pout_db = lin2db(np.sum(db2lin(Pin + g2nd)))
        dgts2 = gp - (pout_db - tot_in_power_db)

        # Center estimate of amp ch gain
        xcent = dgts2
        gcent = g1st - voa + dgt * xcent
        pout_db = lin2db(np.sum(db2lin(Pin + gcent)))
        gavg_cent = pout_db - tot_in_power_db

        # Lower estimate of Amp ch gain
        deltax = np.max(g1st) - np.min(g1st)
        xlow = dgts2 - deltax
        glow = g1st - voa + xlow * dgt
        pout_db = lin2db(np.sum(db2lin(Pin + glow)))
        gavg_low = pout_db - tot_in_power_db

        # Upper gain estimate
        xhigh = dgts2 + deltax
        ghigh = g1st - voa + xhigh * dgt
        pout_db = lin2db(np.sum(db2lin(Pin + ghigh)))
        gavg_high = pout_db - tot_in_power_db

        # compute slope
        slope1 = (gavg_low - gavg_cent) / (xlow - xcent)
        slope2 = (gavg_cent - gavg_high) / (xcent - xhigh)

        if np.abs(gp - gavg_cent) <= err_tolerance:
            dgts3 = xcent
        elif gp < gavg_cent:
            dgts3 = xcent - (gavg_cent - gp) / slope1
        else:
            dgts3 = xcent + (-gavg_cent + gp) / slope2

        gprofile = g1st - voa + dgt * dgts3
    else:
        gprofile = None

    return gprofile


if __name__ == '__main__':

    plt.close('all')
    fc = itufs(0.05)
    lc = freq2wavelength(fc) / 1000
    nchan = list(range(len(lc)))
    df = np.array([0.05] * (nchan[-1] + 1))
    # TODO remove path dependence
    path = ''

    """
    DFG_96:  Design flat gain at each wavelength in the 96 channel 50GHz ITU
    grid in dB.  This can be experimentally determined by measuring the gain
    at each wavelength using a full, flat channel (or ASE) load at the input.
    The amplifier should be set to its maximum flat gain (tilt = 0dB).  This
    measurement captures the ripple of the amplifier.  If the amplifier was
    designed to be mimimum ripple at some other tilt value, then the ripple
    reflected in this measurement will not be that minimum.  However, when
    the DGT gets applied through the provisioning of tilt, the model should
    accurately reproduce the expected ripple at that tilt value.  One could
    also do the measurement at some expected tilt value and back-calculate
    this vector using the DGT method.  Alternatively, one could re-write the
    algorithm to accept a nominal tilt and a tiled version of this vector.
    """

    dfg_96 = np.loadtxt(path + 'DFG_96.txt')

    """maximum gain for flat operation - the amp in the data file was designed
    for 25dB gain and has an internal VOA for setting the external gain
    """

    avg_dfg = dfg_96.mean()

    """
    DGT_96:  This is the so-called Dynamic Gain Tilt of the EDFA in dB/dB. It
    is the change in gain at each wavelength corresponding to a 1dB change at
    the longest wavelength supported.  The value can be obtained
    experimentally or through analysis of the cross sections or Giles
    parameters of the Er fibre.  This is experimentally measured by changing
    the gain of the amplifier above the maximum flat gain while not changing
    the internal VOA (i.e. the mid-stage VOA is set to minimum and does not
    change during the measurement). Note that the measurement can change the
    gain by an arbitrary amount and divide by the gain change (in dB) which
    is measured at the reference wavelength (the red end of the band).
    """

    dgt_96 = np.loadtxt(path + 'DGT_96.txt')

    """
    pNFfit3:  Cubic polynomial fit coefficients to noise figure in dB
    averaged across wavelength as a function of gain change from design flat:

        NFavg = pNFfit3(1)*dG^3 + pNFfit3(2)*dG^2 pNFfit3(3)*dG + pNFfit3(4)
    where
        dG = GainTarget - average(DFG_96)
    note that dG will normally be a negative value.
    """

    nf_fitco = np.loadtxt(path + 'pNFfit3.txt')

    """NFR_96:  Noise figure ripple in dB away from the average noise figure
    across the band.  This captures the wavelength dependence of the NF.  To
    calculate the NF across channels, one uses the cubic fit coefficients
    with the external gain target to get the average nosie figure, NFavg and
    then adds this to NFR_96:
    NF_96 = NFR_96 + NFavg
    """

    nf_ripple = np.loadtxt(path + 'NFR_96.txt')

    # This is an example to set the provisionable gain and gain-tilt values
    # Tilt is in units of dB/THz
    gain_target = 20.0
    tilt_target = -0.7

    # calculate the NF for the EDFA at this gain setting
    dg = gain_target - avg_dfg
    nf_avg = polyval(nf_fitco, dg)
    nf_96 = nf_ripple + nf_avg

    # get the input power profiles to show
    pch2d = np.loadtxt(path + 'Pchan2D.txt')

    # Load legend and assemble legend text
    pch2d_legend_data = np.loadtxt(path + 'Pchan2DLegend.txt')
    pch2d_legend = []
    for ea in pch2d_legend_data:
        s = ''.join([chr(xx) for xx in ea.astype(dtype=int)]).strip()
        pch2d_legend.append(s)

    # assemble plot
    axis_font = {'fontname': 'Arial', 'size': '16', 'fontweight': 'bold'}
    title_font = {'fontname': 'Arial', 'size': '17', 'fontweight': 'bold'}
    tic_font = {'fontname': 'Arial', 'size': '12'}

    plt.rcParams["font.family"] = "Arial"
    plt.figure()
    plt.plot(nchan, pch2d.T, '.-', lw=2)
    plt.xlabel('Channel Number', **axis_font)
    plt.ylabel('Channel Power [dBm]', **axis_font)
    plt.title('Input Power Profiles for Different Channel Loading',
              **title_font)
    plt.legend(pch2d_legend, loc=5)
    plt.grid()
    plt.ylim((-100, -10))
    plt.xlim((0, 110))
    plt.xticks(np.arange(0, 100, 10), **tic_font)
    plt.yticks(np.arange(-110, -10, 10), **tic_font)

    plt.figure()
    ea = pch2d[1, :]
    for ea in pch2d:
        chgain = gain_profile(dfg_96, dgt_96, ea, gain_target, tilt_target)
        pase = noise_profile(nf_96, chgain, fc, df)
        pout = lin2db(db2lin(ea + chgain) + db2lin(pase))
        plt.plot(nchan, pout, '.-', lw=2)
    plt.title('Output Power with ASE for Different Channel Loading',
              **title_font)
    plt.xlabel('Channel Number', **axis_font)
    plt.ylabel('Channel Power [dBm]', **axis_font)
    plt.grid()
    plt.ylim((-50, 10))
    plt.xlim((0, 100))
    plt.xticks(np.arange(0, 100, 10), **tic_font)
    plt.yticks(np.arange(-50, 10, 10), **tic_font)
    plt.legend(pch2d_legend, loc=5)
    plt.show()
