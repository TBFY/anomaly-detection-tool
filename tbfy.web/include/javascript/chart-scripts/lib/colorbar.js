function colorbar()
{
    var svg = null,
        x = 0,
        y = 0,
        width = 30,
        height = 340,
        color = d3.scaleSequential(d3.interpolateYlOrRd),
        colorDomain = [0, 1];
    

    function chart(selection)
    {
        var cScale = d3.scaleLinear().domain(colorDomain).range([0, height]),
            data = d3.range(0, 1 + 0.5/(height), 1/(height));


        svg.selectAll("rect")
            .data(data)
            .enter()
            .append("rect")
            .attr("x", x)
            .attr("width", width)
            .attr("y", (d,i)=>y+i)
            .attr("height", 1)
            .attr("fill", d=>color(d));
        
        var axis = d3.axisRight()
            .scale(cScale)
            .ticks(10);

        svg.append("g")
            .attr("transform", "translate (" + (width + x) + ",0)")
            .call(axis);
    }

    chart.x = function(value)
    {
        if (!arguments.length) return x;
        x = value;
        return chart;
    }

    chart.y = function(value)
    {
        if (!arguments.length) return x;
        y = value;
        return chart;
    }

    chart.svg = function(value)
    {
        if (!arguments.length) return svg;
        svg = value;
        return chart;
    }

    chart.color = function(value)
    {
        if (!arguments.length) return color;
        color = value;
        return chart;
    }

    chart.width = function(value)
    {
        if (!arguments.length) return width;
        width = value;
        return chart;
    }

    chart.height = function(value)
    {
        if (!arguments.length) return height;
        height = value;
        return chart;
    }


    chart.colorDomain = function(value)
    {
        if (!arguments.length) return colorDomain;
        colorDomain = value;
        return chart;
    }

    return chart;

}