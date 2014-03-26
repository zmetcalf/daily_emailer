$(document).ready(function() {
  $('#id_email_order').hide();
  $('.field-id').hide();
  if($('.field-id').children().children().text() === 'ID:(None)') {
    $('.field-email_order').hide();
  } else {
    $('#id_email_order').before('<div id="id_sortable_email"></div>');
    render_list();
  }
});

function render_list() {
  var view = { 'email': [] };
  $('#id_emails option:selected').each(function(index, email) {
    view.email.push({'id': $(email).val(), 'name':  $(email).text()});
  });
  if(view.email.length) {
    $.post('/static/templates/email_list.html', function(mustache_template) {
      $('#id_sortable_email').html(Mustache.render(mustache_template, view));
      setup_sortable();
    });
  }
}

function setup_sortable() {
  $('#sortable').sortable();
  $('#sortable').disableSelection();
  $('#id_email_order').text($('#sortable').sortable('serialize'));

  $('#sortable').sortable(
    { update: function(event, ui) {
      $('#id_email_order').text($('#sortable').sortable('serialize'));
    }
  });
}
