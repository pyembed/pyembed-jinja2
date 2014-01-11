# The MIT License(MIT)

# Copyright (c) 2013-2014 Matt Thomson

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from pyembed.jinja2 import Jinja2Renderer
from pyembed.core import response

from hamcrest import assert_that, equal_to
from mock import Mock
import pytest


def test_default_embed_photo():
    values = {'type': 'photo',
              'version': '1.0',
              'url': 'http://example.com/bees.jpg',
              'width': 300,
              'height': 200}

    oembed_response = response.OEmbedPhotoResponse(
        create_value_function(values))
    assert_that(
        Jinja2Renderer('.').render('http://example.com', oembed_response),
        equal_to('<img src="http://example.com/bees.jpg" ' +
                 'width="300" height="200" />'))


def test_default_embed_video():
    embedding = '<iframe src="http://www.example.com/bees.mpg"></iframe>'
    values = {'type': 'video',
              'version': '1.0',
              'html': embedding}

    oembed_response = response.OEmbedVideoResponse(
        create_value_function(values))
    assert_that(
        Jinja2Renderer('.').render('http://example.com', oembed_response),
        equal_to(embedding))


def test_default_embed_rich():
    embedding = '<h1>Bees!</h1>'
    values = {'type': 'rich',
              'version': '1.0',
              'html': embedding}

    oembed_response = response.OEmbedRichResponse(
        create_value_function(values))
    assert_that(
        Jinja2Renderer('.').render('http://example.com', oembed_response),
        equal_to(embedding))


def test_default_embed_link():
    values = {'type': 'link',
              'title': 'Bees!'}

    oembed_response = response.OEmbedLinkResponse(
        create_value_function(values))
    assert_that(
        Jinja2Renderer('.').render('http://example.com', oembed_response),
        equal_to('<a href="http://example.com">Bees!</a>'))


def test_should_embed_with_template():
    values = {'type': 'video',
              'version': '1.0',
              'html': '<iframe src="http://www.example.com/bees.mpg"></iframe>',
              'title': 'Bees',
              'author_name': 'Ian Bees'}

    oembed_response = response.OEmbedVideoResponse(
        create_value_function(values))
    renderer = Jinja2Renderer('pyembed/jinja2/test/fixtures')
    embedding = renderer.render('http://example.com', oembed_response)

    assert_that(embedding, equal_to(
        'Bees by Ian Bees from http://example.com'))


def test_should_use_default_embedding_if_no_template():
    embedding = '<h1>Bees!</h1>'
    values = {'type': 'rich',
              'version': '1.0',
              'html': embedding}

    oembed_response = response.OEmbedRichResponse(
        create_value_function(values))
    renderer = Jinja2Renderer('pyembed/jinja2/test/fixtures')

    assert_that(
        renderer.render('http://example.com', oembed_response),
        equal_to(embedding))


def create_value_function(values):
    return lambda field: values[field] if field in values else None
