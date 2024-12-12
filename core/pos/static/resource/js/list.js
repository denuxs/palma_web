var tblResources;
var resource = {
    list: function () {
        tblResources = $('#data').DataTable({
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
                {data: "name"},
                {data: "code"},
                {data: "resource_type.name"},
                {data: "price"},
                {data: "stock"},
                {data: "image"},
                {data: "is_equipment"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-5],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + data.toFixed(2);
                    }
                },
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
                        return '<a rel="image" class="btn btn-secondary btn-xs btn-flat"><i class="fas fa-file-image"></i></a>';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.is_equipment) {
                            return '<span class="badge badge-primary badge-pill">Si</span>';
                        }
                        return '<span class="badge badge-info badge-pill">No</span>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var buttons = '<a href="' + pathname + 'update/' + row.id + '/" data-toggle="tooltip" title="Editar" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="' + pathname + 'delete/' + row.id + '/" data-toggle="tooltip" title="Eliminar" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash"></i></a>';
                        return buttons;
                    }
                },
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {
                $('[data-toggle="tooltip"]').tooltip();
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    }
};

$(function () {
    resource.list();

    $('#data').addClass('table-sm');

    $('#data tbody')
        .off()
        .on('click', 'a[rel="stock"]', function () {
            $('.tooltip').remove();
            var tr = tblResources.cell($(this).closest('td, li')).index(),
                row = tblResources.row(tr.row).data();
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
                    {data: "purchase.number"},
                    {data: "purchase.date_joined"},
                    {data: "serie"},
                    {data: "guarantee"},
                    {data: "quantity"},
                    {data: "saldo"},
                ],
                columnDefs: [
                    {
                        targets: [0, 1],
                        class: 'text-center'
                    },
                    {
                        targets: [-3, -4],
                        class: 'text-center',
                        render: function (data, type, row) {
                            if (row.resource.is_equipment) {
                                return data;
                            }
                            return '---';
                        }
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
        })
        .on('click', 'a[rel="image"]', function () {
            var tr = tblResources.cell($(this).closest('td, li')).index();
            var data = tblResources.row(tr.row).data();
            load_image({'url': data.image});
        });
})