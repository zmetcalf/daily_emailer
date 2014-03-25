$(document).ready(function() {
  $('#id_email_order').hide();
  $('#id_email_order').before('<div id="id_sortable_email"></div>');
  render_list();
});

function render_list() {
  var view = { 'email': [] };
  $('#id_emails option:selected').each(function(index, email) {
    view.email.push({'id': $(email).val(), 'name':  $(email).text()});
  });
  $.post('/static/templates/email_list.html', function(mustache_template) {
    $('#id_sortable_email').html(Mustache.render(mustache_template, view));
    setup_sortable();
  });
}

function setup_sortable() {
    $('#sortable').sortable();
    $('#sortable').disableSelection();
    $('#id_email_order').text($('#sortable').sortable('serialize'));

    $('#sortable').sortable(
      { change: function() {
        $('#id_email_order').text($('#sortable').sortable('serialize'));
      }
    });
}
