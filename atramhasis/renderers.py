import csv
from six import StringIO
from pyramid.renderers import JSON
from skosprovider_sqlalchemy.models import (
    Concept,
    Collection
)


class CSVRenderer(object):
    def __init__(self, info):
        pass

    def __call__(self, value, system):
        f_out = StringIO()
        writer = csv.writer(f_out, delimiter=',', quoting=csv.QUOTE_ALL)

        writer.writerow(value['header'])
        writer.writerows(value['rows'])

        resp = system['request'].response
        resp.content_type = 'text/csv'
        resp.content_disposition = 'attachment;filename="' + value['filename'] + '.csv"'
        return f_out.getvalue()


json_tree_renderer = JSON()


def concept_adapter(obj, request):
    '''
    Adapter for rendering a :class:`skosprovider_sqlalchemy.models.Concept` to json for tree view.
    '''
    narrower = [nconcept for nconcept in obj.narrower_concepts] if hasattr(obj, 'narrower_concepts') else None
    return {
        'id': obj.concept_id,
        'type': 'concept',
        'label': obj.label(request.locale_name).label,
        'children': sorted(narrower, key=lambda child: child.label(request.locale_name).label.lower())
    }


def collection_adapter(obj, request):
    '''
    Adapter for rendering a :class:`skosprovider_sqlalchemy.models.Collection` to json for tree view.
    '''

    children = [member for member in obj.members] if hasattr(obj, 'members') else None
    return {
        'id': obj.concept_id,
        'type': 'collection',
        'label': obj.label(request.locale_name).label,
        'children': sorted(children, key=lambda child: child.label(request.locale_name).label.lower())
    }

json_tree_renderer.add_adapter(Concept, concept_adapter)
json_tree_renderer.add_adapter(Collection, collection_adapter)
