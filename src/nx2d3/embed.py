from json import dumps
from string import Template
from random import sample

from IPython.display import Javascript
from networkx.readwrite.json_graph import node_link_data

__all__ = ['embed_networkx']

DEFAULT = Template("""
var process_nx = function(d3, chart_id, graph, width, height) {
    var color = d3.scale.category20();

    var force = d3.layout.force()
        .charge(${charge})
        .linkDistance(${link_distance})
        .size([width, height]);

    var svg = d3.select('#' + chart_id).append("svg")
        .attr("width", width)
        .attr("height", height);

    force
      .nodes(graph.nodes)
      .links(graph.links)
      .start();

    var link = svg.selectAll(".link")
        .data(graph.links)
        .enter().append("line")
        .attr("class", "link")
        .attr("stroke", "${link_stroke_color}")
        .attr("stroke-width", ${link_stroke_width});

    var node = svg.selectAll(".node")
        .data(graph.nodes)
        .enter().append("g")
        .attr("class", "node")
        .call(force.drag);

    node.append("circle")
        .attr("r", ${node_radius})
        .style("fill", function(d) {
            console.log(d, d.color);
            return color(d.color);
        });

    node.append("text")
        .attr("dx", ${node_label_dx})
        .attr("dy", "${node_label_dy}")
        .text(function(d) {
            return d.id;
        });

    force.on("tick", function() {
        link.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        node.attr("transform", function(d) {
            return "translate(" + d.x + "," + d.y + ")";
        });
    });
}
""")

DEFAULT_VALUES = {
    'charge': -200,
    'link_distance': 40,
    'link_stroke_color': '#999',
    'link_stroke_width': 1.5,
    'node_radius': 6,
    'node_label_dx': 12,
    'node_label_dy': '.35em',
}


def embed_networkx(graph, d3_code=None, d3_values=None, width=960, height=600):
    """
    Embeds a networxk into a Jupyter notebook cell with Javascript/D3

    Based on code from http://nbviewer.jupyter.org/github/cmoscardi/embedded_d3_example/blob/master/Embedded_D3.ipynb

    :param graph: a networkx graph
    :param d3_code: a string containing a javascript function, process_nx, with arguments
                    (d3, chart_id, graph, width, height) that creates the svg within #chart_id
    :param width: the generated d3 svg width
    :param height: the generated d3 svg height
    :return: IPython Javascript Object
    """
    if d3_code is None:
        values = DEFAULT_VALUES.copy()
        values.update(d3_values or {})
        d3_code = DEFAULT.substitute(values)
    else:
        d3_code = d3_code.substitute(d3_values or {})

    graph = dumps(node_link_data(graph))
    chart_id = "".join(sample('abcdefghjkmopqrstuvqxyz', 16))

    javascript_vars = "var chart_idx='{}', graphx={}, widthx={}, heightx={};".format(chart_id, graph, width, height)

    require_code = """
        require.config({
          paths: {
              d3: '//cdnjs.cloudflare.com/ajax/libs/d3/3.4.8/d3.min'
          }
        });

        element.append("<div id='" + chart_idx + "'></div>");

        require(['d3'], function(d3) {
            return process_nx(d3, chart_idx, graphx, widthx, heightx)
        })
    """

    return Javascript(javascript_vars + d3_code + require_code)
