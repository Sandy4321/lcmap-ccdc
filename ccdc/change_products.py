"""
Module that extracts product values from pyccd results.

All functions assume the proleptic Gregorian ordinal,
where January 1 of year 1 has ordinal 1.
"""
import numpy as np
from datetime import date


def lastchange(pyccd_result, ordinal):
    """
    Number of days since last detected change.

    Defaults to 0 in cases where the given ordinal day to calculate from
    is either < 1 or no change was detected before it.

    Args:
        pyccd_result: dict return from pyccd
        ordinal: ordinal day to calculate from

    Returns:
        int
    """
    ret = 0

    if ordinal > 0:
        break_dates = []
        for segment in pyccd_result['change_models']:
            if segment['change_probability'] == 1:
                break_dates.append(segment['break_day'])

        diff = [(ordinal - d) for d in break_dates if (ordinal - d) > 0]

        if diff:
           ret = min(diff)

    return ret


def changemag(pyccd_result, ordinal):
    """
    The magnitude of change if it occurred in the same calendar year.

    Defaults to 0 in cases where the given ordinal day to calculate from
    is either < 1 or no change was detected in the same year.

    Args:
        pyccd_result: dict return from pyccd
        ordinal: ordinal day to calculate from

    Returns:
        int
    """
    ret = 0

    if ordinal > 0:
        query_date = date.fromordinal(ordinal)

        for segment in pyccd_result['change_models']:
            break_date = date.fromordinal(segment['break_day'])

            if (query_date.year == break_date.year) and (segment['change_probability'] == 1):
                magnitudes = [pyccd_result[b]['magnitude'] for b
                              in ('nir', 'swir1', 'swir2', 'green', 'red')]
                ret = np.linalg.norm(magnitudes)
                break

    return ret


def changedate(pyccd_result, ordinal):
    """
    The day of year of change if it occurred in the same calendar year.

    Defaults to 0 in cases where the given ordinal day to calculate from
    is either < 1 or no change was detected in the same year.

    Args:
        pyccd_result: dict return from pyccd
        ordinal: ordinal day to calculate from

    Returns:
        int
    """
    ret = 0

    if ordinal > 0:
        query_date = date.fromordinal(ordinal)

        for segment in pyccd_result['change_models']:
            break_date = date.fromordinal(segment['break_day'])

            if (query_date.year == break_date.year) and segment['change_probability'] == 1:
                ret = break_date.timetuple().tm_yday
                break

    return ret


def seglength(pyccd_result, ordinal, series_start):
    """
    The number of days since the beginning of the segment that the ordinal
    intersects with. The days between and around segments identified through
    the change detection process comprise valid segments for this. This why we
    need to know when the actual start ordinal, as the segments identified
    through change detection might not include it.

    Defaults to 0 in cases where the given ordinal day to calculate from
    is either < 1 or is before the start of the time series.

    Args:
        pyccd_result: dict return from pyccd
        ordinal: ordinal day to calculate from
        series_start: ordinal day when the change detection was started from

    Returns:
        int
    """
    ret = 0

    if ordinal > 0:
        all_dates = [series_start]

        for segment in pyccd_result['change_models']:
            all_dates.append(segment['start_day'])
            all_dates.append(segment['end_day'])

        diff = [(ordinal - d) for d in all_dates if (ordinal - d) > 0]

        if diff:
           ret = min(diff)

    return ret


def curveqa(pyccd_result, ordinal):
    """
    Curve fit information for the segment in which the ordinal intersects with.

    Defaults to 0 in cases where the given ordinal day to calculate from
    is either < 1 or it does not intersect with a segment identified in
    pyccd.

    Args:
        pyccd_result: dict return from pyccd
        ordinal: ordinal day to calculate from

    Returns:
        int
    """
    ret = 0

    if ordinal > 0:
        for segment in pyccd_result['change_models']:
            if segment['start_day'] <= ordinal <= segment['end_day']:
                ret = segment['curve_qa']
                break

    return ret