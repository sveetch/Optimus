.. _Django: http://www.djangoproject.com/
.. _Jinja2: http://jinja.pocoo.org/
.. _Jinja2 documentation: http://jinja.pocoo.org/docs/
.. _yui-compressor: http://developer.yahoo.com/yui/compressor/
.. _webassets: https://github.com/miracle2k/webassets
.. _webassets documentation: http://webassets.readthedocs.org/
.. _virtualenv: http://www.virtualenv.org/
.. _Babel: https://pypi.python.org/pypi/Babel
.. _Optimus: https://github.com/sveetch/Optimus

.. _pages_intro:

Pages
=====

A page is built from a view that is either an instance of class ``PageViewBase``, an
instance of a class which inherits from ``PageViewBase``.

The pages to build are registered in a Python module in your project, it must
contains a ``PAGES`` variable that is a list containing view instances.


.. _pages_pageviewbase:

PageViewBase
************

This is the most basic view available which implements everything Optimus needs to
build a page.

.. Warning::
    On its default state this view only outputs an empty string since it is on your
    own to define a proper ``render()`` method.

View object arguments
---------------------

There are three required arguments to initialize a ``PageViewBase`` object:

**title**
    The title of your page, can be anything you want, it's just a context variable
    that you can use in your templates.
**destination**
    Destination file path where the page will be builded, the path is relative to the
    setting ``PUBLISH_DIR``. You can use multiple subdirectory levels if needed, the
    builder will create them if it does not already exists.
**page_datas**
    List of data file paths related to the page building. It is mostly used from the
    watcher to know what data files to watch for and possibly trigger a build.

The short way is like so : ::

    from optimus.pages.views import PageViewBase
    # Enabled pages to build
    PAGES = [
        PageViewBase(title="My page", destination="mypage.html"),
    ]

.. Note::
    These arguments are saved as attributes of your instances, so you can reach
    them more easily from possible extending code but you will still have to set them in
    view context if needed.

But it is more likely you need to build more than one pages and generally you want to
share some attributes like destination or title. So instead of directly using
``PageViewBase``, you should make your own page object like this : ::

    from optimus.pages.views import PageViewBase

    class MyBasePage(PageViewBase):
        title = "A page"
        destination = "index.html"

    # Enabled pages to build
    PAGES = [
        MyBasePage(),
        MyBasePage(destination="foo.html"),
    ]

As you can see the view arguments are not mandatory, they are just required to no be
empty. So if your class define proper attributes you may not need to define them again
from arguments.

.. Warning::
    Arguments set object attributes, be careful to not override internal view
    attribute names like ``settings``, ``context`` or some other ones. Refer to the
    view classes source to know about reserved names.


View context
------------

This is an internal payload inside a view instance to easily reach some variables
during the rendering of the view content.

Default ``PageViewBase`` instance adds some variables to its context:

**page_title**
    This variable contains the value of ``PageViewBase.title`` attribute.
**page_destination**
    This variable contains the value of ``PageViewBase.destination`` attribute.
**page_relative_position**
    This variable contains the relative path position from the destination file to the
    root of the publish directory;
**page_lang**
    This variable contains the value of ``PageViewBase.page_lang`` attribute.
**page_datas**
    This variable contains the value of ``PageViewBase.page_datas`` attribute.


Extending
---------

You can override some methods to add logic or change some behaviors in your
``PageViewBase`` object.

**PageViewBase.get_title()**
    Set the ``page_title`` context variable.
**PageViewBase.get_destination()**
    Set the ``page_destination`` context variable.
**PageViewBase.get_relative_position()**
    Set the ``page_relative_position`` context variable.
**PageViewBase.get_lang()**
    Set the ``page_lang`` context variable.
**PageViewBase.get_datas()**
    Set the ``page_datas`` context variable.
**PageViewBase.get_context()**
    Set the view context to add variables to expose (mostly useful within templates
    like with ``PageTemplateView``). The method does not attempt any argument and
    return the context.

    To add a new variable ``foo`` in your context you may do it like this : ::

        class MyPage(PageViewBase):
            title = "My page"
            destination = "mypage.html"

            def get_context(self):
                # This line set the default context from PageViewBase
                super().get_context()
                # Add your new variables here
                self.context.update({
                    'foo': 'bar',
                })
                return self.context

**PageViewBase.render(environment)**
    This is the method that will build the page content. The view base has nothing to
    render so it just return an empty string. It is on your own to define this method
    for a base view.

    Other view types like ``PageTemplateView`` are already implemented to render a
    proper content so you do not need to define it yourself.

    This method expect a single argument ``environment`` that is expected to a be a
    Jinja environment object.

See ``optimus.pages.views`` sources to see more detail on view classes.


.. _pages_pagetemplateview:

PageTemplateView
****************

View object arguments
---------------------

Additionally to the base view arguments, the template view has some more:

**template_name**
    File path for the template to use, the path is relative to the setting
    ``TEMPLATES_DIR``.

View context
------------

Additionally to the base view, ``PageTemplateView`` adds some more context variables:

**page_template_name**
    This variable contains the value of ``PageTemplateView.template_name`` attribute.


Extending
---------

Additionally to the base view, ``PageTemplateView`` has some more methods to extend if
needed:

**PageTemplateView.get_template_name**
    Set the ``page_template_name`` context variable.
