#!/usr/bin/env python3

import itertools
import os

import jinja2
import yaml

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, '..', '..', '..')

def find_templates(starting_directory):
    for directory, subdirectories, file_names in os.walk(starting_directory):
        for file_name in file_names:
            if file_name.startswith('.'):
                continue
            yield file_name, os.path.join(directory, file_name)

def test_name(directory, template_name, subtest_flags):
    '''
    Create a test name based on a template and the WPT file name flags [1]
    required for a given subtest. This name is used to determine how subtests
    may be grouped together. In order to promote grouping, the combination uses
    a few aspects of how file name flags are interpreted:

    - repeated flags have no effect, so duplicates are removed
    - flag sequence does not matter, so flags are consistently sorted

    directory | template_name    | subtest_flags   | result
    ----------|------------------|-----------------|-------
    cors      | image.html       | []              | cors/image.html
    cors      | image.https.html | []              | cors/image.https.html
    cors      | image.html       | [https]         | cors/image.https.html
    cors      | image.https.html | [https]         | cors/image.https.html
    cors      | image.https.html | [https]         | cors/image.https.html
    cors      | image.sub.html   | [https]         | cors/image.https.sub.html
    cors      | image.https.html | [sub]           | cors/image.https.sub.html

    [1] docs/writing-tests/file-names.md
    '''
    template_name_parts = template_name.split('.')
    flags = set(subtest_flags) | set(template_name_parts[1:-1])
    test_name_parts = (
        [template_name_parts[0]] +
        sorted(flags) +
        [template_name_parts[-1]]
    )
    return os.path.join(directory, '.'.join(test_name_parts))

def merge(a, b):
    if type(a) != type(b):
        raise Exception('Cannot merge disparate types')
    if type(a) == list:
        return a + b
    if type(a) == dict:
        merged = {key: merge(a[key], b[key]) if key in b else a[key] for key in a}
        for key in b:
            if key not in a:
                merged[key] = b[key]

        return merged

    raise Exception(f'Cannot merge {type(a).__name__} type')

def product(a, b):
    '''
    Given two lists of objects, compute their Cartesian product by merging the
    elements together. For example,

       product(
           [{'a': 1}, {'b': 2}],
           [{'c': 3}, {'d': 4}, {'e': 5}]
       )

    returns the following list:

        [
            {'a': 1, 'c': 3},
            {'a': 1, 'd': 4},
            {'a': 1, 'e': 5},
            {'b': 2, 'c': 3},
            {'b': 2, 'd': 4},
            {'b': 2, 'e': 5}
        ]
    '''
    result = []

    for a_object in a:
        result.extend(merge(a_object, b_object) for b_object in b)
    return result

def make_provenance(project_root, cases, template):
    return '\n'.join(
        [
            'This test was procedurally generated. Please do not modify it directly.',
            'Sources:',
            f'- {os.path.relpath(cases, project_root)}',
            f'- {os.path.relpath(template, project_root)}',
        ]
    )

def collection_filter(obj, title):
    if not obj:
        return f'no {title}'

    members = []
    for name, value in obj.items():
        if value == '':
            members.append(name)
        else:
            members.append(f'{name}={value}')

    return f"{title}: {', '.join(members)}"

def pad_filter(value, side, padding):
    if not value:
        return ''
    return padding + value if side == 'start' else value + padding

def main(config_file):
    with open(config_file, 'r') as handle:
        config = yaml.safe_load(handle.read())

    templates_directory = os.path.normpath(
        os.path.join(os.path.dirname(config_file), config['templates'])
    )

    environment = jinja2.Environment(
        variable_start_string='[%',
        variable_end_string='%]'
    )
    environment.filters['collection'] = collection_filter
    environment.filters['pad'] = pad_filter
    templates = {}
    subtests = {}

    for template_name, path in find_templates(templates_directory):
        subtests[template_name] = []
        with open(path, 'r') as handle:
            templates[template_name] = environment.from_string(handle.read())

    for case in config['cases']:
        if unused_templates := set(templates) - set(case['template_axes']):
            print(
                'Warning: case does not reference the following templates:'
            )
            print('\n'.join(f'- {name}' for name in unused_templates))

        common_axis = product(
            case['common_axis'], [case.get('all_subtests', {})]
        )

        for template_name, template_axis in case['template_axes'].items():
            subtests[template_name].extend(product(common_axis, template_axis))

    for template_name, value in templates.items():
        provenance = make_provenance(
            PROJECT_ROOT,
            config_file,
            os.path.join(templates_directory, template_name)
        )
        get_filename = lambda subtest: test_name(
            config['output_directory'],
            template_name,
            subtest['filename_flags']
        )
        subtests_by_filename = itertools.groupby(
            sorted(subtests[template_name], key=get_filename),
            key=get_filename
        )
        for filename, some_subtests in subtests_by_filename:
            with open(filename, 'w') as handle:
                handle.write(
                    value.render(
                        subtests=list(some_subtests), provenance=provenance
                    )
                    + '\n'
                )

if __name__ == '__main__':
    main('fetch-metadata.conf.yml')
