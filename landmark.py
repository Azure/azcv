# -*- coding: utf-8 -*-

# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# Author: Graham.Williams@togaware.com
#
# A script to identify a landmark in a photo.
#
# ml landmark azcv <path>
#

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

import os
import sys
#import time
import argparse

from mlhub.pkg import azkey, is_url
from mlhub.utils import get_cmd_cwd

# ----------------------------------------------------------------------
# Parse command line arguments
# ----------------------------------------------------------------------

option_parser = argparse.ArgumentParser(add_help=False)

option_parser.add_argument(
    'path',
    help='path or url to image')

args = option_parser.parse_args()

# ----------------------------------------------------------------------

SERVICE   = "Computer Vision"
KEY_FILE  = os.path.join(os.getcwd(), "private.txt")

# Request subscription key and endpoint from user.

subscription_key, endpoint = azkey(KEY_FILE, SERVICE, verbose=False)

# Set credentials.

credentials = CognitiveServicesCredentials(subscription_key)

# Create client.

client = ComputerVisionClient(endpoint, credentials)

# Check the URL supplied. Also want to support local file.

# Send image to azure to identify landmark

# url = "https://images.pexels.com/photos/338515/pexels-photo-338515.jpeg"

url = args.path

domain = "landmarks"
language = "en"

if is_url(url):
    analysis = client.analyze_image_by_domain(domain, url, language)
else:
    path = os.path.join(get_cmd_cwd(), url)
    with open(path, 'rb') as fstream:
        analysis = client.analyze_image_by_domain_in_stream(domain, fstream, language)
    
for landmark in analysis.result["landmarks"]:
    print('{} {}'.format(round(landmark["confidence"],2), landmark["name"], ))

# Write results to stdout

# Generate locally annotated image

