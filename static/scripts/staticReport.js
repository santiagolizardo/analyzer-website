
function drawChart()
{
	var data = google.visualization.arrayToDataTable([
		[ 'Label', 'Value' ],
		[ 'Load time', loadTimeMs ],
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

var rating = {
	content: 0,
	presentation: 0,
	usability: 0,
};

$( document ).ready( function()
	{
		$( 'img.Star' ).on( 'click', function( ev )
			{
				var criteria = this.getAttribute( 'data-rating-criteria' );
				var value = this.getAttribute( 'data-rating-value' );

				rating[ criteria ] = value;

				$( 'img', $( this ).parent() ).each( function( i, el )
					{
						this.src = '/images/gray-star.png';
					}
				);
				this.src = '/images/yellow-star.png';
				$( this ).prevAll().each( function( i, e )
					{
						this.src = '/images/yellow-star.png';
					}
				);
			}
		);

		$( '#sendRating' ).on( 'click', function( ev )
			{
				if( rating.content == 0 || rating.presentation == 0 || rating.usability == 0 )
				{
					alert( 'Please rate the site with values from 1-5 on all three criterias (content, presentation and usability)' );
					return;
				}

				var params = rating;
				params['domain'] = domainUrl;

				$.ajax({
					url: baseUrl + '/rate',
					data: params,
					type: 'POST',
					success: function() // done
					{
						$( '#ratingBox' ).html( 'Thanks for your rating.' );
					},
					error: function() // fail
					{
						alert( 'Your rating could not be sent. Please again in a few seconds.' );
					}
				});
			}
		);
	}
);

