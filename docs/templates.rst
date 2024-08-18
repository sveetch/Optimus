.. _Jinja2: http://jinja.pocoo.org/
.. _Jinja2 documentation: http://jinja.pocoo.org/docs/

.. _intro_templates:

Templates
=========

The templates are rendered using template engine `Jinja2`_.

For each template the default context variables are :

* ``debug`` : A boolean, his value comes from ``settings.DEBUG``;
* ``SITE`` : A dict containing some variables from the settings;

  * ``name`` : the value from ``settings.SITE_NAME``;
  * ``domain`` : the value from ``settings.SITE_DOMAIN``;
  * ``web_url`` : the value from ``settings.SITE_DOMAIN`` prefixed by ``http://`` or
    ``https://`` depending setting value for ``HTTPS_ENABLED``;

* ``STATIC_URL`` : A string, containing the value from ``settings.STATIC_URL``;
* ``OPTIMUS`` : Optimus version;
* ``_SETTINGS`` : A copy of settings. Only uppercase names are allowed, every other
  will be ignored. Think about to renamed modules you import in your settings to not be
  fully uppercase so they won't be passed to context;

Read the `Jinja2 documentation`_ for more details on the available template markups.
