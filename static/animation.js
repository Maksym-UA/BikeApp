$(document).ready(function(){
	
	

/*----------------------------------------------------------------------------*/		
	//selectors accroding to bike class(tour, sport, cruiser)
	$('#selectAll').addClass('active');
	
	$('#selectAll').click(function(){
		
		$('#sportSel,#tourSel, #cruiserSel').removeClass('active');
		$(this).addClass('active');
	});
	
	
	$('#sportSel').click(function(){
		
		$('#selectAll, #tourSel, #cruiserSel').removeClass('active');
		$(this).addClass('active');
		;		
	});
	
	
	
	$('#tourSel').click(function(){	
		
		$('#selectAll, #sportSel, #cruiserSel').removeClass('active');
		$(this).addClass('active');		
		
	});
	
	$('#cruiserSel').click(function(){
		$('.row.sport, .row.tourist').hide();
		$('#selectAll, #sportSel, #tourSel').removeClass('active');
		$(this).addClass('active');		
	});
	
	
	
});
