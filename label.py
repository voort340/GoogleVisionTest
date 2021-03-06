#!/usr/bin/env python
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This script uses the Vision API's label detection capabilities to find a label
based on an image's content.
To run the example, install the necessary libraries by running:
    pip install -r requirements.txt
Run the script on an image to get a label, E.g.:
    ./label.py <path-to-image>
"""

# [START import_libraries]
import argparse
import base64
import httplib2

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

# The url template to retrieve the discovery document for trusted testers.
DISCOVERY_URL='https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'
# [END import_libraries]


def main(photo_file):
    """Run a label request on a single image"""

    # [START authenticate]
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials,
                              discoveryServiceUrl=DISCOVERY_URL)
    # [END authenticate]

    # [START construct_request]
    with open(photo_file, 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults': 10
                }]
            }]
        })
        # [END construct_request]
        # [START parse_response]
        response = service_request.execute()
        for labelAnnotation in response['responses'][0]['labelAnnotations']:
            label = labelAnnotation['description']
            print('Found label: %s for %s' % (label, photo_file))

        # label = response['responses'][0]['labelAnnotations'][0]['description']
        # print('Found label: %s for %s' % (label, photo_file))
        return 0
        # [END parse_response]

# [START run_application]
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file', help='The image you\'d like to label.')
    args = parser.parse_args()
    main(args.image_file)
# [END run_application]
