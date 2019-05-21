#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
import argparse

from decorators import check_folder_path_exists
from itertools import groupby
from operator import itemgetter


@check_folder_path_exists
def find_files_from_reg_exp(folder_path, reg_exp):
    """
    Returned all files contained in a given folder_path
    that match given regex expression

    Parameters
    ----------
        folder_path (string): Folder path that is gonna be scanned
        reg_exp (string):
            Regex expression that should be used to evaluate  matching files

    Returns
    -------
        files_list (list):
            List containing all filenames matching regex expression

    Example
    -------
    >>> find_files_from_reg_exp(
            "./synthetic_data/job",r"\w+(\.{1}\d{4}\.{1})\w+")
    >>>>>> ['c.1009.jpg', 'c.1003.jpg', 't.1003.jpg', 't.1002.jpg']

    """

    files_list = []

    for root, dirs, filenames in os.walk(folder_path, topdown=False):

        for filename in filenames:
            if re.search(reg_exp, filename):
                files_list.append(filename)

    return files_list


def get_animated_frames_by_sequence_names_dict(files_list):
    """
    Returned a dictionary containing sorted frames ranges list
    for each sequences.

    Parameters
    ----------
        files_list (list): List of filenames strings

    Returns
    -------
        seq_frames_dict (dict):
            Dictionary storing sequences & sequences_frames values

    Example
    -------
    >>> files_list = ['c.1009.jpg', 'c.1003.jpg', 't.1003.jpg', 't.1002.jpg']
    >>> get_animated_frames_by_sequence_names_dict(files_list)
    >>>>>> {'c': [1003, 1009], 't': [1002, 1003]}

    """
    seq_frames_dict = dict()

    # this function make it easier
    # for us to map
    def update_seq_dict(key, value):
        if key not in seq_frames_dict:
            seq_frames_dict[key] = []
        seq_frames_dict[key].append(int(value))

    # populate dict so seq_frames_dict[seq] = [seq_frames]
    map(
        lambda x: update_seq_dict(*x.split('.')[:2]),
        files_list
    )

    # sort seq frames in ascending order
    for k in seq_frames_dict:
        seq_frames_dict[k].sort()

    return seq_frames_dict


def format_animated_frames_by_sequence_names(seq_frames_dict):
    """
    Format, group and print frame ranges lists for each sequence name.

    Parameters
    ----------
        seq_frames_dict (dict):
            Dictionary storing sequences & sequences_frames values

    Returns
    -------
        None

    Example
    -------
    >>> seq_frames_dict = {'c': [1003, 1009], 't': [1002, 1003]}
    >>> format_animated_frames_by_sequence_names(files_list)
    >>>>>> c 1003, 1009
    >>>>>> t 1002-1003

    """
    for seq_name in seq_frames_dict:
        seq_name_frames = []

        # Group by continuous int
        for sub_iterator, lambda_results in groupby(
                enumerate(seq_frames_dict[seq_name]), lambda (i, x): i-x):
            # string type all frames groups
            frame_range = map(
                lambda x: str(x),
                map(itemgetter(1), lambda_results)
            )

            # Format and append to seq_names_frames list
            frame_range_length = len(frame_range)
            if frame_range_length == 1:
                to_add = frame_range[0]
            elif frame_range_length > 1:
                to_add = '-'.join(frame_range[::frame_range_length-1])
            seq_name_frames.append(to_add)

        # Print animated frames groups by sequence_names
        print ': '.join([seq_name, ', '.join(seq_name_frames)])

    return


def main(job_folder_path, reg_exp):
    """
    Format, group and print frame ranges lists for each sequence name
    given a folder_path and a regex expression.

    Parameters
    ----------
        folder_path (string): Folder path that is gonna be scanned
        reg_exp (string):
            Regex expression that should be used to evaluate  matching files

    Returns
    -------
        None

    Example
    -------
    >>> main("./synthetic_data/job", r"\w+(\.{1}\d{4}\.{1})\w+")
    >>>>>> c 1003, 1009
    >>>>>> t 1002-1003

    """
    # Retrieve all filenames matching the regex expression in job_folder_path
    files_list = find_files_from_reg_exp(job_folder_path, reg_exp)

    # Create a dict with all sequences as a key and associated
    # frame ranges as value (list)
    seq_frames_dict = get_animated_frames_by_sequence_names_dict(files_list)

    # Format, group and print frame ranges for each sequences
    format_animated_frames_by_sequence_names(seq_frames_dict)

    return


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Animated sequence frame ranges retriever.')
    parser.add_argument('-f', '--folder_path', help='filepath', required=True)
    args = vars(parser.parse_args())

    # this is our reg_exp for animated sequence
    reg_exp = r"\w+(\.{1}\d{4}\.{1})\w+"
    main(args["folder_path"], reg_exp)
