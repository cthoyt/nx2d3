nx2d3
=====

Display NetworkX graphs inline in Jupyter notebooks

Installing
----------
From the latest code on GitHub with:

.. code-block:: sh

    $ python3 -m pip install git+https://github.com/cthoyt/nx2d3.git

Example
-------

>>> import networkx as nx
>>> import nx2d3
>>> G = nx.petersen_graph()
>>> nx2d3.embed_networkx(G)

**Note:** GitHub will not render custom javascript on https://github.com/cthoyt/nx2d3/blob/master/example.ipynb. 
Instead, try nbviewer http://nbviewer.jupyter.org/github/cthoyt/nx2d3/blob/master/example.ipynb or viewing the
notebooks in jupyter notebook locally.
