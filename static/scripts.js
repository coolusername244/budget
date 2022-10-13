$(document).ready(function() {

    // Append table with add row form on add new button click
    let deleteButton = '<td><i class="fa-regular fa-trash-can mx-1 delete"></i></td>'

    let expenseRow = '<tr>' +
        '<td><input name="expense" type="text" placeholder="Please Fill Out" required></td>' +
        '<td><input name="amount" type="number" required></td>' + deleteButton + '</tr>';
    
    let savingsRow = '<tr>' +
    '<td><input name="savings" type="text" placeholder="Please Fill Out" required></td>' +
    '<td><input name="amount" type="number" required></td>' + deleteButton + '</tr>';

    let incomeRow = '<tr>' +
    '<td><input name="income" type="text" placeholder="Please Fill Out" required></td>' +
    '<td><input name="amount" type="number" required></td>' + deleteButton + '</tr>';

    $(".add-new-expense").click(function() {
        $("table").append(expenseRow);
    });

    $(".add-new-saving").click(function() {
        $("table").append(savingsRow);
    });

    $(".add-new-income").click(function() {
        $("table").append(incomeRow);
    });

    // Delete row on delete button click
    $(document).on("click", ".delete", function() {
        $(this).parents("tr").remove();
    });


    let outgoingData = $('#outgoing-data').html().replace(',', '');
    let savingsData = $('#saving-data').html().replace(',', '');;
    let remainingData = $('#remaining-data').html().replace(',', '');;

    const data = {
        labels: [
          'Outgoings',
          'Savings',
          'Remaining Cash'
        ],
        datasets: [{
          label: 'My First Dataset',
          data: [outgoingData, savingsData, remainingData],
          backgroundColor: [
            'rgba(255, 00, 00, 0.2)',
            'rgba(00, 255, 00, 0.2)',
            'rgba(00, 00, 255, 0.2)'
          ],
          hoverOffset: 10
        }]
      };
  

    const config = {
    type: 'doughnut',
    data: data,
    };

    const myChart = new Chart(
        document.getElementById('myChart'),
        config
    );
});