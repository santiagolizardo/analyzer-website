
$( document ).ready( function()
{
	var container = document.getElementById( 'domainExtensionChart' );
	var d1=[[0,4]],d2=[[0,3]],d3=[[0,1.03]],d4=[[0,3.5]];
	var series = [{data:d1,label:'HTML5'},{data:d2,label:'HTML 4 Strict'},{data:d3,label:'HTML 4 Frameset',pie:{explode:50}},{data:d4,label:'HTML 4 Transitional'}];
	var options = {
		HtmlText:false,
		grid:{
			outlineWidth: 0,
			verticalLines:false,
horizontalLines:false},xaxis:{showLabels:false},yaxis:{showLabels:false},pie:{show:true,explode:6},mouse:{track:true},legend:{position:'se',backgroundColor:'#D2E8FF'}
	};
	var graph = Flotr.draw(container, series, options );
}
);

