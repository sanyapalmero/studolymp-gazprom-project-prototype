import '../scss/main.scss';

// Libraries
import $ from 'jquery';
import 'bootstrap';

$(".show-modal").each(function(index, element){
    $(element).modal("show");
});
