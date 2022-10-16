$(function () {
  / this code runs after page load /;

  $("#id_subscription_plan").change(function () {
    //  alert('jjjjj');

    var fees = $("#id_subscription_plan option:selected")
      .text()
      .split("-")
      .pop();
    $("#id_fees").val(parseInt(fees));
    $("#id_fees").attr("readonly", "readonly");
  });
});
