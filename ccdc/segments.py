"""
Helpful funcs for dealing with Change or Classified time segments.
"""


def ccd_predict(segment, ordinal):
    """

    Args:
        segment:

    Returns:

    """


def ccd_unpack(result):
    return map(ccd_fit, result['change_models'])


def ccd_fit(segment, order=None):
    """
    Extract all the coefficients and RMSE information for a given segment,
    across all the bands that are contained within the segment.

    Args:
        segment (dict): CCD segment
        order (sequence): list/tuple of band names to ensure the extraction
            happens in a specific order

    Returns:

    """
    if not order:
        order = segment.keys()

    return map(ccd_bandfit, filter(lambda x: isinstance(x, dict),
                                   (segment[k] for k in order)))


def ccd_bandfit(band):
    """
    Extract the coefficients and the RMSE information for a given
    Change Detection band.

    This function appends the intercept on to the end of the other
    coefficients.

    Args:
        band (dict): CCD representation of an individual band contained in a
            segment

    Returns:
        (coefficients, RMSE)

    """
    return band['coefficients'] + (band['intercept'],), band['rmse']


def check_coverage(segment, begin_ordinal, end_ordinal):
    """
    Helper function to determine if a model covers a given time frame, in it's
    entirety.

    Args:
        segment (dict): CCD or Classification segment
        begin_ordinal (int): ordinal day
        end_ordinal (int): ordinal day

    Returns:
        bool
    """
    return (segment['start_day'] <= begin_ordinal) & \
           (segment['end_day'] >= end_ordinal)
