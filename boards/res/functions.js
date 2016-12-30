var sel_el = null;

var setInfo = function(el_svg, tag) {
    // select the new element
    if(sel_el != null) {
	sel_el.style.stroke = 'none';
    }	    
    
    el_svg.style.stroke = '#ffff00';
    el_svg.style['stroke-width'] = '0.2';
    
    document.getElementById('data_tag').innerHTML = tag;
    var data = database[tag];
    if(data) {
	document.getElementById('data_name').innerHTML = data['name'];
	document.getElementById('data_desc').innerHTML = data['description'];
    }
    
    sel_el = el_svg;
};
