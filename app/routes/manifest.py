from flask import Blueprint, current_app, request
from .utils import respond_with
from ..models import User

manifest_bp = Blueprint('manifest', __name__)

# Define MANIFEST dictionary
MANIFEST = {
    'id': 'com.community.stremio-subtitles',
    'version': '0.2.0',
    'name': 'Community Subtitles',
    'logo': 'https://host/logo.png',  # Placeholder logo URL
    'description': 'Community-driven subtitle addon for Stremio with user accounts and uploading.',
    'types': ['movie', 'series'],
    'catalogs': [],
    'contactEmail': 'YOUR_EMAIL@example.com',  # Placeholder email
    'behaviorHints': {'configurable': True, 'configurationRequired': True},
    'resources': ['subtitles'],
}


@manifest_bp.route('/<manifest_token>/manifest.json')
def addon_manifest(manifest_token):
    """
    Provides the manifest for the addon using the user's unique token.
    """
    # Validate token exists
    user = User.get_by_manifest_token(manifest_token)
    if not user:
        current_app.logger.warning(f"Manifest requested for potentially invalid token: {manifest_token}")
    else:
        current_app.logger.info(f"Manifest requested for token: {manifest_token} (User: {user.username})")

    # Make a copy to avoid modifying the original MANIFEST dict
    manifest_data = MANIFEST.copy()
    manifest_data['logo'] = f'https://{request.host}/logo.png'

    # Ensure behaviorHints exists and make a copy
    if 'behaviorHints' in manifest_data:
        manifest_data['behaviorHints'] = manifest_data['behaviorHints'].copy()
    else:
        manifest_data['behaviorHints'] = {}  # Create if it doesn't exist

    manifest_data['behaviorHints']['configurable'] = False
    if 'configurationRequired' in manifest_data['behaviorHints']:
        del manifest_data['behaviorHints']['configurationRequired']

    return respond_with(manifest_data)


@manifest_bp.route('/manifest.json')
def generic_manifest():
    """
    Provides the generic manifest for discovery, requiring configuration.
    """
    current_app.logger.info("Generic manifest requested.")
    # Make a copy to avoid modifying the original MANIFEST dict
    manifest_data = MANIFEST.copy()
    manifest_data['logo'] = f'https://{request.host}/logo.png'

    # Ensure behaviorHints exists and make a copy
    if 'behaviorHints' in manifest_data:
        manifest_data['behaviorHints'] = manifest_data['behaviorHints'].copy()
    else:
        manifest_data['behaviorHints'] = {}  # Create if it doesn't exist

    # Ensure configurationRequired and configurable are True for the generic manifest
    manifest_data['behaviorHints']['configurationRequired'] = True
    manifest_data['behaviorHints']['configurable'] = True
    return respond_with(manifest_data)
