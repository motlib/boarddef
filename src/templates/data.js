{#
 The database macro generates a javascript (JSON) data structure containing
 the basic information of all board elements (connectors, pins, chips)
#}

{% macro database(board) %}
database = {
    {% for conn in board.connectors %}
    'conn_{{ conn.tag }}': {
	'name': '{{ conn.name }}',
	'description': '{{ conn.description }}',
    },
    {% for pin in conn.pins %}
    'pin_{{conn.tag}}_{{pin.tag}}': {
	'name': '{{ pin.name }}',
	'description': '{{ pin.description }}',
    },
    {% endfor %}
    {% endfor %}

    {% for chip in board.chips %}
    'chip_{{ chip.tag }}': {
	'name': '{{ chip.name }}',
	'description': '{{ chip.description }}',
    },
    {% endfor %}
    
};
{% endmacro %}
