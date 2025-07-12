"""
BPM Sort - Configuration Settings

This module contains configuration settings for the BPM Sort application.
Modify these values to customize the behavior of the program without
changing the core functionality.
"""

import os

# =============================================================================
# DIRECTORY SETTINGS
# =============================================================================

# Name of the main output folder where sorted music will be stored
OUTPUT_FOLDER_NAME = "BPMSorted"

# Template for BPM-specific folder names
# {bpm} will be replaced with the actual BPM value
BPM_FOLDER_TEMPLATE = "{bpm} BPM Songs"

# Default input folder name (used if no folder is specified)
DEFAULT_INPUT_FOLDER = "Music Examples"

# =============================================================================
# AUDIO PROCESSING SETTINGS
# =============================================================================

# Default BPM value to use if detection fails
DEFAULT_BPM = 120

# Audio file extensions to process (case-insensitive)
SUPPORTED_AUDIO_EXTENSIONS = [
    '.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg', 
    '.wma', '.aiff', '.au', '.mp4', '.3gp'
]

# =============================================================================
# BEHAVIOR SETTINGS
# =============================================================================

# Whether to copy files (True) or move files (False)
COPY_FILES = True

# Whether to skip files that already exist in the destination
SKIP_EXISTING_FILES = True

# Whether to create subdirectories for different BPM ranges
USE_BPM_RANGES = False

# BPM range settings (only used if USE_BPM_RANGES is True)
BPM_RANGES = {
    "Slow (60-90 BPM)": (60, 90),
    "Medium (91-120 BPM)": (91, 120),
    "Fast (121-150 BPM)": (121, 150),
    "Very Fast (151+ BPM)": (151, 300)
}

# =============================================================================
# DISPLAY SETTINGS
# =============================================================================

# Whether to show detailed processing information
VERBOSE_OUTPUT = True

# Whether to show BPM detection results
SHOW_BPM_DETECTION = True

# Whether to show file operation results
SHOW_FILE_OPERATIONS = True

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_output_folder_path(base_path=None):
    """
    Get the full path to the output folder.
    
    Args:
        base_path (str, optional): Base directory path. If None, uses script directory.
        
    Returns:
        str: Full path to the output folder
    """
    if base_path is None:
        import sys
        base_path = sys.path[0]
    return os.path.join(base_path, OUTPUT_FOLDER_NAME)

def get_bpm_folder_name(bpm_value):
    """
    Generate the folder name for a specific BPM value.
    
    Args:
        bpm_value (int): The BPM value
        
    Returns:
        str: Formatted folder name
    """
    if USE_BPM_RANGES:
        for range_name, (min_bpm, max_bpm) in BPM_RANGES.items():
            if min_bpm <= bpm_value <= max_bpm:
                return range_name
        # If no range matches, use the default template
    
    return BPM_FOLDER_TEMPLATE.format(bpm=bpm_value)

def is_audio_file(filename):
    """
    Check if a file is a supported audio file based on its extension.
    
    Args:
        filename (str): Name of the file to check
        
    Returns:
        bool: True if the file is a supported audio format
    """
    _, ext = os.path.splitext(filename.lower())
    return ext in [extension.lower() for extension in SUPPORTED_AUDIO_EXTENSIONS]

def get_settings_summary():
    """
    Get a summary of current settings for display purposes.
    
    Returns:
        str: Formatted string containing current settings
    """
    settings_info = f"""
BPM Sort Configuration:
- Output Folder: {OUTPUT_FOLDER_NAME}
- BPM Folder Template: {BPM_FOLDER_TEMPLATE}
- Default BPM: {DEFAULT_BPM}
- Copy Files: {COPY_FILES}
- Skip Existing: {SKIP_EXISTING_FILES}
- Use BPM Ranges: {USE_BPM_RANGES}
- Verbose Output: {VERBOSE_OUTPUT}
- Supported Extensions: {', '.join(SUPPORTED_AUDIO_EXTENSIONS)}
"""
    return settings_info.strip()

# =============================================================================
# VALIDATION
# =============================================================================

def validate_settings():
    """
    Validate the current settings and warn about potential issues.
    
    Returns:
        list: List of warning messages (empty if no issues)
    """
    warnings = []
    
    if not OUTPUT_FOLDER_NAME:
        warnings.append("OUTPUT_FOLDER_NAME is empty")
    
    if not BPM_FOLDER_TEMPLATE or '{bpm}' not in BPM_FOLDER_TEMPLATE:
        warnings.append("BPM_FOLDER_TEMPLATE must contain '{bpm}' placeholder")
    
    if DEFAULT_BPM < 1 or DEFAULT_BPM > 300:
        warnings.append("DEFAULT_BPM should be between 1 and 300")
    
    if not SUPPORTED_AUDIO_EXTENSIONS:
        warnings.append("SUPPORTED_AUDIO_EXTENSIONS list is empty")
    
    if USE_BPM_RANGES and not BPM_RANGES:
        warnings.append("USE_BPM_RANGES is True but BPM_RANGES is empty")
    
    return warnings

# Validate settings on import
_validation_warnings = validate_settings()
if _validation_warnings:
    print("Settings validation warnings:")
    for warning in _validation_warnings:
        print(f"  - {warning}")
