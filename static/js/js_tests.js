var simulated_ajax_response = [{"pk": 1, "model": "daily_emailer.email", "fields": {"message": "Message1", "email_group": 1, "subject": "Subject1"}}, {"pk": 3, "model": "daily_emailer.email", "fields": {"message": "Message3", "email_group": 1, "subject": "Subject3"}}];
var myAPI = function() { return $.Deferred().promise(simulated_ajax_response); };
var ajax_stub = sinon.stub($,'ajax', myAPI);

test("merge_list_no_update", function() {
  var ordered_list = new OrderedList;
  ordered_list.merge_order(simulated_ajax_response);
  deepEqual(ordered_list.get('order_list'), [3,1]);
  deepEqual($('#id_email_order').text(), '3,1');
});

test("merge_list_addition", function() {
  $('#id_email_order').text('3');
  var ordered_list = new OrderedList;
  deepEqual(ordered_list.get('order_list'), [3]);
  ordered_list.merge_order(simulated_ajax_response);
  deepEqual(ordered_list.get('order_list'), [3,1]);
  deepEqual($('#id_email_order').text(), '3,1');
});

test("merge_list_subtraction", function() {
  $('#id_email_order').text('3,2,1');
  var ordered_list = new OrderedList;
  deepEqual(ordered_list.get('order_list'), [3,2,1]);
  ordered_list.merge_order(simulated_ajax_response);
  deepEqual(ordered_list.get('order_list'), [3,1]);
  deepEqual($('#id_email_order').text(), '3,1');
});

test("sort_and_set_emails", function() {
  $('#id_email_order').text('3,1');
  var ordered_list = new OrderedList;
  ordered_list.merge_order(simulated_ajax_response);
  ordered_list.sort_and_set_emails();
  deepEqual(ordered_list.email_list[0].pk, 3);
  deepEqual(ordered_list.email_list[1].pk, 1);
});
