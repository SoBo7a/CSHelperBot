import os
import json

# Define the base directory
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load language configuration
with open(os.path.join(base_dir, 'config.json'), encoding='utf-8') as f:
    config = json.load(f)
language = config.get('language', 'en')

# Load language file
with open(os.path.join(base_dir, 'translations', f'{language}.json'), encoding='utf-8') as f:
    translations = json.load(f)

def translate(key):
    """
    Retrieves a translation for a given key from the loaded translations.

    The function expects the key to be in a dot-separated string format, 
    which corresponds to the nested structure of the translation JSON file. 
    For example, 'instructions.headline' would access the 'headline' key 
    within the 'instructions' dictionary.

    Args:
        key (str): A dot-separated string representing the key path in the translations dictionary.

    Returns:
        str: The translated string if found, or an error message if the key does not exist.

    Examples:
        >>> translate('instructions.headline')
        'Anleitung zur Nutzung des CS Butler Bots'

        >>> translate('non.existent.key')
        'Translation not found for non.existent.key.'
    """
    keys = key.split('.')
    value = translations
    for k in keys:
        value = value.get(k)
        if value is None:
            return f'Translation not found for {key}.'
    return value