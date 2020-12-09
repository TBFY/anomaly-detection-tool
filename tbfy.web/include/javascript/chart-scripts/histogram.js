// function draws histogram
// function draws histogram

function histogramChart()
{
    var margin = {top: 10, right: 30, bottom: 50, left: 60},
        width = 750 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom,
        numBins = 50,
        xLabel = '',
        yLabel = '',
        valueFieldName = '',
        metaHtmlElement = '',
        metaFunctionExternal = '',
        lastSelectedRect = -1;

    function chart(selection)
    {
        selection.each(function(data)
        {
            // creates x and y axis
            // creates x and y axis

            var max_x = d3.max(data, function(d) { return + eval("d." + valueFieldName); });
            var min_x = d3.min(data, function(d) { return + eval("d." + valueFieldName); });
            var delta = (max_x - min_x) / numBins;

            var x = d3.scaleLinear()
                .domain([min_x - delta, max_x + delta])
                .rangeRound([0, width]);
            var y = d3.scaleLinear()
                .range([height, 0]);

            // creates new histogram chart
            // creates new histogram chart

            var histogram = d3.histogram()
                .value(function(d) { return eval("d." + valueFieldName); })
                .domain(x.domain())
                .thresholds(x.ticks(numBins));

            // append the svg object to the body of the page
            // append a 'group' element to 'svg'
            // moves the 'group' element to the top left margin

            var svg = selection.append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            // group the data for the bars
            // group the data for the bars

            var bins = histogram(data);

            // scale the range of the data in the y domain
            // scale the range of the data in the y domain

            y.domain([0, d3.max(bins, function(d) { return d.length; })]);

            // add the x axis
            // add the x axis

            svg.append("g")
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(x));

            svg.append("text")
                .attr("transform", "translate(" + (width/2) + " ," +  (height + margin.top + 35) + ")")
                .style("text-anchor", "middle")
                .text(xLabel);

            // add the y axis
            // add the y axis

            svg.append("g")
                .call(d3.axisLeft(y));

            svg.append("text")
                .attr("transform", "rotate(-90)")
                .attr("y", 0 - margin.left)
                .attr("x",0 - (height / 2))
                .attr("dy", "1em")
                .style("text-anchor", "middle")
                .text(yLabel);

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

                    if(lastSelectedRect > -1)
                    {
                        selectedRect = svg.selectAll("rect[tabindex='" + lastSelectedRect + "']");
                        selectedRect.attr("class", "bar");
                    }
                    selectedRect = svg.selectAll("rect[tabindex='" + i + "']");
                    selectedRect.attr("class", "bar_hover");
                    lastSelectedRect = i;

                    // display data
                    // display data

                    var htmlText = eval(metaFunctionExternal + "(d);");
                    tooltip.html(htmlText)
                        //.transition()
                        //.duration(1000);
                        //.style("opacity", 1)
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

            // append the bar rectangles to the svg element
            // append the bar rectangles to the svg element

            svg.selectAll("rect")
                .data(bins)
                .enter().append("rect")
                .attr("class", "bar")
                //.attr("id", function(d) { return x(d.x1) - x(d.x0) -1 ; })
                .attr("tabindex", function(d, i) { return i; })
                .attr("transform", function(d) {return "translate(" + x(d.x0) + "," + y(d.length) + ")"; })
                .attr("width", function(d) { return x(d.x1) - x(d.x0) -1 ; })
                .attr("height", function(d) { return height - y(d.length); })
                // Show tooltip on hover
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

    chart.numBins = function(value)
    {
        if (!arguments.length) return numBins;
        numBins = value;
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

    chart.valueFieldName = function(value)
    {
        if (!arguments.length) return valueFieldName;
        valueFieldName = value;
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