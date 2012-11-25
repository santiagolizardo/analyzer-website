
function drawChart()
{
	var data = google.visualization.arrayToDataTable([
		[ 'Label', 'Value' ],
		[ 'Load time', loadTime ],
	]);

	var options = {
		width: 400, height: 120,
		yellowFrom: 1100, yellowTo: 2000,
		redFrom: 2000, redTo: 3000,
		max: 3000
	};

	var chart = new google.visualization.Gauge( document.getElementById('loadTimeGauge') );
	chart.draw( data, options );
}

google.load( 'visualization', '1', { packages:['gauge'] } );
google.setOnLoadCallback( drawChart );

$( document ).ready( function()
{
});


