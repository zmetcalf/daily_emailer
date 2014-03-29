$(document).ready(function() {
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader('X-CSRFToken', $('input[name="csrfmiddlewaretoken"]').val());
    }
  });
  $('#id_email_order').hide();
  $('.field-id').hide();
  if($('.field-id > div > p').text() === '(None)') {
    $('.field-email_order').hide();
  } else if(!isNaN(parseInt($('.field-id > div > p').text()))) {
    $('#id_email_order').before('<div id="id_sortable_email"></div>');
    order_list = new OrderedList;
  }
});

function setup_sortable() {
  $('#sortable').sortable();
  $('#sortable').disableSelection();
  $('#sortable').sortable(
    { update: function(event, ui) {
      order_list.resort($('#sortable').sortable('toArray'));
    }
  });
}
