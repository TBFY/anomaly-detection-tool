
/*
dtree visoualisation :: based on source https://bl.ocks.org/ajschumacher/65eda1df2b0dd2cf616f

Usage example:

	    var dTreeChart = decisionTreeChart();

		d3.json(dataFileSource, function(error, data)
		{
			d3.select('.tree-custom-container')
                    .datum(data) // bind data to the div
                    .call(dTreeChart); // draw chart in div
		});

*/

function decisionTreeChart()
{
    var margin = {top: 20, right: 120, bottom: 20, left: 180},
        width = 960 - margin.right - margin.left,
        height = 480 - margin.top - margin.bottom;

    var i = 0,
        duration = 750,
        root;

    var tree = d3.layout.tree()
                .size([height, width]);

    var svg, diagonal;

    function chart(selection)
    {
        selection.each(function(data)
        {
            diagonal = d3.svg.diagonal()
                    .projection(function(d) { return [d.y, d.x]; });

            svg = selection.append("svg")
                    //.attr("width", width + margin.right + margin.left)
                    .attr("width", '400%')
                    .attr("height", height + margin.top + margin.bottom)
                    //.attr("height", '200%')
                    .attr("border", '1px solid red')
                    .append("g")
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


            root = data;
            root.x0 = height / 2;
            root.y0 = 0;
            root.children.forEach(collapse);
            update(root);
        });
    };

    function collapse(d)
    {
        if (d.children)
        {
            d._children = d.children;
            d._children.forEach(collapse);
            d.children = null;
        }
    };

    function update(source)
    {
        // Compute the new tree layout.
        var nodes = tree.nodes(root).reverse(),
            links = tree.links(nodes);

        // Normalize for fixed-depth.
        nodes.forEach(function(d) { d.y = d.depth * 180; });

        // Update the nodes…
        var node = svg.selectAll("g.node")
                        .data(nodes, function(d) { return d.id || (d.id = ++i); });


        // Enter any new nodes at the parent's previous position.
        var nodeEnter = node.enter().append("g")
                        .attr("class", "node")
                        .attr("transform", function(d) { return "translate(" + source.y0 + "," + source.x0 + ")"; })
                        .on("click", click);

        nodeEnter.append("circle")
                        .attr("r", 1e-6)
                        .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

        var nameArray = source.name;
        var tmp_i;
        for (tmp_i = 0; tmp_i < nameArray.length; tmp_i++)
        {
            var _name = nameArray[tmp_i];
            var _dy = tmp_i + 0.35;
            var _opacity = 1;
            if(tmp_i == 0) _opacity = 0;
            nodeEnter.append("text")
                        .attr("x", function(d) { return d.children || d._children ? -10 : 10; })
                        .attr("dy", _dy.toString() + 'em')
                        .attr("text-anchor", function(d) { return d.children || d._children ? "end" : "start"; })
                        .text(function(d) { return d.name[tmp_i]; })
                        .style("fill-opacity", _opacity);
        }

        // Transition nodes to their new position.
        var nodeUpdate = node.transition()
                        .duration(duration)
                        .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });

        nodeUpdate.select("circle")
                        .attr("r", 4.5)
                        .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

        nodeUpdate.select("text")
                        .style("fill-opacity", 1);

        // Transition exiting nodes to the parent's new position.
        var nodeExit = node.exit().transition()
                        .duration(duration)
                        .attr("transform", function(d) { return "translate(" + source.y + "," + source.x + ")"; })
                        .remove();

        nodeExit.select("circle")
                        .attr("r", 1e-6);

        nodeExit.select("text")
                        .style("fill-opacity", 1e-6);

        // Update the links…
        var link = svg.selectAll("path.link")
                         .data(links, function(d) { return d.target.id; });

        // Enter any new links at the parent's previous position.
        link.enter().insert("path", "g")
                        .attr("class", "link")
                        .attr("d", function(d) {
                            var o = {x: source.x0, y: source.y0};
                            return diagonal({source: o, target: o});
                        });

        // Transition links to their new position.
        link.transition()
                        .duration(duration)
                        .attr("d", diagonal);

        // Transition exiting nodes to the parent's new position.
        link.exit().transition()
                        .duration(duration)
                        .attr("d", function(d) {
                            var o = {x: source.x, y: source.y};
                            return diagonal({source: o, target: o});
                        })
                        .remove();

        // Stash the old positions for transition.
        nodes.forEach(function(d)
        {
            d.x0 = d.x;
            d.y0 = d.y;
        });
    };

    // Toggle children on click.
    // Toggle children on click.

    function click(d)
    {
        if (d.children)
        {
            d._children = d.children;
            d.children = null;
        } else {
            d.children = d._children;
            d._children = null;
        }
        update(d);
    };

    // variable setters
    // variable setters

    chart.height = function(value)
    {
        if (!arguments.length) return height;
        height = value - margin.top - margin.bottom;
        return chart;
    };

    chart.root = function(value)
    {
        if (!arguments.length) return root;
        root = value;
        return chart;
    };

    return chart;
}