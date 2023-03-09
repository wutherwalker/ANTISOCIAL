

//get parameters of the svg canvas object on the html page
var canvas = d3.select('#canvas');
var width = canvas.attr('width');
var height = canvas.attr('height');

//offset parameter for positioning upper and lower labels
var offset = 10;

//standard margins
var margin = {'left': 20, 'right': 20, 'top': 30, 'bottom': 20};

//scale function for converting utility values to pixels and vice-versa
var yScale = d3.scaleLinear()
  .domain([-1*max_value, max_value])
  .range([height-margin.top, margin.bottom]);

//vertical line dividing self from other utilities
canvas.append('line')
  .attr('x1', width/2)
  .attr('x2', width/2)
  .attr('y1', yScale(max_value))
  .attr('y2', yScale(-1*max_value))
  .style('stroke', 'black')
  .style('stroke-width', 5);

//text label at top of line
canvas.append('text')
  .attr('x', width/2)
  .attr('y', yScale(max_value) - 5)
  .style('text-anchor', 'middle')
  .style('font-size', '15px')
  .style('font-style', 'italic')
  .text(topValueLabel);  //specified on html page

//text label at bottom of line
canvas.append('text')
  .attr('x', width/2)
  .attr('y', yScale(-1*max_value) + 20)
  .style('text-anchor', 'middle')
  .style('font-size', '15px')
  .style('font-family', 'sans-serif')
  .style('font-style', 'italic')
  .text(bottomValueLabel);   //specified on html page

//create data object for self utilities and labels
self = [];
  for(i=0; i<selfUtilities.length; i++)
    //opdtionLabels[] and selfUtilities[] specified on html page
    self.push([optionLabels[i], selfUtilities[i]]);

//display optionLabels at appropriate self utilities
canvas.selectAll('selfText')
  .data(self)
  .enter()
  .append('text')
  .attr('x', width/2 - offset)
  .attr('y', function(d) {return yScale(d[1]);})
  .style( 'text-anchor', 'end')
  .style('alignment-baseline', 'central')
  .style('font-family', 'sans-serif')
  .style('font-size', '15px')
  .text(function(d) {return d[0]});

//create a data object for the other utilities
other = [];
  for(i=0; i<otherUtilities.length; i++)
    other.push([optionLabels[i], otherUtilities[i]]);


//display other utilities and labels
canvas.selectAll('otherText')
  .data(other)
  .enter()
  .append('text')
  .attr('x', width/2 + offset)
  .attr('y', function(d) {return yScale(d[1]);})
  .attr('id', function(d,i) {return 'label'+i;})
  .style( 'text-anchor', 'start')
  .style('alignment-baseline', 'central')
  .style('font-family', 'sans-serif')
  .style('font-size', '15px')
  .style('fill', 'red')
  .call(d3.drag()  //allow other labels to be dragged
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended))
  .text(function(d) {return d[0]});

//different rules for updating the utilties can be
//implemented in the drag functions.

//variables used for computing new utilities while dragging
  var initial;
  var start = [];
  var starMin;
  var startMax;

  function dragstarted() {
    start = [];  //clear out start vector
    //turn dragged label blue
    d3.select(this).style('fill', 'blue');
    //save initial value for computing constant
    initial = yScale.invert(d3.select(this).attr('y'));
    //save the starting values of all labels
    for(i=0; i<selfUtilities.length; i++) {
      start.push(yScale.invert(d3.select('#label'+i).attr('y')));
    }
    //save max and min starting values for computing limits
    startMax = d3.max(start);
    startMin = d3.min(start);
  }

  function dragged() {
    if(yScale.invert(d3.event.y) > 0){
        newY = Math.min(Math.max(yScale.invert(d3.event.y),0.0000001), max_value);
    } else {
        newY = Math.max(Math.min(yScale.invert(d3.event.y),-0.0000001), -1*max_value);
    };
    cons = newY/initial;  //get scaling constant
    //make sure rescaled utilities are within range
    //if((Math.abs(cons * startMax) <= max_value && Math.abs(cons * startMin) >= 0.0000001) || (Math.abs(cons * startMax) <= -0.0000001 && Math.abs(cons * startMin) >= -1*max_value) || (Math.abs(cons * startMax) <= max_value && Math.abs(cons * startMin) >= -1*max_value)) {
    if(cons > 0 && (cons * startMax) <= max_value && (cons * startMin) >= -1*max_value){
      d3.select(this).attr('y', yScale(newY));
      //move labels to their new locations
      for(i=0; i<otherUtilities.length; i++) {
        d3.select('#label'+i).attr('y', yScale(cons*start[i]));
        otherUtilities[i] = cons*start[i];
      }
    }
  }


  function dragended() {
    //return label color to red when dragging stops
    d3.select(this).style('fill', 'red');
  }
