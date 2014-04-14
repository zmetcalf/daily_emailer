var email_collection = new Backbone.Collection();

$(document).ready(function() {
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader('X-CSRFToken', $('input[name="csrfmiddlewaretoken"]').val());
    }
  });


  // Add and remove fields
  $('.field-status > div > p').hide();
  $('.field-status > div > label').after('<div id="id_status"></div>');
  $('.field-id').hide();
  if($('.field-id > div > p').text()) {
    show_status();
  }

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
  $.ajax(('/daily_emailer/campaign_emails/' +
    $('.field-id > div > p').text() + '/'), {
      type: 'POST',
      success: [
        function(email_list) {
          _.each(email_list, function(email) {
            email_collection.add(email);
          });
        },
        render_status
      ]
    }
  );
}

function render_status() {
  var view = { 'email': [] };
  var sent_emails = eval("(" + $('.field-status > div > p').text() + ")");
  email_collection.each(function(email) {
    var sent = false;

    var key = _.find(_.keys(sent_emails), function(key) {
      return key == email.get('pk');
    });

    if(key) {
      sent = sent_emails[key];
    }

    view.email.push({ 'name': email.get('fields').subject, 'date_sent': sent });
  });

  $.ajax('/static/templates/status.html', {
    type: 'GET',
    success: function(mustache_template) {
      $('#id_status').html(Mustache.render(mustache_template, view));
    }
  });
}
