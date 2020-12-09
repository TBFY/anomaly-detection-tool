// function needs to be revised
// function needs to be revised

function drawPieChart(dataArray, cssClassElement, numOfData2Print)
{
    // check if data exists
    // check if data exists

    if(dataArray.length == 0) return;

    // out of the set, select only most relevant data
    // out of the set, select only most relevant data

    var selectedData = [];
    for(var i = 0; i < numOfData2Print; i++)
        selectedData.push(dataArray[i]);

    if(numOfData2Print < dataArray.length)
    {
        var restOfDataSum = 0;
        for(var i = numOfData2Print; i < dataArray.length; i++)
        {
            restOfDataSum += dataArray[i];
        }
        selectedData.push(restOfDataSum);
    }

    // draw piechart
    // draw piechart

    var width = 500,
        height = 500,
        radius = Math.min(width, height) / 2;

    //var color = d3.scaleOrdinal().range(["#3366cc", "#dc3912", "#ff9900", "#109618", "#990099", "#0099c6", "#dd4477", "#66aa00", "#b82e2e", "#316395", "#994499", "#22aa99", "#aaaa11", "#6633cc", "#e67300", "#8b0707", "#651067", "#329262", "#5574a6", "#3b3eac"]);
    var color = d3.scaleOrdinal(d3.schemeSet3);

    var arc = d3.arc()
        .outerRadius(radius - 10)
        .innerRadius(0);

    var labelArc = d3.arc()
        .outerRadius(radius - 40)
        .innerRadius(radius - 40);

    var pie = d3.pie()
        .sort(null)
        .value(function(d) { return d; });

    var svg = d3.select(cssClassElement).append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    var g = svg.selectAll(".arc")
        .data(pie(selectedData))
        .enter().append("g")
        .attr("class", "arc");

        g.append("path")
            .attr("d", arc)
            .attr("fill", function(d, i) { return color(i); });

        g.append("text")
            .attr("transform", function(d) { return "translate(" + labelArc.centroid(d) + ")"; })
            .attr("dy", ".35em")
            .text(function(d) { return d.selectedData; });
}