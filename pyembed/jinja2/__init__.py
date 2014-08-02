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

from pyembed.core.render import PyEmbedRenderer

import os
from pkg_resources import resource_string
from jinja2 import ChoiceLoader, FileSystemLoader, Environment, PackageLoader


class Jinja2Renderer(PyEmbedRenderer):

    """Renders OEmbed responses using Jinja2 templates."""

    def __init__(self, template_dir):
        loader = self.__create_loader(template_dir)
        self.environment = Environment(loader=loader)

    def render(self, content_url, response):
        """Generates an HTML representation of an OEmbed response.

        :param content_url: the content URL.
        :param response: the response to render.
        :returns: an HTML representation of the resource.
        """

        template = self.environment.get_template('%s.html' % response.type)

        params = dict(response.__dict__)
        params['content_url'] = content_url

        return template.render(params)

    @staticmethod
    def __create_loader(template_dir):
        return ChoiceLoader([
            FileSystemLoader(template_dir),
            PackageLoader('pyembed.jinja2')
        ])
