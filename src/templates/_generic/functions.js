// Currently selected element
var sel_el = null;

/*
 * Mouseover handler for the svg elements. This function highlights
 * the element and shows the related data.
 */
var setInfo = function(el_svg, tag) {
    // deselect the last selected element
    if(sel_el != null) {
	sel_el.style.stroke = 'none';
    }	    

    // select the new element by setting its stroke attribute
    el_svg.style.stroke = '#ffff00';
    el_svg.style['stroke-width'] = '0.2';

    // show info related to the selected element
    document.getElementById('data_tag').innerHTML = tag;
    var data = database[tag];
    if(data) {
	document.getElementById('data_name').innerHTML = data['name'];
	document.getElementById('data_desc').innerHTML = data['description'];
    }

    // store new selected element
    sel_el = el_svg;
};
