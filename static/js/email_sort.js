var OrderedList = Backbone.Model.extend({

  initialize: function() {
    Backbone.Model.prototype.initialize.apply(this, arguments);

    _.bindAll(this, 'merge_order');

    this.get_order();
    $.ajax(('/associated_emails/' +
      $('.field-id > div > p').text() + '/'), {
        type: 'POST',
        success: this.merge_order
      }
    );
  },

  get_order: function() {
    this.set('order_list', _.map($('#id_email_order').text().split(",") || [],
             function(value) {
                return parseInt(value);
             })
    );
  },

  set_order: function() {
    $('#id_email_order').text(this.get('order_list'));
  },

  merge_order: function(json_list) {
    var order_list = this.get('order_list');
    var list = [];

    _.each(json_list, function(item) {
      list.push(item.pk);
    });

    _.each(order_list, function(list_item) {
      if(!_.contains(list, list_item)) {
        order_list.splice(order_list.indexOf(list_item), 1);
      }
    });
    _.each(list, function(list_item) {
      if(!_.contains(order_list, list_item)) {
        order_list.push(list_item);
      }
    });

    this.set_order();
    this.sort_and_set_emails(json_list);
    this.render_list();
  },

  sort_and_set_emails: function(json_list) {
    var order_list = this.get('order_list');
    this.set('email_list', json_list.sort(function(email) {
        return _.indexOf(order_list, email.pk)
    }));
  },

  render_list: function() {
    var view = { 'email': [] };
    _.each(this.get('email_list'), function(email) {
      view.email.push({'id': email.pk, 'name':  email.fields.subject});
    });
    if(view.email.length) {
      $.ajax('/static/templates/email_list.html', {
        type: 'POST',
        success: [
          function(mustache_template) {
            $('#id_sortable_email').html(Mustache.render(mustache_template, view));
          },
          setup_sortable
        ]
      });
    }
  },

  resort: function(list) {
    this.set('order_list', _.map(list, function(item) {
      return parseInt(item.slice(9));
      })
    );
    this.set_order();
  }
});

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
