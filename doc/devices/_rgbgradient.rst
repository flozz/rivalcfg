This mouse supports RGB Gradient. In addition of static colors, you can
configure a gradient. The color of the mouse will change according to the
colors of the gradient.

RGB Gradient expression
~~~~~~~~~~~~~~~~~~~~~~~

The RGB Gradient follows this format::

    rgbgradient(duration=<DURATION>; colors=<POS1>: <COLOR1>, <POSN>: COLORN>)

* ``duration``: the time in miliseconds of the color loop. This parameter is optional. Default value: ``1000`` (1 second).
* ``colors``: the colors of the gradient.

  * The ``<POS>`` parameters are the position of the color stops (e.g. ``0%``, ``50%``,...).
  * The ``<COLOR>`` parameters are the colors in any suported format (se above).

.. NOTE::

   A maximum of 14 color are supported in a RGB Gradient.


Example Gradients
~~~~~~~~~~~~~~~~~

.. raw:: html

   <div class="gradient-preview" style="background: linear-gradient(90deg, #ff0000 0%, #00ff00 33%, #0000ff 66%, #ff0000 100%);"></div>

.. code-block:: text

    rgbgradient(duration=5000; colors=0%: red, 33%: lime, 66%: blue)


.. raw:: html

   <div class="gradient-preview" style="background: linear-gradient(90deg, #e90cce 0%, #ffe701 33%, #01cafe 66%, #e90cce 100%);"></div>

.. code-block:: text

    rgbgradient(duration=5000; colors=0%: #e90cce, 33%: #ffe701, 66%: #01cafe)


.. raw:: html

   <div class="gradient-preview" style="background: linear-gradient(90deg, #ff1800 0%, #fde700 50%, #ff1800 100%);"></div>

.. code-block:: text

    rgbgradient(duration=1000; colors=0%: #ff1800, 50%: #fde700)


.. raw:: html

   <div class="gradient-preview" style="background: linear-gradient(90deg, #3acbe8 0%, #8706fe 50%, #3acbe8 100%);"></div>

.. code-block:: text

    rgbgradient(duration=1000; colors=0%: #3acbe8, 50%: #8706fe)


.. raw:: html

   <div class="gradient-preview" style="background: linear-gradient(90deg, black 0%, red 8%, black 16%, yellow 24%, black 32%, lime 40%, black 48%, aqua 56%, black 64%, blue 72%, black 80%, fuchsia 88%, black 100%);"></div>

.. code-block:: text

    rgbgradient(duration=15000; colors=0%: black, 8%: red, 16%: black, 24%: yellow, 32%: black, 40%: lime, 48%: black, 56%: aqua, 64%: black, 72%: blue, 80%: black, 88%: fuchsia)


RGB Gradient Dict (Python API only)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are using the **Python API** (not the command line interface), you can also pass a Python ``dict`` to define a gradient.

Example:

.. raw:: html

   <div class="gradient-preview" style="background: linear-gradient(90deg, #ff0000 0%, #00ff00 33%, #0000ff 66%, #ff0000 100%);"></div>

.. code-block:: python

   {
       "duration": 5000,  # ms
       "colors": [
           {"pos": 0, "color": "red"},
           {"pos": 33, "color": "#00FF00"},
           {"pos": 66, "color": (0, 0, 255)},
       ]
   }



.. raw:: html

   <style>
       .gradient-preview {
            height: 24px;
            border: #444 solid 1px;
            vertical-align: middle;
            border-radius: 2px;
            box-shadow: inset -1px -1px 0 rgba(255, 255, 255, .5), inset 1px 1px 0 rgba(255, 255, 255, .5);
       }
   </style>

