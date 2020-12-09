function sizebar()
{
    var svg = null,
        x = 0,
        y = 0,
        width = 30,
        height = 340,
        minR = 5,
        maxR = 20,
        color = d3.scaleSequential(d3.interpolateYlOrRd)(0.5),
        sizeDomain = [0, 1];
    

    function chart(selection)
    {
        var sScale = d3.scaleLinear().domain(sizeDomain).range([minR, height-maxR]);
        // var data = d3.range(minR, maxR+1e-6, (maxR - minR)/nCircles);


        svg.append("circle")
            .attr("cx", x+maxR)
            .attr("cy", y+minR)
            .attr("r", minR)
            .attr("fill", color);
            // .attr("stroke", "black");

        svg.append("circle")
            .attr("cx", x+maxR)
            .attr("cy", height-maxR)
            .attr("r", maxR)
            .attr("fill", color);
            // .attr("stroke", "black");

        svg.append("polygon")
            .attr("points", "" + (x + maxR-minR) + "," + (y + minR) + " " 
                    + (x + maxR + minR) +"," + (y + minR) + " " 
                    + (x + 2*maxR) + "," + (y + height - maxR) + " "
                    +  x + "," + (y + height - maxR))
            .attr("fill", color); 
            
        // svg.append("line")
        //     .attr("x1", x + maxR - minR)
        //     .attr("x2", x )
        //     .attr("y1", y + minR)
        //     .attr("y2", y + height - maxR)
        //     .attr("stroke", "black");

        // svg.append("line")
        //     .attr("x1", x + maxR + minR)
        //     .attr("x2", x + 2*maxR )
        //     .attr("y1", y + minR)
        //     .attr("y2", y + height - maxR)
        //     .attr("stroke", "black");

        
        var axis = d3.axisRight()
            .scale(sScale)
            .ticks(10);

        svg.append("g")
            .attr("transform", "translate (" + (x + width + maxR) + ",0)")
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

    chart.minR = function(value)
    {
        if (!arguments.length) return minR;
        minR = value;
        return chart;
    }

    chart.maxR = function(value)
    {
        if (!arguments.length) return maxR;
        maxR = value;
        return chart;
    }

    chart.svg = function(value)
    {
        if (!arguments.length) return svg;
        svg = value;
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

    chart.color = function(value)
    {
        if (!arguments.length) return color;
        color = value;
        return chart;
    }


    chart.sizeDomain = function(value)
    {
        if (!arguments.length) return sizeDomain;
        sizeDomain = value;
        return chart;
    }

    return chart;

}