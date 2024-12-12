var input_date_range;
var tblProduction;
var production = {
    list: function (all) {
        var parameters = {
            'action': 'search',
            'start_date': input_date_range.data('daterangepicker').startDate.format('YYYY-MM-DD'),
            'end_date': input_date_range.data('daterangepicker').endDate.format('YYYY-MM-DD'),
        };
        if (all) {
            parameters['start_date'] = '';
            parameters['end_date'] = '';
        }
        tblProduction = $('#data').DataTable({
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: parameters,
                dataSrc: ""
            },
            columns: [
                {data: "id"},
                {data: "start_date"},
                {data: "end_date"},
                {data: "days"},
                {data: "lots"},
                {data: "active"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-4],
                    class: 'text-center'
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var content = '';
                        row.lots.forEach(function (value, index, array) {
                            content += '<span class="badge badge-secondary badge-pill mr-2">' + value.name + '</span>';
                        });
                        return content;
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (data) {
                            return '<a rel="activate" class="badge badge-success badge-pill cursor-pointer">Activo</a>';
                        }
                        return '<a rel="inactivate" class="badge badge-danger badge-pill cursor-pointer">Inactivo</a>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var buttons = '<a rel="detail" data-toggle="tooltip" title="Detalle" class="btn btn-success btn-xs btn-flat"><i class="fas fa-search"></i></a> ';
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
    input_date_range = $('input[name="date_range"]');

    input_date_range
        .daterangepicker({
                language: 'auto',
                startDate: new Date(),
                locale: {
                    format: 'YYYY-MM-DD',
                },
                autoApply: true,
            }
        )
        .on('change.daterangepicker apply.daterangepicker', function (ev, picker) {
            production.list(false);
        });

    $('.drp-buttons').hide();

    production.list(false);

    $('.btnSearchAll').on('click', function () {
        production.list(true);
    });

    $('#data tbody')
        .off()
        .on('click', 'a[rel="detail"]', function () {
            $('.tooltip').remove();
            var tr = tblProduction.cell($(this).closest('td, li')).index(),
                row = tblProduction.row(tr.row).data();
            $('#tblContracts').DataTable({
                autoWidth: false,
                destroy: true,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: {
                        'action': 'search_contract',
                        'id': row.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: "id"},
                    {data: "contract.employee.names"},
                    {data: "contract.employee.dni"},
                    {data: "contract.employee.mobile"},
                    {data: "contract.employee.email"}
                ],
                columnDefs: [
                    {
                        targets: [-1, -2],
                        class: 'text-center'
                    }
                ],
                initComplete: function (settings, json) {
                    $(this).wrap('<div class="dataTables_scroll"><div/>');
                }
            });
            $('#tblSupplies').DataTable({
                autoWidth: false,
                destroy: true,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: {
                        'action': 'search_supply',
                        'id': row.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: "id"},
                    {data: "resource.name"},
                    {data: "resource.code"},
                    {data: "resource.resource_type.name"},
                    {data: "quantity"},
                ],
                columnDefs: [
                    {
                        targets: [-1, -2],
                        class: 'text-center'
                    }
                ],
                initComplete: function (settings, json) {
                    $(this).wrap('<div class="dataTables_scroll"><div/>');
                }
            });
            $('#tblEquipment').DataTable({
                autoWidth: false,
                destroy: true,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: {
                        'action': 'search_equipment',
                        'id': row.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: "id"},
                    {data: "resource.name"},
                    {data: "resource.code"},
                    {data: "resource.resource_type.name"},
                    {data: "inventory.serie"},
                    {data: "inventory.guarantee"},
                ],
                columnDefs: [
                    {
                        targets: [-1, -2, -3],
                        class: 'text-center'
                    }
                ],
                initComplete: function (settings, json) {
                    $(this).wrap('<div class="dataTables_scroll"><div/>');
                }
            });
            $('#tblPlants').DataTable({
                autoWidth: false,
                destroy: true,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: {
                        'action': 'search_plant',
                        'id': row.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: "id"},
                    {data: "plant.plant_type.name"},
                    {data: "plant.code"},
                    {data: "plant.plant_type.category.name"},
                    {data: "plant.lot.name"},
                    {data: "plant.latitude"},
                    {data: "plant.longitude"},
                ],
                columnDefs: [
                    {
                        targets: [-1, -2, -3, -4, -5],
                        class: 'text-center'
                    }
                ],
                initComplete: function (settings, json) {
                    $(this).wrap('<div class="dataTables_scroll"><div/>');
                }
            });
            $('.nav-tabs a[href="#menu1"]').tab('show')
            $('#myModalDetail').modal('show');
        })
        .on('click', 'a[rel="activate"]', function () {
            $('.tooltip').remove();
            var tr = tblProduction.cell($(this).closest('td, li')).index(),
                row = tblProduction.row(tr.row).data();
            execute_ajax_request({
                'params': {
                    'action': 'inactivate_production',
                    'id': row.id
                },
                'success': function (request) {
                    tblProduction.ajax.reload();
                }
            })
        })
        .on('click', 'a[rel="inactivate"]', function () {
            $('.tooltip').remove();
            var tr = tblProduction.cell($(this).closest('td, li')).index(),
                row = tblProduction.row(tr.row).data();
            execute_ajax_request({
                'params': {
                    'action': 'activate_production',
                    'id': row.id
                },
                'success': function (request) {
                    tblProduction.ajax.reload();
                }
            })
        });
});