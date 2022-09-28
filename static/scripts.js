$(document).ready(function() {
    let actions = $("table td:last-child").html();

    // Append table with add row form on add new button click
    $(".add-new").click(function() {
        $(this).attr("disabled", "disabled");
        let index = $("table tbody tr:last-child").index();
        let row = '<tr>' +
            '<td><input class="form-control" type="text"></td>' +
            '<td>$ <input type="number"></td>' +
            '<td><select class="form-control"><option>Every Month</option><option>Every 3 Months</option><option>Every Week</option><option>Every 2 weeks</option></select></td>' +
            '<td>' + actions + '</td>' +
            '</tr>';
        $("table").append(row);
        $("table tbody tr").eq(index + 1).find(".add, .edit").toggle();
    });

    // Add row on add button click
    $(document).on("click", ".add", function() {
        let empty = false;
        let input = $(this).parents("tr").find('input[type="text"]');
        input.each(function() {
            if (!$(this).val()) {
                $(this).attr("Placeholder", "Please fill out");
            } 
        });
        $(this).parents("tr").find(".error").first().focus();
        if (!empty) {
            input.each(function() {
                $(this).parent("td").html($(this).val());
            });
            $(this).parents("tr").find(".add, .edit").toggle();
        }
    });
    // Edit row on edit button click
    $(document).on("click", ".edit", function(){
        $(this).parents("tr").children(":first").each(function(){
            $(this).html('<input type="text" class="form-control text-center" value="' + $(this).text() + '">');
        });
        $(this).parents("tr").find(".add, .edit").toggle();
    });

    // Delete row on delete button click
    $(document).on("click", ".delete", function() {
        $(this).parents("tr").remove();
    });
});