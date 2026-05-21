#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
File    :   Utilities.py
Time    :   2025/03/28 13:39:30
Author  :   Bertold Ian Bitachon
"""

import json
import os
from pathlib import Path
import re
import shutil
import unicodedata
from importlib.metadata import version, PackageNotFoundError
from os import makedirs
from os.path import join, dirname, abspath, exists, basename


def get_versioning():
    git_short_ref = "-"
    try:
        version_str = version("LabExT-nice")
    except PackageNotFoundError:
        version_str = None

    if version_str is None:
        try:
            setup_py_path = join(dirname(dirname(__file__)), "setup.py")
            with open(setup_py_path, "r") as f:
                content = f.read()
        except FileNotFoundError:
            content = ""

        m = re.search(r"version=['\"][0-9]+\.[0-9]+\.[0-9]+['\"]", content)
        if m is not None:
            version_str = m[0].split("=")[1][1:-1]  # get the version numbers alone
        else:
            version_str = "-"

    # access git folder relative to this file
    git_folder_path = join(dirname(dirname(dirname(__file__))), ".git")
    if exists(git_folder_path):
        with open(join(git_folder_path, "HEAD"), "r") as fp_head:
            head_ref = fp_head.read()
        try:
            head_ref = head_ref.split(":", 1)[1].strip()
        except IndexError:
            # in case there is no :, the HEAD file just includes the hash for the checked-out commit
            long_ref = head_ref
            head_ref = None

        if head_ref is not None:
            # in case we have to follow a reference path to get the commit hash
            with open(join(git_folder_path, str(head_ref))) as fp_ref:
                long_ref = fp_ref.read().strip()
            git_short_ref = long_ref[0:8]

    return version_str, git_short_ref


def make_filename_compliant(value, force_lower=False):
    """
    Makes a string filename compliant.
    From: https://github.com/django/django/blob/master/django/utils/text.py

    Convert to ASCII. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.
    """
    value = str(value)
    value = (
        unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    )
    value = re.sub(r"[^\w\s-]", "", value).strip()
    if force_lower:
        value = value.lower()
    return re.sub(r"[-\s]+", "-", value)


def setup_user_settings_directory(makedir_if_needed=False):
    """
    Setups the labext settings directory in the users home folder.

    Parameters
    ----------
    makedir_if_needed
        (optional) boolean flag default false, set to True if you want to create the settings directory if doesnt exist

    Returns
    -------
        str, the path to the labext settings directory
    """
    settings_directory = abspath(join(str(Path.home()), ".labext"))
    if makedir_if_needed:
        makedirs(settings_directory, exist_ok=True)
    config_file_path = join(
        dirname(dirname(__file__)), "Instruments", "instruments.config"
    )
    if not exists(join(settings_directory, "instruments.config")):
        shutil.copy(config_file_path, settings_directory)
    return settings_directory


def get_configuration_file_path(config_file_path_in_settings_dir, ignore_missing=True):
    """Searches for a given configuration file in the users labext configuration directory at: ~/.labext/

    Should be used in two cases:
        ignore_missing=False - if you want to find a configuration file to load it within LabExT
        ignore_missing=True - if you want to find the path where you should write a non-existing configuration file

    Parameters
    ----------
    config_file_path_in_settings_dir:
        path to the file within the settings directory
    ignore_missing
        (optional) boolean flag by default True, set to False if you want to raise an error if the file does not exist

    Returns
    -------
        the path to the found configuration file
    """
    config_fn = basename(config_file_path_in_settings_dir)
    settings_directory = setup_user_settings_directory(makedir_if_needed=False)
    path_in_settings_dir = abspath(join(settings_directory, config_fn))
    if exists(path_in_settings_dir):
        config_path = path_in_settings_dir
    else:
        if ignore_missing:
            config_path = path_in_settings_dir
        else:
            raise FileNotFoundError(config_file_path_in_settings_dir)
    return config_path


def find_dict_with_ignore(target, search_list, ignore_keys):
    """
    Search for the dictionary target within the list of dictionaries search_list.
    Any keys in ignore_keys are completely ignored in the search.
    The index of the first dictionary where keys and values match in search_list is returned.
    :param target: the dictionary to be found
    :param search_list: the list of dictionaries of which one is to be found.
    :param ignore_keys:
    :return: The index of the first dictionary matching target. None if no match was found.
    """

    target_clean = {k: v for k, v in target.items() if k not in ignore_keys}

    for cidx, candidate in enumerate(search_list):
        cand_clean = {k: v for k, v in candidate.items() if k not in ignore_keys}
        if target_clean == cand_clean:
            return cidx
    return None


def get_visa_lib_string():
    """
    Gets the visa library string specified in the LabExT settings. See
    https://pyvisa.readthedocs.io/en/latest/introduction/configuring.html

    Returns
    -------
    A pyvisa-compatible settings string. If the settings file is not found, it returns "@py" to use the pyvisa-py
    implementation.
    """
    cfg_path = get_configuration_file_path("instruments.config", ignore_missing=True)
    if not os.path.isfile(cfg_path):
        return "@py"
    else:
        with open(cfg_path, "r") as fp:
            cfg_content = json.load(fp)
        return cfg_content["Visa Library Path"]
