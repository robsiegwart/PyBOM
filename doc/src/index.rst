Welcome to pyBOM's documentation
================================

Background
----------

Some conventions used in this module are based on a few of the concepts from the
book *Engineering Documentation Control Handbook*, 4th Ed. by Frank B. Watts.
One of which is the use of a master parts list, which represents a singular
source of information for items - parts, drawings, documents, etc.
In the context of this program this is represented by an Excel file with a
special name (defaults to ``Parts list.xlsx``). For example, parts for a
skateboard might have:

=========== ============= ============================== ======================= ============== ======== ============== =====
PN          Name          Description                    Supplier                Supplier PN    Pkg QTY  Pkg Price      Item
=========== ============= ============================== ======================= ============== ======== ============== =====
SK1001-01   Deck          Pavement Pro 9" Maple Deck     Grindstone Supply Co.   BRX-02         1        67.95          part
SK1002-01   Truck         HollowKing Standard Trucks     Grindstone Supply Co.   TR1-A          1        28.95          part
SK1003-01   Bearing       ABEC-7 Steel Bearings          BoltRun Hardware        74295-942      1        9.95           part
SK1004-01   Wheel         SlickCore 54mm Cruiser Wheels  Grindstone Supply Co.   WHL-PRX        4        44.95          part
SK1005-01   Screw         10-32, 1", Phillips            BoltRun Hardware        92220A         25       12.49          part
SK1006-01   Nut           10-32                          BoltRun Hardware        95479A         25       9.89           part
SK1007-01   Grip Tape     SuperStick 9"                  BoltRun Hardware        GTSS99         1        8.95           part
=========== ============= ============================== ======================= ============== ======== ============== =====

For each assembly, all that is required is the part identification number and
its quantity which correspond to the following fields:

- PN
- QTY

Example wheel assembly (1 wheel + 2 bearings):

=========== =====
PN          QTY
=========== =====
SK1004-01   1
SK1003-01   2
=========== =====

Certain fields are used in calculating totals, such as in :py:attr:`BOM.BOM.summary`,
which are:

================= ==============================================================
``Pkg QTY``       The quantity of items in a specific supplier SKU (i.e. a bag
                  of 100 screws)
``Pkg Price``     The cost of a specific supplier SKU
================= ==============================================================


Usage
-----

Create a folder to contain your BOM files and create a parts list and any
assemblies as individual Excel files (the file name becomes the assembly item
number by default). Then, call class method :py:meth:`BOM.BOM.from_folder()`
with the path to your folder to instantiate and build BOM objects.

Alternatively, use :py:meth:`BOM.BOM.single_file()` to load all parts and
assemblies from a single multi-sheet Excel file.

Then, call methods or properties on the root BOM to obtain derived information:

:py:attr:`BOM.BOM.parts`
   Get a list of all direct-child parts

:py:attr:`BOM.BOM.assemblies`
   Get a list of all direct-child assemblies

:py:attr:`BOM.BOM.flat`
   Get a flattened list of all parts, recursively expanding sub-assemblies

:py:meth:`BOM.BOM.QTY`
   Get the quantity of a specific item by its part number in the current BOM
   context

:py:attr:`BOM.BOM.aggregate`
   Get the aggregated quantity of each part/assembly from the current BOM level
   down

:py:attr:`BOM.BOM.summary`
   Get a summary in the form of a DataFrame containing the master parts list
   with each item's aggregated quantity and the required packages to buy if the
   ``Pkg QTY`` field is not 1.

:py:attr:`BOM.BOM.tree`
   Return a string representation of the BOM tree hierarchy

:py:attr:`BOM.BOM.dot`
   Return the BOM tree in DOT graph format (Graphviz)


Command-Line Interface
----------------------

The package installs a ``pybom`` command (also accessible as ``python -m pybom``)
for quick access to BOM properties from the terminal.

Usage::

   pybom -f FILE action
   pybom -d FOLDER action

Arguments:

``-f FILE``
   Path to a single Excel BOM file.

``-d FOLDER``
   Path to a folder of BOM Excel files (uses :py:meth:`BOM.BOM.from_folder()`).

``action``
   Any property or method name on the :py:class:`BOM.BOM` object, e.g.
   ``tree``, ``aggregate``, ``summary``.

Example::

   pybom -d ./skateboard tree


Classes
-------

.. autoclass:: BOM.BaseItem
   :members:
.. autoclass:: BOM.Item
   :members:
.. autoclass:: BOM.ItemLink
   :members:
.. autoclass:: BOM.BOM
   :members:
.. autoclass:: BOM.PartsDB
   :members: