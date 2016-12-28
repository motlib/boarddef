var sel_el = null;

var unselect = function() {
    if(sel_el != null) {
    }
}

var select = function(el_svg, text) {
    sel_el = el_svg;
    
    el_svg.style.stroke = '#ff0000';
    el_svg.style['stroke-width'] = '0.2';

    document.getElementById('info').innerHtml = text;
}

var setInfo = function(el_svg, text) {
    if(sel_el == el_svg) {
	// unselect the element
	document.getElementById("info").innerHTML = '';
	sel_el.style.stroke = 'none';
	sel_el = null;
    }
    else {
	// select the new element
	if(sel_el != null) {
	    sel_el.style.stroke = 'none';
	}	    
	
	el_svg.style.stroke = '#ff0000';
	el_svg.style['stroke-width'] = '0.2';

	document.getElementById('info').innerHTML = text;
	
	sel_el = el_svg;
    }
};
