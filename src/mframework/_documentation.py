#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2019-2020 Airinnova AB and the Model-Framework authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------

# Author: Aaron Dettmann

"""
Documentation generator for user models
"""

import os


URL_RESSOURCE = 'https://raw.githubusercontent.com/airinnova/model-framework/master/src/mframework/ressources'
URL_ICONS = f"{URL_RESSOURCE}/icons"

RST_GENERAL_USAGE = """
How to use the Model object
===========================

This page describes the usage of the ``Model`` object. This object provides a
pure Python API, so some basic knowledge about Python is assumed.

Model paradigm
--------------

A ``Model`` consists one or more *features*. For instance, an *aircraft* model
might have the feature *propulsion* and the feature *wing*. Such a feature
consists of one or more *properties*. Concrete values can be assigned to these
properties. So, in our example propulsion might have the properties *thrust*
and *type*, and the *wing* feature might have properties *span* and
*mount_point* (e.g. for an engine, landing gear, or some other technical
system). We may assign some values to each of these properties. For instance,
we may set thrust to :math:`50\,\\textrm{kN}` or the span to
:math:`20\,\\textrm{m}`. How do we set these values in a Python script?

.. code:: python

    # Get an instance of the Model object
    model = Model()

    # From the model instance, we can create a 'propulsion' instance. We can
    # now set actual value to the properties 'trust' and propulsion 'type'.
    prop = model.set_feature('propulsion')
    prop.set('thrust', 50e3)
    prop.set('type', 'turbofan engine')

    # Now we create a new 'wing'. We can set the 'span' and add mount points
    wing = model.add_feature('wing')
    wing.set('span', 20)
    wing.add('mount_point', (4, 2, 4))
    wing.add('mount_point', (4, 6, 4))
    wing.add('mount_point', (4, 20, 4))

"""

RST_GENERAL_USAGE += f"""
.. figure:: {URL_RESSOURCE}/aircraft_model.svg
   :width: 500
   :alt: Simple aircraft model
   :align: center

   Simple aircraft model with a *propulsion* features, and a *wing* feature

Notice the method ``add_feature()``. When calling this method, we create a
*instance* of the feature we want to add (here ``'propulsion'`` and
``'wing'``). The feature instance has ``set()`` and ``add()`` methods to assign
a value to some property. The model object will check the value. That means
that you must provide a number for the property *trust*. If you try to assign,
say a string (``'50e3'``), an error will be thrown, and the model will not
continue to be built.
"""

RST_GENERAL_USAGE += f"""

.. figure:: {URL_RESSOURCE}/model_api_hierarchy.svg
   :alt: Model hierarchy
   :align: center

   A model object can have multiple features, and each feature can have
   multiple properties

Model and feature methods
-------------------------

The ``Model`` object and its features provide only few methods. The main thing
to remember is that there are ``set*`` and ``add*`` methods. The ``set*``
method will always apply if there can only be one instance, and the ``add*``
method will apply if there can be multiple instances. For example, an aircraft
can have more than one wing, hence the ``add_feature()`` method applies. To
create another wing, we simply call the method again. However, some feature may
only exists once. In our dummy aircraft model, we impose the restriction of
only adding *one* propulsion feature (arguably, an aircraft model could have
multiple propulsion instances, but here we assume otherwise). To highlight that
propulsion is a *singleton* feature, we use the ``set_feature()`` method.
Trying to use ``add_feature('propulsion')`` will result in an error and the
model will not continue to build. Property values in a feature can be assigned
with the ``add()`` and ``set()`` methods, depending on whether the properties
are singleton or not. In the example above, the wing may have multiple mount
points, but there can only be a single wing span.

+---------------+----------------------------------+---------------------------------+
|               | **Model**                        | **Feature**                     |
+---------------+----------------------------------+---------------------------------+
| Singleton     | ``set_feature('feature_name')``  | ``set('property_name', value)`` |
+---------------+----------------------------------+---------------------------------+
| Non-singleton | ``add_feature('feature_name')``  | ``add('property_name', value)`` |
+---------------+----------------------------------+---------------------------------+

You can retrieve feature instances from your model at any time. Note that you
must have created these instances first with the methods discussed above. The
table below shows the available methods you may use.

..
    TODO
    * More detailed explanation of difference between 'get()' and 'iter()'

+---------------+--------------------------+---------------------------+
|               | **Model**                | **Feature**               |
+---------------+--------------------------+---------------------------+
| Singleton     | ``get('feature_name')``  | ``get('property_name')``  |
+---------------+--------------------------+---------------------------+
| Non-singleton | ``iter('feature_name')`` | ``iter('property_name')`` |
+---------------+--------------------------+---------------------------+

Running the model
-----------------

The last thing you need to know is how to run the model. Once you set up the
entire, you can call the ``run()`` method. This method will start the actual
evaluation of the model.

.. code:: python

    model = Model()
    ...  # Add features and assign values here
    results = model.run()

Results
-------

TODO

\n
"""

RST_INTRO_MODEL_API = f"""Below you will find a comprehensive list of all
available features and properties. The model object has the following features:

\n\n
"""



def gen_feature_graph(mspec):
    """
    Generate a graph listing all the available features
    """

    # TODO: check if 'mermaid' is available, or use alternative display...

    rst = ""
    rst += ".. mermaid::\n\n"
    rst += "    graph TD\n"
    rst += "    A[Model]\n"
    for i, key in enumerate(mspec.keys):
        rst += f"    A --> F{i}[{key}]\n"
    rst += "\n\n"
    return rst


def gen_graph_property_relation(prop_name, parent_feature):
    """
    TODO
    """

    # TODO: check if 'mermaid' is available, or use alternative display...

    rst = ""
    rst += ".. mermaid::\n\n"
    rst += "    graph LR\n"
    rst += "    A[Model]\n"
    rst += f"    A --> F1[{parent_feature}] \n"
    rst += f"    F1 --> P1[{prop_name}] \n"
    rst += "\n\n"
    return rst


def doc2rst(mspec, dir_path=None):
    """
    Convert model documentation to RST

    Args:
        :mspec: (obj) model specification

    Returns:
        :rst: (str) RST documentation
        :file_path: (str) output file
    """

    doc = mspec.get_docs()

    rst = ""
    rst += get_header('Model', level=0)
    rst += RST_INTRO_MODEL_API

    rst += gen_feature_graph(mspec)

    for f_name, f_dict in doc.items():
        if f_name.startswith('$'):
            continue

        rst += get_header(f"Feature: {f_name}", level=1)

        f_main_doc = f_dict.get('main', '')
        if f_main_doc:
            rst += f"{rst_add_icon('description')}*Description*: "
            rst += f_main_doc
            rst += "\n\n"

        rst += f"{rst_add_icon('singleton')}*Singleton*: {f_dict['singleton']}\n\n"
        rst += f"{rst_add_icon('required')}*Required*: {f_dict['required']}\n\n"

        for p_name, p_dict in f_dict['sub'].items():
            rst += get_header(f"Property: {p_name}", level=2)
            rst += gen_graph_property_relation(p_name, f_name)

            p_main_doc = p_dict.get('main', '')
            if p_main_doc:
                rst += f"{rst_add_icon('description')}*Description*: "
                rst += p_main_doc + '\n\n'

            rst += f"{rst_add_icon('singleton')}*Singleton*: {p_dict['singleton']}\n\n"
            rst += f"{rst_add_icon('required')}*Required*: {p_dict['required']}\n\n"

            p_schema_doc = p_dict.get('schema', '')
            if p_schema_doc:
                rst += f"{rst_add_icon('schema')}*Schema*:\n\n"
                rst += schemadict2rst(p_schema_doc)

    if dir_path is not None:
        file_path = os.path.join(dir_path, 'model_api_general.rst')
        with open(file_path, "w") as fp:
            fp.write(RST_GENERAL_USAGE)

        file_path = os.path.join(dir_path, 'model_api.rst')
        with open(file_path, "w") as fp:
            fp.write(rst)

    return rst


def schemadict2rst(sd):
    """
    TODO
    """

    max_key_len = max([len(key) for key in sd.keys()]) + 4
    max_value_len = max([len(str(value)) for value in sd.values()])

    n1 = max_key_len
    n2 = max_value_len
    table_env = f"{'='*n1} {'='*n2}\n"

    rst = ''
    rst += table_env
    for key, schema in sd.items():
        key_string = f"**{key}**"
        rst += f"{key_string.center(max_key_len, ' ')} {str(schema).center(max_value_len, ' ')}\n"

    rst += table_env
    rst += '\n'
    return rst


def get_header(string, level=0):
    """
    Make a header

    Args:
        :string: (str) header
        :level: (int) header level

    Returns:
        :rst: (str) RST documentation
    """

    header = {
        0: "=",
        1: "-",
        2: "~",
        3: "^",
    }

    return f"{string}\n{header[level]*len(string)}\n\n"


def rst_add_icon(icon_type):
    """
    TODO
    """

    icons = {
        'feature': 'archive.svg',
        'property': 'parking.svg',
        'description': 'notes.svg',
        'required': 'lifebuoy.svg',
        'singleton': 'point.svg',
        'schema': 'clipboard-check.svg',
    }

    rst = ""
    rst += f".. image:: {URL_ICONS}/{icons[icon_type]}\n"
    rst += f"   :align: left\n"
    rst += f"   :alt: {icon_type}\n"
    rst += "\n"
    return rst
