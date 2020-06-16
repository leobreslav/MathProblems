console.log("tasks.js is 1234 ready");


function try_ajax(){
    var all_data = [];
    var table = $(":text");

    for (var i=0; i<table.length; i++){
        var task_id = table[i].id.split('_')[0];
        var task_field = table[i].id.split('_')[1];
        var field_value = table[i].value;
        all_data.push({'task_id': task_id, 'task_field': task_field, 'field_value': field_value})
    }

    console.log(all_data);

    let send_data = {
        'all_data' : JSON.stringify(all_data)
    };

    $.ajax({
        url: "/tasks/try_ajax",
        type: "POST",
        data: send_data,
        success: function(res) {
            console.log(res)
            document.getElementById('ajax_result').innerHTML = 'Задача '+res+ " сохранена успешно!";


            console.log("success")
        },
        error: function(ts) {
            alert('Какая-то ошибка :(')
            // console.log(ts)
            document.getElementById('ajax_result').innerHTML = 'Какая-то ошибка!';
        }
    })
}