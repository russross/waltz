import difflib
import json
import os
import sys

from waltz.registry import Registry
from waltz.resources.canvas_resource import CanvasResource
from waltz.tools import h2m, extract_front_matter
from waltz.resources.raw import RawResource
from waltz.resources.resource import Resource
from waltz.tools.html_markdown_utilities import hide_data_in_html, m2h
from waltz.tools.utilities import get_files_last_update, from_canvas_date, to_friendly_date_from_datetime, start_file


class Page(CanvasResource):
    """
    DOWNLOAD: gets a copy of the raw JSON version of this from Canvas
    PULL: DOWNLOAD as JSON, then RESTYLE into Markdown
    PUSH: RESTYLE from Markdown into JSON, then UPLOAD
    UPLOAD: sends the copy of the raw JSON version of this into Canvas
    EXTRACT: RESTYLE from HTML to YAML using a template
    BUILD: RESTYLE from YAML to HTML using a template
    """
    name = "page"
    name_plural = "pages"
    category_names = ['page', 'pages']
    id = "url"
    endpoint = "pages/"

    @classmethod
    def upload(cls, registry: Registry, args):
        canvas = registry.get_service(args.service, "canvas")
        raw_resource = registry.find_resource(title=args.title, service=args.service,
                                              category=args.category, disambiguate=args.url)
        full_page = json.loads(raw_resource.data)
        canvas.api.put("pages/{url}".format(url=full_page['title']), data={
            'wiki_page[title]': full_page['title'],
            'wiki_page[body]': full_page['body'],
            'wiki_page[published]': full_page['published']
        })
        # TODO: Handle other fields
        # wiki_page[editing_roles]
        # wiki_page[notify_of_update]
        # wiki_page[front_page]

    @classmethod
    def decode_json(cls, registry: Registry, data: str, args):
        raw_data = json.loads(data)
        return h2m(raw_data['body'], {
            'title': raw_data['title'],
            'resource': 'Page',
            'published': raw_data['published']
        })

    @classmethod
    def encode_json(cls, registry: Registry, data: str, args):
        regular, waltz, body = extract_front_matter(data)
        body = hide_data_in_html(regular, m2h(body))
        return json.dumps({
            'title': waltz['title'],
            'published': waltz['published'],
            'body': body
            # TODO: Other fields
        })

