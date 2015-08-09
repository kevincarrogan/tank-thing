(function () {

'use strict';

var currentTemperatureEl = d3.select('#current-temperature');

var getInt = function (attr) {
    var num = currentTemperatureEl.attr('data-' + attr);

    return parseInt(num, 10);
};

var temperature = getInt('temperature');
var low = getInt('low');
var high = getInt('high');
var optimalLow = getInt('optimal-low');
var optimalHigh = getInt('optimal-high');

var graph = currentTemperatureEl.append('svg');
var graphWidth = 300;
var graphHeight = 170;
graph.attr('width', graphWidth + 'px').attr('height', graphHeight + 'px');

var initialStartAngle = -Math.PI + 0.9;
var initialEndAngle = Math.PI - 0.9;
var scale = d3.scale.linear()
    .domain([low, high])
    .range([initialStartAngle, initialEndAngle]);

var arc = d3.svg.arc();
arc.innerRadius(70)
    .outerRadius(100)
    .startAngle(function (d) {
        return scale(d[0]);
    })
    .endAngle(function (d) {
        return scale(d[1]);
    });

var colours = ['#4ecdc4', '#c7f464', '#c44d58'];

var coloursScale = d3.scale.quantize()
    .domain([0, 10, 20, 30, 40, 50])
    .range(['#4ecdc4', '#4ecdc4', '#c7f464', '#c44d58', '#c44d58']);

var group = graph.append('g');

group.selectAll('path')
    .data([
        [low, optimalLow],
        [optimalLow, optimalHigh],
        [optimalHigh, high]
    ])
    .enter().append('path')
    .style('fill', function (d, i) {
        return colours[i];
    })
    .attr('d', arc);

var transform;

group.attr('transform', function() {
    var bbox = this.getBBox();
    var width = bbox.width;
    var horizontalMargin = (graphWidth - width) / 2;
    var x = Math.abs(bbox.x) + horizontalMargin;
    var height = bbox.height;
    var verticalMargin = (graphHeight - height) / 2;
    var y = Math.abs(bbox.y) + verticalMargin;

    transform = 'translate(' + x + ',' + y + ')';

    return transform;
});

var radToDegreeRatio = 180 / Math.PI;
var rotateScale = d3.scale.linear()
    .domain([low, high])
    .range([    
        initialStartAngle * radToDegreeRatio,
        initialEndAngle * radToDegreeRatio
    ]);

var temperatureData = [temperature];

var circleGroup = graph.append('g');

circleGroup.data(temperatureData);

circleGroup.attr('transform', function (d) {
    var rotation = rotateScale(d);
    return transform + ' rotate(' + rotation + ')';
});

circleGroup.append('circle')
    .style('fill', '#555')
    .attr('r', 60);

circleGroup.append('path')
    .style('fill', '#555')
    .attr('d', 'M 0 -68 l 10 10 l -20 0 z');

var textGroup = graph.append('g');

textGroup.data(temperatureData);

var text = textGroup.append('text');

text.style('fill', function (d) {
        return coloursScale(d);
    })
    .text(function (d) {
        return d + '°';
    })
    .attr('font-size', 50)
    .attr('font-weight', 600)
    .attr('transform', function () {
        var bbox = this.getBBox();
        var width = bbox.width;
        var horizontalMargin = (graphWidth - width) / 2;
        var x = Math.abs(bbox.x) + horizontalMargin + 8;
        var height = bbox.height;
        var verticalMargin = (graphHeight - height) / 2;
        var y = Math.abs(bbox.y) + verticalMargin + 18;

        return 'translate(' + x + ',' + y + ')';
    });

var update = function () {
    text.data(temperatureData)
        .text(function (d) {
            return d + '°';
        })
        .attr('transform', function () {
            var bbox = this.getBBox();
            var width = bbox.width;
            var horizontalMargin = (graphWidth - width) / 2;
            var x = Math.abs(bbox.x) + horizontalMargin + 8;
            var height = bbox.height;
            var verticalMargin = (graphHeight - height) / 2;
            var y = Math.abs(bbox.y) + verticalMargin + 18;

            return 'translate(' + x + ',' + y + ')';
        })
        .transition()
        .style('fill', function (d) {
            return coloursScale(d);
        });
    circleGroup.data(temperatureData)
        .transition()
        .attr('transform', function (d) {
            var rotation = rotateScale(d);
            return transform + ' rotate(' + rotation + ')';
        });
};

var src = new EventSource('/current-temperature/');
src.addEventListener('current-temperature', function (evt) {
    temperatureData[0] = parseInt(evt.data, 10);
    update();
});

}());
