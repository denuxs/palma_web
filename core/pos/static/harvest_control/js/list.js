var tblHarvestControl;
var input_date_range;

var harvest_control = {
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
        tblHarvestControl = $('#data').DataTable({
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
                {data: "date_joined"},
                {data: "production"}, // number
                {data: "production"}, // lots
                {data: "total_bunches"},
                {data: "total_boxes"},
                {data: "observations"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-6],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if ($.isEmptyObject(row.production)) {
                            return '---';
                        }
                        return row.production.short_name;
                    }
                },
                {
                    targets: [-5],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if ($.isEmptyObject(row.production)) {
                            return '---';
                        }
                        var content = '';
                        row.production.lots.forEach(function (value, index, array) {
                            content += '<span class="badge badge-secondary badge-pill mr-2">' + value.name + '</span>';
                        });
                        return content;
                    }
                },
                {
                    targets: [-3, -4, 1],
                    class: 'text-center'
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a class="btn btn-success btn-xs btn-flat" rel="detail" data-toggle="tooltip" title="Detalle"><i class="fas fa-folder-open"></i></a> ';
                        buttons += '<a href="' + pathname + 'delete/' + row.id + '/" data-toggle="tooltip" title="Eliminar" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash"></i></a>';
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
            harvest_control.list(false);
        });

    $('.drp-buttons').hide();

    harvest_control.list(false);

    $('#data tbody')
        .off()
        .on('click', 'a[rel="detail"]', function () {
            $('.tooltip').remove();
            var tr = tblHarvestControl.cell($(this).closest('td, li')).index(),
                row = tblHarvestControl.row(tr.row).data();
            $('#tblHarvestControlDetail').DataTable({
                autoWidth: false,
                destroy: true,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: {
                        'action': 'search_harvest_control_detail',
                        'id': row.id
                    },
                    dataSrc: ""
                },
                info: false,
                columns: [
                    {data: "tape_assignment.production_plant.plant.short_name"},
                    {data: "tape_assignment.production_plant.plant.lot.name"},
                    {data: "quantity"},
                    {data: "boxes"},
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
            $('#myModalDetail').modal('show');
        });

    $('.btnSearchAll').on('click', function () {
        harvest_control.list(true);
    });
});