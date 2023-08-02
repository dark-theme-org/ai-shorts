"""Module to format some strings for entrypoint code"""
from random import choice
from re import search

from utils.environment import Environment
from utils.logger import logger_config

# Declare logger

logger = logger_config()

# Create functions


def privacy(env: Environment) -> str:
    """Define video privace, based on scope passed"""
    # Create variable, log and return result
    privacy_ = "public" if env.get_scope() == "prod" else "unlisted"
    logger.debug(f"[privacy] The 'privacy' in shorts will be '{privacy_}'.")
    return privacy_


def keywords() -> str:
    """Return keywords separeted by comma in a single string"""
    return "shorts,ai,lofi"


def title(file: str, keywords_: str = keywords()) -> str:
    """
    Extract the relevant part from the video string as title.

    ...

    ----------
    Parameters
    ----------
    file: str
        Pass file name from downloaded video

    -------
    Returns
    -------
    Formatted title string
    """
    match = search(r'from_(.+?)-to', file)
    # If returns value, extract string and format as desired
    if match:
        group_ = match.group(1)
        video_str = group_.replace('_', ' ').title()
    # Add new words for final title
    expressions = ["AWESOME", "FANTASTIC", "FASCINATING", "INCREDIBLE", "OMG", "WOW"]
    random_ = choice(expressions)
    hashtags = ' '.join(['#' + word for word in keywords_.split(',')])
    final_title = f"{random_}! {video_str} created by Stable Diffusion AI {hashtags}"
    # Log and return value
    logger.debug(f"[format_title] The 'title' in shorts will be '{final_title}'.")
    return final_title


def description(file: str) -> str:
    """
    # Extract name from file and create description template

    ...

    ----------
    Parameters
    ----------
    file: str
        Pass file name from downloaded video

    -------
    Returns
    -------
    Formatted description string
    """
    # Split by dot and take the first part
    match_ = file.split('.')[0]
    # Split the title into individual words
    words = match_.split('_')
    # Create the description template
    raw_description = ' '.join(words).replace('-', ' ')
    final_description = (
        f"See how Stable Diffusion AI transform '{raw_description}' execution."
    )
    # Log and return value
    logger.debug(
        f"[format_title] The 'description' in shorts will be '{final_description}'."
    )
    return final_description
