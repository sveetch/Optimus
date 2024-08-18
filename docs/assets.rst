.. _webassets: https://github.com/miracle2k/webassets
.. _webassets documentation: http://webassets.readthedocs.org/

.. _assets_intro:

.. _basics-assets-label:

Assets
======

You can simply put your assets where you want in the ``sources`` directory and add your
assets directories in ``settings.FILES_TO_SYNC``, they will be copied to your build
directory.

But with Optimus this is only required for *real* static assets like images or fonts.
For CSS and Javascript you should manage them with `webassets`_ that is already
installed with Optimus.

With `webassets`_ you manage your assets as packages named ``Bundle``, like a bundle
for your main CSS, another for your IE CSS hacks/patchs and another for your
Javascripts files. You will have to register your custom bundles in
``settings.BUNDLES`` and enable them in ``settings.ENABLED_BUNDLES``.

The benefit of `webassets`_ is that it can pre and post process all your assets. This
is usually used to *minify* and pack multiple files in one final file. Read the
`webassets documentation`_ for more details how to use this and to manage bundle assets
in your templates.
