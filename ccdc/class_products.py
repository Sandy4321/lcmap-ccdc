"""
Module that extracts product values from pyclass results.

All functions assume the proleptic Gregorian ordinal,
where January 1 of year 1 has ordinal 1.
"""
import numpy as np

trans_class = 9


def sort_models(class_result):
    """
    Sorts the classification results if order is in question.

    Args:
        class_result: list of dicts return from pyclass classification

    Returns:
        sorted list
    """
    if len(class_result) == 1:
        return class_result

    idxs = np.argsort([m['start_day'] for m in class_result])

    return [class_result[i] for i in idxs]


def class_primary(class_result, ordinal):
    """
    Identify the primary cover class for the given ordinal day. The days
    between and around segments identified through the classification
    process comprise valid segments for this. They also receive differing
    values based on if they occur at the beginning/end or if they are
    between classified segments.

    <- .... |--seg 1--| ...... |--seg 2--| .... ->
        0      val    trans_val    val      0

    Args:
        class_result: ordered list of dicts return from pyclass classification
        ordinal: ordinal day to calculate from

    Returns:
        int
    """
    ret = 0

    if ordinal > 0:
        prev_end = 0

        for segment in class_result:

            if segment['start_day'] <= ordinal <= segment['end_day']:
                ret = segment['class_vals'][np.argmax(segment['class_probs'][0])]
                break

            elif prev_end < ordinal < segment['start_day']:
                ret = trans_class
                break

            prev_end = segment['end_day']

    return ret


def class_secondary(class_result, ordinal):
    """
    Identify the secondary cover class for the given ordinal day. The days
    between and around segments identified through the classification
    process comprise valid segments for this. They also receive differing
    values based on if they occur at the beginning/end or if they are
    between classified segments.

    <- .... |--seg 1--| ...... |--seg 2--| .... ->
        0      val    trans_val    val      0

    Args:
        class_result: ordered list of dicts return from pyclass classification
        ordinal: ordinal day to calculate from

    Returns:
        int
    """
    ret = 0

    if ordinal > 0:
        prev_end = 0

        for segment in class_result:

            if segment['start_day'] <= ordinal <= segment['end_day']:
                ret = segment['class_vals'][np.argmax(segment['class_probs'][0])[-2]]
                break

            elif prev_end < ordinal < segment['start_day']:
                ret = trans_class
                break

            prev_end = segment['end_day']

    return ret


def conf_primary(class_result, ordinal):
    """
    Identify the confidence of the primary cover class for the given
    ordinal day. The days between and around segments identified through the
    classification process comprise valid segments for this. They also receive
    differing values based on if they occur at the beginning/end or if they are
    between classified segments.

    <- .... |--seg 1--| ...... |--seg 2--| .... ->
        0      val        100    val      0

    Args:
        class_result: ordered list of dicts return from pyclass classification
        ordinal: ordinal day to calculate from

    Returns:
        int
    """
    ret = 0

    if ordinal > 0:
        prev_end = 0

        for segment in class_result:

            if segment['start_day'] <= ordinal <= segment['end_day']:
                ret = int(max(segment['class_probs'][0]) * 100)
                break

            elif prev_end < ordinal < segment['start_day']:
                ret = 100
                break

            prev_end = segment['end_day']

    return ret


def conf_secondary(class_result, ordinal):
    """
    Identify the confidence of the secondary cover class for the given
    ordinal day. The days between and around segments identified through the
    classification process comprise valid segments for this. They also receive
    differing values based on if they occur at the beginning/end or if they are
    between classified segments.

    <- .... |--seg 1--| ...... |--seg 2--| .... ->
        0      val        100    val      0

    Args:
        class_result: ordered list of dicts return from pyclass classification
        ordinal: ordinal day to calculate from

    Returns:
        int
    """
    ret = 0

    if ordinal > 0:
        prev_end = 0

        for segment in class_result:

            if segment['start_day'] <= ordinal <= segment['end_day']:
                ret = int(segment['class_probs'][0][np.argsort(segment['class_probs'][0])[-2]] * 100)
                break

            elif prev_end < ordinal < segment['start_day']:
                ret = 100
                break

            prev_end = segment['end_day']

    return ret
