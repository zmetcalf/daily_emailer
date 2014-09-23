$(document).ready(function() {
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
    }
  });
  $('#id_email_order').hide();
  $('.field-id').hide();

  if($('.field-id > div > p').text()) {
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

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
