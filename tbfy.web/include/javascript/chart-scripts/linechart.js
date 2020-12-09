// function draws line chart
// function draws line chart

function lineChart()
{
    var margin = {top: 10, right: 30, bottom: 50, left: 60},
        width = 750 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom,
        xLabel = '',
        yLabel = '',
        xValueFieldName = '',
        yValueFieldName = '',
        xScaleType = 'linear',
        appendLine = [],
        metaFieldName = '',
        metaHtmlElement = '',
        metaFunctionExternal = '';

    function chart(selection)
    {
        selection.each(function(data)
        {
            // get plot range
            // get plot range

            min_x = d3.min(data, function(d) { return eval("d." + xValueFieldName); });
            max_x = d3.max(data, function(d) { return eval("d." + xValueFieldName); });

            min_y = d3.min(data, function(d) { return eval("d." + yValueFieldName); });
            max_y = d3.max(data, function(d) { return eval("d." + yValueFieldName); });

            // create x and y axis
            // create x and y axis

            if(xScaleType == 'time')
            {
                var xScale = d3.scaleTime()
                    .domain([min_x, max_x])
                    .range([0, width]);
            }
            else
            {
                var xScale = d3.scaleLinear()
                    .domain([min_x, max_x])
                    .range([0, width]);
            }

            var yScale = d3.scaleLinear()
                .domain([min_y, max_y])
                .range([height, 0]);

            // creates new line chart
            // creates new line chart

            var line = d3.line()
                .x(function(d, i) { return xScale(eval("d." + xValueFieldName)); })
                .y(function(d, i) { return yScale(eval("d." + yValueFieldName)); })
                .curve(d3.curveMonotoneX);

            // append the svg object to the body of the page
            // append a 'group' element to 'svg'
            // moves the 'group' element to the top left margin

            var svg = selection.append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            // add the x axis
            // add the x axis

            svg.append("g")
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(xScale));

            svg.append("text")
                .attr("transform", "translate(" + (width/2) + " ," +  (height + margin.top + 35) + ")")
                .style("text-anchor", "middle")
                .text(xLabel);

            // add the y axis
            // add the y axis

            svg.append("g")
                .call(d3.axisLeft(yScale));

            svg.append("text")
                .attr("transform", "rotate(-90)")
                .attr("y", 0 - margin.left)
                .attr("x",0 - (height / 2))
                .attr("dy", "1em")
                .style("text-anchor", "middle")
                .text(yLabel);

            // add additional lines
            // add additional lines

            if(appendLine.length > 0)
            {
                var i;
                for (i = 0; i < appendLine.length; i++)
                {
                    // draw line
                    // draw line

                    coordinates = appendLine[i]['coordinates'];
                    linecss     = appendLine[i]['css'];

                    // parse x coordinates
                    // parse x coordinates

                    var x1 = coordinates["x1"];
                    if(coordinates["xscale"] == true) x1 = xScale(x1);
                    else
                    {
                        if(x1 == "max")
                        {
                            x1 = max_x;
                            x1 = xScale(x1)
                        }
                        if(x1 == "min")
                        {
                            x1 = min_x;
                            x1 = xScale(x1)
                        }
                    }
                    var x2 = coordinates["x2"];
                    if(coordinates["xscale"] == true) x2 = xScale(x2);
                    else
                    {
                        if(x2 == "max")
                        {
                            x2 = max_x;
                            x2 = xScale(x2)
                        }
                        if(x2 == "min")
                        {
                            x2 = min_x;
                            x2 = xScale(x2)
                        }
                    }

                    // parse y coordinates
                    // parse y coordinates

                    var y1 = coordinates["y1"];
                    if(coordinates["yscale"] == true) y1 = yScale(y1);
                    else
                    {
                        if(y1 == "max")
                        {
                            y1 = max_y;
                            y1 = yScale(y1)
                        }
                        if(y1 == "min")
                        {
                            y1 = min_y;
                            y1 = yScale(y1)
                        }
                    }
                    var y2 = coordinates["y2"];
                    if(coordinates["yscale"] == true) y2 = yScale(y2);
                    else
                    {
                        if(y2 == "max")
                        {
                            y2 = max_y;
                            y2 = yScale(y2)
                        }
                        if(y2 == "min")
                        {
                            y2 = min_y;
                            y2 = yScale(y2)
                        }
                    }

                    // append line
                    // append line

                    svg.append("svg:line")
                        .attr("x1", x1)
                        .attr("y1", y1)
                        .attr("x2", x2)
                        .attr("y2", y2)
                        .style("stroke-width", linecss["lwidth"])
                        .style("stroke", linecss["stroke"])
                        .style("fill", linecss["fill"]);

                    // draw line legend
                    // draw line legend

                    // parse positon
                    // parse positon

                    coordinates = appendLine[i]['legend']["position"];

                    var px = coordinates["px"];
                    if(coordinates["xscale"] == true) px = xScale(px);
                    else
                    {
                        if(px == "max")
                        {
                            px = max_x;
                            px = xScale(px)
                        }
                        if(px == "min")
                        {
                            px = min_x;
                            px = xScale(px)
                        }
                    }
                    var py = coordinates["py"];
                    if(coordinates["yscale"] == true) py = yScale(py);
                    else
                    {
                        if(py == "max")
                        {
                            py = max_y;
                            py = yScale(py)
                        }
                        if(py == "min")
                        {
                            py = min_y;
                            py = yScale(py)
                        }
                    }

                    svg.append("rect")
                        //.attr("class", "legend")
                        .attr("x", px)
                        .attr("y", py)
                        .attr("width", 20)
                        .attr("height", 2)
                        .attr("stroke", linecss["stroke"])
                        .attr("fill", linecss["fill"]);

                    svg.append("text")
                        .attr("x", px + 30)
                        .attr("y", py + 5)
                        .style("fill", "ff0000")
                        .text(appendLine[i]['legend']['title']);
                }
            }

            // append path, bind the data, and call the line generator
            // append path, bind the data, and call the line generator

            svg.append("path")
                .datum(data)       // binds data
                .attr("class", "path_line")
                .attr("d", line);   // calls the line generator

            svg.selectAll(".dot")
                .data(data)
                .enter().append("circle") // Uses the enter().append() method
                .attr("class", "dot") // Assign a class for styling
                .attr("cx", function(d, i) { return xScale(eval("d." + xValueFieldName)) })
                .attr("cy", function(d) { return yScale(eval("d." + yValueFieldName)) })
                .attr("r", 5)
                .on("mouseover", function(a, b, c) {
                    //console.log(a)
                    this.attr('class', 'focus')
                })
                .on("mouseout", function() {  })
        });
    };

    // getter and setter functions. See Mike Bostocks post "Towards Reusable Charts" [https://bost.ocks.org/mike/chart/] for a tutorial on how this works.
    chart.width = function(value)
    {
        if (!arguments.length) return width;
        width = value - margin.left - margin.right;
        return chart;
    };

    chart.height = function(value)
    {
        if (!arguments.length) return height;
        height = value - margin.top - margin.bottom;
        return chart;
    };

    chart.margin = function(value)
    {
        if (!arguments.length) return margin;
        margin = value;
        return chart;
    };

    chart.xLabel = function(value)
    {
        if (!arguments.length) return xLabel;
        xLabel = value;
        return chart;
    };

    chart.yLabel = function(value)
    {
        if (!arguments.length) return yLabel;
        yLabel = value;
        return chart;
    };

    chart.xValueFieldName = function(value)
    {
        if (!arguments.length) return xValueFieldName;
        xValueFieldName = value;
        return chart;
    };

    chart.yValueFieldName = function(value)
    {
        if (!arguments.length) return yValueFieldName;
        yValueFieldName = value;
        return chart;
    };

    chart.xScaleType = function(value)
    {
        if (!arguments.length) return xScaleType;
        xScaleType = value;
        return chart;
    };

    //expected value structure:
    //
    //value = {
    //  "coordinates":
    //  {
    //    "x1": float/int/string,
    //    "y1": float/int/string,
    //    "x2": float/int/string,
    //    "y2": float/int/string,
    //    "xscale": boolean,        => set true if providing x as a value from coordinate system
    //    "yscale":boolean          => set true if providing x as a value from coordinate system
    //  },
    //  "css": {"lwidth": int, "stroke": string, "fill": string},
    //  "legend": {"title": string, "position":{"px": float/int/string, "py": float/int/string, "xscale": boolean, "yscale": boolean}}
    //}

    chart.appendLine = function(value)
    {
        if (!arguments.length) return appendLine;
        appendLine.push(value);
        return chart;
    };

    chart.metaFieldName = function(value)
    {
        if (!arguments.length) return metaFieldName;
        metaFieldName = value;
        return chart;
    };

    chart.metaHtmlElement = function(value)
    {
        if (!arguments.length) return metaHtmlElement;
        metaHtmlElement = value;
        return chart;
    };

    chart.metaFunctionExternal = function(value)
    {
        if (!arguments.length) return metaFunctionExternal;
        metaFunctionExternal = value;
        return chart;
    };

    return chart;
}