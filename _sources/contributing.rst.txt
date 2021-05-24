.. _contributing:

Contributing
============

Thank you for your interest about Rivalcfg. You will find here all useful
information to contribute.


Questions
---------

If you have any question, you can:

* `open an issue <https://github.com/flozz/rivalcfg/issues>`_ on Github,
* or `ask on Discord <https://discord.gg/P77sWhuSs4>`_ (I am not always
  available for chatting but I try to answer to everyone).


Unsupported devices
-------------------

You just bought a brand new SteelSeries mouse and it is not supported by
rivalcfg? The first thing to do is to check if someone else already reported
this on the issue tracker on Github:

* https://github.com/flozz/rivalcfg/issues

If not, open an issue providing the following information:

* The mouse ``vendor_id``, ``product_id`` and ``product_string``. On Linux you
  will find this information with the following command::

     lsusb -d 1038:

  Example result for a Rival 100::

     Bus 005 Device 009: ID 1038:1702 SteelSeries ApS SteelSeries Rival 100 Gaming Mouse

* When possible, a link to the product description (on the SteelSeries
  website or any other online shop)

Then, it depend...

Sometime SteelSeries release new mice that are identical to an exiting model
but only with some aesthetic changes (like the Rival 100, Rival 100 Dota
2 Edition, and so on). In that case, it will be easy to support your mouse.

And sometime it is a brand new model that will need some reverse engineering...
This can only be done by someone that own the mouse. It can be you (it is
easier than you think), it can be me (if I can find someone to lend me the
mouse) or it can be any other contributor.

You can also consider supporting the project using the ``Sponsor`` button on
Github to allow me buying new SteelSeries mice in order to support them in
rivalcfg.


Bugs
----

Rivalcfg does not work? Please `open an issue
<https://github.com/flozz/rivalcfg/issues>`_ on Github with as much information
as possible.

When possible:

* Run the ``rivalcfg --print-debug`` command and include its output to your
  report (note that you may need to run this command as root to get all
  information).

If this command cannot be run, include at least the following information:

* What is your operating system / Linux distribution (and its version),
* Which SteelSeries mouse you have trouble with,
* How you installed Rivalcfg.

And always provide all error messages outputted by Rivalcfg.


Pull Requests
-------------

Please consider `filing a bug <https://github.com/flozz/rivalcfg/issues>`_
before starting to work on a new feature or on the support of a new mouse. This
will allow us to discuss the best way to do it. This is of course not necessary
if you just want to fix some typo in the documentation or small errors in the
code.

Please note that your code must pass tests and follow the coding style defined
by the `pep8 <https://pep8.org/>`_. The code of this project is automatically
checked by `Flake8 <https://flake8.pycqa.org/en/latest/>`_ and the coding style
is enforced using `Black <https://black.readthedocs.io/en/stable/>`_.


Running The Tests
-----------------

You will first have to install `nox <https://nox.thea.codes/>`_::

    pip3 install nox

Then you can check for lint error::

    nox --session lint

If Black reports you coding style errors, you can automatically fix them with
this command::

    nox -s black_fix

To run the tests use::

    nox --session test

To run the tests only for a specific Python version, you can use following
commands (the corresponding Python interpreter must be installed on your
machine)::

    nox --session test-2.7
    nox --session test-3.6
    nox --session test-3.7
    nox --session test-3.8
    nox --session test-3.9


Building The Documentation
--------------------------

You will first have to install `nox <https://nox.thea.codes/>`_::

    pip3 install nox

Then you can run the following command::

    nox --session gendoc

