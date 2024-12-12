var tblPlantType;
var plant_type = {
    list: function () {
        tblPlantType = $('#data').DataTable({
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
                    'action': 'search'
                },
                dataSrc: ""
            },
            columns: [
                {data: "id"},
                {data: "code"},
                {data: "name"},
                {data: "category.name"},
                {data: "stock"},
                {data: "price"},
                {data: "description"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.stock > 0) {
                            return '<a rel="stock" class="badge badge-success badge-pill cursor-pointer">' + row.stock + '</a>';
                        }
                        return '<a rel="stock" class="badge badge-danger badge-pill cursor-pointer">' + row.stock + '</a>';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + data.toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a href="' + pathname + 'update/' + row.id + '/" data-toggle="tooltip" title="Editar" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="' + pathname + 'delete/' + row.id + '/" data-toggle="tooltip" title="Eliminar" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {
                $('[data-toggle="tooltip"]').tooltip();
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    }
};

$(function () {
    plant_type.list();

    $('#data').addClass('table-sm');

    $('#data tbody')
        .off()
        .on('click', 'a[rel="stock"]', function () {
            $('.tooltip').remove();
            var tr = tblPlantType.cell($(this).closest('td, li')).index(),
                row = tblPlantType.row(tr.row).data();
            $('#tblInventory').DataTable({
                autoWidth: false,
                destroy: true,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: {
                        'action': 'search_inventory',
                        'id': row.id
                    },
                    dataSrc: ""
                },
                info: false,
                columns: [
                    {data: "harvest_control.production.short_name"},
                    {data: "harvest_control.date_joined"},
                    {data: "boxes"},
                    {data: "saldo"},
                ],
                columnDefs: [
                    {
                        targets: [1],
                        class: 'text-center'
                    },
                    {
                        targets: [-1, -2],
                        class: 'text-center'
                    }
                ],
                initComplete: function (settings, json) {
                    $(this).wrap('<div class="dataTables_scroll"><div/>');
                }
            });
            $('#myModalInventory').modal('show');
        });
});