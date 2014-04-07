$(document).ready(function() {
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader('X-CSRFToken', $('input[name="csrfmiddlewaretoken"]').val());
    }
  });

  // Add and remove fields
  $('.field-status > div > p').hide();
  $('.field-status').before('<div id="id_status"></div>');
  // show_status();
  $('.field-id').hide();

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

function show_status() {
  $.ajax(('/campaign_emails/' +
    $('.field-id > div > p').text() + '/'), {
      type: 'POST',
      success: function() {}
    }
  );
  $.ajax('/static/templates/status.html', {
    type: 'GET',
    success: function(mustache_template) {
      $('#id_status').html(Mustache.render(mustache_template, view));
    }
  });
}
