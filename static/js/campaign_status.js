var reference_name_edited = false;

$(document).ready(function() {
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader('X-CSRFToken', $('input[name="csrfmiddlewaretoken"]').val());
    }
  });
  $('#id_status').hide();
  $('.field-id').hide();

  if($('#id_reference_name').text().length) {
    reference_name_edited = true;
  }
});

function set_reference_name() {
  if(!reference_name_edited) {
    d = new Date();
    $('#id_reference_name').text((d.getMonth()+1) + '-' + d.getFullYear()
                                  + '-' + d.getDate() + ' - ' +
                                  $('#id_email_group option:selected').text() +
                                  '-' + $('#id_recipient option:selected').text()
                                 );

  }
}
