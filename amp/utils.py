#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import html
from PIL import Image
from validators.url import url
import requests
from io import BytesIO
from urllib.parse import urlparse
from .constants import AMP_INVALID_ELEMENTS


class TransformHtmlToAmp:
    """
    AMP HTML Specification: https://www.ampproject.org/docs/fundamentals/spec
    """
    def __init__(self, html_, url_prefix=None):
        self.code = html_
        self.url_prefix = url_prefix

    @staticmethod
    def remove_attribute(tag, attribute):
        try:
            del tag.attrib[attribute]
        except KeyError:
            pass

    @staticmethod
    def construct_url(url_src, url_prefix=None):
        if url(url_src):
            return url_src
        return url_prefix + url_src

    def transform_img_tags(self, el):
        for tag in el.xpath('//img'):
            tag.tag = 'amp-img'
            tag.attrib['src'] = tag.attrib['src']

            # get image size from remote
            r = requests.get(self.construct_url(tag.attrib['src'], url_prefix=self.url_prefix), stream=True)
            width = None
            height = None
            if r.status_code == 200:
                with Image.open(BytesIO(r.content)) as img:
                    width, height = img.size

            tag.attrib['width'] = str(width)
            tag.attrib['height'] = str(height)
            tag.attrib['layout'] = 'responsive'
            self.remove_attribute(tag, 'class')

    @staticmethod
    def remove_invalid_tags(el):
        for tag in el.iterdescendants():
            if tag.tag not in AMP_INVALID_ELEMENTS:
                continue
            parent = tag.getparent()
            parent.remove(tag)

    @staticmethod
    def remove_invalid_attributes(el):
        for tag in el.iterdescendants():
            for key in tag.attrib.keys():
                remove = False
                if key.startswith('on') and key != 'on':
                    remove = True
                elif key == 'style':
                    remove = True
                elif key == 'xmlns' or key.startswith('xml:'):
                    remove = True
                if remove:
                    del tag.attrib[key]

    def __call__(self):
        el = html.fromstring(self.code)

        # by default our RichText generates a list of <p> tags without parent
        # in this case lxml automatically add a <span> around these tags
        # here we change this parent tag into a <div class='amp-text'>
        el.tag = 'div'
        el.attrib['class'] = 'amp-text'

        self.transform_img_tags(el)
        self.remove_invalid_tags(el)
        self.remove_invalid_attributes(el)
        return html.tostring(el)
