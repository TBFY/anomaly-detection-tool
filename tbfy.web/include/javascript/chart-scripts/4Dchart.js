
/**
 * @class chart4D draws a 4D chart using d3 v5.7 The dimensions are represented by:
 * (.) x axis
 * (.) y axis
 * (.) circle size
 * (.) circle color
 */

function chart4D()
{
    /**
     * Creates an instance of 4D chart. Parameters are:
     *
     * @param {margin} char margin
     * @param {width} char width
     * @param {height} char height
     * @param {xLabel} x axis label text
     * @param {yLabel} y axis label text
     * @param {cLabel} color label txt
     * @param {cLabelDisplay} show / hide color label
     * @param {rLabel} radius label text
     * @param {rLabelDisplay} show / hide circle size label
     * @param {xFieldName} name of the tsv field applied to x axis
     * @param {yFieldName} name of the tsv field applied to y axis
     * @param {rFieldName} name of the tsv field applied to radius
     * @param {cFieldName} name of the tsv field applied to color
     * @param {colorScale} predefined d3 color scale schema, see http://using-d3js.com/04_05_sequential_scales.html
     * @param {maxRadius} limit the size of smallest possible circle (to avoid too small circles)
     * @param {minRadius} limit the size of biggest possible circle (to avoid too big circles)
     */

    var margin = {top: 10, right: 30, bottom: 50, left: 60},
        labelWidth = 100,
        width = 980 - margin.left - margin.right - 2 * (labelWidth + margin.right),
        height = 400,
        xLabel = '',
        yLabel = '',
        cLabel = '',
        cLabelDisplay = true,
        rLabel = '',
        rLabelDisplay = true,
        xFieldName = '',
        yFieldName = '',
        rFieldName = '',
        cFieldName = '',
        colorScale = d3.interpolateRgb('#0d5296', '#facb01'),
        //colorScale = d3.interpolateViridis,
        maxRadius = 30,
        minRadius = 5,
        metaHtmlElement = '',
        metaFunctionExternal = '',
        metaDataSourceExternal = '',
        lastSelectedCircle = -1;

    function chart(selection)
    {
        selection.each(function(data)
        {
            var max_x = d3.max(data, function(d) { return + eval("d." + xFieldName); });
            var min_x = d3.min(data, function(d) { return + eval("d." + xFieldName); });
            var max_y = d3.max(data, function(d) { return + eval("d." + yFieldName); });
            var min_y = d3.min(data, function(d) { return + eval("d." + yFieldName); });
            var max_r = d3.max(data, function(d) { return + eval("d." + rFieldName); });
            var min_r = d3.min(data, function(d) { return + eval("d." + rFieldName); });
            var max_c = d3.max(data, function(d) { return + eval("d." + cFieldName); });
            var min_c = d3.min(data, function(d) { return + eval("d." + cFieldName); });

            // update width based on cLabelDisplay and rLabelDisplay
            // update width based on cLabelDisplay and rLabelDisplay

            if(!cLabelDisplay) width = width + labelWidth + margin.right;
            if(!rLabelDisplay) width = width + labelWidth + margin.right;

            // set scale vars
            // set scale vars

            var xScale = d3.scaleLinear()
                .domain([min_x, max_x])
                .range([maxRadius + minRadius, width - maxRadius - minRadius]);
            var xScaleNM = d3.scaleLinear()
                .domain([xScale.invert(0), xScale.invert(width)])
                .range([0, width])
                .nice();
            var yScale = d3.scaleLinear()
                .domain([min_y, max_y])
                .range([height - maxRadius - minRadius, maxRadius + minRadius]);
            var yScaleNM = d3.scaleLinear()
                .domain([yScale.invert(height), yScale.invert(0)])
                .range([height, 0])
                .nice();
            var rScale = d3.scaleLinear()
                .domain([min_r, max_r])
                .range([minRadius, maxRadius]);
            var cScale = d3.scaleLinear()
                .domain([min_c, max_c])
                .range([0, 1]);

            var line = d3.line()
                .x(function(d, i) { return xScale(eval("d." + xValueFieldName)); })
                .y(function(d, i) { return yScale(eval("d." + yValueFieldName)); })
                .curve(d3.curveMonotoneX);

            // create SVG element
            // create SVG element

			var svg = selection.append("svg")
                .attr("width", width + margin.left * 4 + margin.right * 2)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            // add the x axis
            // add the x axis

            svg.append("g")
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(xScaleNM));

            svg.append("text")
                .attr("transform", "translate(" + (width/2) + " ," +  (height + margin.top + 35) + ")")
                .style("text-anchor", "middle")
                .text(xLabel);

            // add the y axis
            // add the y axis

            svg.append("g")
                .call(d3.axisLeft(yScaleNM));

            svg.append("text")
                .attr("transform", "rotate(-90)")
                .attr("y", 0 - margin.left)
                .attr("x",0 - (height / 2))
                .attr("dy", "1em")
                .style("text-anchor", "middle")
                .text(yLabel);

            // add the colorbar
            // add the colorbar

            cLabelSize = 0
            if(cLabelDisplay)
            {
                // update label size
                cLabelSize = margin.right;

                var cb = colorbar()
                    .svg(svg)
                    .colorDomain([min_c, max_c])
                    .x(width + cLabelSize)
                    .height(height)
                    .color(d3.scaleSequential(colorScale));

                svg.append("g")
                    .attr("class", "colourLegend")
                    .attr("transform", "translate(" + (width + margin.right) + ",0)");

                svg.select(".colourLegend")
                    .call(cb);

                svg.append("text")
                    .attr("transform", "rotate(-90)")
                    .attr("y", width + margin.left + margin.right)
                    .attr("x",0 - (height / 2))
                    .attr("dy", "1em")
                    .style("text-anchor", "middle")
                    .text(cLabel);
            }

            // add size legend
            // add size legend

            if(rLabelDisplay)
            {
                var sb = sizebar()
                    .svg(svg)
                    .x(width + 2 * cLabelSize + margin.left)
                    .height(height)
                    .sizeDomain([min_r, max_r])
                    .color(d3.scaleSequential(colorScale)(max_c));

                svg.append("g")
                    .attr("class", "sizeLegend")
                    .attr("transform", "translate(" + (width + margin.left * 2 + margin.right) + ",0)");

                svg.select(".sizeLegend")
                    .attr("font-size", "10")
                    .attr("font-family", "sans-serif")
                    .call(sb);

                svg.append("text")
                    .attr("transform", "rotate(-90)")
                    .attr("y", width + 2 * cLabelSize + 2.5 * margin.left)
                    .attr("x",0 - (height / 2))
                    .attr("dy", "1em")
                    .style("text-anchor", "middle")
                    .text(rLabel);
            }

            // META DATA SECTION START
            // META DATA SECTION START

            if(metaHtmlElement.length > 0)
            {
                var tooltip = d3.select(metaHtmlElement)
                    .style("opacity", 1)
                    .attr("class", "metaDataContainer");

                // a function that activates when mouse over a bar in histogram
                // a function that activates when mouse over a bar in histogram

                var showMetaData = function(d, i) {

                    // change class to selected rect element
                    // change class to selected rect element

                    if(lastSelectedCircle > -1)
                    {
                        selectedRect = svg.selectAll("circle[tabindex='" + lastSelectedCircle + "']");
                        selectedRect.attr("class", "bar");
                    }
                    selectedRect = svg.selectAll("circle[tabindex='" + i + "']");
                    selectedRect.attr("class", "bar_hover");
                    lastSelectedCircle = i;

                    // display data
                    // display data

                    // first find path to filename
                    // first find path to filename

                    filename = metaDataSourceExternal.replace('IDCLUSTER', lastSelectedCircle);
                    console.log(filename);


                    fullFileName = window.location.protocol + "//" + window.location.hostname;
                    fullFileName = fullFileName + '/data_results/publicTenders/kMeans/';
                    fullFileName = fullFileName + filename;

                    // after file name obtained, load data
                    // after file name obtained, load data

                    d3.tsv(fullFileName).then(function(clusterData)
                    {
                        // provide data to meta function
                        // provide data to meta function

                        var htmlText = eval(metaFunctionExternal + "(clusterData, '" + lastSelectedCircle + "', '" + xFieldName + "', '" + xLabel + "', '" + yFieldName + "', '" + yLabel + "');");
                        tooltip.html(htmlText)
                            //.transition()
                            //.duration(1000);
                            //.style("opacity", 1)
                    });
                }

                // A function that change this tooltip when the leaves a point: just need to set opacity to 0 again
                var hideMetaData = function(d, i) {
                    /*
                    tooltip
                        .transition()
                        .duration(100)
                        .style("opacity", 0)
                     */
                }
            }

            // META DATA SECTION END
            // META DATA SECTION END

            // create circles
            // create circles

            svg.selectAll("circle")
                .data(data)
                .enter()
                .append("circle")
                .attr("tabindex", function(d, i) { return i; })
                .attr("cx", function(d) {
                    return xScaleNM( eval("d." + xFieldName) );
                })
                .attr("cy", function(d) {
                    return yScaleNM( eval("d." + yFieldName) );
                })
                .attr("r", function(d) {
                    return rScale(eval("d." + rFieldName) );
                })
                .style("fill", function(d) {
                    return colorScale(cScale( eval("d." + cFieldName)));
                })
                .on("mouseover", showMetaData)
                .on("mouseleave", hideMetaData);
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

    chart.padding = function(value)
    {
        if (!arguments.length) return padding;
        padding = value;
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

    chart.cLabel = function(value)
    {
        if (!arguments.length) return cLabel;
        cLabel = value;
        return chart;
    };

    chart.cLabelDisplay = function(value)
    {
        if (!arguments.length) return cLabelDisplay;
        cLabelDisplay = value;
        return chart;
    };

    chart.rLabel = function(value)
    {
        if (!arguments.length) return rLabel;
        rLabel = value;
        return chart;
    };

    chart.rLabelDisplay = function(value)
    {
        if (!arguments.length) return rLabelDisplay;
        rLabelDisplay = value;
        return chart;
    };

    chart.xFieldName = function(value)
    {
        if (!arguments.length) return xFieldName;
        xFieldName = value;
        return chart;
    };

    chart.yFieldName = function(value)
    {
        if (!arguments.length) return yFieldName;
        yFieldName = value;
        return chart;
    };

    chart.rFieldName = function(value)
    {
        if (!arguments.length) return rFieldName;
        rFieldName = value;
        return chart;
    };

    chart.cFieldName = function(value)
    {
        if (!arguments.length) return cFieldName;
        cFieldName = value;
        return chart;
    };

    chart.maxRadius = function(value)
    {
        if (!arguments.length) return maxRadius;
        maxRadius = value;
        return chart;
    };

    chart.minRadius = function(value)
    {
        if (!arguments.length) return minRadius;
        minRadius = value;
        return chart;
    };

    chart.nSizeMarkers = function(value)
    {
        if (!arguments.length) return nSizeMarkers;
        nSizeMarkers = value;
        return chart;
    };

    chart.colorScale = function(value)
    {
        if (!arguments.length) return colorScale;
        colorScale = value;
        return chart;
    }

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

    chart.metaDataSourceExternal = function(value)
    {
        if (!arguments.length) return metaDataSourceExternal;
        metaDataSourceExternal = value;
        return chart;
    };

    return chart;
};