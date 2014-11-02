$(document).ready(function() {
  // Create default reference name
  if($('#id_reference_name').val()) {
    $('#id_reference_name').addClass('user-changed');
  }
  $('#id_reference_name').on('keyup keydown', function (e) {
    $(this).addClass('user-changed');
  });
  $('#id_email_group').change(function() { set_reference_name(); });
  $('#id_recipient').change(function() { set_reference_name(); });
});

function set_reference_name() {
  if(!$('#id_reference_name').hasClass('user-changed')) {
    d = new Date();
    $('#id_reference_name').val((d.getMonth()+1) + '-' + d.getDate()
                                  + '-' + d.getFullYear() + ' - ' +
                                  $('#id_email_group option:selected').text() +
                                  ' - ' + $('#id_recipient option:selected').text()
                                 );
  }
}
