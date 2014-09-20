
$( document ).ready( function()
{
	var container = document.getElementById( 'htmlDocumentTypesChart' ).getContext( '2d' );
	new Chart( container ).Doughnut( htmlDocumentTypes, {} );
	
	var container = document.getElementById( 'domainTlds' ).getContext( '2d' );
	new Chart( container ).Doughnut( domainTlds, {} );
	
	for( var i = 0; i < pageRanksLabels.length; i++ ) pageRanksLabels[i] = 'PageRank #' + pageRanksLabels[i];
	var pageRanksObject = {
		labels: pageRanksLabels,
		datasets: [
			{
				fillColor: "rgba(220,220,220,0.5)",
				strokeColor: "rgba(220,220,220,0.8)",
				highlightFill: "rgba(220,220,220,0.75)",
				highlightStroke: "rgba(220,220,220,1)",
				data: pageRanksData
			}	
		],
	};
	var container = document.getElementById( 'pageRanks' ).getContext( '2d' );
	new Chart( container ).Bar( pageRanksObject, {} );
}
);

