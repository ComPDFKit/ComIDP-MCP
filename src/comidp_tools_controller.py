# coding: utf-8

from __future__ import absolute_import
import requests
import config


def api_idp_data_extract_post(filename):
        """Test case for api_idp_data_extract_post

        关键信息提取，同步版
        """

        url = 'https://api-service.compdf.com/api/idp/data-extract'
        headers = { 
            'api_key': config.IDPKEY,
        }
        files={
              'file': open(filename,"rb")
        }

        data = {
            'keys': '',
            'tableHandles': '',
            'pages': ''
        }
        response = requests.post(url, headers=headers, files=files, data=data)

        return response.text

def api_idp_data_extract_post_with_data(filedata):
        """Test case for api_idp_data_extract_post_with_key

        关键信息提取，同步版
        """

        url = 'https://api-service.compdf.com/api/idp/data-extract'
        headers = { 
            'api_key': config.IDPKEY,
        }
        files={
              'file': filedata
        }

        data = {
            'keys': '',
            'tableHandles': '',
            'pages': ''
        }
        response = requests.post(url, headers=headers, files=files, data=data)

        return response.text


if __name__ == '__main__':
    filename = R"C:\pdf\idp.pdf"
    res = api_idp_data_extract_post(filename)
    print(res)
