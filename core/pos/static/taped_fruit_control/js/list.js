var select_production, select_tape;

var taped_fruit_control = {
    list: function () {
        $('#data').DataTable({
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action': 'search',
                    'production': select_production.val(),
                    'tape': select_tape.val()
                },
                dataSrc: ""
            },
            columns: [
                {data: "id"},
                {data: "date_joined"},
                {data: "tape_assignment.production_plant.plant.short_name"},
                {data: "tape_assignment.production_plant.plant.lot.name"},
                {data: "tape_assignment.tape.name"},
                {data: "quantity"},
                {data: "observations"},
                // {data: "id"},
            ],
            columnDefs: [
                 {
                    targets: [-2, 1],
                    class: 'text-center'
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    ordering: false,
                    render: function (data, type, row) {
                        return '<div class="container-square" style="background-color: ' + row.tape_assignment.tape.color + '"><span class="badge badge-secondary badge-pill">' + row.tape_assignment.tape.week + '</span></div>';
                    }
                },
                // {
                //     targets: [-1],
                //     class: 'text-center',
                //     orderable: false,
                //     render: function (data, type, row) {
                //         var buttons = '<a href="' + pathname + 'update/' + row.id + '/" data-toggle="tooltip" title="Editar" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                //         buttons += '<a href="' + pathname + 'delete/' + row.id + '/" data-toggle="tooltip" title="Eliminar" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                //         return buttons;
                //     }
                // },
            ],
            initComplete: function (settings, json) {
                $('[data-toggle="tooltip"]').tooltip();
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    }
};

$(function () {
    select_production = $('select[name="production"]');
    select_tape = $('select[name="tape"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    select_production.on('change', function () {
        taped_fruit_control.list();
    });

    select_tape.on('change', function () {
        taped_fruit_control.list();
    });

    taped_fruit_control.list();
});